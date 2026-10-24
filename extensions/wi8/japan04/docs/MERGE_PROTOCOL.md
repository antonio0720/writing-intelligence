# Four independent ZIPs: collision-free merge and canonical reconstitution

1. **Pin repo**: compare Git `HEAD`, clean status, v4/v5/v6/v7 regression snapshots, licenses and current manifest against `SOURCE_PIN.json`. The observed target SHA is not an authorization to install against changed code.
2. **Extract ZIPs without overlay**: preserve each archive's own top-level folder. ZIP #1 owns B001-B060; #2 owns N061-N120; #3 owns C121-C180; #4 owns JP-181..JP-340. Validate numeric IDs and semantic contract duplicates. Do not let common `README.md`, `schemas/` or `tests/` filenames override each other.
3. **Mount namespaced extensions**: #4 installs only into `extensions/wi8/japan04/`. The `tools/additive_install.py` script refuses overwriting existing paths and pins a Git HEAD. It neither changes core files nor creates a release branch. Existing extension experiments remain separate.
4. **Unify semantics, not databases**: core `STORYWORLD_OS` and v6 semantic IR are the sole owners of canonical narrative state. Consolidate proposed edge types and schema changes with all other v8 modules, then add one versioned adapter in the canonical owner. Never let the Japan JSON projection be treated as graph authority.
5. **Resolve overlapping material**: JP-286 wants/needs belongs to ZIP #2; JP-297 fair mystery and JP-300 logistics belong to ZIP #3; JP-184 prose voice and JP-290 emotional continuity align with ZIP #1. Japan supplies cultural specialization and exact evidence scopes, not a second arc/craft engine.
6. **Migrate aliases**: preserve legacy `CID::`, `CHAR::`, `TECH::`, `NAME::`, `LOC::` as historic aliases; map to new logical IDs only through a reviewed, rollback-capable migration. Never rewrite original PDFs or infer a unique phonetic reading from kanji.
7. **Exercise actual integration**: core script tests, negative controls, cases from all four ZIPs, old v4–v7 test suites, production app permission paths if selected, actual authorized author flows, readback from canonical state, and content-based regression checks. Local unit tests do **not** prove this.
8. **Release receipts**: every planned wave WI8-24..43 becomes shipped only when owner, exact revision, measured commands, failing negative control, independent readback, and record-specific evidence exist. v7 `plans/receipts` and the canonical manifest remain the only upstream status owners.

## What the merge must NOT do

- Change the global constitution or v6 source-of-truth semantics by importing Japan copy wholesale.
- Replace user-authored prose from a supposed 'cultural validator'.
- Fail a fantasy story for lacking Ki-Threads, twelve episodes or a Japanese folklore term.
- Ingest third-party copyright-excerpt PDF into a redistributable production bundle by default.
- Treat a self-asserted guardian flag as authenticated authority.
- Claim real Japanese accuracy, adoption, publication, commercial production or readership based on local tests.

## Stop conditions

Stop before merge on changed upstream HEAD, path collision, unresolved core graph schema ownership, governance downgrade, missing author role authentication, nonportable source rights, failed negative tests, or a proposed status falsely promoted to shipped. Reconcile the defect; do not introduce second canonical truth.
