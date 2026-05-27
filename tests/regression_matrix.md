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

## Watch List

After each release, maintainers monitor:

- Operator feedback (issues, PRs, discussion)
- Benchmark report deltas (auto-reported)
- Voice drift complaints (users report flattening)
- Compliance complaints (users report missed claim flags)
- Doc drift reports (users report stale docs)

A pattern of regression in any area triggers an investigation and possibly a patch release.
