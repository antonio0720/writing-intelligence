# Regression Matrix — v3.0

This matrix tracks every place v3.0 has the potential to regress against v2.0. Maintainers consult this during release review.

## Functional Regression Hazards

| Hazard | Surface | Mitigation |
|---|---|---|
| Pass 0 over-constrains | Intake Contract too rigid | User override always wins; ambiguity_flags surface for review |
| Pass 2 blocks more than it should | Corpus Auditor too strict | `fabrication_tolerance: flag_only` mode for low-stakes work |
| Pass 5 caps scores unfairly | Epistemic Ledger applied where not needed | High_stakes gating; opt-in for other domains |
| Pass 6 flattens voice | Sentence Surgeon over-cleans | Pass 7 restoration; voice_fidelity_delta surfaced |
| Pass 7 over-corrects | Voice restoration introduces hard-bans | Pass 6 + Pass 7 iteration; rewrite log audit |
| Pass 8 invents content | Delivery Packager creates new claims | Hard rule: cannot invent; surfaces violation |
| Pass 10 conflicts with Pass 5 | Scorekeeper tries to override cap | Hard rule: cannot override |
| Pass 11 corrupts memory | Storyworld updates overwrite valid data | Append-only by default; explicit user instruction required for delete |
| Multi-arena bundle voice drift | Pass 8 doesn't preserve fingerprint | Fingerprint enforcement in Delivery Packager |
| Series escalation curve plateau | Narrative Architect misses repetition | Stakes-per-book score must climb |
| Plant orphaning | Pass 4 misses unpaid plants | Surface; user confirms |
| Agent conflict resolution failure | Two agents disagree on output | Conflict resolution table; surface to user |

## Performance Regression Hazards

| Hazard | Cause | Mitigation |
|---|---|---|
| Long runtime | 11 passes vs. 7 | Allow skip with explicit reason |
| Token consumption | Schema validation adds overhead | Reference implementations should cache schemas |
| Latency in multi-arena | Pass 8 runs once per arena | Parallel execution per arena |
| Storyworld memory growth | Series accumulates state | Archive old chapters; surface deltas |

## Documentation Regression Hazards

| Hazard | Surface | Mitigation |
|---|---|---|
| README and SKILL drift | Different version numbers | Release checklist requires sync |
| ROADMAP shows shipped as future | Stale | Release checklist requires reconcile |
| CHEATSHEET behind on operators | New operators not listed | Release checklist requires update |
| USER_GUIDE missing new packs | Authors of new packs forget to update | Pack PR template requires USER_GUIDE update |
| Migration guide unclear | Users don't know what changed | Maintained per release |

## Quality Regression Hazards

| Hazard | Detection | Mitigation |
|---|---|---|
| Benchmark suite passes but real work degrades | Operator feedback | Operator-tier reviewers run real work; surface |
| Voice fingerprints diverge from descriptions | Inconsistency | RFC review checks for alignment |
| Genre packs become contradictory | Stack collision unresolved | Collision matrix updates required with every new pack |
| Schema versions drift from kernel | Outdated artifacts | Release checklist requires schema version stamp |

## Process Regression Hazards

| Hazard | Mitigation |
|---|---|
| Contributions skip RFC | PR template requires RFC link for minor+ |
| Benchmark cases added without v2 baseline | PR template requires baseline |
| Voiceprints added without measurable fingerprint | PR template enforces fingerprint requirement |
| New genre packs without collision matrix update | PR template requires matrix update |
| Schema changes without backwards compatibility | Maintainer review gate |

## v9 Preview Lanes (PR #8 — proposal, not a release)

v9 adds experimental lanes beside the v4–v8 suites. They are separate from them, change no version string, and guard the v9 proposal only. Passing them does not validate a wave: wave states live in `references/v9/WAVES.yaml`, and WI9-07 (the 60-case editorial benchmark) has not run.

| Lane | Command | Guards |
|---|---|---|
| Authorship checker | `python3 -m unittest discover -s tests/v9 -p 'test_*.py'` | `scripts/wi-authorship.py` P0 negative controls, schema parity with `schemas/v9/authorship-dossier.schema.json`, and the meaning-led doctrine scan |
| Reference kernel | `python3 -m unittest discover -s prototypes/wi9/tests -p 'test_*.py'` | 334-rule phrase scanner, review ledger digests, composition contract |
| v7 consistency | `bash tests/v7/test_wi7.sh` | version strings agree across `wi.py`, `SKILL.md` and `plans/*.manifest.yaml` — v9 must not change them |
| Links | `python3 scripts/check-links.py` | every relative link in the markdown resolves |

### v9 hazards and their negative controls

| Hazard | Negative control (must stay red when the guard is disabled) |
|---|---|
| A human-only venue accepts an assisted or generated draft | `HUMAN_ONLY_CONFLICT` / `SUBSTANTIVE_AI_CONTRIBUTION` HOLD, exit 3, even with a clean detector result — see `examples/v9/01-human-only-venue-hold.md` |
| One safe anchor carries several unsourced claims | `CLAIM_UNANCHORED` HOLD per uncovered claim — see `examples/v9/02-claim-coverage.md` |
| A planned or hypothetical item supports a firsthand claim | `experience_state` HOLD |
| The reviewed bytes differ from the submitted bytes | `expected_sha256` mismatch HOLD; required for any submission |
| An exact excerpt is read as truth | anchors report `ANCHOR_RESOLVED`, support stays `unadjudicated` |
| REVIEW is read as permission | `audit` never returns a release state and prints a notice on stderr |
| Release without a bound human decision or unexpired grant | `release` HOLD (`DECISION_REQUIRED`, `AUTHORITY_*`) |
| A symlink or `..` path escapes the dossier folder | file-boundary refusals |
| A detector-oriented instruction returns to the doctrine | `tests/v9/test_doctrine_meaning_led.py`, with a planted twin |
| A phrase match is treated as proof of AI authorship or auto-rewritten | scanner reports questions with offsets and digests only; the review ledger needs a human disposition |

Every v9 report is `declaration_status: self_reported`. These controls prove the declarations are checked for consistency; they do not prove who wrote a text.

## Watch List

After each release, maintainers monitor:

- Operator feedback (issues, PRs, discussion)
- Benchmark report deltas (auto-reported)
- Voice drift complaints (users report flattening)
- Compliance complaints (users report missed claim flags)
- Doc drift reports (users report stale docs)

A pattern of regression in any area triggers an investigation and possibly a patch release.
