# Canonical Ownership / Source-Rule Crosswalk

This is a merge plan, **not a claim that any existing repo file was modified**.

| Existing owner | Upgrade intent | Requirement IDs |
|---|---|---|
| `references/genre_packs/fiction.md` | want/need, nonbinary endings, independent agency, exceptions | B025–B034, N061–N070, N081–N090 |
| `references/genre_packs/dialogue.md` | relationships and belief changes expressed in speech + action | B028–B030, N073, N077–N080 |
| `references/compiler/character_role_archetypes.md` | archetypes remain jobs, not personhood | B025, N087–N090 |
| `references/compiler/narrative_intelligence_engine.md` | graph-root-linked arc snapshots, ending derivation | B045–B052, N061–N120 |
| `references/v5/STORYWORLD_OS.md` | event time, character state, canon authority | B035–B044, N071–N112 |
| `references/v5/AUTHORSHIP_GRAPH.md` | derived dependencies and evidence edges | N087–N112 |
| `references/v6/SEMANTIC_IR.md` + `schemas/v6/semantic_node.schema.json` | admissible node extensions; no bypass of closed vocabulary | N111–N114 |
| `references/v6/BITEMPORAL_STATE.md` | preserve decision-time versions | N063, N094, N112 |
| `references/v6/AUTHORITY_MODEL.md` | authorized author choices and waivers | B012, N118 |
| `references/positive_patterns/tension_mechanics.md` | no universally compulsory phases/percentages | B013–B024, N116 |
| `references/diagnostics/scorecard.md` | distinct mechanical / artistic / reader / publication claims | B059–B060, N110, N119 |
| `benchmarks/cases/`, `tests/v8/` | paired controls and genuine-reader future calibration | N113–N120 |
| `plans/v8.manifest.yaml` after integration | receipt-governed canonical release source | N120 |

The earlier independent ZIP owns B001–B060 implementation, so this package's rule catalog must remain a **traceable registry** for B rules, not a second competing evaluator for them.

---

## v9 preview crosswalk

The table above is the v8 fiction merge plan. This one maps the v9 waves (PR #8, preview, release on HOLD until WI9-09) to the files that own them today. Wave states are from [`../references/v9/WAVES.yaml`](../references/v9/WAVES.yaml); a state here is not a claim that the wave is released.

| Wave | State | Owner / files today |
|---|---|---|
| WI9-00 Baseline and evidence audit | VALIDATED (owner approval pending) | `references/v9/defects.md`, `plans/receipts/WI9-00.json` |
| WI9-01 Authorship contract | PROTOTYPE | `scripts/wi-authorship.py` (`audit`, `release`), `schemas/v9/authorship-dossier.schema.json`, `tests/v9/test_authorship*.py`, `tests/v9/test_schema_parity.py` |
| WI9-02 Firsthand material vault | PLANNED | Only `experience_state` typing exists, inside the dossier schema and checker |
| WI9-03 Voice baseline | PROTOTYPE | `prototypes/wi9/wi9_core.py voice` (statistics only; no consented corpus) |
| WI9-04 Thought fidelity | PLANNED | No owner file yet |
| WI9-05 Craft repair | IN_PROGRESS | Doctrine repair across `references/compiler/`, `references/diagnostics/` (`repair_rhythm` in `rewrite_operators.md`), `references/anti_patterns/`; `prototypes/wi9/wi9_hotphrases.py`, `wi9_phrase_review.py`; guard `tests/v9/test_doctrine_meaning_led.py` |
| WI9-06 Human-only venue gate | PROTOTYPE | `release` in `scripts/wi-authorship.py`; `prototypes/wi9/wi9_composition.py` (refuses `human_only` venues) |
| WI9-07 Editorial benchmark | PLANNED, not executed | `references/v9/QUALITY_BENCHMARK.md`; `wi9_core.py benchmark` holds until 60 matched cases exist |
| WI9-08 Integration | PLANNED | Will fold into `scripts/wi.py`, `docs/api/API_SPEC.md`, `docs/mcp/MCP_SPEC.md`, and bind the `release` grant to the v6 store |
| WI9-09 Independent review and rollout | PLANNED, release HOLD | Receipt and owner approval still to come |

Rule carried over from v8: the standalone v9 tools are traceable additions, not a second evaluator for rules `scripts/wi.py` owns. Where the two disagree, `scripts/wi-authorship.py` is the answer for authorship and venue, and the difference is a defect to record.
