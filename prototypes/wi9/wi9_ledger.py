#!/usr/bin/env python3
"""v9 review ledger: every reviewer decision bound to that person's v6 grant.

Project owner: Antonio T. Smith Jr. / Density6 LLC

A decision used to carry a typed reviewer name, which anyone could type. Here
a decision is recorded only after the operator's v6 grant store (the same one
`wi authorship release` reads) shows that the person holds the capability for
that kind of decision, as a human, in scope. The entry carries the grant id.

The ledger is append-only and hash-chained. A decision is never edited: a
later entry may supersede an earlier one for the same document and item, and
the earlier one stays on record. `verify` re-checks every grant at the time of
the decision and now, so a revoked or expired grant stops an entry counting
without deleting it.

The ledger lives in the reviewer's own private folder (0700, outside any git
working tree) and the grant store must sit outside that folder: whoever
controls the ledger folder could otherwise plant a store granting themselves.

  record   append one decision (refused unless the grant covers it)
  verify   chain, grants then and now, and the effective decision per item
  export   the effective phrase decisions as a wi9.editorial.review/1 file
"""
import argparse
import datetime as _dt
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wi9_fs import StoreRefusal, append_line, canonical, open_private_root, read_file

SCHEMA = "wi9.review-ledger/1"
KINDS = {
    # decision kind -> (allowed decisions, default capability)
    "phrase": ({"retain_as_written", "revise_for_clarity", "needs_source", "not_applicable"},
               "claim.accept.wording_only"),
    "meaning": ({"accept", "reject"}, "claim.accept"),
}
MAX_LEDGER_BYTES = 20_000_000
SCOPE_KINDS = {"workspace", "work", "node_family", "node", "branch", "jurisdiction", "release_target"}


def _now():
    # Same form as the v6 store's own timestamps, which the grant check compares as strings.
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


def _authorship():
    """The v6 store reader in scripts/wi-authorship.py: one implementation, read-only."""
    path = Path(__file__).resolve().parents[2] / "scripts" / "wi-authorship.py"
    if not path.is_file():
        raise StoreRefusal("AUTHORITY_TOOLS_MISSING", "scripts/wi-authorship.py is not beside this kernel")
    spec = importlib.util.spec_from_file_location("wi_authorship_v9", str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_grant(store, ledger_root, actor, capability, scope, times):
    """Return the grant covering `capability` in `scope` at every time in `times`."""
    wa = _authorship()
    try:
        conn = wa._open_store_readonly(store, ledger_root)
        try:
            granted = None
            for when in times:
                granted = wa._store_authorize(conn, actor, capability, scope, when)
        finally:
            conn.close()
    except wa.Refusal as exc:
        raise StoreRefusal(exc.code, str(exc))
    if granted.get("subject_kind") != "human":
        raise StoreRefusal("AUTHORITY_NOT_HUMAN", "%s is a %s; a review decision is a person's"
                           % (actor, granted.get("subject_kind")))
    return {"grant_id": granted.get("grant_id"), "capability": capability, "scope": scope,
            "subject_kind": granted.get("subject_kind"), "issuer": granted.get("issuer")}


def _sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def read_entries(fd):
    try:
        raw = read_file(fd, "ledger.jsonl", MAX_LEDGER_BYTES).decode("utf-8")
    except FileNotFoundError:
        return []
    return [json.loads(line) for line in raw.splitlines() if line.strip()]


def chain_intact(entries):
    prev = None
    for entry in entries:
        body = {k: v for k, v in entry.items() if k != "hash"}
        if entry.get("prev") != prev or _sha(body) != entry.get("hash"):
            return False
        prev = entry["hash"]
    return True


def record(ledger, store, actor, kind, target_sha256, item, decision, rationale,
           scope_kind="workspace", scope_value=None, capability=None, supersedes=None, now=None):
    if kind not in KINDS:
        raise StoreRefusal("LEDGER_KIND_INVALID", "kind must be one of %s" % ", ".join(sorted(KINDS)))
    allowed, default_cap = KINDS[kind]
    if decision not in allowed:
        raise StoreRefusal("LEDGER_DECISION_INVALID", "%s decisions are %s" % (kind, ", ".join(sorted(allowed))))
    if not isinstance(target_sha256, str) or len(target_sha256) != 64 or \
            any(c not in "0123456789abcdef" for c in target_sha256):
        raise StoreRefusal("LEDGER_TARGET_INVALID", "the target is a document's sha256")
    if not isinstance(item, str) or not item.strip():
        raise StoreRefusal("LEDGER_ITEM_INVALID", "name the item decided")
    if not isinstance(rationale, str) or len(rationale.strip()) < 12:
        raise StoreRefusal("RATIONALE_MISSING", "say why, in at least a short sentence")
    if scope_kind not in SCOPE_KINDS:
        raise StoreRefusal("LEDGER_SCOPE_INVALID", "scope kind must be a v6 scope kind")
    scope = {"kind": scope_kind}
    if scope_value:
        scope["value"] = scope_value
    capability = capability or default_cap
    if kind == "phrase" and capability != default_cap:
        raise StoreRefusal("LEDGER_CAPABILITY_INVALID", "phrase decisions need %s" % default_cap)
    when = now or _now()
    fd = open_private_root(ledger, create=True)
    try:
        grant = check_grant(store, ledger, actor, capability, scope, [when])
        entries = read_entries(fd)
        if not chain_intact(entries):
            raise StoreRefusal("LEDGER_CHAIN_BROKEN", "ledger.jsonl was edited; nothing more may be appended")
        live = [e for e in entries if e["target_sha256"] == target_sha256 and e["kind"] == kind
                and e["item"] == item]
        superseded = {e.get("supersedes") for e in entries if e.get("supersedes")}
        current = [e for e in live if e["hash"] not in superseded]
        if supersedes:
            if supersedes not in {e["hash"] for e in live}:
                raise StoreRefusal("LEDGER_SUPERSEDES_UNKNOWN", "supersedes must name an entry for this item")
            if supersedes in superseded:
                raise StoreRefusal("LEDGER_ALREADY_SUPERSEDED", "that entry was already superseded")
        elif current:
            raise StoreRefusal("LEDGER_DECISION_EXISTS",
                               "this item already has a decision; pass --supersedes %s to replace it"
                               % current[-1]["hash"])
        entry = {"schema": SCHEMA, "seq": len(entries) + 1, "prev": entries[-1]["hash"] if entries else None,
                 "kind": kind, "target_sha256": target_sha256, "item": item, "decision": decision,
                 "rationale": rationale.strip()[:2000], "actor": actor, "decided_at": when,
                 "grant": grant, "supersedes": supersedes}
        entry["hash"] = _sha(entry)
        append_line(fd, "ledger.jsonl", json.dumps(entry, sort_keys=True, ensure_ascii=False))
    finally:
        os.close(fd)
    return entry


def verify(ledger, store, target_sha256=None, kind=None, now=None):
    """Chain and grants. Returns the effective (latest, unsuperseded, still granted) entry per item."""
    fd = open_private_root(ledger)
    try:
        entries = read_entries(fd)
    finally:
        os.close(fd)
    issues = []
    if not chain_intact(entries):
        return {"status": "HOLD", "issues": [{"code": "LEDGER_CHAIN_BROKEN", "detail": "ledger.jsonl was edited"}],
                "effective": {}, "entries": len(entries)}
    superseded = {e.get("supersedes") for e in entries if e.get("supersedes")}
    effective = {}
    when_now = now or _now()
    for entry in entries:
        if target_sha256 and entry["target_sha256"] != target_sha256:
            continue
        if kind and entry["kind"] != kind:
            continue
        if entry["hash"] in superseded:
            continue
        try:
            check_grant(store, ledger, entry["actor"], entry["grant"]["capability"], entry["grant"]["scope"],
                        [entry["decided_at"], when_now])
        except StoreRefusal as exc:
            issues.append({"code": "LEDGER_GRANT_" + exc.code, "item": entry["item"], "entry": entry["hash"],
                           "detail": str(exc)})
            continue
        effective[(entry["kind"], entry["target_sha256"], entry["item"])] = entry
    return {"status": "HOLD" if issues else "REVIEW", "issues": issues, "entries": len(entries),
            "effective": effective, "release_authorized": False}


def phrase_item(rule_id, start, end):
    return "%s@%d:%d" % (rule_id, start, end)


def export_phrase_review(ledger, store, text_sha256, rules_sha256, report):
    """Build a wi9.editorial.review/1 file from the effective grant-bound phrase decisions."""
    result = verify(ledger, store, target_sha256=text_sha256, kind="phrase")
    decisions = []
    for finding in report.get("findings", []):
        entry = result["effective"].get(("phrase", text_sha256, phrase_item(finding["id"], finding["start"],
                                                                             finding["end"])))
        if entry is None:
            continue
        decisions.append({"rule_id": finding["id"], "start": finding["start"], "end": finding["end"],
                          "excerpt": finding["excerpt"], "status": entry["decision"],
                          "rationale": entry["rationale"], "reviewer": entry["actor"],
                          "reviewed_at": entry["decided_at"], "ledger_entry": entry["hash"],
                          "grant_id": entry["grant"]["grant_id"]})
    return {"schema": "wi9.editorial.review/1", "document_sha256": text_sha256, "rules_sha256": rules_sha256,
            "decisions": decisions}, {e["hash"] for e in result["effective"].values()}, result["issues"]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    rec = sub.add_parser("record", help="append one grant-bound decision")
    rec.add_argument("--actor", required=True, help="the v6 subject making the decision")
    rec.add_argument("--kind", required=True, choices=sorted(KINDS))
    rec.add_argument("--target", required=True, help="sha256 of the document decided on")
    rec.add_argument("--item", required=True, help="the finding or delta id")
    rec.add_argument("--decision", required=True)
    rec.add_argument("--rationale", required=True)
    rec.add_argument("--capability")
    rec.add_argument("--scope", default="workspace", choices=sorted(SCOPE_KINDS))
    rec.add_argument("--scope-value", dest="scope_value")
    rec.add_argument("--supersedes")
    ver = sub.add_parser("verify", help="check the chain and every grant, then and now")
    ver.add_argument("--target")
    ver.add_argument("--kind", choices=sorted(KINDS))
    for cmd in (rec, ver):
        cmd.add_argument("--ledger", required=True, help="your private ledger folder, outside any repository")
        cmd.add_argument("--authority-store", dest="store", required=True,
                         help="the v6 workspace holding grants; must be outside the ledger folder")
    args = parser.parse_args(argv)
    try:
        if args.command == "record":
            entry = record(args.ledger, args.store, args.actor, args.kind, args.target, args.item, args.decision,
                           args.rationale, args.scope, args.scope_value, args.capability, args.supersedes)
            result = {"status": "RECORDED", "entry": entry, "release_authorized": False}
        else:
            result = verify(args.ledger, args.store, args.target, args.kind)
            result["effective"] = sorted(({"kind": k[0], "target": k[1], "item": k[2], "decision": e["decision"],
                                           "actor": e["actor"], "entry": e["hash"]}
                                          for k, e in result["effective"].items()), key=lambda x: x["entry"])
    except StoreRefusal as exc:
        result = {"status": "HOLD", "issues": [{"code": exc.code, "detail": str(exc)}], "release_authorized": False}
    except (OSError, ValueError, KeyError, TypeError) as exc:
        result = {"status": "HOLD", "issues": [{"code": "LEDGER_ERROR", "detail": "%s: %s" % (type(exc).__name__, exc)}],
                  "release_authorized": False}
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))
    return 3 if result["status"] == "HOLD" else 0


if __name__ == "__main__":
    raise SystemExit(main())
