#!/usr/bin/env python3
"""
check-manifest.py — validate every plans/*.manifest.yaml.

A roadmap written only in prose can hide three things: a dependency cycle, a
wave with no exit condition, and a claim that something shipped when nothing
answers to the name. This script makes all three impossible to merge.

The last check is the one that matters. A wave marked `shipped` must name the
commands that prove it, and every named command must appear in the CLI's own
`--help`. That is Law C compiled: the manifest cannot say a thing runs unless
the thing runs.

Stdlib only, Python 3.8+. Exits 1 on any violation.

A manifest that declares `receipts_required: true` (the v7 program does) adds
one more rule. A wave may be marked `shipped` only if it names a `receipt:`
file, that receipt reads PASS for the same wave, carries the measured command,
its result, at least one negative control and an independent readback, and
every wave it depends on is itself shipped. A status written by hand with no
receipt behind it is the fabricated progress the program exists to refuse.

Usage: python3 scripts/check-manifest.py [manifest ...]
"""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / "plans" / "v6.manifest.yaml"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
RECEIPT_FIELDS = ("checkpoint", "status", "baseline_sha", "commands",
                  "observed_result", "negative_controls", "independent_readback")
CLI = REPO / "scripts" / "wi.py"

STATUSES = ("shipped", "in_progress", "planned")


def load_manifest(path):
    """Parse the small YAML subset this manifest uses.

    A dependency-free repository cannot import PyYAML, and the shape here is
    fixed: a top-level map, one list of maps under `waves`, and inside each
    wave scalars, flow sequences and one nested map. Anything this parser does
    not understand is reported, never guessed.
    """
    waves, top = [], {}
    cur, sub = None, None
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split(" #")[0].rstrip() if " #" in raw else raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        body = line.strip()

        if indent == 0 and body.endswith(":") and body[:-1] == "waves":
            cur = None
            continue
        if indent == 0 and ":" in body:
            k, v = body.split(":", 1)
            top[k.strip()] = v.strip()
            continue

        if body.startswith("- ") and indent == 2:
            cur = {"_line": lineno}
            waves.append(cur)
            body, sub = body[2:], None

        if cur is None:
            continue

        if body.startswith("- "):
            if sub is not None:
                cur.setdefault(sub, []).append(body[2:].strip().strip("'\""))
            continue

        if ":" not in body:
            sys.exit("line %d is not a key/value pair or a list item: %r" % (lineno, raw))
        k, v = body.split(":", 1)
        k, v = k.strip(), v.strip()

        if indent >= 6 and sub == "proves":
            cur.setdefault("proves", {})[k] = _scalar(v)
            continue
        if v == "":
            sub = k
            if k == "proves":
                cur.setdefault("proves", {})
            continue
        sub = None
        cur[k] = _scalar(v)
    return top, waves


def _scalar(v):
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        return [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
    return v.strip("'\"")


def cli_commands():
    out = subprocess.run([sys.executable, str(CLI), "--help"],
                         capture_output=True, text=True).stdout
    block = out.split("{", 1)[1].split("}", 1)[0]
    return set(re.findall(r"[a-z][a-z-]+", block))


def check_receipt(wid, path, problems):
    """A receipt is the only thing that may turn a wave PASS. Read it, never trust it."""
    target = REPO / path
    if not target.exists():
        problems.append("%s names receipt %s, which does not exist" % (wid, path))
        return
    try:
        r = json.loads(target.read_text(encoding="utf-8"))
    except ValueError as exc:
        problems.append("%s receipt %s does not parse: %s" % (wid, path, exc))
        return
    for f in RECEIPT_FIELDS:
        if r.get(f) in (None, "", [], {}):
            problems.append("%s receipt %s has no %s; an unmeasured field stays "
                            "UNKNOWN and a wave with an UNKNOWN proof is not shipped"
                            % (wid, path, f))
    if r.get("checkpoint") not in (None, wid):
        problems.append("%s receipt %s belongs to %s" % (wid, path, r.get("checkpoint")))
    if r.get("status") not in (None, "PASS"):
        problems.append("%s is marked shipped but its receipt reads %s"
                        % (wid, r.get("status")))
    if r.get("baseline_sha") and not SHA_RE.match(str(r["baseline_sha"])):
        problems.append("%s receipt baseline_sha is not a 40-hex commit" % wid)


def main():
    manifests = [Path(a).resolve() for a in sys.argv[1:]] \
        or sorted((REPO / "plans").glob("*.manifest.yaml"))
    if not manifests:
        sys.exit("FAIL no plans/*.manifest.yaml found; nothing was checked")
    return max(check_one(m) for m in manifests)


def check_one(manifest):
    if not manifest.exists():
        print("::error::%s does not exist" % manifest)
        return 1

    top, waves = load_manifest(manifest)
    problems = []
    receipts_required = top.get("receipts_required") == "true"

    if top.get("schema") != "wi.build-manifest/v1":
        problems.append("top-level schema is %r, expected wi.build-manifest/v1"
                        % top.get("schema"))

    ids = [w.get("id") for w in waves]
    seen = set()
    for i in ids:
        if i in seen:
            problems.append("duplicate wave id %s" % i)
        seen.add(i)

    known = set(ids)
    for w in waves:
        wid = w.get("id", "(no id)")
        if not w.get("name"):
            problems.append("%s has no name" % wid)

        status = w.get("status")
        if status not in STATUSES:
            problems.append("%s has status %r; expected one of %s"
                            % (wid, status, ", ".join(STATUSES)))

        # Every wave must declare how anyone would know it is done.
        if not w.get("exit"):
            problems.append("%s declares no exit condition; a wave nobody can "
                            "close is a wish, not a plan" % wid)

        for dep in w.get("depends_on", []) or []:
            if dep not in known:
                problems.append("%s depends on %s, which is not a wave" % (wid, dep))

        # Law C. A shipped wave must name what proves it, and the proof must
        # answer when called.
        if status == "shipped":
            proves = w.get("proves") or {}
            if not proves:
                problems.append("%s is marked shipped but names nothing that "
                                "proves it" % wid)
            for cmd in proves.get("commands", []) or []:
                if cmd not in CLI_COMMANDS:
                    problems.append("%s claims command `wi %s` shipped, but the "
                                    "CLI does not have it" % (wid, cmd))
            for art in proves.get("artifacts", []) or []:
                if not (REPO / art).exists():
                    problems.append("%s claims artifact %s shipped, but it does "
                                    "not exist" % (wid, art))
            if receipts_required:
                if not w.get("receipt"):
                    problems.append("%s is marked shipped with no receipt; this "
                                    "manifest requires one" % wid)
                else:
                    check_receipt(wid, w["receipt"], problems)
                by_id = {x.get("id"): x for x in waves}
                for dep in w.get("depends_on", []) or []:
                    if dep in by_id and by_id[dep].get("status") != "shipped":
                        problems.append("%s is marked shipped but its dependency "
                                        "%s is %s" % (wid, dep, by_id[dep].get("status")))

    # Acyclicity, by iterative removal of waves whose dependencies are settled.
    pending = {w["id"]: set(w.get("depends_on", []) or []) for w in waves if w.get("id")}
    settled = set()
    progress = True
    while pending and progress:
        progress = False
        for wid in list(pending):
            if pending[wid] <= settled:
                settled.add(wid)
                del pending[wid]
                progress = True
    if pending:
        problems.append("dependency cycle among: %s" % ", ".join(sorted(pending)))

    shipped = [w["id"] for w in waves if w.get("status") == "shipped"]
    planned = [w["id"] for w in waves if w.get("status") == "planned"]

    try:
        shown = manifest.relative_to(REPO)
    except ValueError:
        shown = manifest
    print("checked %d wave(s) in %s" % (len(waves), shown))
    print("  shipped: %d (%s)" % (len(shipped), ", ".join(shipped)))
    print("  planned: %d" % len(planned))

    if problems:
        for p in problems:
            print("::error::" + p)
            print("FAIL " + p, file=sys.stderr)
        return 1

    print("manifest is acyclic, every wave declares an exit condition, and every")
    print("wave marked shipped names something that answers when called.")
    return 0


CLI_COMMANDS = cli_commands()

if __name__ == "__main__":
    sys.exit(main())
