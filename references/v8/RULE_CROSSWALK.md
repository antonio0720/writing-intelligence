# Fiction Intelligence v8 — complete 60-rule crosswalk

**Status:** proposed. Existing Writing Intelligence canonical owners listed here were verified in the GitHub main tree on 2026-10-24. All rules have a positive and negative editorial vector; that alone does not mean all rules have implemented detectors.

| ID | Rule | Owner | Current mechanism | Evidence limit |
|---|---|---|---|---|
| FI-01 | Metaphor Saturation Governor | `references/anti_patterns/cadence_expanded.md` | `text.figuration_density` | heuristic: executable_signal |
| FI-02 | Figurative Language Value Test | `references/anti_patterns/cadence_expanded.md` | `review.required` | editorial: requires_human_judgment |
| FI-03 | Manuscript-Wide Repetition Detection | `references/compiler/continuity.md` | `text.repeated_phrases` | heuristic: executable_signal |
| FI-04 | Metaphor Family Registry | `references/compiler/continuity.md` | `typed.motif_recurrence` | typed: executable_typed_check |
| FI-05 | Plain Prose Counterweight | `references/anti_patterns/cadence_expanded.md` | `review.required` | editorial: requires_human_judgment |
| FI-06 | Narrative Overexplanation Detector | `references/anti_patterns/cadence_expanded.md` | `review.required` | editorial: requires_human_judgment |
| FI-07 | Emotional Declaration Restraint | `references/anti_patterns/cadence_expanded.md` | `review.required` | editorial: requires_human_judgment |
| FI-08 | Sentence-Rhythm Diversity Audit | `references/anti_patterns/cadence_expanded.md` | `text.rhythm` | heuristic: executable_signal |
| FI-09 | Authorial Intrusion Detector | `references/anti_patterns/cadence_expanded.md` | `text.authorial_intrusion` | heuristic: executable_signal |
| FI-10 | Sensory Progression Engine | `references/anti_patterns/cadence_expanded.md` | `review.required` | editorial: requires_human_judgment |
| FI-11 | Descriptive Compression Operator | `references/anti_patterns/cadence_expanded.md` | `review.required` | editorial: requires_human_judgment |
| FI-12 | Prose Preservation Rule | `references/genre_packs/fiction.md` | `review.required` | editorial: requires_human_judgment |
| FI-13 | Escalation Novelty Law | `references/genre_packs/thriller_scene_architecture.md` | `typed.escalation_novelty` | typed: executable_typed_check |
| FI-14 | Tension Plateau Detector | `references/genre_packs/thriller_scene_architecture.md` | `typed.tension_plateau` | typed: executable_typed_check |
| FI-15 | Threat Consequence Requirement | `references/genre_packs/thriller_scene_architecture.md` | `typed.threat_consequence` | typed: executable_typed_check |
| FI-16 | Threat Specificity Test | `references/genre_packs/thriller_scene_architecture.md` | `review.required` | editorial: requires_human_judgment |
| FI-17 | Suspense Information-Asymmetry Engine | `references/compiler/novel_architecture.md` | `review.required` | editorial: requires_human_judgment |
| FI-18 | Earned Mystery Doctrine | `references/genre_packs/thriller_scene_architecture.md` | `review.required` | editorial: requires_human_judgment |
| FI-19 | Mystery Debt Ledger | `references/compiler/novel_architecture.md` | `typed.mystery_debt` | typed: executable_typed_check |
| FI-20 | Failure-Driven Escalation | `references/genre_packs/thriller_scene_architecture.md` | `review.required` | editorial: requires_human_judgment |
| FI-21 | Antagonist Competence Standard | `references/genre_packs/thriller_scene_architecture.md` | `review.required` | editorial: requires_human_judgment |
| FI-22 | Escalation Variety Requirement | `references/genre_packs/thriller_scene_architecture.md` | `typed.pressure_variety` | typed: executable_typed_check |
| FI-23 | Tension Recovery Discipline | `references/genre_packs/thriller_scene_architecture.md` | `typed.recovery` | typed: executable_typed_check |
| FI-24 | Chapter-Ending Integrity | `references/genre_packs/thriller_scene_architecture.md` | `review.required` | editorial: requires_human_judgment |
| FI-25 | Human Before Function Law | `references/genre_packs/fiction.md` | `typed.character_humanity` | typed: executable_typed_check |
| FI-26 | Personal Desire Conflict Engine | `references/genre_packs/fiction.md` | `typed.desire_conflict` | typed: executable_typed_check |
| FI-27 | Costly Rule Violation Test | `references/genre_packs/fiction.md` | `review.required` | editorial: requires_human_judgment |
| FI-28 | Distinct Character Decision Profiles | `references/genre_packs/dialogue.md` | `review.required` | editorial: requires_human_judgment |
| FI-29 | Relationship Evolution Ledger | `references/compiler/novel_architecture.md` | `typed.relationship_evolution` | typed: executable_typed_check |
| FI-30 | Emotional Memory Continuity | `references/genre_packs/fiction.md` | `typed.emotional_memory` | typed: executable_typed_check |
| FI-31 | Human Stakes Translation | `references/genre_packs/fiction.md` | `review.required` | editorial: requires_human_judgment |
| FI-32 | Character Agency Verification | `references/genre_packs/fiction.md` | `typed.character_agency` | typed: executable_typed_check |
| FI-33 | Competence Without Emotional Uniformity | `references/genre_packs/fiction.md` | `review.required` | editorial: requires_human_judgment |
| FI-34 | Emotional Payoff Audit | `references/genre_packs/fiction.md` | `review.required` | editorial: requires_human_judgment |
| FI-35 | World Rules Constitution | `references/v5/STORYWORLD_OS.md` | `typed.world_rules` | typed: executable_typed_check |
| FI-36 | Power Boundary Enforcement | `references/v5/STORYWORLD_OS.md` | `typed.power_boundary` | typed: executable_typed_check |
| FI-37 | Cost Conservation Doctrine | `references/v5/STORYWORLD_OS.md` | `typed.cost_conservation` | typed: executable_typed_check |
| FI-38 | Victory Versus Closure Distinction | `references/v5/STORYWORLD_OS.md` | `review.required` | editorial: requires_human_judgment |
| FI-39 | Consent and Authority Conflict Model | `references/v5/STORYWORLD_OS.md` | `review.required` | editorial: requires_human_judgment |
| FI-40 | Timeline Perspective Registry | `references/compiler/fiction_rule_integrity.md` | `typed.timeline` | typed: executable_typed_check |
| FI-41 | Canon Contradiction Classification | `references/compiler/fiction_rule_integrity.md` | `review.required` | editorial: requires_human_judgment |
| FI-42 | Speculative Mechanism Demonstration | `references/v5/STORYWORLD_OS.md` | `typed.mechanism_demonstration` | typed: executable_typed_check |
| FI-43 | Scientific Claim Boundary | `references/compiler/fiction_rule_integrity.md` | `review.required` | editorial: requires_human_judgment |
| FI-44 | Worldbuilding Restraint | `references/v5/STORYWORLD_OS.md` | `review.required` | editorial: requires_human_judgment |
| FI-45 | Novel-Length Escalation Graph | `references/compiler/novel_architecture.md` | `typed.escalation_graph` | typed: executable_typed_check |
| FI-46 | Act-to-Act Transformation Test | `references/compiler/narrative_intelligence_engine.md` | `typed.act_transform` | typed: executable_typed_check |
| FI-47 | Third-Act Acceleration Audit | `references/compiler/novel_architecture.md` | `review.required` | editorial: requires_human_judgment |
| FI-48 | Opening Promise Verification | `references/compiler/narrative_intelligence_engine.md` | `typed.opening_promises` | typed: executable_typed_check |
| FI-49 | Payoff Quality Engine | `references/compiler/novel_architecture.md` | `typed.payoff` | typed: executable_typed_check |
| FI-50 | Ending Without Explanation Law | `references/compiler/reader_experience.md` | `review.required` | editorial: requires_human_judgment |
| FI-51 | Standalone Satisfaction / Series Continuation Test | `references/compiler/narrative_intelligence_engine.md` | `typed.central_resolution` | typed: executable_typed_check |
| FI-52 | Emotional Center Protection | `references/compiler/reader_experience.md` | `review.required` | editorial: requires_human_judgment |
| FI-53 | Front Matter Separation | `references/diagnostics/scorecard.md` | `review.required` | editorial: requires_human_judgment |
| FI-54 | Document Placement Validator | `references/diagnostics/scorecard.md` | `review.required` | editorial: requires_human_judgment |
| FI-55 | Mathematical and Symbol Rendering Verification | `references/diagnostics/scorecard.md` | `text.raw_latex` | heuristic: executable_signal |
| FI-56 | Publishing Metadata Completeness | `references/diagnostics/scorecard.md` | `typed.metadata` | typed: executable_typed_check |
| FI-57 | Timeline and Cross-Book Reference Proofing | `references/diagnostics/scorecard.md` | `review.required` | editorial: requires_human_judgment |
| FI-58 | Typesetting and Pagination Audit | `references/diagnostics/scorecard.md` | `review.required` | editorial: requires_human_judgment |
| FI-59 | Independent Reader Evaluation | `references/compiler/reader_experience.md` | `process.reader_study` | process: executable_process_check |
| FI-60 | Genre-Specific Publication Gate | `references/diagnostics/scorecard.md` | `process.release` | process: executable_process_check |

## Layered execution and acceptance

The table describes *obligations*, not automatic judgments. See the originating words in `provenance/USER_REQUIREMENTS.txt`. The runtime reads `rules/fiction_v8_rules.json`; future changes require a rule catalog digest change, authored rationale, regression fixtures, and upstream authority.

1. **Text heuristics** identify phrase repetition, comparison-density candidates, rhythm uniformity, authorial intrusion and raw publication-symbol problems. Regex cannot identify figurative value, narrator intent or reader effect.
2. **Typed scene checks** can find declared plateaus, missing causality, motif stasis, unproven threat annotations, abnormal timelines and unresolved promises. When data is absent, they never infer from zero findings that the book passed.
3. **Hard structural invariants** prohibit explicit canon-forbidden actions, omitted mandatory costs and internally invalid references. These have a reproducible failure path with inspectable scene identifiers.
4. **Human/editorial obligations** require actual literary interpretation and grounded examples. Model-generated assessments may propose, never certify.
5. **Reader/publication obligations** require version-bound reader responses, manuscript/export evidence and accountable human authorization.

## Required reviewer answer for every rule

For each FI-XX: cite exactly what the manuscript does; quote the smallest necessary span; identify the intended genre/voice effect; record the strongest reason the passage might be acceptable; state the smallest change that would improve it; preserve the original and evidence of author choice. If a reviewer cannot distinguish an intentional exception from a defect, report that uncertainty, not an invented grade.

