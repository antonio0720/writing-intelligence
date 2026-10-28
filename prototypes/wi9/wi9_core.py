#!/usr/bin/env python3
"""Writing Intelligence v9 reference kernel (experimental, offline, Python >=3.8).

Project owner: Antonio T. Smith Jr. / Density6 LLC
This is an additive engineering specimen, not the shipped Writing Intelligence CLI.
No authorship certification, publication authorization, or detector optimization.
"""
import argparse
import hashlib
import json
import math
import os
import re
import stat
import statistics
import sys
from collections import Counter
from pathlib import Path

MAX_FILE_BYTES = 5_000_000
MAX_MANIFEST_BYTES = 1_000_000
MAX_LIST = 5_000  # bounds work per manifest (independent review finding 14)
SCHEMA = "wi9.preflight/1"
ORIGINS = {"human_authored", "ai_assisted", "ai_generated", "unknown"}
USES = {"research", "internal_review", "submission"}
POLICIES = {"human_only", "disclosure_required", "ai_permitted", "unknown"}
CONTRIBUTIONS = {"human_original", "human_edit", "human_review", "ai_research", "ai_generated_prose", "ai_substantive_rewrite", "mechanical_proofread"}
SOURCE_KINDS = {"firsthand", "external", "interpretation", "hypothetical", "planned"}
RISKY_AI = {"ai_generated_prose", "ai_substantive_rewrite"}
METRICS = ("original_thought", "evidence_integrity", "voice_fidelity", "argument_consequence", "reader_usefulness", "natural_phrasing", "uncertainty_discipline", "editorial_restraint")


def sha256(blob):
    return hashlib.sha256(blob).hexdigest()


def bounded_read(root, relpath, limit=MAX_FILE_BYTES):
    """Open local regular files through dir_fd; reject traversal and symlinks.

    Implemented for POSIX hosts with O_NOFOLLOW + dir_fd. No promise of protection
    against hostile changes by a privileged actor controlling the root directory.
    """
    if not isinstance(relpath, str) or not relpath or "\x00" in relpath:
        raise ValueError("PATH_INVALID")
    p = Path(relpath)
    if p.is_absolute() or any(part in (".", "..", "") for part in p.parts):
        raise ValueError("PATH_TRAVERSAL")
    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY") or os.open not in os.supports_dir_fd:
        raise RuntimeError("PLATFORM_UNSUPPORTED_POSIX_REQUIRED")
    directory = Path(root).resolve(strict=True)
    dirfd = os.open(str(directory), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        parts = p.parts
        for part in parts[:-1]:
            nextfd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=dirfd)
            os.close(dirfd)
            dirfd = nextfd
        fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW, dir_fd=dirfd)
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode):
                raise ValueError("NON_REGULAR_FILE")
            if info.st_size > limit:
                raise ValueError("FILE_OVERSIZE")
            with os.fdopen(fd, "rb", closefd=False) as inp:
                raw = inp.read(limit + 1)
            if len(raw) > limit:
                raise ValueError("FILE_OVERSIZE")
            return raw
        finally:
            os.close(fd)
    finally:
        os.close(dirfd)


def read_text(root, path):
    return bounded_read(root, path).decode("utf-8", errors="strict")


def _is_sha(s):
    return isinstance(s, str) and bool(re.fullmatch(r"[0-9a-f]{64}", s))


def _report(code, severity, detail, target=""):
    return {"code": code, "severity": severity, "detail": detail, "target": target}


def _check_id(items, label, issues):
    ids = set()
    for i, obj in enumerate(items):
        key = obj.get("id") if isinstance(obj, dict) else None
        if not isinstance(key, str) or not key.strip():
            issues.append(_report("ID_MISSING", "HOLD", "Nonempty ID required", "%s[%d]" % (label, i)))
        elif key in ids:
            issues.append(_report("DUPLICATE_ID", "HOLD", "Duplicate object ID: %s" % key, label))
        else:
            ids.add(key)
    return ids


def preflight(data, root):
    """Finite, deterministic dossier checks. HOLD != an authorship verdict.

    This tool checks only declared claims and text anchors. It does not claim
    exhaustive claim extraction, factual entailment, or independent author ID.
    """
    issues = []
    if not isinstance(data, dict):
        return {"status": "HOLD", "issues": [_report("INVALID_ROOT", "HOLD", "Top-level JSON must be an object")], "release_authorized": False}
    for key in ("contributions", "evidence", "claim_links"):
        if isinstance(data.get(key), list) and len(data[key]) > MAX_LIST:
            return {"status": "HOLD", "issues": [_report("LIST_TOO_LONG", "HOLD", "%s exceeds %d items" % (key, MAX_LIST))], "release_authorized": False}
    if data.get("schema") != SCHEMA:
        issues.append(_report("SCHEMA_UNKNOWN", "HOLD", "Expected %s" % SCHEMA))
    doc = data.get("document")
    venue = data.get("venue")
    if not isinstance(doc, dict):
        doc = {}
        issues.append(_report("DOCUMENT_MISSING", "HOLD", "Document object required"))
    if not isinstance(venue, dict):
        venue = {}
        issues.append(_report("VENUE_MISSING", "HOLD", "Venue object required"))
    use, origin, policy = doc.get("intended_use"), doc.get("origin"), venue.get("policy")
    if use not in USES:
        issues.append(_report("USE_INVALID", "HOLD", "Use must be research/internal_review/submission"))
    if origin not in ORIGINS:
        issues.append(_report("ORIGIN_INVALID", "HOLD", "Origin must be explicitly classified"))
    if policy not in POLICIES:
        issues.append(_report("POLICY_INVALID", "HOLD", "Venue policy must be classified"))
    if policy == "unknown" and use == "submission":
        issues.append(_report("POLICY_UNKNOWN", "HOLD", "Venue policy cannot authorize a submission"))
    if use == "submission" and origin == "unknown":
        issues.append(_report("ORIGIN_UNKNOWN", "HOLD", "Authorship origin unknown"))
    if policy == "human_only" and use == "submission" and origin != "human_authored":
        issues.append(_report("HUMAN_ONLY_ORIGIN", "HOLD", "Declared origin conflicts with venue policy"))
    if policy == "disclosure_required" and use == "submission" and origin in ("ai_assisted", "ai_generated") and venue.get("disclosure_recorded") is not True:
        issues.append(_report("DISCLOSURE_ABSENT", "HOLD", "AI assistance disclosure required"))
    if venue.get("policy_source") in (None, ""):
        issues.append(_report("POLICY_SOURCE_MISSING", "HOLD" if use == "submission" else "ADVISORY", "Record the source of the policy"))
    contributions = data.get("contributions")
    if not isinstance(contributions, list):
        contributions = []
        issues.append(_report("CONTRIBUTIONS_INVALID", "HOLD" if use == "submission" else "ADVISORY", "Contribution log list required"))
    if use == "submission" and not contributions:
        issues.append(_report("CONTRIBUTIONS_EMPTY", "HOLD", "No contribution events recorded"))
    for i, event in enumerate(contributions):
        if not isinstance(event, dict) or event.get("kind") not in CONTRIBUTIONS:
            issues.append(_report("CONTRIBUTION_INVALID", "HOLD", "Unknown contribution", str(i)))
        elif policy == "human_only" and use == "submission" and event["kind"] in RISKY_AI:
            issues.append(_report("HUMAN_ONLY_AI_PROSE", "HOLD", "Substantive AI prose in a human-only submission", str(i)))
    if policy == "human_only" and use == "submission" and any(isinstance(x, dict) and x.get("kind") == "ai_research" for x in contributions):
        issues.append(_report("VENUE_ASSISTANCE_SCOPE_REVIEW", "HOLD", "Human-only venue may prohibit additional AI assistance; explicit review needed"))
    raw = None
    try:
        raw = bounded_read(root, doc.get("path"))
    except (OSError, UnicodeError, ValueError, RuntimeError, TypeError) as exc:
        issues.append(_report("DOCUMENT_READ_FAILED", "HOLD", type(exc).__name__ + ": " + str(exc)))
    if raw is not None:
        if not _is_sha(doc.get("expected_sha256")):
            issues.append(_report("DOCUMENT_DIGEST_REQUIRED", "HOLD" if use == "submission" else "ADVISORY", "Pin document digest to reviewed bytes"))
        elif sha256(raw) != doc["expected_sha256"]:
            issues.append(_report("DOCUMENT_DIGEST_MISMATCH", "HOLD", "Document changed since review"))
        try:
            body = raw.decode("utf-8", errors="strict")
        except UnicodeError:
            body = ""
            issues.append(_report("DOCUMENT_UTF8_INVALID", "HOLD", "Document must be UTF-8"))
    else:
        body = ""
    evidence = data.get("evidence")
    if not isinstance(evidence, list):
        evidence = []
        issues.append(_report("EVIDENCE_INVALID", "HOLD", "Evidence list required"))
    ids = _check_id(evidence, "evidence", issues)
    if doc.get("arena") in ("journalism", "legal", "academic", "government") and not evidence:
        issues.append(_report("STRICT_EVIDENCE_REQUIRED", "HOLD", "Consequential work requires evidence"))
    for i, item in enumerate(evidence):
        target = "evidence[%d]" % i
        if not isinstance(item, dict):
            issues.append(_report("EVIDENCE_ITEM_INVALID", "HOLD", "Evidence must be an object", target))
            continue
        if item.get("kind") not in SOURCE_KINDS:
            issues.append(_report("EVIDENCE_KIND_INVALID", "HOLD", "Unknown evidence kind", target))
        if item.get("consent") is not True:
            issues.append(_report("SOURCE_CONSENT_ABSENT", "HOLD", "Source consent not recorded", target))
        if item.get("kind") == "firsthand" and item.get("origin") != "human_authored":
            issues.append(_report("FIRSTHAND_NOT_AUTHORED", "HOLD", "Firsthand memory not supported by declared human-original source", target))
        quote = item.get("exact_excerpt")
        try:
            material = bounded_read(root, item.get("path"))
            if not isinstance(quote, str) or not quote or quote not in material.decode("utf-8", errors="strict"):
                issues.append(_report("SOURCE_ANCHOR_MISSING", "HOLD", "Exact excerpt absent", target))
            if item.get("expected_sha256") is not None:
                if not _is_sha(item["expected_sha256"]) or sha256(material) != item["expected_sha256"]:
                    issues.append(_report("SOURCE_DIGEST_MISMATCH", "HOLD", "Pinned source digest mismatch", target))
        except (OSError, UnicodeError, ValueError, RuntimeError, TypeError) as exc:
            issues.append(_report("SOURCE_READ_FAILED", "HOLD", type(exc).__name__ + ": " + str(exc), target))
    links = data.get("claim_links")
    if not isinstance(links, list):
        links = []
        issues.append(_report("CLAIM_LINKS_INVALID", "HOLD", "Claim-link list required"))
    for i, link in enumerate(links):
        target = "claim_links[%d]" % i
        if not isinstance(link, dict):
            issues.append(_report("LINK_INVALID", "HOLD", "Claim link must be object", target))
            continue
        passage, evidence_id = link.get("exact_passage"), link.get("evidence_id")
        if not isinstance(passage, str) or not passage or passage not in body:
            issues.append(_report("CLAIM_PASSAGE_MISSING", "HOLD", "Claim passage absent from document", target))
        if not isinstance(evidence_id, str) or evidence_id not in ids:
            issues.append(_report("CLAIM_EVIDENCE_UNRESOLVED", "HOLD", "Evidence ID does not exist", target))
    if use == "submission" and doc.get("arena") in ("journalism", "legal", "academic", "government") and not links:
        issues.append(_report("CLAIM_LINKS_EMPTY", "HOLD", "Submission needs claims linked to sources"))
    if use == "submission" and data.get("full_claim_review") is not True:
        issues.append(_report("FULL_CLAIM_REVIEW_ABSENT", "HOLD", "A reviewer must certify claim-coverage work; excerpt checks are not exhaustive"))
    # Report never permits release. A separate canonical v6 authority-controlled
    # transition must exist and bind review to exact source/document digests.
    status = "HOLD" if any(x["severity"] == "HOLD" for x in issues) else "REVIEW"
    return {"schema": "wi9.preflight.report/1", "status": status, "release_authorized": False,
            "document_sha256": sha256(raw) if raw is not None else None,
            "declared_origin": origin, "venue_policy": policy, "intended_use": use,
            "evidence_count": len(evidence), "linked_claims": len(links), "issues": issues,
            "limitations": ["Declarations are self-reported, not independent identity proof.",
                            "Exact excerpt matching is not entailment or factual truth.",
                            "Claim coverage is not mechanically exhaustive.",
                            "REVIEW is never a send, publish, or release authorization."]}


def _sentences(text):
    pieces = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", text.replace("\n", " "))
    return [x.strip() for x in pieces if x.strip()]


QUALIFIERS = re.compile(r"\b(?:may|might|could|perhaps|possibly|likely|probably|seems?|appears?|suggests?|"
                        r"i think|i suspect|in my view|maybe|tends? to|somewhat|arguably|apparently)\b", re.I)
INTENSIFIERS = re.compile(r"\b(?:very|really|extremely|incredibly|truly|absolutely|totally|deeply|highly|"
                          r"utterly|completely|enormously)\b", re.I)
DISAGREEMENT = re.compile(r"\b(?:disagree|wrong|however|but|yet|i doubt|not convinced|mistaken|on the contrary|"
                          r"misses the point|i don't buy|that is not)\b", re.I)
EXAMPLE = re.compile(r"\b(?:for example|for instance|such as|e\.g\.|take the case|consider)\b", re.I)
CAUSAL = re.compile(r"\b(?:because|due to|so that|therefore|thus|as a result|led to|caused)\b", re.I)
CONCEDE = re.compile(r"\b(?:although|though|admittedly|granted|to be fair|that said|even so)\b", re.I)
CONCRETE_DETAIL = re.compile(r"\d|(?<=\w\s)[A-Z][a-z]{2,}")
STRATEGIES = ("example", "causal", "concession", "question")
# Voice measures compared for drift and held-out stability. The floor is the
# smallest band that is not noise for a few hundred words of text.
VOICE_MEASURES = {
    "mean_sentence_words": 2.0, "sentence_length_sd": 2.0, "type_token_ratio": 0.03,
    "first_person_per_1000": 3.0, "qualifiers_per_1000": 3.0, "intensifiers_per_1000": 2.0,
    "disagreement_per_1000": 3.0, "concrete_detail_share": 0.05, "example_share": 0.05,
    "causal_share": 0.05, "concession_share": 0.05, "question_share": 0.05,
}


def _per_1000(pattern, text, words):
    return round(1000 * len(pattern.findall(text)) / words, 2) if words else 0


def _share(pattern, sentences):
    return round(sum(1 for x in sentences if pattern.search(x)) / len(sentences), 4) if sentences else 0


def profile_text(text):
    words = re.findall(r"\b[\w'-]+\b", text.lower(), re.UNICODE)
    sentences = _sentences(text)
    lengths = [len(re.findall(r"\b[\w'-]+\b", x)) for x in sentences]
    paras = [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    counts = Counter(words)
    shares = {"example": _share(EXAMPLE, sentences), "causal": _share(CAUSAL, sentences),
              "concession": _share(CONCEDE, sentences),
              "question": round(sum(1 for x in sentences if x.rstrip().endswith("?")) / len(sentences), 4)
              if sentences else 0}
    top = max(STRATEGIES, key=lambda k: shares[k])
    return {"qualifiers_per_1000": _per_1000(QUALIFIERS, text, len(words)),
            "intensifiers_per_1000": _per_1000(INTENSIFIERS, text, len(words)),
            "disagreement_per_1000": _per_1000(DISAGREEMENT, text, len(words)),
            "concrete_detail_share": _share(CONCRETE_DETAIL, sentences),
            "example_share": shares["example"], "causal_share": shares["causal"],
            "concession_share": shares["concession"], "question_share": shares["question"],
            "argument_strategy": top if shares[top] >= 0.1 else "mixed",
            "word_count": len(words), "sentence_count": len(sentences), "paragraph_count": len(paras),
            "mean_sentence_words": round(statistics.mean(lengths), 2) if lengths else 0,
            "sentence_length_sd": round(statistics.pstdev(lengths), 2) if len(lengths) >= 2 else 0,
            "type_token_ratio": round(len(counts) / len(words), 4) if words else 0,
            "first_person_per_1000": round(1000 * sum(counts.get(w, 0) for w in ("i", "my", "me", "mine")) / len(words), 2) if words else 0,
            "question_count": text.count("?"), "exclamation_count": text.count("!"),
            "top_terms": [w for w, n in counts.most_common(12)]}


def editorial_diagnostics(text):
    """Surface editorial warnings only; none measure AI origin or quality."""
    findings = []
    patterns = [
        ("HOLLOW_CONTRAST", r"\b(?:it's|it is) not\b.{0,95}\b(?:it's|it is|but)\b", "Inspect whether the contrast contains a real difference."),
        ("VAGUE_ORIGIN", r"\b(?:many experts agree|it is widely known|studies show)\b", "A source and exact scope are required."),
        ("FORMULAIC_OPEN", r"(?mi)^\s*(?:in today's fast-paced world|in a world where|what if i told you)\b", "Open on the actual observation or problem."),
        ("EMPTY_CLOSURE", r"\b(?:and that changes everything|this is a game.changer)\b", "Make the consequence concrete or remove the slogan."),
    ]
    for code, regex, suggestion in patterns:
        for m in list(re.finditer(regex, text, flags=re.I | re.S))[:20]:
            findings.append({"code": code, "start": m.start(), "end": m.end(),
                             "excerpt": text[m.start():m.end()][:180], "question": suggestion})
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if len(paras) >= 5:
        counts = [len(_sentences(p)) for p in paras]
        if len(set(counts)) <= 2:
            findings.append({"code": "PARAGRAPH_PATTERN", "question": "Do these paragraph lengths arise from the argument, or a template?"})
    from wi9_hotphrases import scan_text
    from wi9_structure import analyze as structure_analyze
    hot_phrases = scan_text(text)
    return {"profile": profile_text(text), "findings": findings, "hot_phrases": hot_phrases,
            "structure": structure_analyze(text),
            "scope": "editorial diagnostics, not authorship classification"}


def voice_baseline(samples, root, min_samples=3, min_words=500):
    issues, metrics = [], []
    if not isinstance(samples, list) or len(samples) > MAX_LIST:
        return {"status": "HOLD", "issues": [_report("VOICE_SAMPLES_INVALID", "HOLD", "samples must be a list of at most %d" % MAX_LIST)]}
    for i, sample in enumerate(samples):
        if not isinstance(sample, dict) or sample.get("origin") != "human_authored" or sample.get("consent") is not True:
            issues.append(_report("VOICE_SOURCE_INELIGIBLE", "HOLD", "Human-authored and consented sample required", str(i)))
            continue
        try:
            blob = bounded_read(root, sample.get("path"))
            if not _is_sha(sample.get("sha256")) or sha256(blob) != sample["sha256"]:
                issues.append(_report("VOICE_DIGEST_MISMATCH", "HOLD", "Sample digest missing or changed", str(i)))
            profile = profile_text(blob.decode("utf-8", errors="strict"))
            if profile["word_count"] < min_words:
                issues.append(_report("VOICE_SAMPLE_SHORT", "HOLD", "Need at least %d words" % min_words, str(i)))
            metrics.append({"sample_id": sample.get("id"), "genre": sample.get("genre"), "sha256": sha256(blob),
                            "metrics": profile, "_text": blob.decode("utf-8")})
        except (OSError, UnicodeError, ValueError, RuntimeError, TypeError) as exc:
            issues.append(_report("VOICE_READ_FAILED", "HOLD", str(exc), str(i)))
    if len(metrics) < min_samples:
        issues.append(_report("VOICE_SAMPLE_COUNT", "HOLD", "Need %d distinct eligible samples" % min_samples))
    digests = [x["sha256"] for x in metrics]
    if len(digests) != len(set(digests)):
        issues.append(_report("VOICE_DUPLICATED_SAMPLE", "HOLD", "Same source submitted twice"))
    genres = {x["genre"] for x in metrics}
    if len(genres) > 1:
        issues.append(_report("VOICE_GENRE_MIX", "HOLD", "Separate per-genre voice baselines"))
    compared = metrics[:MAX_PAIRWISE_SAMPLES]
    if len(metrics) > MAX_PAIRWISE_SAMPLES:
        issues.append(_report("VOICE_TOO_MANY_SAMPLES", "HOLD", "Use at most %d samples per baseline"
                              % MAX_PAIRWISE_SAMPLES))
    for a in range(len(compared)):
        for b in range(a + 1, len(compared)):
            overlap = _shingle_overlap(metrics[a]["_text"], metrics[b]["_text"])
            if overlap >= NEAR_DUPLICATE:
                issues.append(_report("VOICE_SAMPLES_TOO_SIMILAR", "HOLD",
                                      "Samples %s and %s share %d%% of their phrasing; a baseline built on one "
                                      "passage describes that passage, not you" % (
                                          metrics[a]["sample_id"], metrics[b]["sample_id"], round(100 * overlap))))
    stability = _held_out_stability([x["metrics"] for x in metrics]) if len(metrics) >= 3 else {}
    for x in metrics:
        x.pop("_text", None)
    status = "HOLD" if issues else "REVIEW"
    genre = next(iter(genres)) if len(genres) == 1 else None
    return {"status": status, "source_count": len(metrics), "genre": genre,
            "baseline_digest": sha256(json.dumps([genre, sorted(digests)]).encode("utf-8")) if metrics else None,
            "sources": metrics, "mean_metrics": {
                k: round(statistics.mean(x["metrics"][k] for x in metrics), 3) for k in VOICE_MEASURES
            } if metrics else {}, "held_out_stability": stability, "issues": issues,
            "note": "Similarity to these samples is a voice diagnostic, not proof of human authorship."}


NEAR_DUPLICATE = 0.6
MAX_PAIRWISE_SAMPLES = 200


def _shingles(text, n=8):
    words = re.findall(r"\b[\w'-]+\b", text.lower())
    return {" ".join(words[i:i + n]) for i in range(max(0, len(words) - n + 1))}


def _shingle_overlap(a, b):
    sa, sb = _shingles(a), _shingles(b)
    return len(sa & sb) / min(len(sa), len(sb)) if sa and sb else 0.0


def _band(values, measure):
    centre = statistics.mean(values)
    spread = statistics.pstdev(values) if len(values) >= 2 else 0
    return centre, max(2 * spread, 0.2 * abs(centre), VOICE_MEASURES[measure])


def _held_out_stability(profiles):
    """Leave one sample out, build the band from the rest, and ask whether the
    held-out sample falls inside it. A measure that holds for every sample is
    one this writer's baseline can speak to; one that does not is reported, not hidden."""
    report = {}
    for measure in VOICE_MEASURES:
        inside = 0
        for i, held in enumerate(profiles):
            rest = [p[measure] for j, p in enumerate(profiles) if j != i]
            centre, width = _band(rest, measure)
            inside += abs(held[measure] - centre) <= width
        report[measure] = {"held_out_within_band": inside, "samples": len(profiles),
                           "stable": inside == len(profiles)}
    return report


def voice_compare(samples, root, text):
    """Where a text sits against the writer's own baseline, measure by measure.

    Drift is a question for the writer. Sitting inside every band does not show
    the writer wrote the text: a careful imitation can match these numbers.
    """
    baseline = voice_baseline(samples, root)
    if baseline["status"] != "REVIEW":
        return {"status": "HOLD", "issues": [_report("VOICE_BASELINE_NOT_READY", "HOLD",
                                                     "Compare against a baseline that qualifies")] + baseline["issues"]}
    profile = profile_text(text)
    drift = []
    for measure in VOICE_MEASURES:
        centre, width = _band([x["metrics"][measure] for x in baseline["sources"]], measure)
        if abs(profile[measure] - centre) > width:
            drift.append({"measure": measure, "text": profile[measure], "baseline": round(centre, 3),
                          "band": round(width, 3), "direction": "higher" if profile[measure] > centre else "lower",
                          "held_out_stable": baseline["held_out_stability"][measure]["stable"]})
    return {"status": "REVIEW", "baseline_digest": baseline["baseline_digest"], "genre": baseline["genre"],
            "profile": profile, "drift": drift, "release_authorized": False,
            "note": "Drift is an editorial question for the writer. Matching the baseline does not show who wrote "
                    "the text; a deliberate imitation can match every measure."}


VOICE_DECISIONS = ("approve", "reject")


def voice_review(samples, root, decision, reviewed_at, note=""):
    """Record one writer's own decision about their own baseline, in their own folder.

    Every user supplies their own samples; nothing here ships a corpus. The record
    binds the decision to the baseline digest, so changing a sample makes it stale.
    An approval says the writer recognises the measurements. It proves nothing about
    who wrote any other text.
    """
    if decision not in VOICE_DECISIONS:
        return {"status": "HOLD", "issues": [_report("VOICE_DECISION_INVALID", "HOLD", "decision must be approve or reject")]}
    baseline = voice_baseline(samples, root)
    if decision == "approve" and baseline["status"] != "REVIEW":
        return {"status": "HOLD", "issues": [_report("VOICE_BASELINE_NOT_READY", "HOLD", "Only a baseline that qualifies can be approved")] + baseline["issues"]}
    if baseline.get("baseline_digest") is None:
        return {"status": "HOLD", "issues": [_report("VOICE_BASELINE_NOT_READY", "HOLD", "No readable sample to review")] + baseline["issues"]}
    record = {"schema": "wi9.voice-review/1", "decision": decision, "reviewed_at": reviewed_at,
              "genre": baseline["genre"], "baseline_digest": baseline["baseline_digest"],
              "sample_digests": sorted(x["sha256"] for x in baseline["sources"]),
              "mean_metrics": baseline["mean_metrics"], "note": str(note)[:2000],
              "scope": "The writer's own review of their own measurements. Not proof of authorship."}
    name = "voice-review-%s.json" % baseline["baseline_digest"][:12]
    directory = Path(root)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    dirfd = os.open(str(directory), os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0))
    try:
        try:
            fd = os.open(name, flags, 0o600, dir_fd=dirfd)
        except FileExistsError:
            return {"status": "HOLD", "issues": [_report("VOICE_ALREADY_REVIEWED", "HOLD", "This exact baseline already has a review; change a sample to review again", name)]}
        with os.fdopen(fd, "w", encoding="utf-8") as out:
            json.dump(record, out, indent=2, sort_keys=True)
    finally:
        os.close(dirfd)
    return {"status": "REVIEW" if decision == "approve" else "HOLD", "written": name, "record": record, "issues": baseline["issues"]}


def editorial_plan(dossier):
    """Prompting questions only; never a prohibited human-only submission draft."""
    doc = dossier.get("document", {})
    evidence = dossier.get("evidence", [])
    facts = [x.get("claim", "") for x in evidence if isinstance(x, dict) and x.get("kind") == "firsthand"]
    return {"intent": doc.get("mission", "unspecified"), "arena": doc.get("arena"),
            "author_owned_facts": facts,
            "questions": [
                "Which actual incident supports the central claim? Where/when did it happen?",
                "What expectation failed, and what did the author change in response?",
                "Which surprising or unpopular conclusion would the author defend?",
                "What alternative explanation might a serious critic raise?",
                "Which planned or hypothetical details might readers mistake for completed work?",
                "What numbers or quotes can be checked against original sources?",
                "What would change the author's mind?",
            ],
            "instruction": "Answer independently from authentic memories and documents. Do not treat this research plan as a human-only pitch."}


def _quantile(vals, fraction):
    vals = sorted(vals)
    if not vals:
        return None
    pos = (len(vals) - 1) * fraction
    lo, hi = math.floor(pos), math.ceil(pos)
    return vals[lo] * (hi - pos) + vals[hi] * (pos - lo) if hi != lo else vals[lo]


def evaluate_benchmark(data, minimum_pairs=60):
    """Locked before evaluation: pair exact same case and reviewer; no detector scoring."""
    rows = data.get("ratings") if isinstance(data, dict) else None
    if not isinstance(rows, list) or len(rows) > MAX_LIST * 4:
        return {"status": "HOLD", "reason": "Ratings must be a list of at most %d" % (MAX_LIST * 4)}
    cells, errs = {}, []
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            errs.append("row %d not an object" % i)
            continue
        key = (row.get("case_id"), row.get("reviewer_id"), row.get("arm"))
        if (not all(isinstance(v, str) and v for v in key) or key[2] not in ("v8", "v9") or (all(isinstance(v, str) for v in key) and key in cells)):
            errs.append("row %d has invalid or duplicate identity" % i)
            continue
        scores = row.get("scores")
        if not isinstance(scores, dict) or any(not isinstance(scores.get(m), int) or isinstance(scores.get(m), bool) or not 1 <= scores[m] <= 5 for m in METRICS):
            errs.append("row %d has invalid scores" % i)
            continue
        violations = row.get("critical_violations", None)
        if not isinstance(violations, int) or isinstance(violations, bool) or violations < 0:
            errs.append("row %d has invalid violation count" % i)
            continue
        cells[key] = row
    pairs = []
    for (case, reviewer, arm), row in cells.items():
        if arm == "v8" and (case, reviewer, "v9") in cells:
            pairs.append((row, cells[(case, reviewer, "v9")]))
    case_count = len({a["case_id"] for a, b in pairs})
    violation_count = sum(row["critical_violations"] for row in cells.values())
    report = {"paired_ratings": len(pairs), "distinct_cases": case_count,
              "critical_violations": violation_count, "errors": errs,
              "deltas": {m: {"median_v9_minus_v8": round(statistics.median([b["scores"][m] - a["scores"][m] for a, b in pairs]), 3),
                              "lower_quartile": _quantile([b["scores"][m] - a["scores"][m] for a, b in pairs], 0.25),
                              "upper_quartile": _quantile([b["scores"][m] - a["scores"][m] for a, b in pairs], 0.75)} for m in METRICS} if pairs else {},
              "limitations": ["No detector-based optimization.", "Blind randomization and reviewer independence cannot be established from ratings alone.", "This is a pilot summary, not release permission."]}
    report["status"] = "HOLD" if errs or violation_count or case_count < minimum_pairs else "REVIEW"
    if case_count < minimum_pairs:
        report["reason"] = "Not enough distinct matched cases; need %d" % minimum_pairs
    return report


def _load_json(path, base):
    raw = bounded_read(base, path, limit=MAX_MANIFEST_BYTES)
    return json.loads(raw.decode("utf-8", errors="strict"))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Writing Intelligence v9 experimental offline quality + provenance tools")
    commands = parser.add_subparsers(dest="command", required=True)
    compare = commands.add_parser("voice-compare", help="Where a text sits against your own baseline")
    compare.add_argument("--root", required=True, help="Your private folder holding your samples and voice.json")
    compare.add_argument("--input", required=True, help="voice.json, relative to --root")
    compare.add_argument("--text", required=True, help="the text to compare, a path anywhere")
    for command in ("preflight", "plan", "diagnose", "voice", "benchmark"):
        entry = commands.add_parser(command)
        entry.add_argument("--root", required=True, help="Directory holding the input dossier, source and document files")
        entry.add_argument("--input", required=True, help="Relative JSON or UTF-8 document file name")
    review = commands.add_parser("voice-review", help="Record your own decision about your own voice baseline")
    review.add_argument("--root", required=True, help="Your private folder holding your samples and voice.json")
    review.add_argument("--input", required=True, help="voice.json, relative to --root")
    review.add_argument("--decision", required=True, choices=VOICE_DECISIONS)
    review.add_argument("--note", default="", help="Which measurements describe you, and which do not")
    args = parser.parse_args(argv)
    try:
        if args.command == "voice-compare":
            data = _load_json(args.input, args.root)
            target = Path(args.text)
            if target.is_symlink() or not target.is_file() or target.stat().st_size > MAX_FILE_BYTES:
                raise ValueError("TEXT_NOT_A_BOUNDED_FILE")
            result = voice_compare(data.get("samples", []) if isinstance(data, dict) else None, args.root,
                                   target.read_text(encoding="utf-8"))
        elif args.command == "voice-review":
            import datetime
            data = _load_json(args.input, args.root)
            when = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
            result = voice_review(data.get("samples", []) if isinstance(data, dict) else None,
                                  args.root, args.decision, when, args.note)
        elif args.command == "diagnose":
            result = editorial_diagnostics(read_text(args.root, args.input))
        else:
            data = _load_json(args.input, args.root)
            if args.command == "preflight":
                result = preflight(data, args.root)
            elif args.command == "plan":
                result = editorial_plan(data) if isinstance(data, dict) else {"status": "HOLD", "error": "Invalid dossier"}
            elif args.command == "voice":
                result = voice_baseline(data.get("samples", []), args.root) if isinstance(data, dict) else {"status": "HOLD"}
            else:
                result = evaluate_benchmark(data)
    except (OSError, UnicodeError, ValueError, TypeError, RuntimeError, json.JSONDecodeError) as exc:
        result = {"status": "HOLD", "error": type(exc).__name__ + ": " + str(exc)}
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 3 if result.get("status") == "HOLD" else 0


if __name__ == "__main__":
    sys.exit(main())
