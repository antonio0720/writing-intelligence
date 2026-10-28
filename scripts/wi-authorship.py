#!/usr/bin/env python3
"""Writing Intelligence v9 EXPERIMENTAL authorship-claim declaration checker.

Project owner: Antonio T. Smith Jr. (Density6 LLC)

This is a declaration checker, not an authorship verifier. Every origin,
consent and contribution field is self-reported; nothing here can establish
who wrote a passage or whether a supplied source is true. It checks that the
declarations are complete, consistent with each other and with the declared
venue rules, that every consequential claim the v4 classifier finds in the
draft is anchored to an exact span of a declared source, and that the bytes
reviewed are the bytes pinned.

Stdlib only, Python 3.8+, POSIX file opening (fails closed elsewhere). Never
rewrites prose and never optimizes an AI detector score.

  audit    REVIEW (limited checks passed, exit 0) or HOLD (exit 3).
  release  RELEASE_ELIGIBLE (exit 0) or HOLD (exit 3). Requires a REVIEW
           audit, a person's review decision bound to the exact document
           digest, a declared authority grant that covers release and the
           venue and has not expired, and a venue contract that records
           submission as open.

REVIEW is never permission to send. RELEASE_ELIGIBLE is never proof of human
authorship; it means the declared gates agree with each other. This tool
transmits nothing.
"""
import argparse
import datetime as _dt
import errno
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import bisect
import re
import sqlite3
import stat
import sys

SCHEMAS = {"wi9-authorship-1", "wi9-authorship-2"}
AUDIT_SCHEMA = "wi9-authorship-audit-2"
RELEASE_SCHEMA = "wi9-authorship-release-1"
ORIGINS = {"human_authored", "ai_assisted", "ai_generated"}
VENUES = {"unrestricted", "disclose_ai", "human_only"}
INTENDED = {"submission", "research_demo", "internal_review"}
KINDS = {"firsthand", "external", "interpretation"}
STRICT_ARENAS = {"journalism", "academic", "legal", "government"}
CONTRIBUTION_KINDS = {
    "human_original", "human_edit", "ai_research", "ai_generated_prose",
    "ai_substantive_rewrite", "mechanical_proofread",
}
AI_PROSE = {"ai_generated_prose", "ai_substantive_rewrite"}
AI_ASSIST = {"ai_research", "mechanical_proofread"}
SUPPORT_STATES = {"supported_by_reviewer", "needs_source", "conflicted", "unadjudicated"}
EXPERIENCE_STATES = {"observed", "said_by_author", "inferred", "sourced",
                     "hypothetical", "planned", "measured"}
PERFORMED_STATES = {"observed", "said_by_author", "measured", "sourced"}
DECISION_OUTCOMES = {"approve", "reject"}
MAX_BYTES = 5_000_000
MAX_DOSSIER_BYTES = 2_000_000
MAX_JSON_DEPTH = 32
MAX_LIST = 5_000
MAX_ANCHORS = 1_000
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
CONSEQUENTIAL_CLASSES = {"observed_fact", "sourced_fact", "inference"}

LIMITATIONS = [
    "Origin, consent and contribution declarations are self-reported and not independently authenticated.",
    "Exact excerpt presence establishes a text anchor, not truth, entailment or lived experience.",
    "REVIEW is a limited-check result; it does not authorize publication, submission or a claim of human authorship.",
    "Claim discovery uses the v4 sentence classifier; sentences it classifies as rhetoric are not checked.",
    "No detector probability, detector bypass, rewriting or authorship certification is performed.",
]


class Refusal(Exception):
    """A structured refusal: becomes a HOLD finding, never an uncaught crash."""

    def __init__(self, code, message):
        Exception.__init__(self, message)
        self.code = code


def digest(content):
    return hashlib.sha256(content).hexdigest()


def _check_relative(relative):
    if not isinstance(relative, str) or not relative:
        raise Refusal("PATH_MISSING", "path is missing")
    if "\x00" in relative:
        raise Refusal("PATH_INVALID", "path contains a NUL byte")
    if relative.startswith("/") or relative.startswith("\\") or re.match(r"^[A-Za-z]:", relative):
        raise Refusal("PATH_ABSOLUTE", "absolute paths are refused")
    parts = PurePosixPath(relative).parts
    if any(part == ".." for part in parts):
        raise Refusal("PATH_ESCAPE", "path escapes the dossier directory")
    parts = tuple(p for p in parts if p != ".")
    if not parts:
        raise Refusal("PATH_INVALID", "path names no file")
    return parts


def safe_read(root, relative, limit=MAX_BYTES):
    """Read a bounded UTF-8 file under `root`.

    Each component is opened relative to its parent directory with
    O_NOFOLLOW, so a symlink anywhere on the path is refused and the file
    read is the file checked (no stat-then-open race). The size is taken from
    the open descriptor and at most limit+1 bytes are ever read.
    """
    parts = _check_relative(relative)
    nofollow = getattr(os, "O_NOFOLLOW", None)
    directory = getattr(os, "O_DIRECTORY", None)
    if nofollow is None or directory is None or os.open not in os.supports_dir_fd:
        raise Refusal("PLATFORM_UNSUPPORTED",
                      "secure relative opening (O_NOFOLLOW, dir_fd) is unavailable on this platform")
    fds = []
    try:
        try:
            fds.append(os.open(str(root), os.O_RDONLY | directory))
        except OSError as exc:
            raise Refusal("ROOT_NOT_READABLE", "dossier directory is not readable: %s" % exc.strerror)
        for part in parts[:-1]:
            try:
                fds.append(os.open(part, os.O_RDONLY | directory | nofollow, dir_fd=fds[-1]))
            except OSError as exc:
                if exc.errno in (errno.ELOOP, errno.ENOTDIR):
                    raise Refusal("PATH_SYMLINK", "a path component is a symlink or not a directory")
                raise Refusal("PATH_NOT_FOUND", "path component not readable: %s" % exc.strerror)
        try:
            fd = os.open(parts[-1], os.O_RDONLY | nofollow, dir_fd=fds[-1])
        except OSError as exc:
            if exc.errno == errno.ELOOP:
                raise Refusal("PATH_SYMLINK", "the file is a symlink")
            raise Refusal("PATH_NOT_FOUND", "file not readable: %s" % exc.strerror)
        fds.append(fd)
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode):
            raise Refusal("PATH_NOT_FILE", "path is not a regular file")
        if info.st_size > limit:
            raise Refusal("FILE_TOO_LARGE", "file exceeds %d bytes" % limit)
        chunks, total = [], 0
        while total <= limit:
            chunk = os.read(fd, min(65536, limit + 1 - total))
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
        if total > limit:
            raise Refusal("FILE_TOO_LARGE", "file grew past %d bytes while reading" % limit)
        data = b"".join(chunks)
    finally:
        for fd in reversed(fds):
            os.close(fd)
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise Refusal("FILE_NOT_UTF8", "file is not valid UTF-8")
    return text, digest(data)


def _depth(value, level=0):
    if level > MAX_JSON_DEPTH:
        return level
    if isinstance(value, dict):
        if len(value) > MAX_LIST:
            raise Refusal("DOSSIER_OBJECT_TOO_LARGE", "an object exceeds %d keys" % MAX_LIST)
        return max([_depth(v, level + 1) for v in value.values()] or [level])
    if isinstance(value, list):
        if len(value) > MAX_LIST:
            raise Refusal("DOSSIER_LIST_TOO_LONG", "a list exceeds %d items" % MAX_LIST)
        return max([_depth(v, level + 1) for v in value] or [level])
    return level


def load_json_bounded(path, limit=MAX_DOSSIER_BYTES):
    """Parse a dossier with a byte, depth and size ceiling."""
    text, sha = safe_read(path.parent, path.name, limit)
    try:
        value = json.loads(text)
    except RecursionError:
        raise Refusal("DOSSIER_TOO_DEEP", "JSON nesting is too deep to parse")
    except ValueError as exc:
        raise Refusal("DOSSIER_JSON_INVALID", "not valid JSON: %s" % exc)
    if _depth(value) > MAX_JSON_DEPTH:
        raise Refusal("DOSSIER_TOO_DEEP", "JSON nesting exceeds %d levels" % MAX_JSON_DEPTH)
    return value, sha


_WI = None


def _wi_module():
    """The canonical v4 sentence splitter and classifier in scripts/wi.py."""
    global _WI
    if _WI is None:
        spec = importlib.util.spec_from_file_location(
            "wi_core_v8", str(Path(__file__).resolve().parent / "wi.py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _WI = module
    return _WI


def discover_claims(body):
    """Claim atoms the v4 classifier finds in `body`, with offsets."""
    wi = _wi_module()
    claims, offset = [], 0
    for sent in wi.sentences(body):
        pos = body.find(sent, offset)
        if pos < 0:
            pos = offset
        offset = pos + len(sent)
        cls, signals = wi.classify(sent)
        if cls == "rhetoric":
            continue
        claims.append({"id": "c%04d" % (len(claims) + 1), "text": sent, "class": cls,
                       "signals": signals, "start": pos, "end": pos + len(sent)})
    return claims


def parse_time(value):
    """Offset-aware ISO 8601, or None. A naive timestamp is refused."""
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = _dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def _str(value):
    return value if isinstance(value, str) and value.strip() else None


def _report(status, findings, fields):
    report = {
        "schema": AUDIT_SCHEMA,
        "status": status,
        "decision_scope": "limited_checks",
        "release_authorized": False,
        "declaration_status": "self_reported",
        "findings": findings,
        "limitations": list(LIMITATIONS),
    }
    report.update(fields)
    return report


def analyze(dossier, root, now=None):
    now = now or _dt.datetime.now(_dt.timezone.utc)
    findings = []

    def flag(code, level, message, target=None):
        findings.append({"code": code, "level": level, "message": message, "target": target})

    if not isinstance(dossier, dict):
        flag("ROOT_NOT_OBJECT", "hold", "The dossier root must be a JSON object.")
        return _report("HOLD", findings, {})

    if dossier.get("schema") not in SCHEMAS:
        flag("SCHEMA_INVALID", "hold", "Expected wi9-authorship-1 or wi9-authorship-2.")
    doc = dossier.get("document")
    if not isinstance(doc, dict):
        doc = {}
        flag("DOCUMENT_REQUIRED", "hold", "Document metadata must be an object.")
    origin = doc.get("origin")
    venue = doc.get("venue_policy")
    intended = doc.get("intended_use")
    arena = doc.get("arena")
    if arena is not None and not isinstance(arena, str):
        flag("ARENA_INVALID", "hold", "arena must be a string.")
        arena = None
    if isinstance(arena, str):
        arena = arena.strip().lower() or None
    consequential = doc.get("consequential", True)
    if not isinstance(consequential, bool):
        flag("CONSEQUENTIAL_INVALID", "hold", "document.consequential must be true or false.")
        consequential = True
    # An unknown or missing arena never lowers the bar: a submission is held
    # to the strict evidence rules unless it says, explicitly, that it makes
    # no consequential claim.
    strict = arena in STRICT_ARENAS or (doc.get("intended_use") == "submission" and consequential)
    if origin not in ORIGINS:
        flag("ORIGIN_UNKNOWN", "hold", "Declare human_authored, ai_assisted, or ai_generated.")
    if venue not in VENUES:
        flag("VENUE_POLICY_UNKNOWN", "hold", "Declare unrestricted, disclose_ai, or human_only.")
    if intended not in INTENDED:
        flag("INTENDED_USE_UNKNOWN", "hold", "Declare submission, research_demo, or internal_review.")
    submission = intended == "submission"
    human_only_sub = venue == "human_only" and submission
    if human_only_sub and origin != "human_authored":
        flag("HUMAN_ONLY_CONFLICT", "hold",
             "Human-only submissions cannot package AI-generated or AI-assisted authorship.")

    # Venue contract. Assistance the venue has not been recorded as allowing
    # is treated as not allowed on a human-only venue: unknown means no.
    contract = dossier.get("venue_contract")
    allowed_assist = set()
    if contract is not None:
        if not isinstance(contract, dict):
            flag("VENUE_CONTRACT_INVALID", "hold", "venue_contract must be an object.")
        else:
            raw = contract.get("allowed_assistance", [])
            if not isinstance(raw, list) or not all(isinstance(x, str) for x in raw):
                flag("VENUE_CONTRACT_INVALID", "hold", "allowed_assistance must be a list of strings.")
            else:
                unknown = sorted(x for x in raw if x not in CONTRIBUTION_KINDS)
                if unknown:
                    flag("VENUE_CONTRACT_INVALID", "hold", "Unknown assistance kinds: %s" % ", ".join(unknown))
                allowed_assist = set(raw) & CONTRIBUTION_KINDS
                if venue == "human_only" and allowed_assist & AI_PROSE:
                    flag("VENUE_CONTRACT_CONTRADICTION", "hold",
                         "A human-only venue contract cannot permit AI prose.")
            if contract.get("expires_at") is not None:
                when = parse_time(contract.get("expires_at"))
                if when is None:
                    flag("VENUE_CONTRACT_INVALID", "hold", "expires_at must be offset-aware ISO 8601.")
                elif when < now:
                    flag("VENUE_CONTRACT_EXPIRED", "hold", "The recorded venue policy has expired; re-read it.")

    # Contribution history: self-declared, typed, and checked against origin.
    log = dossier.get("contribution_log")
    if submission and not isinstance(log, list):
        flag("CONTRIBUTION_LOG_REQUIRED", "hold",
             "Submissions require a contribution history; missing data cannot certify eligibility.")
        log = []
    elif log is None:
        log = []
    elif not isinstance(log, list):
        flag("CONTRIBUTION_LOG_INVALID", "hold", "contribution_log must be a list.")
        log = []
    kinds_seen = set()
    for index, change in enumerate(log):
        tag = "contribution_log[%d]" % index
        if not isinstance(change, dict):
            flag("CONTRIBUTION_INVALID", "hold", "Contribution must be an object.", tag)
            continue
        kind = change.get("kind")
        if kind not in CONTRIBUTION_KINDS:
            flag("CONTRIBUTION_KIND_INVALID", "hold", "Unknown contribution kind.", tag)
            continue
        kinds_seen.add(kind)
        if human_only_sub and kind in AI_PROSE:
            flag("SUBSTANTIVE_AI_CONTRIBUTION", "hold",
                 "A declared AI prose contribution conflicts with human-only venue rules.", tag)
        if human_only_sub and kind in AI_ASSIST and kind not in allowed_assist:
            flag("ASSISTANCE_NOT_PERMITTED", "hold",
                 "The venue is not recorded as permitting %s; unknown means no." % kind, tag)
    if origin == "human_authored" and kinds_seen & AI_PROSE:
        flag("ORIGIN_CONTRADICTS_LOG", "hold",
             "origin says human_authored while the log declares AI prose or an AI substantive rewrite.")
    if origin == "ai_generated" and log and "ai_generated_prose" not in kinds_seen:
        flag("ORIGIN_CONTRADICTS_LOG", "hold",
             "origin says ai_generated while the log declares no AI-generated prose.")
    if human_only_sub and not log:
        flag("CONTRIBUTION_HISTORY_EMPTY", "hold",
             "Human-only submission needs an explicit authorship history.")

    if venue == "human_only" and intended == "research_demo" and origin != "human_authored":
        flag("RESEARCH_ONLY", "info", "AI material here is research-only, not a pitch.")
    if venue == "disclose_ai" and (origin != "human_authored" or kinds_seen & (AI_PROSE | AI_ASSIST)):
        flag("DISCLOSURE_NEEDED", "info", "AI contribution requires venue-appropriate disclosure.")

    body, document_hash = None, None
    try:
        body, document_hash = safe_read(root, doc.get("path"))
    except Refusal as exc:
        flag("DOCUMENT_NOT_READABLE", "hold", "%s: %s" % (exc.code, exc))
    expected_doc = doc.get("expected_sha256")
    if expected_doc is not None:
        if not isinstance(expected_doc, str) or not SHA_RE.match(expected_doc):
            flag("DOCUMENT_DIGEST_INVALID", "hold", "expected_sha256 must be 64 lowercase hex.")
        elif document_hash is not None and expected_doc != document_hash:
            flag("DOCUMENT_DIGEST_MISMATCH", "hold",
                 "The draft changed after its digest was pinned; any prior decision is stale.")
    elif submission:
        flag("DOCUMENT_DIGEST_UNPINNED", "hold",
             "A submission must pin document.expected_sha256 to the exact reviewed bytes.")

    # Evidence: unique ids, typed state, exact anchors in the declared source.
    evidence = dossier.get("evidence")
    if not isinstance(evidence, list):
        evidence = []
        flag("EVIDENCE_REQUIRED", "hold", "An evidence list is required.")
    if strict and not evidence:
        flag("STRICT_EVIDENCE_EMPTY", "hold", "This arena requires sourced claims.")
    evidence_by_id, anchor_ledger = {}, []
    for i, item in enumerate(evidence):
        tag = "evidence[%d]" % i
        if not isinstance(item, dict):
            flag("EVIDENCE_INVALID", "hold", "Evidence item must be an object.", tag)
            continue
        eid = _str(item.get("id"))
        if eid is None:
            flag("EVIDENCE_ID_MISSING", "hold", "Evidence needs a nonempty string id.", tag)
        elif eid in evidence_by_id:
            flag("EVIDENCE_ID_DUPLICATE", "hold", "Evidence id %r appears twice." % eid, tag)
            eid = None
        else:
            evidence_by_id[eid] = item
        if item.get("kind") not in KINDS:
            flag("KIND_UNKNOWN", "hold", "Choose firsthand, external, or interpretation.", tag)
        if item.get("consent") is not True:
            flag("CONSENT_ABSENT", "hold", "Explicit author consent is required.", tag)
        if item.get("kind") == "firsthand" and item.get("source_origin") != "human_authored":
            flag("FIRSTHAND_UNVERIFIED", "hold",
                 "Firsthand events cannot be inferred from AI text or a company roadmap.", tag)
        state = item.get("experience_state")
        if state is not None:
            if state not in EXPERIENCE_STATES:
                flag("EXPERIENCE_STATE_INVALID", "hold", "Unknown experience_state.", tag)
            elif item.get("kind") == "firsthand" and state not in PERFORMED_STATES:
                flag("FIRSTHAND_NOT_PERFORMED", "hold",
                     "A %s item cannot support a firsthand claim that something was done." % state, tag)
        support = item.get("support_status", "unadjudicated")
        if support not in SUPPORT_STATES:
            flag("SUPPORT_STATUS_INVALID", "hold", "Unknown support_status.", tag)
            support = "unadjudicated"
        if not item.get("claim"):
            flag("CLAIM_MISSING", "hold", "Claim description required.", tag)
        entry = {"evidence_id": eid, "anchor": "UNRESOLVED", "support_status": support,
                 "source_sha256": None}
        anchor_ledger.append(entry)
        quote = item.get("exact_excerpt")
        if not isinstance(quote, str) or not quote:
            flag("EXCERPT_MISSING", "hold", "Exact supporting excerpt required.", tag)
            continue
        try:
            source, source_hash = safe_read(root, item.get("source_path"))
        except Refusal as exc:
            flag("SOURCE_NOT_READABLE", "hold", "%s: %s" % (exc.code, exc), tag)
            continue
        entry["source_sha256"] = source_hash
        if quote not in source:
            flag("ANCHOR_MISSING", "hold", "Exact excerpt does not occur in the source.", tag)
        else:
            entry["anchor"] = "ANCHOR_RESOLVED"
        expected = item.get("sha256")
        if expected is not None and expected != source_hash:
            flag("SOURCE_DIGEST_MISMATCH", "hold", "Source bytes changed.", tag)
            entry["anchor"] = "STALE"
        elif expected is None and submission and strict:
            flag("SOURCE_DIGEST_UNPINNED", "hold",
                 "A consequential submission must pin each source's sha256.", tag)
        if submission and strict and support in {"needs_source", "conflicted"}:
            flag("SUPPORT_UNRESOLVED", "hold",
                 "Evidence is marked %s; a consequential submission cannot rest on it." % support, tag)

    # Draft anchors: each must resolve uniquely in the draft and name known evidence.
    passages = dossier.get("document_claim_anchors", [])
    if passages is None:
        passages = []
    if not isinstance(passages, list):
        flag("DOCUMENT_CLAIM_ANCHORS_INVALID", "hold", "document_claim_anchors must be a list.")
        passages = []
    if submission and strict and not passages:
        flag("DOCUMENT_CLAIM_ANCHORS_REQUIRED", "hold",
             "Consequential submissions must anchor claims to draft passages.")
    if len(passages) > MAX_ANCHORS:
        flag("DOCUMENT_CLAIM_ANCHORS_TOO_MANY", "hold",
             "More than %d draft anchors; split the document." % MAX_ANCHORS)
        passages = []
    spans = []
    for index, passage in enumerate(passages):
        tag = "document_claim_anchors[%d]" % index
        if not isinstance(passage, dict):
            flag("DOCUMENT_ANCHOR_INVALID", "hold", "Anchor must be an object.", tag)
            continue
        target = _str(passage.get("evidence_id"))
        if target is None:
            flag("DOCUMENT_ANCHOR_UNLINKED", "hold", "Draft passage must name its evidence item.", tag)
        elif target not in evidence_by_id:
            flag("DOCUMENT_EVIDENCE_NOT_FOUND", "hold",
                 "Draft anchor references no known evidence item.", tag)
            target = None
        snippet = passage.get("exact_excerpt")
        if not isinstance(snippet, str) or not snippet:
            flag("DOCUMENT_ANCHOR_EMPTY", "hold", "Document passage excerpt required.", tag)
            continue
        if body is None or snippet not in body:
            flag("DOCUMENT_ANCHOR_MISSING", "hold", "Claim excerpt is absent from the submitted draft.", tag)
            continue
        start = passage.get("start")
        if start is not None:
            if (not isinstance(start, int) or isinstance(start, bool) or start < 0
                    or not body.startswith(snippet, start)):
                flag("DOCUMENT_ANCHOR_OFFSET_MISMATCH", "hold",
                     "start does not locate the excerpt in the draft.", tag)
                continue
        else:
            start = body.find(snippet)
            if body.find(snippet, start + 1) >= 0:
                flag("DOCUMENT_ANCHOR_AMBIGUOUS", "hold",
                     "Excerpt occurs more than once in the draft; give its start offset.", tag)
                continue
        if target is not None:
            spans.append((start, start + len(snippet), target))

    # Claim coverage: every consequential claim the v4 classifier finds must
    # overlap an anchored span. One safe anchor cannot carry the rest.
    coverage = []
    if body is not None:
        try:
            claims = discover_claims(body)
        except Exception as exc:  # another file; report the failure, never crash
            claims = []
            flag("CLAIM_DISCOVERY_FAILED", "hold", "Claim discovery failed: %s" % exc)
        spans.sort()
        starts = [s for s, _, _ in spans]
        widest = max([e - s for s, e, _ in spans] or [0])
        for claim in claims:
            lo = bisect.bisect_left(starts, claim["start"] - widest)
            hi = bisect.bisect_left(starts, claim["end"])
            linked = sorted({t for s, e, t in spans[lo:hi] if e > claim["start"]})
            coverage.append({"claim_id": claim["id"], "class": claim["class"],
                             "start": claim["start"], "end": claim["end"],
                             "anchored": bool(linked), "evidence_ids": linked,
                             "support": "anchor_resolved_unadjudicated" if linked else "needs_source"})
            if claim["class"] in CONSEQUENTIAL_CLASSES and not linked:
                flag("CLAIM_UNANCHORED", "hold" if submission and strict else "advisory",
                     "Draft claim has no anchored evidence: %r" % claim["text"][:120], claim["id"])

    samples = dossier.get("voice_samples", [])
    if samples is None:
        samples = []
    if not isinstance(samples, list):
        flag("VOICE_SAMPLES_INVALID", "hold", "voice_samples must be a list.")
        samples = []
    if len(samples) < 3:
        flag("VOICE_BASELINE_INSUFFICIENT", "advisory",
             "A measured personal voiceprint needs >=3 consented, human-authored samples of >=500 words.")
    for i, sample in enumerate(samples):
        tag = "voice_samples[%d]" % i
        if not isinstance(sample, dict) or sample.get("consent") is not True or sample.get("origin") != "human_authored":
            flag("VOICE_SAMPLE_INELIGIBLE", "hold", "Sample must be consented and human-authored.", tag)
            continue
        try:
            content, source_hash = safe_read(root, sample.get("path"))
        except Refusal as exc:
            flag("VOICE_SAMPLE_NOT_READABLE", "hold", "%s: %s" % (exc.code, exc), tag)
            continue
        if len(re.findall(r"\b[\w'-]+\b", content)) < 500:
            flag("VOICE_SAMPLE_TOO_SHORT", "advisory", "Sample has fewer than 500 words.", tag)
        if sample.get("sha256") is not None and sample["sha256"] != source_hash:
            flag("VOICE_SAMPLE_DIGEST_MISMATCH", "hold", "Voice sample changed.", tag)

    status = "HOLD" if any(f["level"] == "hold" for f in findings) else "REVIEW"
    return _report(status, findings, {
        "document_sha256": document_hash,
        "declared_origin": origin,
        "venue_policy": venue,
        "intended_use": intended,
        "arena": arena,
        "claim_count": len(evidence),
        "evidence_anchors": anchor_ledger,
        "claim_coverage": coverage,
    })


RELEASE_CAPABILITY = "release.approve"


def _open_store_readonly(store, dossier_root):
    """Open an operator-named v6 store read-only, or raise Refusal.

    The store must sit outside the dossier directory: anyone who controls the
    dossier can write a store that grants themselves release. `.wi` and its
    database must be real files, not symlinks, and the database is opened with
    sqlite's read-only mode so a release check can never write to it.
    """
    if not isinstance(store, str) or not store:
        raise Refusal("AUTHORITY_STORE_REQUIRED",
                      "release needs --authority-store: the v6 workspace that holds release grants")
    root = Path(store).resolve()
    inner = Path(dossier_root).resolve()
    if root == inner or inner in root.parents:
        raise Refusal("AUTHORITY_STORE_UNTRUSTED",
                      "the authority store is inside the dossier directory; its author could grant themselves release")
    wi_dir = root / ".wi"
    db = wi_dir / "workspace.db"
    for part in (wi_dir, db):
        try:
            mode = os.lstat(str(part)).st_mode
        except OSError:
            raise Refusal("AUTHORITY_STORE_MISSING", "no v6 workspace store at %s" % store)
        if stat.S_ISLNK(mode):
            raise Refusal("AUTHORITY_STORE_SYMLINK", "%s is a symlink" % part.name)
    if not stat.S_ISREG(os.lstat(str(db)).st_mode):
        raise Refusal("AUTHORITY_STORE_MISSING", "workspace.db is not a regular file")
    try:
        conn = sqlite3.connect("file:%s?mode=ro" % db.as_posix(), uri=True)
        conn.row_factory = sqlite3.Row
        conn.execute("SELECT 1 FROM v6_grant LIMIT 1")
    except sqlite3.Error as exc:
        raise Refusal("AUTHORITY_STORE_UNREADABLE", "v6 store could not be read: %s" % exc)
    return conn


def _store_authorize(conn, actor, capability, scope, at):
    """The v6 authorize rule over a read-only connection; same order, same codes."""
    wi = _wi_module()
    held = []
    for r in conn.execute("SELECT * FROM v6_grant WHERE subject=? ORDER BY created_at", (actor,)):
        row = conn.execute("SELECT payload_json FROM v6_object WHERE digest=?", (r["digest"],)).fetchone()
        if row is None:
            raise Refusal("AUTHORITY_STORE_UNREADABLE", "a grant object is missing from the store")
        g = json.loads(row["payload_json"])
        g["_revoked_at"] = r["revoked_at"]
        held.append(g)
    if not held:
        raise Refusal("AUTHORITY_DENIED", "%s holds no capability grant" % actor)
    expired, revoked, out_of_scope = [], [], []
    for g in held:
        if not wi.v6_capability_covers(g.get("capability", ""), capability):
            continue
        if g.get("_revoked_at"):
            revoked.append(g)
            continue
        if (g.get("activates_at") and at < str(g["activates_at"])) or \
           (g.get("expires_at") and at >= str(g["expires_at"])):
            expired.append(g)
            continue
        if not wi.v6_scope_covers(g.get("scope") or {}, scope):
            out_of_scope.append(g)
            continue
        return g
    if revoked:
        raise Refusal("AUTHORITY_REVOKED", "every grant %s holds for %s has been revoked" % (actor, capability))
    if expired:
        raise Refusal("AUTHORITY_EXPIRED", "%s holds %s but the grant is not active at %s" % (actor, capability, at))
    if out_of_scope:
        raise Refusal("AUTHORITY_GRANT_SCOPE_EXCEEDED", "%s holds %s but not in this scope" % (actor, capability))
    raise Refusal("AUTHORITY_DENIED", "%s holds no grant covering %s" % (actor, capability))


def _v6_authorize(store, dossier_root, actor, venue, now, decided, flag):
    """Ask the operator's v6 store whether `actor` holds release.approve here.

    Checked twice: when the decision was made, and now. A grant revoked or
    expired since the decision cannot release, and a decision made before its
    grant was active was never authorized.
    """
    if actor is None or venue is None:
        return None
    scope = {"kind": "release_target", "value": venue}
    label = "now"
    try:
        conn = _open_store_readonly(store, dossier_root)
        try:
            granted = None
            for label, when in [("now", now)] + ([("decided_at", decided)] if decided is not None else []):
                granted = _store_authorize(conn, actor, RELEASE_CAPABILITY, scope,
                                           when.astimezone(_dt.timezone.utc).isoformat())
        finally:
            conn.close()
    except Refusal as exc:
        flag(exc.code, "v6 store refused release at %s: %s" % (label, exc))
        return None
    except (sqlite3.Error, ValueError, TypeError) as exc:
        flag("AUTHORITY_STORE_UNREADABLE", "v6 store could not be read: %s" % exc)
        return None
    return {"grant_id": granted.get("grant_id"), "capability": RELEASE_CAPABILITY,
            "scope": scope, "subject": actor, "subject_kind": granted.get("subject_kind"),
            "issuer": granted.get("issuer"), "basis": "verified", "store": str(Path(store).resolve())}


def release(dossier, root, now=None, authority_store=None):
    """Bind a person's review decision and authority grant to the exact draft."""
    now = now or _dt.datetime.now(_dt.timezone.utc)
    audit = analyze(dossier, root, now)
    findings = [dict(f) for f in audit["findings"] if f["level"] == "hold"]

    def flag(code, message):
        findings.append({"code": code, "level": "hold", "message": message, "target": "release"})

    if not isinstance(dossier, dict):
        dossier = {}
    if audit["status"] != "REVIEW":
        flag("AUDIT_NOT_REVIEW", "The limited audit holds; release cannot be considered.")
    doc_sha = audit.get("document_sha256")
    if audit.get("intended_use") != "submission":
        flag("NOT_A_SUBMISSION", "Only a declared submission can become release-eligible.")

    contract = dossier.get("venue_contract")
    contract = contract if isinstance(contract, dict) else {}
    venue_name = _str(contract.get("venue"))
    if venue_name is None:
        flag("VENUE_UNNAMED", "The venue contract must name the venue it was read from.")
    ops = contract.get("allowed_operations")
    if not isinstance(ops, list) or "submit" not in ops:
        flag("SUBMIT_NOT_PERMITTED", "The venue contract does not record that submission is open.")
    if contract.get("deadline") is not None:
        deadline = parse_time(contract.get("deadline"))
        if deadline is None:
            flag("DEADLINE_INVALID", "deadline must be offset-aware ISO 8601.")
        elif deadline < now:
            flag("DEADLINE_PASSED", "The venue deadline has passed.")

    decision = dossier.get("review_decision")
    if not isinstance(decision, dict):
        flag("DECISION_REQUIRED", "A person's review decision bound to this draft is required.")
        decision = {}
    outcome = decision.get("outcome")
    if outcome not in DECISION_OUTCOMES:
        flag("DECISION_OUTCOME_INVALID", "outcome must be approve or reject.")
    elif outcome != "approve":
        flag("DECISION_REJECTED", "The reviewer rejected this draft.")
    if doc_sha is None or decision.get("target_sha256") != doc_sha:
        flag("DECISION_TARGET_STALE", "The decision names a different draft digest; it is stale.")
    if decision.get("actor_kind") != "human":
        flag("DECISION_NOT_HUMAN", "Release decisions are made by a person, never by a model or tool.")
    actor = _str(decision.get("actor"))
    if actor is None:
        flag("DECISION_ACTOR_MISSING", "The deciding person must be named.")
    decided = parse_time(decision.get("decided_at"))
    if decided is None:
        flag("DECISION_TIME_INVALID", "decided_at must be offset-aware ISO 8601.")
    elif decided > now:
        flag("DECISION_TIME_FUTURE", "decided_at is in the future.")

    # Authority is read from the v6 grant store, never from the dossier. A
    # grant written into the dossier is a claim about authority, and the
    # person who wrote the dossier is the person whose authority is in doubt.
    binding = decision.get("authority")
    receipt = None
    if not isinstance(binding, dict):
        flag("AUTHORITY_REQUIRED", "The decision must name the v6 grant store it acts under.")
        binding = {}
    if binding.get("store") != "v6":
        flag("AUTHORITY_UNBOUND",
             "A grant declared in the dossier is not authority; bind the decision "
             "to the v6 store (authority.store = \"v6\").")
    elif "workspace" in binding:
        flag("AUTHORITY_STORE_FROM_DOSSIER",
             "The dossier may not choose the authority store; the operator names it with --authority-store.")
    else:
        receipt = _v6_authorize(authority_store, root, actor, venue_name, now, decided, flag)
    if receipt is not None and receipt.get("subject_kind") != "human":
        flag("AUTHORITY_NOT_HUMAN",
             "The v6 grant is held by a %s; release is decided by a person." % receipt.get("subject_kind"))
        receipt = None

    status = "HOLD" if findings else "RELEASE_ELIGIBLE"
    return {
        "schema": RELEASE_SCHEMA,
        "status": status,
        "document_sha256": doc_sha,
        "venue": venue_name,
        "release_authorized": status == "RELEASE_ELIGIBLE",
        "transmission_performed": False,
        "declaration_status": "self_reported",
        "authority_receipt": receipt if status == "RELEASE_ELIGIBLE" else None,
        "findings": findings,
        "limitations": LIMITATIONS + [
            "RELEASE_ELIGIBLE means the gates agree; this tool sends nothing.",
            "Authority is checked in the local v6 grant store; the store proves who was granted what, not who typed the decision.",
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command")
    sub.required = True
    for name, text in (("audit", "audit a local authorship and evidence dossier"),
                       ("release", "check a reviewed submission against its decision and grant")):
        cmd = sub.add_parser(name, help=text)
        cmd.add_argument("--input", required=True)
        cmd.add_argument("--out")
        if name == "release":
            cmd.add_argument("--authority-store", dest="authority_store",
                             help="the v6 workspace holding release grants; must be outside the dossier directory")
    args = parser.parse_args(argv)
    try:
        path = Path(args.input)
        if path.is_symlink():
            raise Refusal("PATH_SYMLINK", "the dossier is a symlink")
        path = path.resolve()
        dossier, _ = load_json_bounded(path)
        result = (analyze(dossier, path.parent) if args.command == "audit"
                  else release(dossier, path.parent, authority_store=args.authority_store))
    except Refusal as exc:
        result = _report("HOLD", [{"code": exc.code, "level": "hold", "message": str(exc),
                                   "target": "dossier"}], {})
    except (OSError, ValueError, TypeError, RecursionError) as exc:
        result = _report("HOLD", [{"code": "DOSSIER_INVALID", "level": "hold", "message": str(exc),
                                   "target": "dossier"}], {})
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        try:
            fd = os.open(args.out, os.O_WRONLY | os.O_CREAT | os.O_TRUNC | getattr(os, "O_NOFOLLOW", 0), 0o644)
            with os.fdopen(fd, "w", encoding="utf-8") as out:
                out.write(rendered)
        except OSError as exc:
            sys.stdout.write(json.dumps(_report("HOLD", [{"code": "OUT_NOT_WRITABLE", "level": "hold",
                                                           "message": str(exc), "target": "--out"}], {}),
                                        indent=2, sort_keys=True) + "\n")
            return 3
    else:
        sys.stdout.write(rendered)
    if result["status"] == "REVIEW":
        sys.stderr.write("REVIEW: limited checks passed. This is not permission to publish or send.\n")
    ok = {"audit": "REVIEW", "release": "RELEASE_ELIGIBLE"}[args.command]
    return 0 if result["status"] == ok else 3


if __name__ == "__main__":
    raise SystemExit(main())
