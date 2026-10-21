# RFC-0001 — What "v7" means

**Status:** ACCEPTED · 2026-10-21 · decided by the repository owner, Antonio T. Smith Jr. (Density6 LLC)
**Program:** WI7-IIP — the Institutional Intelligence Expansion
**Baseline:** `b59ef9544e9da78bab3dfa8db2178d4e6b569d16`

## The conflict

Until 7.0.0, `ROADMAP.md` used "v7.0" for one thing: the full sovereign runtime
horizon (surfaces, the Workbench, storyworlds, autonomous workers, migration,
`.wipack` packages), targeted for 2029 and governed by the planned waves
W13–W28 in `plans/v6.manifest.yaml`. The WI7-IIP program plan uses "v7" for a
second thing: the institutional product program (Research, Legal, Capital, and
Awards & Contracts). Two meanings for one version number is the same defect
this project refuses everywhere else — two answers to one question, agreeing
until somebody reads the wrong one.

## Decision

1. **Writing Intelligence v7 is the Institutional Intelligence line.** Its
   program identifier is WI7-IIP, its waves are WI7-00 … WI7-19, and its one
   status source is `plans/v7.manifest.yaml`.
2. **The runtime horizon is not discarded or renamed away.** It becomes the
   substrate v7 is built on. Waves W13–W28 stay in `plans/v6.manifest.yaml`,
   keep their IDs, dependencies and exit conditions, and remain authoritative.
   WI7 waves that need them (judgment gateway, evidence adapters, renderer
   source maps, Workbench, autonomy, migration) wait on them.
3. **WI7 wave identifiers never reuse W-numbers.** WI7-05 is not W05.
4. **7.0.0 ships governance, not institutional capability.** It contains the
   doctrine repair (WI7-01), the reproducibility floor (WI7-02), the baseline
   freeze (WI7-00), this RFC, the program plan, the program manifest and a
   checker that refuses a shipped wave with no receipt. Waves WI7-03 … WI7-19
   are `planned`. No release note, README line or skill description may claim
   a doctoral, legal, capital, grant, procurement or investor workflow works
   until its wave is shipped with a receipt.
5. **Semantic versioning still applies.** 7.0.0 is a major version because the
   meaning of "v7" changed and the academic doctrine changed behavior; the
   CLI, the v4/v5/v6 commands, digests and bundle formats are unchanged.
   Existing `.wiab` bundles and v6 workspaces need no migration.
6. **The MIT core stays MIT.** Paid institutional services may be built beside
   it; nothing in v7 claims exclusivity over code already published under MIT.

## Consequences

- `ROADMAP.md` now describes v7 as the institutional line and the former v7.0
  horizon as "the sovereign runtime substrate (W13–W28)".
- `scripts/check-manifest.py` validates every `plans/*.manifest.yaml`, and
  enforces receipts wherever a manifest declares `receipts_required: true`.
- `tests/v7/test_wi7.sh` proves both the doctrine repair and the receipt rule,
  each with a negative control that must go red.
