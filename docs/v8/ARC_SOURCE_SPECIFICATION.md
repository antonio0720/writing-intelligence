# Writing Intelligence v8 — Fiction, Character Arc & Ending Intelligence

**Proposed upgrade specification — no GitHub edits have been made.**

- **Repository:** [https://github.com/antonio0720/writing-intelligence/](https://github.com/antonio0720/writing-intelligence/)
- **Observed branch:** `main` at `d4524f3caa5f75e005b23f94dcd1c71bb5002127` (24 October 2026 review)
- **Primary attachment:** *The Only 4 Ways To End A Story* (9-page PDF; user's accumulated notes; film examples and K. M. Weiland references embedded in the notes)
- **Earlier requirements incorporated:** 60-item fiction/thriller/editorial review derived from *Aperture I: The Entropic Ledger*
- **This specification:** 120 requirements; 60 carried-forward + 60 derived/extended from the new notes and repository gaps
- **Implementation status:** PROPOSED; no code changes, tests, deployments, or release claims.

## Executive diagnosis

v3 already has genre craft and a Fiction v2 pack, chapter construction, role archetypes, dialogue, scene tension, and long-form memory. v5 *specifies* richer storyworld nodes and canon timelines but explicitly says many of them are not executable; `wi test` and graph identity/impact are executable. v6 supplies governed semantic state and version-aware authority; v7's primary program is institutional and several domain workflows remain planned. Do not invent a separate competing story database. Implement v8 as fiction-specific semantic extensions and authoring/evaluation projections over the canonical meaning graph.

### Important interpretation of the attachment

The attachment defines wants as conscious external goals and needs as often latent inner goals, then presents sweet, semi-sweet, bittersweet and bitter endings as a 2×2 classification. It also explores positive-change, flat, corruption, and fall arcs using *Back to the Future*, *The Godfather*, *Joker*, *Onward*, *Rain Man*, and *The Social Network*. These are the **notes' interpretive examples**, not independent determinations of the films' meanings. The notes refer to K. M. Weiland and screenplay page numbers; preserve provenance rather than attributing the underlying craft ideas as wholly original.

**Crucial correction:** the four quadrants classify binary want/need outcomes; they do not exhaust fictional endings. Arc trajectory and ending outcome are separate, multi-dimensional variables. v8 must support partial fulfillment, changed wants, sacrifice, unresolved arcs, multiple protagonists, subjective needs, and endings that intentionally resist the framework.

## Full proposed requirement register

Each item is an addition or strengthening of an existing canonical primitive. `B` means carried-forward baseline, `N` a new notes-driven requirement. Numbering is stable for implementation and test planning.

### Prose Intelligence — prior recommendations (01–12)

1. **B001 — Metaphor Saturation Governor.** Detect excessive similes, metaphors, and poetic interpretations across passages; recommend selective edits without flattening voice.
2. **B002 — Figurative Language Value Test.** Require major imagery to add perception, emotional consequence, characterization, or thematic meaning rather than paraphrase the previous line.
3. **B003 — Manuscript-Wide Repetition Detection.** Count repetitive expressions and sentence patterns by chapter and across the complete manuscript, reporting locations rather than guessing quality.
4. **B004 — Metaphor Family Registry.** Distinguish deliberately recurrent imagery from overused image families and semantic equivalents.
5. **B005 — Plain Prose Counterweight.** Protect direct physical description, ordinary sentences, and restraint as deliberate parts of literary rhythm.
6. **B006 — Narrative Overexplanation Detector.** Flag passages where exposition names the meaning of an already intelligible dramatic image.
7. **B007 — Emotional Declaration Restraint.** Find repeated statements of emotion that could be carried more effectively by action, dialogue, thought, or consequence.
8. **B008 — Sentence-Rhythm Diversity Audit.** Evaluate fragment chains, parallel constructions, paragraph length, and narration cadence over sustained passages.
9. **B009 — Authorial Intrusion Detector.** Catch narration that announces a chapter's or book's intended meaning without explicit metafictional justification.
10. **B010 — Sensory Progression Engine.** Track recurring sensations and require evolution in cause, meaning, stakes, or consequence.
11. **B011 — Descriptive Compression Operator.** Identify redundant description while safeguarding atmosphere, orientation, voice, and character.
12. **B012 — Prose Preservation Rule.** Forbid automatic deletion by word-frequency threshold; edits require contextual review and author approval.

### Thriller & Suspense Intelligence — prior recommendations (13–24)

13. **B013 — Escalation Novelty Law.** New danger beats must alter exposure, constraints, knowledge, relationships, or options; heightened adjectives alone do not qualify.
14. **B014 — Tension Plateau Detector.** Find adjacent scenes repeating the same pressure without a dramatic state change.
15. **B015 — Threat Consequence Requirement.** Demand a concrete demonstrated consequence of a major threat before mystery is prolonged too far.
16. **B016 — Threat Specificity Test.** Separate disquiet from recognizable danger and mark where a reader obtains actionable understanding.
17. **B017 — Suspense Information-Asymmetry Engine.** Track knowledge differences among reader, protagonist, allies, and antagonists at scene and act boundaries.
18. **B018 — Earned Mystery Doctrine.** Preserve uncertainty over answers while orienting the reader to the operative question.
19. **B019 — Mystery Debt Ledger.** Track raised questions, clues, partial answers, reveals, and deliberately deferred mysteries across a series.
20. **B020 — Failure-Driven Escalation.** Favor complications causally generated by characters' attempts rather than unrelated arbitrary interruptions.
21. **B021 — Antagonist Competence Standard.** Keep adversarial choices strategically credible and bounded by established abilities and resources.
22. **B022 — Escalation Variety Requirement.** Vary physical, social, relational, institutional, informational, psychological, and moral pressure.
23. **B023 — Tension Recovery Discipline.** Preserve genuine relief, humor, intimacy, and normal life rather than one sustained maximum intensity.
24. **B024 — Chapter-Ending Integrity.** Reject arbitrary cliffhangers that depend on withheld information characters already know.

### Character & Emotional Intelligence — prior recommendations (25–34)

25. **B025 — Human Before Function Law.** Treat narrative and professional functions as secondary to desire, relationships, memories, contradictions, and agency.
26. **B026 — Personal Desire Conflict Engine.** Ensure major characters can want things that conflict with duty, ideology, loyalty, or one another.
27. **B027 — Costly Rule Violation Test.** Make rule-breaking psychologically credible, causally legible, and consequence-bearing.
28. **B028 — Distinct Character Decision Profiles.** Differentiate people through decisions under stress as well as dialogue mannerisms.
29. **B029 — Relationship Evolution Ledger.** Track shifts in trust, intimacy, status, obligation, resentment, and betrayal over time.
30. **B030 — Emotional Memory Continuity.** Carry psychological consequences into later scenes without implausible automatic reset.
31. **B031 — Human Stakes Translation.** Bind large-system threats to intimate, recognizable consequences in bodies, relationships, memory, and homes.
32. **B032 — Character Agency Verification.** Find turning points where characters merely observe a mechanism; require consequential agency or explicit helplessness.
33. **B033 — Competence Without Emotional Uniformity.** Permit expertise and personality, weakness, bias, humor, grief, and irrationality to coexist.
34. **B034 — Emotional Payoff Audit.** Require earned dramatization of losses, reunions, betrayals, sacrifices, and wins.

### Worldbuilding & Speculative Fiction — prior recommendations (35–44)

35. **B035 — World Rules Constitution.** Model fictional capacities, exclusions, conditions, costs, and exceptions; distinguish established fact from character belief.
36. **B036 — Power Boundary Enforcement.** Prevent convenient ability expansion unsupported by canon or explicit storyworld exception.
37. **B037 — Cost Conservation Doctrine.** Track debts and consequences of extraordinary interventions without narrative erasure.
38. **B038 — Victory Versus Closure Distinction.** Separate objective completion, legitimacy, moral correctness, physical safety, and enduring resolution.
39. **B039 — Consent and Authority Conflict Model.** Track who can act, who claims permission, who actually holds authority, and who bears costs.
40. **B040 — Timeline Perspective Registry.** Distinguish event, document, observation, narration, and record-revision times.
41. **B041 — Canon Contradiction Classification.** Distinguish deliberate paradox, mistaken character belief, unreliable narrator, unresolved mystery, and actual continuity defect.
42. **B042 — Speculative Mechanism Demonstration.** Show fictional rules through actions, limitations, and costs rather than abstract lectures alone.
43. **B043 — Scientific Claim Boundary.** Label real science, contested interpretation, fictional extrapolation, and invented mechanisms differently.
44. **B044 — Worldbuilding Restraint.** Reject worldbuilding additions that provide no causal, emotional, aesthetic, or narrative benefit.

### Novel Architecture & Series — prior recommendations (45–52)

45. **B045 — Novel-Length Escalation Graph.** Measure structural change in stakes, vulnerability, information, and irreversibility across all chapters.
46. **B046 — Act-to-Act Transformation Test.** Ensure major phases change the protagonist's choices, identity, relationships, or understanding.
47. **B047 — Third-Act Acceleration Audit.** Detect aftermath scenes that restate victory consequences without producing new changes.
48. **B048 — Opening Promise Verification.** Compare opening emotional/genre promises and mysteries with their delivery later in the novel.
49. **B049 — Payoff Quality Engine.** Audit setup-to-payoff causal legitimacy and emotional yield, not only matching references.
50. **B050 — Ending Without Explanation Law.** Flag explicit declarations that a book is ending or that its final line is significant.
51. **B051 — Standalone Satisfaction / Series Continuation Test.** Test local arc closure separately from unresolved long-series hooks.
52. **B052 — Emotional Center Protection.** Check that spectacular systems do not displace the human conflict at the center of the novel.

### Editorial & Publication — prior recommendations (53–60)

53. **B053 — Front Matter Separation.** Disentangle necessary story orientation from author manifestos, marketing, and optional essays.
54. **B054 — Document Placement Validator.** Find glossaries, guides, and explanatory materials inserted at distracting or impossible reading positions.
55. **B055 — Mathematical and Symbol Rendering Verification.** Detect broken LaTeX, escapes, Unicode, equations, and layout in produced editions.
56. **B056 — Publishing Metadata Completeness.** Report unfinished ISBN, edition, imprint, attribution, and production placeholders as applicable.
57. **B057 — Timeline and Cross-Book Reference Proofing.** Validate date/event references and serialized continuity without suppressing deliberate nonlinear histories.
58. **B058 — Typesetting and Pagination Audit.** Check formatting, spacing, widows/orphans, and print/ebook usability in addition to word counts.
59. **B059 — Independent Reader Evaluation.** Collect observations from human readers on suspense, confusion, emotional impact, and satisfaction.
60. **B060 — Genre-Specific Publication Gate.** Never infer publication readiness solely from grammatical, structural, or canon test passes.

### Want/Need & Ending Semantics — new from notes (61–70)

61. **N061 — Conscious External Want Contract.** Record the concrete outcome the character knowingly seeks, its owner, earliest statement, and whether its pursuit drives external plot. [Notes pp.1–2]
62. **N062 — Latent Internal Need Contract.** Record the proposed inner development, why it matters, when/if the character recognizes it, and who is interpreting it. [Notes pp.1,5]
63. **N063 — Want/Need Version History.** A want may be replaced, reprioritized, attained, abandoned, or become a need; preserve prior states instead of overwriting history. [Notes pp.2,4,6]
64. **N064 — Outcome Quadrant Calculator.** Provide sweet, semi-sweet, bittersweet, and bitter as a transparent 2×2 **view** of want/need outcomes, not an exhaustive theory of narrative endings. [Notes pp.1,3,5,7]
65. **N065 — Nonbinary Outcome Vocabulary.** Support fulfilled, partially fulfilled, relinquished, sacrificed, thwarted, unknown, disputed, and not-applicable rather than forcing every ending to yes/no.
66. **N066 — Want Versus Need Collision Model.** Track scenes in which attaining the visible goal compromises inner need, or satisfying the need requires giving up the goal. [Notes pp.4,6–9]
67. **N067 — Multiple Simultaneous Wants.** Support competing goals at different levels, including immediate scene objectives, act-level targets, and a changed central goal. [Notes pp.2,4,6]
68. **N068 — Need Interpretation Provenance.** Treat 'this character needs X' as author-declared craft interpretation, not an objectively discoverable truth about a person.
69. **N069 — Multi-Protagonist Ending Matrix.** Allow different characters to occupy different outcome quadrants; avoid requiring one universal ending label.
70. **N070 — Ending Valence Independence.** Represent hope, dread, irony, moral cost, justice, closure, and audience feeling separately from want/need status.

### Ghost, Lie, Truth & Choice — new from notes (71–80)

71. **N071 — Character Ghost With Causal Evidence.** Represent formative wounds, betrayals, losses, and experiences as possible causes of present defenses without assuming all behavior arises from trauma. [Notes pp.5–7]
72. **N072 — Misbelief or Lie Representation.** State the distorted rule a character treats as true and how it predicts their choices. [Notes pp.7–9]
73. **N073 — Truth Counterposition Registry.** Record competing values or perspectives that challenge the lie; do not declare one interpretation morally absolute by automation.
74. **N074 — Valued-Good Inventory.** Identify something meaningful the character already possesses but undervalues, especially when a negative arc endangers it. [Notes pp.7–9]
75. **N075 — Characteristic Moment Plant.** Plant a telling early behavior that demonstrates temperament, capability, contradiction, or vulnerability. [Notes pp.3–4]
76. **N076 — Foreshadowed Potential Test.** A corruption, redemption, or major reversal should be causally legible from early evidence without becoming predictable. [Notes pp.3–4]
77. **N077 — Crisis of Belief Engine.** Track the moment a character's action collides with the belief that guided earlier actions.
78. **N078 — Revelation Versus Transformation Distinction.** A character recognizing a truth is not evidence of lasting change; require later behavioral consequence.
79. **N079 — Choice-as-Proof Rule.** Evaluate whether the climactic decision demonstrates adoption, rejection, or ambiguity of a belief instead of relying only on dialogue.
80. **N080 — Truth-Rejection Escalation.** In negative arcs, track each credible opportunity to change and the character's chosen refusal, with accumulating harm. [Notes pp.7–9]

### Character Arc Families & Dynamics — new from notes (81–90)

81. **N081 — Positive Change Arc Specification.** Model flaw/defense, catalytic pressure, competing truth, costly actions, new behavior, and its consequences. [Notes pp.5–7]
82. **N082 — Flat Arc Specification.** Allow the protagonist's core conviction to remain stable while their influence transforms other characters or the environment. [Notes p.2]
83. **N083 — Corruption Arc Specification.** Distinguish gradual embrace of morally destructive choices from sudden arbitrary villainy. [Notes pp.3–5]
84. **N084 — Fall Arc Specification.** Track the repeated failure to confront a central misconception and the good that is progressively sacrificed. [Notes pp.7–9]
85. **N085 — Disillusionment and Open Arc Support.** Represent arcs ending in wiser pessimism, unchanged belief, unresolved identity, or deliberate anti-transformation.
86. **N086 — Arc-Type Versus Ending-Type Independence.** Never infer positive/flat/negative trajectory solely from sweet/semi-sweet/bitter outcome, or vice versa.
87. **N087 — Impact Character Graph.** Track the character whose value, choices, example, or confrontation pressures the protagonist to reconsider. [Notes p.6]
88. **N088 — Truth-Bearer and Lie-Bearer Roles.** Represent people who embody competing models of a meaningful life without flattening them into moral instruction devices. [Notes pp.8–9]
89. **N089 — Transformation of Secondary Characters.** For flat protagonists, explicitly test whether meaningful change occurs in supporting people or institutions. [Notes p.2]
90. **N090 — Character Agency Across Arc.** Every major arc transition must identify what the character chose, resisted, or suffered; distinguish forced change from chosen change.

### Arc Causality, Midpoints & Reversals — new from notes (91–100)

91. **N091 — Page-One Ending Seed.** Trace the eventual outcome to early desire, belief, flaw, resource, promise, or conflict, rather than retrofitting a finale. [Notes p.2]
92. **N092 — Catalyst and First Threshold.** Record the event that makes the established want harder, reveals a new want, or forces commitment.
93. **N093 — Midpoint Revaluation.** Support mid-story reinterpretation of the want, the lie, relationships, identity, or the nature of victory without hard-coding a 50% timestamp. [Notes pp.7–8]
94. **N094 — Want Replacement Causal Chain.** Verify that a new central goal grows from events and does not erase the significance of the original goal. [Notes pp.2,4,6]
95. **N095 — Incremental Moral Thresholds.** Show small choices making larger choices increasingly plausible, particularly in corruption arcs. [Notes pp.3–5]
96. **N096 — Genuine Alternatives Before Sacrifice.** A final sacrifice matters more if the easier or desired alternative was genuinely attainable at a cost.
97. **N097 — Minor Defeat and Reversal Chain.** Make positive endings earned through real resistance, loss, recovery, and altered tactics rather than effortless reward. [Notes pp.2–3]
98. **N098 — Character's Shadow Cost Accounting.** Track whose needs, safety, relationships, or possibilities are harmed by pursuit of the protagonist's desire. [Notes pp.3–5,7–9]
99. **N099 — Turning-Point Counterfactual.** Ask whether removing a stated turning point changes later decisions; if not, the claimed turning point may be decorative.
100. **N100 — Final State Versus Starting State Diff.** Produce an evidence-linked comparison of the character's beliefs, relationships, conduct, wants, and losses at opening and closing scenes. [Notes pp.7–9]

### Finale, Catharsis & Reader Experience — new from notes (101–110)

101. **N101 — Earned Sweet Ending Test.** Require meaningful adversity, loss risk, and causally earned reconciliation before allowing both goal and need to be satisfied. [Notes pp.2–3]
102. **N102 — Semi-Sweet Renunciation Test.** Verify that loss or sacrifice of a want materially expresses fulfilled inner need, rather than random deprivation. [Notes pp.5–7]
103. **N103 — Bittersweet External Victory Test.** Distinguish visible external success from interior emptiness, broken relationships, or moral defeat. [Notes pp.7–9]
104. **N104 — Bitter Ending Integrity.** Make loss of both want and need causally connected to decisions or constraints, not imposed for artificial bleakness. [Notes pp.3–5]
105. **N105 — Tragic Satisfaction Paradox.** Allow readers to feel triumph, sympathy, dread, or admiration even when the protagonist's moral and personal trajectory is devastating. [Notes pp.3–5]
106. **N106 — Catharsis Through Consequence.** Ground emotional release in irreversible action, changed relationship, recognition, or loss rather than declarative speeches. [Notes pp.1,5–7]
107. **N107 — Ending Irony Composer.** Support outcomes where attaining the stated instrument destroys the underlying value, such as connection versus status. [Notes pp.8–9]
108. **N108 — Ending Echo With Difference.** Return to an opening object, choice, gesture, relationship, or claim whose meaning has changed by the finale.
109. **N109 — Last-Scene Character Proof.** Use observed conduct and changed circumstances to demonstrate final arc state without narrator explanation. [Notes pp.7–9]
110. **N110 — Reader Response Versus Author Intent.** Measure readers' perceived satisfaction/ambiguity separately from the writer's intended arc or ending quadrant.

### V8 Compiler, Testing & Governance — new requirements (111–120)

111. **N111 — Canonical Arc Nodes, Not a Second Database.** Extend existing `fictional_canon` and storyworld graph semantics with `narrative.want`, `narrative.need`, `narrative.belief`, `narrative.ghost`, `narrative.arc_turn`, and `narrative.ending` as typed nodes or compatible extension fields.
112. **N112 — State-Time-Aware Arc Transitions.** Attach `valid_from`, `valid_until`, `known_at`, provenance, character, and causing scene/event to changes in desire and belief; preserve decision-time meaning.
113. **N113 — Two-Layer Tests: Deterministic and Interpretive.** Test IDs, continuity, dependencies, transitions, and matrix projections deterministically; send psychological credibility and catharsis to qualified review.
114. **N114 — Fiction-Safe Proof Vocabulary.** State `consistent_with_canon`, `author_asserted`, `reviewer_inferred`, `reader_reported`, or `unverified`; never call aesthetic excellence machine-proven.
115. **N115 — Adversarial Fiction Benchmark Set.** Test flat arcs, positive and negative arcs, partial outcomes, changed wants, multi-protagonist conflicts, anti-formula stories, and deceptively polished but emotionally hollow endings.
116. **N116 — Negative Controls Against Template Tyranny.** The system must not automatically fail intentional nonlinear arcs, tragedy, unchanged protagonists, ambiguous endings, or endings without a single revelation.
117. **N117 — Source Provenance & Fair-Use Discipline.** Preserve origins and rights status for the notes' film examples and named theorist; create new explanatory wording and original test fiction rather than reproducing protected scripts.
118. **N118 — Writer Override With Rationale.** Permit author-authorized deviations from recommended craft patterns without silently altering canonical facts; preserve reasons, scope, and version history.
119. **N119 — Independent Reader Calibration.** Compare automated findings with blinded human readers, including false-positive/false-negative findings and variance by genre and audience.
120. **N120 — Receipt-Governed v8 Release.** Freeze a versioned program/manifest, enumerate actual executable checks, run negative and regression tests, preserve v4–v7 behavior, and forbid `shipped` without inspectable command/result/readback receipt.

## Architectural placement: extend, do not fork

| Canonical path                                         | v8 change                                                                                               | Status in observed repository                               |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| `references/genre_packs/fiction.md`                    | Wants/needs, ending types, non-formula exceptions, character humanity                                   | Existing doctrine; extend                                   |
| `references/genre_packs/dialogue.md`                   | Dialogue as evidence of belief, changed relationships and chosen sacrifice                              | Existing doctrine; extend                                   |
| `references/compiler/character_role_archetypes.md`     | Separate narrative job from independent psychological agency                                            | Existing doctrine; amend                                    |
| `references/compiler/narrative_intelligence_engine.md` | Project time-aware arc state and ending outcome from canonical state                                    | Existing concept; extend                                    |
| `references/v5/STORYWORLD_OS.md`                       | Add arc/ending typed states and event-linked changes to *existing* graph                                | Character state largely specified; do not claim implemented |
| `references/v5/AUTHORSHIP_GRAPH.md`                    | New typed narrative edges for motivates, contradicts, pressures, renounces, transforms, costs, resolves | Extend canonical graph model                                |
| `references/positive_patterns/tension_mechanics.md`    | Preserve patterns as optional templates rather than universal percentage gates                          | Existing rigid eight-phase doctrine; revise                 |
| `references/compiler/chapter_construction.md`          | Turning-point evidence, desire reversals, escalating costs                                              | Existing doctrine; extend                                   |
| `references/anti_patterns/cadence_expanded.md`         | Novel-scale simile/fragment/semantic-refrain audits                                                     | Existing cadence rules; extend                              |
| `references/diagnostics/scorecard.md`                  | Split character arc, plot causality, reader response and print readiness                                | Existing general scoring; extend                            |
| `references/v8/`                                       | Versioned proposal, migration design, risk register, acceptance matrix                                  | New folder, after explicit versioning decision              |
| `schemas/v8/`                                          | Typed arc and ending extension schemas; backward compatible                                             | New proposed schemas                                        |
| `benchmarks/cases/` and `tests/v8/`                    | Deterministic and human-calibrated evaluation cases                                                     | Extend existing test system                                 |
| `plans/v8.manifest.yaml` + `plans/receipts/`           | Workstream graph and shipped-state proof                                                                | New versioned program with current receipt conventions      |

## Minimal proposed semantic representation

Illustrative only, **not an existing executable schema**:

```
character_arc:
  id: arc-imani-01
  realm: fictional_canon
  character_ref: ch-imani
  valid_from_event: event-opening
  arc_family: positive_change # positive_change | flat | corruption | fall | open | custom
  conscious_wants:
    - id: want-01
      proposition: 'Retain custody of her own lived history'
      state: pursued
      introduced_at: event-opening
  needs:
    - id: need-01
      proposition: 'Author interpretation of the character’s internal requirement'
      epistemic_status: author_asserted
      recognition_state: unrecognized
  beliefs:
    - id: belief-01
      statement: 'A testable belief that drives choices'
      status: held
  ghost_refs: []
  impact_character_refs: []
  turning_points: []
  final_choice_ref: null
  ending:
    want_outcome: unresolved # attained|partial|renounced|sacrificed|thwarted|unresolved|n_a
    need_outcome: unresolved # fulfilled|partial|rejected|unresolved|n_a
    outcome_quadrant: null # derived only when unambiguous and binary
    reader_valence: null # independent human-feedback field
    closure: open
```

The example names and propositions are placeholders for schema design and must not be treated as certified *Aperture I* canon. The `ending` classifier must not invent answers to unknown fields; it should return `not_classifiable` with reasons.

## Sample falsifiable v8 acceptance tests

| Test                                                                 | Expected result / negative control                                                     |
| -------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Stable-belief protagonist changes the community                      | Valid flat arc; no missing 'personal transformation' failure                           |
| Protagonist gains wealth but destroys a valued relationship          | Externally attained want and unmet need remain distinct; possible bittersweet quadrant |
| Protagonist gives up an available prize to protect another character | Renunciation and fulfilling need linked through witnessed final action                 |
| Protagonist says 'I changed' but never behaves differently           | Transformation marked unverified/review-needed                                         |
| Protagonist changes objective mid-book                               | Old want remains historically queryable; new want begins at its own event              |
| Ending has ambiguous psychological resolution                        | No forced sweet/bitter label; ambiguity retained                                       |
| Two POV characters have opposed outcomes                             | Separate ending projections; no fabricated book-wide singular outcome                  |
| Alleged corruption turn has no earlier planted potential             | Review finding naming missing setup; no ungrounded certainty of defect                 |
| Character violates world rule to rescue someone                      | Causal cost and affected rule flagged; not automatically treated as continuity error   |
| Strong literary scene intentionally lacks eight fixed suspense beats | Valid exception; diagnostic reports intended structure rather than automatic fail      |
| Added finale severs earlier foreshadowing dependency                 | Impact walk flags orphaned payoff; existing canonical source remains authoritative     |
| Output 'excellent ending' without reader evidence                    | Unsupported outcome claim refused or explicitly labeled subjective assessment          |
| Regressions on v4-v7 test suites                                     | All previously executable behavior remains passing                                     |
| Release reports a specified-only capability as shipped               | Fail receipt/status audit                                                              |

## Proposed implementation waves (dependency-aware; all PROPOSED)

| Wave   | Deliverable                                                                                | Gate                                                                       |
| ------ | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| WI8-00 | Baseline capture, owner paths, repo commit pin, version RFC, negative controls             | Reproducible repo state and recorded current capabilities                  |
| WI8-01 | Narrative semantic type system: wants, needs, belief, ghost, choice, arc, ending           | Typed schemas; no second canonical store                                   |
| WI8-02 | Event-time transitions and character-state projections                                     | Changed desires and beliefs reconstructable before/after event             |
| WI8-03 | Want/need quadrant derived view with partial/unknown/multiprotagonist support              | Negative tests protect ambiguity and alternative arcs                      |
| WI8-04 | Arc families: positive, flat, corruption, fall, custom and open                            | Causally grounded fixture tests across all families                        |
| WI8-05 | Impact character, lie/truth and relationship transition graph                              | Character-level causal evidence; no 'character as function' replacement    |
| WI8-06 | Finale, catharsis, sacrifice and irony structural reviewer                                 | Notes-driven case suite and human-review limitations explicit              |
| WI8-07 | Integrate prior 60 prose, suspense, world-rule and editorial requirements                  | Corpus findings with source spans and opt-in edits                         |
| WI8-08 | Reader-experience research protocols and calibration                                       | Review instruments and measured disagreement across reviewers              |
| WI8-09 | Author-controlled editing workflow, approvals, and canonical impact preview                | Change simulations before commits; reject unauthorized replacements        |
| WI8-10 | Publication preflight, author-rights and transmedia/canon regression                       | Multi-format and versioned source checks                                   |
| WI8-11 | Release audit: complete benchmarks, regression, negative controls and independent readback | Every shipped wave has receipt; unimplemented items remain visibly planned |

## Non-negotiable invariants

1. **Fiction remains fiction:** canon is author-governed; creative claims must never be silently represented as external scientific facts.
2. **A rubric is not a law of nature:** deliberate deviations are permitted, explainable, and may outperform standard patterns.
3. **Do not treat characters as vectors with one scalar score:** authorial interpretation, text evidence, and reader responses are distinct.
4. **No canon rewrite by convenience:** modifying wants, needs, or arc claims must show impacted scenes, payoffs and series works.
5. **No false maturity claims:** specified != coded != tested != deployed != demonstrated with readers.
6. **Preserve provenance:** give appropriate credit for analytical frameworks drawn from other creators; write fresh test stories; assess rights before reproducing film dialogue or scripts.
7. **No aesthetic automation supremacy:** deterministic checks catch structural conditions; literary excellence needs qualified human judgment and reader observation.
8. **No invisible editorial damage:** report every suggested cut, replaced line, and semantic effect before accepting edits.

## Source notes map

- **PDF page 1:** conscious wants, latent needs, four-quadrant ending diagram.
- **PDF page 2:** a finale begins at page one; flat arcs and evolving wants in *Back to the Future*; earned sweet endings.
- **PDF pages 3–5:** bitter endings, early corruption potential, morally consequential decisions and sacrifices in examples discussing *The Godfather* and *Joker*.
- **PDF pages 5–7:** semi-sweet and positive-change arcs; character ghost, impact character, rejection of early material aims in examples discussing *Onward* and *Rain Man*.
- **PDF pages 7–9:** negative/fall arc, lie, truth, undervalued good, midpoint, lie-based actions, cost to relationships, ending irony in notes discussing *The Social Network*.

### Caveat on film evidence

Examples and screenplay page claims are transcribed as the user's notes' interpretations. Film versions, scripts, drafts and page numbering may differ, and the judgments themselves are contestable; v8 must not encode any such interpretation as objectively proven or reproduce long protected screenplay passages.

**Status:** specification delivered as a proposal, not code, not verified reader outcome, and not a v8 release.

## v9 preview note (added after the original specification)

*Preview (PR #8); proposed, not a release. v8.0.0 is the published version.* The text above is the v8 proposal as delivered and is kept as history. v9 does not alter any of its 120 requirements or its caveats. For fiction, v9 changes no gate; it adds the no-borrowed-memory rule for memoir and autofiction, treats the phrase scanner as an editorial question (quoted dialogue is character voice), and keeps authorship a self-reported declaration. See `docs/FICTION_V8_ARCHITECTURE.md` (v9 section) and `references/v9/README.md`.
