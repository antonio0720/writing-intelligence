# Migrating v4 → v5

**Short version: nothing breaks.** v5 is additive. The eleven passes, twelve engines, twelve agents, genre packs, voiceprints, schemas and anti-slop doctrine are unchanged, and so are the six v4 laws. Every v4 command takes the same arguments and produces the same verdict words.

What v5 adds is memory: a workspace that knows what supports what, so an edit made three weeks after a check does not quietly inherit the check's result.

---

## Do this

```bash
cd ~/.claude/skills/writing-intelligence && git pull
python3 scripts/wi.py --version    # wi 5.0.0
bash tests/v4/test_wi.sh           # 3 x PASS — the v4 floor still passes
bash tests/v5/test_wi5.sh          # 32 x PASS — the v5 core
python3 scripts/wi.py doctor       # what this machine can and cannot do
```

That is the whole upgrade. No schema migration, no config file to write, no re-authoring.

---

## Your existing commands

Unchanged, in the same file, with the same flags:

```bash
python3 scripts/wi.py preserve draft.md
python3 scripts/wi.py scan-sources sources/
python3 scripts/wi.py extract-claims draft.md --out claims.json
python3 scripts/wi.py verify claims.json sources/
python3 scripts/wi.py gate claims.json --mode strict --exit-code
```

Existing CI jobs and git hooks keep working with no edit. `gate` now accepts **either** a v4 sentence ledger or a v5 atom ledger and reports accordingly — sentences for the former, claim atoms plus a stale-node count for the latter.

**Existing claim ledgers.** A v4 `claims.json` stays valid input to `verify` and `gate` forever. There is no converter and none is needed: to move a document onto the v5 unit, re-run `wi atomize` on the draft, which produces a fresh atom ledger inside the workspace. The old file is not consumed, migrated or deleted.

---

## What to adopt, in the order it pays off

| Step | Command | What you get |
|---|---|---|
| 1 | `wi init --mode strict` | A `.wi/` workspace and a `wi.project.yaml`. One directory, no server |
| 2 | `wi ingest sources/` | Sources addressed by content digest, with versions. This is what makes staleness detectable |
| 3 | `wi atomize` + `wi anchor` | The claim atom replaces the sentence as the verified unit; results persist |
| 4 | `wi impact <source>` | The minimum repair frontier the first time a source changes — the moment v5 stops being ceremony |
| 5 | `wi test` | Writing tests beside `gate --exit-code` in CI |
| 6 | `wi bundle` / `wi verify-release` | A release a stranger can check offline, with no model |

Full walkthrough with real output: [`../USER_GUIDE.md`](../USER_GUIDE.md).

---

## What is new

| | New in v5 | Where |
|---|---|---|
| Six system laws G–L | Meaning identity, semantic delta, dependency-aware proof, decision records, one engine, explainable release | [`../references/v5/CONSTITUTION.md`](../references/v5/CONSTITUTION.md) |
| The workspace | SQLite index plus a content-addressed object store, in a directory | [`../references/v5/WORKSPACE.md`](../references/v5/WORKSPACE.md) |
| Claim atoms | A compound sentence becomes independently checkable assertions | [`../references/v5/SEMANTIC_IR.md`](../references/v5/SEMANTIC_IR.md) |
| Evidence anchors | Typed, resolvable pointers with byte offsets and quote digests | [`../references/v5/EVIDENCE_ANCHORS.md`](../references/v5/EVIDENCE_ANCHORS.md) |
| Semantic diff | `wi diff --semantic` classifies what a rewrite did to meaning | [`../references/v5/SEMANTIC_DIFF.md`](../references/v5/SEMANTIC_DIFF.md) |
| Staleness and repair frontier | `wi impact` names what broke and what is provably untouched | [`../references/v5/STALENESS.md`](../references/v5/STALENESS.md) |
| Writing tests | Assertions about a document, with exit codes | [`../references/v5/CONCEPT_REGISTRY.md`](../references/v5/CONCEPT_REGISTRY.md) |
| Proof-carrying release | `.wiab` bundles, verified offline with no model | [`../references/v5/PROOF_CARRYING_RELEASE.md`](../references/v5/PROOF_CARRYING_RELEASE.md) |
| Capability report | `wi doctor` — Law C as protocol | [`../references/v5/SURFACES.md`](../references/v5/SURFACES.md) |

---

## What behaves differently

**Two new statuses.** `span_supported` and `candidate_support` sit between `supported` and `needs_source`. A v4 claim that read `needs_source` because it was a good paraphrase will often now read `span_supported` — located, components matched, entailment explicitly not judged. That is more information, not a relaxation: `span_supported` still holds at `regulated`.

**Staleness can hold a gate that used to release.** A claim verified against a source version that has since been superseded holds, even though every check it was given passed. That is the point of v5. Re-run `wi anchor` to rebind, then read what actually changed.

**`wi gate` does not read the project file's evidence mode.** `wi init --mode strict` writes `evidence.default_mode: strict` into `wi.project.yaml`, but `gate` still defaults to `standard` unless you pass `--mode`. Put the mode in your CI command and your hook.

**`wi test` fails on an assertion it does not implement.** `SKIP ... is not implemented in this tier` counts toward the exit code. A test you believe is running and is not is worse than no test.

---

## What did not arrive, and is labelled so everywhere

`paraphrase entailment` — no judgment provider ships anywhere, so entailment is never evaluated by anything · `pdf_region`, `sheet_range`, `audio_time`, `video_time`, `image_region` anchors — adapter contracts specified, not executable · external signing (Sigstore, C2PA) — bundles are digest-sealed, not signed · machine-readable proposal objects and hashed decision records (Laws A and J) · the full concept registry beyond `concept.equals` and `terminology.forbidden` · `wi.lock` · Workbench · MCP server · REST v5 endpoints.

`wi doctor` prints the list for the machine you are standing on. Nothing in this repository reports any of it as done.

---

## Rolling back

```bash
rm -rf .wi wi.project.yaml
```

The v4 commands are unchanged and still there. You lose the graph, the source versions and the staleness history; you lose nothing in `sources/`, `drafts/` or anything already shipped. A later `wi init` + `ingest` + `atomize` + `anchor` rebuilds an equivalent workspace from the same inputs.

---

Read next: [`../USER_GUIDE.md`](../USER_GUIDE.md) · [`../CHEATSHEET.md`](../CHEATSHEET.md) · [`INSTALL.md`](INSTALL.md) · [`MIGRATION_v3_to_v4.md`](MIGRATION_v3_to_v4.md)

---

**Antonio T. Smith Jr. / Density6 LLC** · MIT · v5.0.0
