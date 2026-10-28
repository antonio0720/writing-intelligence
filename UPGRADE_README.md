# Writing Intelligence — Fiction & Thriller Intelligence v8 Candidate

**Deliverable:** standalone, add-only implementation package for `antonio0720/writing-intelligence`. **Status:** locally tested proposal, not merged, not deployed, not the published v8 release. GitHub main observed at `d4524f3caa5f75e005b23f94dcd1c71bb5002127` on 2026-10-24.

## What you have

The 60 requirements are preserved in `provenance/USER_REQUIREMENTS.txt` and normalized into `rules/fiction_v8_rules.json`, each with its source requirement, stable FI-XX ID, canonical owner, acceptance condition, positive and negative example, execution owner and evidence limit. The proposed constitution and three new compiler documents add novel architecture, causal rule integrity, and independent reader experience **without replacing** existing v7 machinery.

The executable component `scripts/wi-fiction.py` is offline, stdlib-only, read-only with respect to manuscript/canon, and produces digest-bound JSON audit results. It implements genuine typed constraints, limited text heuristics, and a three-stage release gate; the other rules explicitly remain editorial judgments. The gate does not equate a green checksum with a good novel. `tests/v8` contains 41 unit, adversarial and CLI tests (run again locally to verify this claim in your environment). The pipeline recognizes mechanical defects, uncertain pattern signals, incomplete annotation, honest human editorial review and independent reader study as **different states**.

## Run immediately

From the **package root** (Python 3.8+):

```bash
bash tests/v8/run.sh
python3 scripts/wi-fiction.py catalog > /tmp/fiction-rules.json
python3 scripts/wi-fiction.py explain-rule FI-25
python3 scripts/wi-fiction.py validate --input tests/v8/fixtures/valid_draft.json
python3 scripts/wi-fiction.py audit --input tests/v8/fixtures/flat_tension.json
python3 scripts/wi-fiction.py text-signals --text tests/v8/fixtures/anti_patterns.txt
python3 scripts/wi-fiction.py gate --input tests/v8/fixtures/valid_draft.json --mode publication
# Expected exit 3 (HOLD), not a publication-ready certificate.
```

To create a report file without overwriting previous evidence:

```bash
python3 scripts/wi-fiction.py audit --input tests/v8/fixtures/valid_draft.json --out /tmp/wi-fiction-draft-report.json
```

## Install into the **existing repo** after review

```bash
python3 scripts/install_additive.py --target /path/to/writing-intelligence
python3 scripts/install_additive.py --target /path/to/writing-intelligence --apply
```

Installer rejects all existing-file collisions; it does not modify upstream v7 files, commit, push or merge. The source checkout must already exist. Follow `docs/FICTION_V8_INTEGRATION.md` before editing existing canonical docs or packaging `.skill` archives. The wrapper CLI is `wi-fiction.py`, **not** an imaginary `wi fiction` command. The official `scripts/wi.py` remains untouched.

## Reading order

1. `references/v8/FICTION_INTELLIGENCE_CONSTITUTION.md` — creative invariants and explicit exception doctrine.
2. `docs/FICTION_V8_ARCHITECTURE.md` — graph, evidence, dependency and release semantics.
3. `references/compiler/novel_architecture.md`, `fiction_rule_integrity.md`, `reader_experience.md` — three targeted specialized contracts.
4. `rules/fiction_v8_rules.json` and `references/v8/RULE_CROSSWALK.md` — 60 requirement mapping and test vectors.
5. `docs/FICTION_V8_INTEGRATION.md` — canonical owner crosswalk and the **not yet implemented** adapter.
6. `docs/FICTION_V8_RELEASE_AND_SECURITY.md` — adversarial boundaries, remaining unknowns.

## What is intentionally not being represented as shipped

Automatic extraction of every scene from a full novel, AI-quality adjudication, token-consuming literary rewriting, reader recruitment, actual physical print/EPUB proof, canonical `wi.py` integration, native `.skill` bundle inclusion, live-repo v4–v7 regression, PR creation, merges or v8 release. Those depend on canonical authority and independent evidence rather than a polished ZIP file.

---

## v8 -> v9 preview

**Status:** v9 is a **preview** on [PR #8](https://github.com/antonio0720/writing-intelligence/pull/8) — proposed, not released. 8.0.0 is the published release, version strings are unchanged, and the release is on HOLD until WI9-09. Records: [`references/v9/README.md`](references/v9/README.md), [`references/v9/WAVES.yaml`](references/v9/WAVES.yaml).

- **Nothing breaks.** Every v4–v8 command, exit code, digest and bundle format behaves as before. v9 adds files; it removes none of your tooling.
- **New, optional commands, all through `wi authorship`.** `audit` and `release` (REVIEW/RELEASE_ELIGIBLE exit 0, HOLD exit 3; sends nothing); `vault` for your own firsthand material; `meaning` to see every change a revision makes to what you meant; `ledger` and `phrase-review` for review decisions bound to your own v6 grant; `voice`, `voice-review` and `voice-compare` for your own voice; `scan` (chunked for long manuscripts) and `structure` for editorial questions; `compose` to call a model you choose, after the venue and evidence gates.
- **Your material stays yours.** v9 ships no voice samples, notes or model. Vault, voice and ledger folders are yours, kept outside any repository; the tools refuse to create them inside one.
- **One behaviour to know.** A phrase review whose decisions carry only a typed reviewer name now holds `REVIEWER_UNBOUND`; record decisions with `wi authorship ledger record` under your grant.
- **One rename in craft doctrine.** The retired v8 length-quota rewrite operator is now `repair_rhythm`, and it no longer prescribes length quotas or detector-oriented edits. Log operation `rhythm_repaired` is emitted going forward; logs that contain the old `variance_injected` operation still validate and are never rewritten.
- **Dossier schema.** `schemas/v9/authorship-dossier.schema.json` is `wi9-authorship-2`; `wi9-authorship-1` dossiers are still read.
- **Requirements added by v9.** POSIX file semantics (the checker, vault and ledger refuse with `PLATFORM_UNSUPPORTED` where `O_NOFOLLOW` is unavailable, e.g. Windows — tested on a Windows runner) and Python 3.8+. Paths in a dossier are relative to its directory.
- **What to expect, and not.** Reports are `self_reported` declarations. Nothing authenticates a writer, and no benchmark or quality result exists yet (WI9-07 has not run).

Verify on a checkout of the branch: `bash scripts/test-v9.sh` and `bash tests/v7/test_wi7.sh`.
