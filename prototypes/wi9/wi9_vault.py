#!/usr/bin/env python3
"""WI9-02 firsthand-material vault: each writer's own notes, kept on their own machine.

Project owner: Antonio T. Smith Jr. / Density6 LLC

A vault is a private folder that holds the material a writer's first-person
claims rest on: notes, transcripts, dated drafts, sketches, interviews they
conducted, research they gathered. Nothing ships with v9 and nothing here
uploads, commits or sends anything. The folder is created 0700, refused inside
any git working tree, and every change is appended to a hash-chained event
log that records digests, never text.

Each item carries a label saying what kind of knowledge it is. Only
`observed`, `said_by_author`, `measured` and `sourced` can support a claim
that something happened. `planned`, `hypothetical` and `inferred` cannot:
a roadmap is not a completed build, and a model-written anecdote is not a
memory.

  init      create a vault for one project
  add       copy a file in, with its label and consent
  redact    remove a span; the earlier bytes are deleted, only digests remain
  withdraw  withdraw consent; the bytes are deleted, the item stops supporting anything
  list      labels, digests and states, never text
  check     every autobiographical claim needs an attributable source, or it HOLDs

Exit 0 on REVIEW (check) or a completed action, 3 on HOLD. REVIEW is not
permission to publish, and an anchored note proves the note says it, not that
it is true.
"""
import argparse
import datetime as _dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wi9_fs import (StoreRefusal, append_line, canonical, open_private_root, open_subdir, read_file,
                    remove_file, replace_file, require_posix, write_new)

SCHEMA = "wi9.vault/1"
CLAIMS_SCHEMA = "wi9.vault-claims/1"
REPORT_SCHEMA = "wi9.vault-check/1"
LABELS = ("observed", "said_by_author", "measured", "sourced", "inferred", "hypothetical", "planned")
SUPPORTS_EXPERIENCE = {"observed", "said_by_author", "measured", "sourced"}
KINDS = ("note", "transcript", "draft", "sketch", "interview", "research", "photo_metadata", "model", "other")
ORIGINS = ("author", "external", "ai_generated")
MAX_ITEM_BYTES = 5_000_000
MAX_MANIFEST_BYTES = 2_000_000
MAX_ITEMS = 5_000
MAX_CLAIMS = 5_000
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
FIRST_PERSON = re.compile(r"\bI\b|\bI'(?:m|ve|d|ll)\b|\b(?:me|my|mine|myself|we|we've|we're|our|ours|us)\b",
                          re.IGNORECASE)
DATE_RE = re.compile(r"^\d{4}(?:-\d{2}(?:-\d{2})?)?$")
LIMITATIONS = [
    "Labels, consent and origin are the writer's own declaration about their own material.",
    "An exact excerpt proves the note contains those words, not that the event happened.",
    "Nothing in a vault is uploaded, committed or sent by v9.",
]


def _now():
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()


def _sha(data):
    return hashlib.sha256(data).hexdigest()


def _date_prefix(value):
    """The comparable prefix of an ISO date or datetime, or None."""
    if not isinstance(value, str):
        return None
    head = value[:10] if len(value) >= 10 else value
    return head if DATE_RE.match(head) else None


class Vault:
    def __init__(self, root, create=False):
        self.root = root
        self.fd = open_private_root(root, create=create)
        self.objects = open_subdir(self.fd, "objects", create=create)

    def close(self):
        os.close(self.objects)
        os.close(self.fd)

    def manifest(self):
        try:
            data = json.loads(read_file(self.fd, "vault.json", MAX_MANIFEST_BYTES).decode("utf-8"))
        except FileNotFoundError:
            raise StoreRefusal("VAULT_UNINITIALISED", "run `vault init` first")
        if not isinstance(data, dict) or data.get("schema") != SCHEMA or not isinstance(data.get("items"), dict):
            raise StoreRefusal("VAULT_MANIFEST_INVALID", "vault.json is not a %s manifest" % SCHEMA)
        return data

    def save(self, manifest):
        replace_file(self.fd, "vault.json", json.dumps(manifest, indent=2, sort_keys=True).encode("utf-8"))

    def events(self):
        try:
            raw = read_file(self.fd, "events.jsonl", MAX_MANIFEST_BYTES * 5).decode("utf-8")
        except FileNotFoundError:
            return []
        return [json.loads(line) for line in raw.splitlines() if line.strip()]

    def log(self, action, item_id, digest_value):
        prior = self.events()
        entry = {"seq": len(prior) + 1, "at": _now(), "action": action, "item": item_id,
                 "sha256": digest_value, "prev": prior[-1]["hash"] if prior else None}
        entry["hash"] = _sha(canonical(entry))
        append_line(self.fd, "events.jsonl", json.dumps(entry, sort_keys=True))

    def verify_log(self):
        prev = None
        for entry in self.events():
            body = {k: v for k, v in entry.items() if k != "hash"}
            if entry.get("prev") != prev or _sha(canonical(body)) != entry.get("hash"):
                return False
            prev = entry["hash"]
        return True

    def object_bytes(self, digest_value):
        return read_file(self.objects, digest_value, MAX_ITEM_BYTES)

    def store_object(self, data):
        digest_value = _sha(data)
        try:
            write_new(self.objects, digest_value, data)
        except FileExistsError:
            pass
        return digest_value


def _refuse(code, message):
    raise StoreRefusal(code, message)


def cmd_init(args):
    vault = Vault(args.root, create=True)
    try:
        try:
            vault.manifest()
            _refuse("VAULT_EXISTS", "a vault already exists here")
        except StoreRefusal as exc:
            if exc.code != "VAULT_UNINITIALISED":
                raise
        if not ID_RE.match(args.project or ""):
            _refuse("PROJECT_INVALID", "a project id of letters, digits, . _ - is required")
        vault.save({"schema": SCHEMA, "project": args.project, "created_at": _now(), "items": {}})
        vault.log("init", None, None)
    finally:
        vault.close()
    return {"status": "DONE", "action": "init", "project": args.project}


def cmd_add(args):
    if not args.consent:
        _refuse("CONSENT_REQUIRED", "pass --consent to confirm you choose to keep this material in your vault")
    if not ID_RE.match(args.id or ""):
        _refuse("ITEM_ID_INVALID", "an item id of letters, digits, . _ - is required")
    if args.label not in LABELS:
        _refuse("LABEL_INVALID", "label must be one of %s" % ", ".join(LABELS))
    source = Path(args.file)
    if source.is_symlink() or not source.is_file():
        _refuse("SOURCE_NOT_FILE", "the file to add must be a regular file, not a link")
    if source.stat().st_size > MAX_ITEM_BYTES:
        _refuse("FILE_TOO_LARGE", "items are limited to %d bytes" % MAX_ITEM_BYTES)
    data = source.read_bytes()
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        _refuse("FILE_NOT_UTF8", "vault items are UTF-8 text")
    recorded = _now()
    if args.valid_at is not None:
        if _date_prefix(args.valid_at) is None:
            _refuse("DATE_INVALID", "--valid-at is an ISO date (YYYY, YYYY-MM or YYYY-MM-DD)")
        if _date_prefix(args.valid_at) > recorded[:10]:
            _refuse("DATE_IMPLAUSIBLE", "material cannot describe a day after it was recorded")
    vault = Vault(args.root)
    try:
        manifest = vault.manifest()
        if args.id in manifest["items"]:
            _refuse("ITEM_EXISTS", "item %s already exists; add a new id rather than replacing it" % args.id)
        if len(manifest["items"]) >= MAX_ITEMS:
            _refuse("VAULT_FULL", "a vault holds at most %d items" % MAX_ITEMS)
        digest_value = vault.store_object(data)
        manifest["items"][args.id] = {
            "id": args.id, "sha256": digest_value, "label": args.label, "kind": args.kind,
            "origin": args.origin, "verbatim": bool(args.verbatim), "recorded_at": recorded,
            "valid_at": args.valid_at, "state": "active", "redactions": [],
            "consent": {"granted": True, "granted_at": recorded, "scope": "local_only", "withdrawn_at": None},
        }
        vault.save(manifest)
        vault.log("add", args.id, digest_value)
    finally:
        vault.close()
    return {"status": "DONE", "action": "add", "item": args.id, "sha256": digest_value, "label": args.label}


def cmd_redact(args):
    vault = Vault(args.root)
    try:
        manifest = vault.manifest()
        item = manifest["items"].get(args.id)
        if item is None or item["state"] != "active":
            _refuse("ITEM_UNKNOWN", "no active item %s" % args.id)
        text = vault.object_bytes(item["sha256"]).decode("utf-8")
        if not (0 <= args.start < args.end <= len(text)):
            _refuse("SPAN_INVALID", "the span must lie inside the item (0..%d)" % len(text))
        if not args.reason or len(args.reason.strip()) < 4:
            _refuse("REASON_REQUIRED", "say why the span is redacted")
        redacted = (text[:args.start] + "[redacted]" + text[args.end:]).encode("utf-8")
        prior = item["sha256"]
        item["sha256"] = vault.store_object(redacted)
        item["redactions"].append({"at": _now(), "prior_sha256": prior, "start": args.start,
                                   "end": args.end, "reason": args.reason.strip()[:500]})
        vault.save(manifest)
        if not any(other["sha256"] == prior for other in manifest["items"].values()):
            remove_file(vault.objects, prior)
        vault.log("redact", args.id, item["sha256"])
    finally:
        vault.close()
    return {"status": "DONE", "action": "redact", "item": args.id, "sha256": item["sha256"],
            "removed_prior_bytes": True}


def cmd_withdraw(args):
    vault = Vault(args.root)
    try:
        manifest = vault.manifest()
        item = manifest["items"].get(args.id)
        if item is None or item["state"] != "active":
            _refuse("ITEM_UNKNOWN", "no active item %s" % args.id)
        item["state"] = "withdrawn"
        item["consent"]["withdrawn_at"] = _now()
        vault.save(manifest)
        if not any(o["sha256"] == item["sha256"] and o["state"] == "active" for o in manifest["items"].values()):
            remove_file(vault.objects, item["sha256"])
        vault.log("withdraw", args.id, item["sha256"])
    finally:
        vault.close()
    return {"status": "DONE", "action": "withdraw", "item": args.id, "bytes_deleted": True}


def cmd_list(args):
    vault = Vault(args.root)
    try:
        manifest = vault.manifest()
        items = [{k: v for k, v in item.items() if k != "redactions"} for item in manifest["items"].values()]
        log_ok = vault.verify_log()
    finally:
        vault.close()
    return {"status": "DONE" if log_ok else "HOLD", "action": "list", "project": manifest["project"],
            "items": sorted(items, key=lambda x: x["id"]), "event_log_intact": log_ok,
            "issues": [] if log_ok else [{"code": "VAULT_LOG_BROKEN", "detail": "events.jsonl does not chain"}]}


def _is_autobiographical(claim):
    declared = claim.get("autobiographical")
    if isinstance(declared, bool):
        return declared, "declared"
    return bool(FIRST_PERSON.search(claim.get("text", ""))), "detected"


def check_claims(vault, claims_doc):
    """The WI9-02 exit check over one claims file."""
    issues = []

    def flag(code, claim_id, detail):
        issues.append({"code": code, "claim": claim_id, "detail": detail})

    manifest = vault.manifest()
    if not isinstance(claims_doc, dict) or claims_doc.get("schema") != CLAIMS_SCHEMA:
        return {"schema": REPORT_SCHEMA, "status": "HOLD", "release_authorized": False,
                "issues": [{"code": "CLAIMS_INVALID", "claim": None, "detail": "expected %s" % CLAIMS_SCHEMA}]}
    if claims_doc.get("project") != manifest["project"]:
        flag("VAULT_PROJECT_MISMATCH", None,
             "these claims name project %r; this vault holds project %r. Material does not cross projects."
             % (claims_doc.get("project"), manifest["project"]))
    claims = claims_doc.get("claims")
    if not isinstance(claims, list) or len(claims) > MAX_CLAIMS:
        flag("CLAIMS_INVALID", None, "claims must be a list of at most %d" % MAX_CLAIMS)
        claims = []
    if not vault.verify_log():
        flag("VAULT_LOG_BROKEN", None, "events.jsonl does not chain; the vault history was edited")
    texts = {}
    seen_ids = set()
    results = []
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict) or not isinstance(claim.get("text"), str):
            flag("CLAIM_INVALID", index, "a claim needs a text")
            continue
        cid = claim.get("id") if isinstance(claim.get("id"), str) else str(index)
        if cid in seen_ids:
            flag("CLAIM_DUPLICATE_ID", cid, "claim ids must be unique")
        seen_ids.add(cid)
        auto, how = _is_autobiographical(claim)
        evidence = claim.get("evidence") or []
        if not isinstance(evidence, list):
            flag("EVIDENCE_INVALID", cid, "evidence must be a list")
            evidence = []
        start_count = len(issues)
        dated = set()
        for ev in evidence:
            if not isinstance(ev, dict):
                flag("EVIDENCE_INVALID", cid, "each evidence entry is an object")
                continue
            item = manifest["items"].get(ev.get("item"))
            if item is None:
                flag("EVIDENCE_ITEM_UNKNOWN", cid, "no vault item %r" % ev.get("item"))
                continue
            if item["state"] != "active" or item["consent"].get("withdrawn_at"):
                flag("EVIDENCE_WITHDRAWN", cid, "item %s was withdrawn; it supports nothing" % item["id"])
                continue
            if item["consent"].get("granted") is not True or item["consent"].get("scope") != "local_only":
                flag("EVIDENCE_CONSENT_INVALID", cid, "item %s has no valid consent record" % item["id"])
                continue
            if item["sha256"] not in texts:
                try:
                    raw = vault.object_bytes(item["sha256"])
                except (FileNotFoundError, StoreRefusal):
                    flag("EVIDENCE_MISSING_BYTES", cid, "item %s has no stored bytes" % item["id"])
                    continue
                if _sha(raw) != item["sha256"]:
                    flag("EVIDENCE_STALE", cid, "item %s bytes no longer match their digest" % item["id"])
                    continue
                texts[item["sha256"]] = raw.decode("utf-8")
            body = texts[item["sha256"]]
            excerpt = ev.get("excerpt")
            if not isinstance(excerpt, str) or not excerpt.strip():
                flag("ANCHOR_MISSING", cid, "evidence from %s needs an exact excerpt" % item["id"])
                continue
            start = ev.get("start")
            if isinstance(start, int) and not isinstance(start, bool):
                if body[start:start + len(excerpt)] != excerpt:
                    flag("ANCHOR_NOT_FOUND", cid, "the excerpt is not at offset %d of %s" % (start, item["id"]))
                    continue
            else:
                first = body.find(excerpt)
                if first < 0:
                    flag("ANCHOR_NOT_FOUND", cid, "the excerpt does not occur in %s" % item["id"])
                    continue
                if body.find(excerpt, first + 1) >= 0:
                    flag("ANCHOR_AMBIGUOUS", cid, "the excerpt occurs twice in %s; give a start offset" % item["id"])
                    continue
            if item["valid_at"] and _date_prefix(item["valid_at"]) and \
                    _date_prefix(item["valid_at"]) > _date_prefix(item["recorded_at"]):
                flag("EVIDENCE_DATE_IMPLAUSIBLE", cid, "item %s claims to describe a day after it was recorded"
                     % item["id"])
            if auto:
                if item["origin"] == "ai_generated":
                    flag("EVIDENCE_MODEL_GENERATED", cid, "item %s was written by a model; it is not a memory"
                         % item["id"])
                elif item["label"] == "planned":
                    flag("PLANNED_AS_DONE", cid, "item %s records a plan; it cannot show the thing was done"
                         % item["id"])
                elif item["label"] == "hypothetical":
                    flag("HYPOTHETICAL_AS_EXPERIENCE", cid, "item %s is labelled hypothetical" % item["id"])
                elif item["label"] == "inferred":
                    flag("INFERENCE_AS_EXPERIENCE", cid, "item %s is an inference, not an account" % item["id"])
            if claim.get("quote") is True and not item.get("verbatim"):
                flag("QUOTE_NOT_VERBATIM", cid, "item %s is not marked verbatim; an edited transcript cannot "
                     "back a direct quotation" % item["id"])
            if item["valid_at"]:
                dated.add(_date_prefix(item["valid_at"]))
            claim_date = _date_prefix(claim.get("date"))
            if claim_date and item["valid_at"] and not (
                    claim_date.startswith(_date_prefix(item["valid_at"])) or
                    _date_prefix(item["valid_at"]).startswith(claim_date)):
                flag("DATE_CONFLICT", cid, "the claim says %s; item %s is dated %s"
                     % (claim_date, item["id"], item["valid_at"]))
        dated.discard(None)
        if any(not (a.startswith(b) or b.startswith(a)) for a in dated for b in dated):
            flag("CONFLICTING_ACCOUNTS", cid, "the evidence gives different dates: %s; the conflict stays "
                 "unresolved until you choose" % ", ".join(sorted(dated)))
        if issues[start_count:]:
            state = "held"
        elif evidence:
            state = "anchored"
        elif auto:
            flag("CLAIM_NEEDS_SOURCE", cid, "a first-person claim needs material from your vault")
            state = "needs_source"
        else:
            state = "not_autobiographical"
        results.append({"claim": cid, "autobiographical": auto, "autobiographical_basis": how, "state": state})
    hold = bool(issues)
    return {"schema": REPORT_SCHEMA, "status": "HOLD" if hold else "REVIEW", "release_authorized": False,
            "project": manifest["project"], "claims": results, "issues": issues,
            "needs_source": [r["claim"] for r in results if r["state"] == "needs_source"],
            "limitations": LIMITATIONS}


def cmd_check(args):
    path = Path(args.claims)
    if path.is_symlink() or not path.is_file():
        _refuse("CLAIMS_NOT_FILE", "the claims file must be a regular file")
    if path.stat().st_size > MAX_MANIFEST_BYTES:
        _refuse("FILE_TOO_LARGE", "the claims file exceeds %d bytes" % MAX_MANIFEST_BYTES)
    claims_doc = json.loads(path.read_text(encoding="utf-8"))
    vault = Vault(args.root)
    try:
        return check_claims(vault, claims_doc)
    finally:
        vault.close()


COMMANDS = {"init": cmd_init, "add": cmd_add, "redact": cmd_redact, "withdraw": cmd_withdraw,
            "list": cmd_list, "check": cmd_check}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init", help="create a private vault for one project")
    init.add_argument("--project", required=True)
    add = sub.add_parser("add", help="copy a file into the vault")
    add.add_argument("--file", required=True)
    add.add_argument("--id", required=True)
    add.add_argument("--label", required=True, choices=LABELS)
    add.add_argument("--kind", default="note", choices=KINDS)
    add.add_argument("--origin", default="author", choices=ORIGINS)
    add.add_argument("--valid-at", dest="valid_at", help="the date the material describes (ISO)")
    add.add_argument("--verbatim", action="store_true", help="the text is an unedited record, fit for quotation")
    add.add_argument("--consent", action="store_true", help="you choose to keep this material in your vault")
    redact = sub.add_parser("redact", help="remove a span from an item")
    redact.add_argument("--id", required=True)
    redact.add_argument("--start", type=int, required=True)
    redact.add_argument("--end", type=int, required=True)
    redact.add_argument("--reason", required=True)
    withdraw = sub.add_parser("withdraw", help="withdraw consent and delete an item's bytes")
    withdraw.add_argument("--id", required=True)
    sub.add_parser("list", help="labels, digests and states; never text")
    check = sub.add_parser("check", help="check first-person claims against the vault")
    check.add_argument("--claims", required=True)
    for cmd in sub.choices.values():
        cmd.add_argument("--root", required=True, help="your private vault folder, outside any repository")
    args = parser.parse_args(argv)
    try:
        require_posix()
        result = COMMANDS[args.command](args)
    except StoreRefusal as exc:
        result = {"status": "HOLD", "issues": [{"code": exc.code, "detail": str(exc)}], "release_authorized": False}
    except (OSError, ValueError, UnicodeError, TypeError, RecursionError) as exc:
        result = {"status": "HOLD", "issues": [{"code": "VAULT_ERROR", "detail": "%s: %s" % (type(exc).__name__, exc)}],
                  "release_authorized": False}
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 3 if result.get("status") == "HOLD" else 0


if __name__ == "__main__":
    raise SystemExit(main())
