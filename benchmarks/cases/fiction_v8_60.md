# 60 rule-specific editorial regression vectors

**Status: unexecuted editorial cases.** These positive and negative examples are concept-level falsification vectors from the attached specification; they are not 60 machine-positive tests and must not be claimed as such.

A future author/evaluator should generate real manuscript passages for each pair, blind the labels, independently annotate outcome and register agreement/disagreement without changing literary criteria after seeing the result.

## FI-01 — Metaphor Saturation Governor

**Positive candidate:** Three metaphors across a 2,000-word scene; each changes what the narrator notices.

**Negative candidate:** Seven unrelated similes in a single short paragraph restate the same dread.

**Acceptance:** Positive: Three metaphors across a 2,000-word scene; each changes what the narrator notices. Negative: Seven unrelated similes in a single short paragraph restate the same dread. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `text.figuration_density`; class `heuristic`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/anti_patterns/cadence_expanded.md`.

## FI-02 — Figurative Language Value Test

**Positive candidate:** Comparison reveals that the supposedly harmless machine is operated by the child's father.

**Negative candidate:** The room was cold, like a cold room.

**Acceptance:** Positive: Comparison reveals that the supposedly harmless machine is operated by the child's father. Negative: The room was cold, like a cold room. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/anti_patterns/cadence_expanded.md`.

## FI-03 — Manuscript-Wide Repetition Detection

**Positive candidate:** A repeated phrase changes meaning at the closing scene.

**Negative candidate:** The same 'as if' opener appears in 12 chapters without narrative purpose.

**Acceptance:** Positive: A repeated phrase changes meaning at the closing scene. Negative: The same 'as if' opener appears in 12 chapters without narrative purpose. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `text.repeated_phrases`; class `heuristic`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/compiler/continuity.md`.

## FI-04 — Metaphor Family Registry

**Positive candidate:** The clock motif changes from comfort to warning to debt.

**Negative candidate:** Four clock similes mean only urgency.

**Acceptance:** Positive: The clock motif changes from comfort to warning to debt. Negative: Four clock similes mean only urgency. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.motif_recurrence`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/compiler/continuity.md`.

## FI-05 — Plain Prose Counterweight

**Positive candidate:** A plain inventory sentence gives relief after an intense confession.

**Negative candidate:** Every sentence attempts an aphorism; scenes have no neutral register.

**Acceptance:** Positive: A plain inventory sentence gives relief after an intense confession. Negative: Every sentence attempts an aphorism; scenes have no neutral register. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/anti_patterns/cadence_expanded.md`.

## FI-06 — Narrative Overexplanation Detector

**Positive candidate:** He leaves the ring and locks the door; narration lets the reader infer rejection.

**Negative candidate:** He leaves the ring; narration explains in three sentences that this means rejection.

**Acceptance:** Positive: He leaves the ring and locks the door; narration lets the reader infer rejection. Negative: He leaves the ring; narration explains in three sentences that this means rejection. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/anti_patterns/cadence_expanded.md`.

## FI-07 — Emotional Declaration Restraint

**Positive candidate:** She hides her shaking hand behind the ledger.

**Negative candidate:** She is scared, terrified, frightened and deeply afraid.

**Acceptance:** Positive: She hides her shaking hand behind the ledger. Negative: She is scared, terrified, frightened and deeply afraid. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/anti_patterns/cadence_expanded.md`.

## FI-08 — Sentence-Rhythm Diversity Audit

**Positive candidate:** An action sequence compresses, then opens into long aftermath syntax.

**Negative candidate:** Six chapters use the same seven-word fragment cadence.

**Acceptance:** Positive: An action sequence compresses, then opens into long aftermath syntax. Negative: Six chapters use the same seven-word fragment cadence. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `text.rhythm`; class `heuristic`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/anti_patterns/cadence_expanded.md`.

## FI-09 — Authorial Intrusion Detector

**Positive candidate:** Narrator remains inside the character's available perceptions.

**Negative candidate:** The narrator declares: 'This was the moment the novel became unforgettable.'

**Acceptance:** Positive: Narrator remains inside the character's available perceptions. Negative: The narrator declares: 'This was the moment the novel became unforgettable.' An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `text.authorial_intrusion`; class `heuristic`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/anti_patterns/cadence_expanded.md`.

## FI-10 — Sensory Progression Engine

**Positive candidate:** The tapping sound first comforts, then identifies an intruder.

**Negative candidate:** Metallic tapping is used ten times only to mean anxiety.

**Acceptance:** Positive: The tapping sound first comforts, then identifies an intruder. Negative: Metallic tapping is used ten times only to mean anxiety. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/anti_patterns/cadence_expanded.md`.

## FI-11 — Descriptive Compression Operator

**Positive candidate:** Three sharp details establish power and room geometry.

**Negative candidate:** A twelve-line furniture list changes neither space nor character.

**Acceptance:** Positive: Three sharp details establish power and room geometry. Negative: A twelve-line furniture list changes neither space nor character. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/anti_patterns/cadence_expanded.md`.

## FI-12 — Prose Preservation Rule

**Positive candidate:** Proposed edit preserves a recurring character-specific metaphor and supplies comparative rationale.

**Negative candidate:** Autorewriter deletes every figurative sentence to hit an arbitrary count.

**Acceptance:** Positive: Proposed edit preserves a recurring character-specific metaphor and supplies comparative rationale. Negative: Autorewriter deletes every figurative sentence to hit an arbitrary count. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/fiction.md`.

## FI-13 — Escalation Novelty Law

**Positive candidate:** The second threat removes evacuation, changing the available choices.

**Negative candidate:** A second identical alarm raises volume but changes no knowledge or options.

**Acceptance:** Positive: The second threat removes evacuation, changing the available choices. Negative: A second identical alarm raises volume but changes no knowledge or options. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.escalation_novelty`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/thriller_scene_architecture.md`.

## FI-14 — Tension Plateau Detector

**Positive candidate:** At stable dread, a scene changes political power and reader knowledge.

**Negative candidate:** Four adjacent scenes have equal dread and no state delta.

**Acceptance:** Positive: At stable dread, a scene changes political power and reader knowledge. Negative: Four adjacent scenes have equal dread and no state delta. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.tension_plateau`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/thriller_scene_architecture.md`.

## FI-15 — Threat Consequence Requirement

**Positive candidate:** Early sabotage injures a trusted courier, proving the threat's capability.

**Negative candidate:** A supposedly deadly system issues threats for 200 pages with no demonstrated consequence.

**Acceptance:** Positive: Early sabotage injures a trusted courier, proving the threat's capability. Negative: A supposedly deadly system issues threats for 200 pages with no demonstrated consequence. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.threat_consequence`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/thriller_scene_architecture.md`.

## FI-16 — Threat Specificity Test

**Positive candidate:** Danger's reach is shown before its origin is revealed.

**Negative candidate:** Narrator withholds both the mechanism and what anyone fears.

**Acceptance:** Positive: Danger's reach is shown before its origin is revealed. Negative: Narrator withholds both the mechanism and what anyone fears. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/thriller_scene_architecture.md`.

## FI-17 — Suspense Information-Asymmetry Engine

**Positive candidate:** Reader knows the guard was bribed; protagonist still trusts him.

**Negative candidate:** Character inexplicably knows the guard was bribed without receiving the clue.

**Acceptance:** Positive: Reader knows the guard was bribed; protagonist still trusts him. Negative: Character inexplicably knows the guard was bribed without receiving the clue. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/compiler/novel_architecture.md`.

## FI-18 — Earned Mystery Doctrine

**Positive candidate:** Reader understands the mystery question while the answer remains hidden.

**Negative candidate:** Missing subject, location and causal question make every scene incomprehensible.

**Acceptance:** Positive: Reader understands the mystery question while the answer remains hidden. Negative: Missing subject, location and causal question make every scene incomprehensible. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/thriller_scene_architecture.md`.

## FI-19 — Mystery Debt Ledger

**Positive candidate:** Three raised mysteries close; one series thread is explicitly deferred with a concrete reason.

**Negative candidate:** Twelve major mysteries are opened and none receives a payoff.

**Acceptance:** Positive: Three raised mysteries close; one series thread is explicitly deferred with a concrete reason. Negative: Twelve major mysteries are opened and none receives a payoff. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.mystery_debt`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/compiler/novel_architecture.md`.

## FI-20 — Failure-Driven Escalation

**Positive candidate:** Attempt to bypass security permanently exposes a witness.

**Negative candidate:** Character attempts have no effect; surprise disasters arrive arbitrarily.

**Acceptance:** Positive: Attempt to bypass security permanently exposes a witness. Negative: Character attempts have no effect; surprise disasters arrive arbitrarily. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/thriller_scene_architecture.md`.

## FI-21 — Antagonist Competence Standard

**Positive candidate:** Antagonist alters strategy after a failed trap and pays for a surveillance gap.

**Negative candidate:** A capable antagonist forgets the one defense shown in the prior chapter.

**Acceptance:** Positive: Antagonist alters strategy after a failed trap and pays for a surveillance gap. Negative: A capable antagonist forgets the one defense shown in the prior chapter. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/thriller_scene_architecture.md`.

## FI-22 — Escalation Variety Requirement

**Positive candidate:** Moral jeopardy follows financial jeopardy, then shifts to an intimate betrayal.

**Negative candidate:** Eight scenes repeatedly threaten physical injury without other pressure.

**Acceptance:** Positive: Moral jeopardy follows financial jeopardy, then shifts to an intimate betrayal. Negative: Eight scenes repeatedly threaten physical injury without other pressure. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.pressure_variety`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/thriller_scene_architecture.md`.

## FI-23 — Tension Recovery Discipline

**Positive candidate:** After the explosion, characters share an unguarded joke that changes their bond.

**Negative candidate:** Tension stays at five throughout, with no true release.

**Acceptance:** Positive: After the explosion, characters share an unguarded joke that changes their bond. Negative: Tension stays at five throughout, with no true release. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.recovery`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/thriller_scene_architecture.md`.

## FI-24 — Chapter-Ending Integrity

**Positive candidate:** Chapter closes on a decision that creates a new obligation.

**Negative candidate:** Narrator cuts mid-answer only to force a page turn.

**Acceptance:** Positive: Chapter closes on a decision that creates a new obligation. Negative: Narrator cuts mid-answer only to force a page turn. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/thriller_scene_architecture.md`.

## FI-25 — Human Before Function Law

**Positive candidate:** The analyst wants to reconcile with her daughter and harbors a damaging secret.

**Negative candidate:** The analyst's only traits are technical competence and plot function.

**Acceptance:** Positive: The analyst wants to reconcile with her daughter and harbors a damaging secret. Negative: The analyst's only traits are technical competence and plot function. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.character_humanity`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/fiction.md`.

## FI-26 — Personal Desire Conflict Engine

**Positive candidate:** Pilot wants recognition but duty requires confessing a mistake.

**Negative candidate:** Everyone desires only to complete the mission.

**Acceptance:** Positive: Pilot wants recognition but duty requires confessing a mistake. Negative: Everyone desires only to complete the mission. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.desire_conflict`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/fiction.md`.

## FI-27 — Costly Rule Violation Test

**Positive candidate:** Doctor risks a license to save a stranger and must face proceedings.

**Negative candidate:** Hero violates every rule with no consequence or reason.

**Acceptance:** Positive: Doctor risks a license to save a stranger and must face proceedings. Negative: Hero violates every rule with no consequence or reason. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/fiction.md`.

## FI-28 — Distinct Character Decision Profiles

**Positive candidate:** Two trained officers make different costly decisions under the same risk.

**Negative candidate:** Everyone chooses the same plan and differs only in catchphrases.

**Acceptance:** Positive: Two trained officers make different costly decisions under the same risk. Negative: Everyone chooses the same plan and differs only in catchphrases. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/dialogue.md`.

## FI-29 — Relationship Evolution Ledger

**Positive candidate:** Trust falls after betrayal and recovers only after demonstrated sacrifice.

**Negative candidate:** A betrayal is followed by immediate unexplained intimacy.

**Acceptance:** Positive: Trust falls after betrayal and recovers only after demonstrated sacrifice. Negative: A betrayal is followed by immediate unexplained intimacy. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.relationship_evolution`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/compiler/novel_architecture.md`.

## FI-30 — Emotional Memory Continuity

**Positive candidate:** Survivor's sleep and choices change after the fire.

**Negative candidate:** Character witnesses a death and jokes normally next chapter without residue.

**Acceptance:** Positive: Survivor's sleep and choices change after the fire. Negative: Character witnesses a death and jokes normally next chapter without residue. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.emotional_memory`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/fiction.md`.

## FI-31 — Human Stakes Translation

**Positive candidate:** Citywide network outage prevents mother reaching her missing son.

**Negative candidate:** Threat to the world is explained only by abstract statistics.

**Acceptance:** Positive: Citywide network outage prevents mother reaching her missing son. Negative: Threat to the world is explained only by abstract statistics. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/fiction.md`.

## FI-32 — Character Agency Verification

**Positive candidate:** Protagonist chooses exposure over safety, creating the climax.

**Negative candidate:** Victory occurs because of an accidental external reset.

**Acceptance:** Positive: Protagonist chooses exposure over safety, creating the climax. Negative: Victory occurs because of an accidental external reset. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.character_agency`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/fiction.md`.

## FI-33 — Competence Without Emotional Uniformity

**Positive candidate:** Brilliant analyst makes a shame-driven mistake yet remains competent.

**Negative candidate:** Experts behave like identical emotionally neutral calculators.

**Acceptance:** Positive: Brilliant analyst makes a shame-driven mistake yet remains competent. Negative: Experts behave like identical emotionally neutral calculators. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/fiction.md`.

## FI-34 — Emotional Payoff Audit

**Positive candidate:** After reunification, character grieves what was irreversibly lost.

**Negative candidate:** Beloved character dies and the story treats it as resolved paperwork.

**Acceptance:** Positive: After reunification, character grieves what was irreversibly lost. Negative: Beloved character dies and the story treats it as resolved paperwork. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/genre_packs/fiction.md`.

## FI-35 — World Rules Constitution

**Positive candidate:** The device has stable input, output, cost, and forbidden operations.

**Negative candidate:** Power acquires abilities without constraints as needed.

**Acceptance:** Positive: The device has stable input, output, cost, and forbidden operations. Negative: Power acquires abilities without constraints as needed. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.world_rules`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/v5/STORYWORLD_OS.md`.

## FI-36 — Power Boundary Enforcement

**Positive candidate:** Enemy's forbidden remote action is refused, forcing a physical incursion.

**Negative candidate:** Enemy uses an expressly forbidden remote attack without a retcon.

**Acceptance:** Positive: Enemy's forbidden remote action is refused, forcing a physical incursion. Negative: Enemy uses an expressly forbidden remote attack without a retcon. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.power_boundary`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/v5/STORYWORLD_OS.md`.

## FI-37 — Cost Conservation Doctrine

**Positive candidate:** Each resurrection drains a finite shared memory reserve.

**Negative candidate:** The reserve refills at chapter end for no reason.

**Acceptance:** Positive: Each resurrection drains a finite shared memory reserve. Negative: The reserve refills at chapter end for no reason. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.cost_conservation`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/v5/STORYWORLD_OS.md`.

## FI-38 — Victory Versus Closure Distinction

**Positive candidate:** Extraction succeeds but causes political and moral damage.

**Negative candidate:** Narration labels operational success as total ethical closure.

**Acceptance:** Positive: Extraction succeeds but causes political and moral damage. Negative: Narration labels operational success as total ethical closure. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/v5/STORYWORLD_OS.md`.

## FI-39 — Consent and Authority Conflict Model

**Positive candidate:** Operator can activate device, lacks authority, obtains affected person's consent.

**Negative candidate:** Technological capability is treated as automatic moral permission.

**Acceptance:** Positive: Operator can activate device, lacks authority, obtains affected person's consent. Negative: Technological capability is treated as automatic moral permission. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/v5/STORYWORLD_OS.md`.

## FI-40 — Timeline Perspective Registry

**Positive candidate:** Flashback marks event time separately from the diary's creation date.

**Negative candidate:** A diary written before an event contains details no witness could yet know.

**Acceptance:** Positive: Flashback marks event time separately from the diary's creation date. Negative: A diary written before an event contains details no witness could yet know. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.timeline`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/compiler/fiction_rule_integrity.md`.

## FI-41 — Canon Contradiction Classification

**Positive candidate:** Unreliable account is tagged as disputed, not normalized into canon.

**Negative candidate:** Two opposing facts silently coexist as simultaneously canonical.

**Acceptance:** Positive: Unreliable account is tagged as disputed, not normalized into canon. Negative: Two opposing facts silently coexist as simultaneously canonical. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/compiler/fiction_rule_integrity.md`.

## FI-42 — Speculative Mechanism Demonstration

**Positive candidate:** A rule is demonstrated via its cost during a failed escape.

**Negative candidate:** Mechanism appears only in a long lecture without consequences.

**Acceptance:** Positive: A rule is demonstrated via its cost during a failed escape. Negative: Mechanism appears only in a long lecture without consequences. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.mechanism_demonstration`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/v5/STORYWORLD_OS.md`.

## FI-43 — Scientific Claim Boundary

**Positive candidate:** Faster-than-light gate labeled as invented mechanism.

**Negative candidate:** Fictional claim is stated as confirmed physics.

**Acceptance:** Positive: Faster-than-light gate labeled as invented mechanism. Negative: Fictional claim is stated as confirmed physics. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/compiler/fiction_rule_integrity.md`.

## FI-44 — Worldbuilding Restraint

**Positive candidate:** An invented agency alters protagonist's legal and personal options.

**Negative candidate:** Seven agencies are named but none affects action or meaning.

**Acceptance:** Positive: An invented agency alters protagonist's legal and personal options. Negative: Seven agencies are named but none affects action or meaning. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/v5/STORYWORLD_OS.md`.

## FI-45 — Novel-Length Escalation Graph

**Positive candidate:** Midpoint changes power, information and future risks despite a quiet chapter.

**Negative candidate:** Three acts repeat identical stakes, objectives and options.

**Acceptance:** Positive: Midpoint changes power, information and future risks despite a quiet chapter. Negative: Three acts repeat identical stakes, objectives and options. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.escalation_graph`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/compiler/novel_architecture.md`.

## FI-46 — Act-to-Act Transformation Test

**Positive candidate:** Act break makes the protagonist abandon rescue for exposure.

**Negative candidate:** Act breaks change setting only, no options or knowledge.

**Acceptance:** Positive: Act break makes the protagonist abandon rescue for exposure. Negative: Act breaks change setting only, no options or knowledge. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.act_transform`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/compiler/narrative_intelligence_engine.md`.

## FI-47 — Third-Act Acceleration Audit

**Positive candidate:** After victory, legal proceedings reveal a new irreparable cost.

**Negative candidate:** Six concluding scenes repeat that the day was saved.

**Acceptance:** Positive: After victory, legal proceedings reveal a new irreparable cost. Negative: Six concluding scenes repeat that the day was saved. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/compiler/novel_architecture.md`.

## FI-48 — Opening Promise Verification

**Positive candidate:** Opening promise of saving the sibling receives a consequential answer.

**Negative candidate:** Opening asks who betrayed the sibling; closing never addresses it.

**Acceptance:** Positive: Opening promise of saving the sibling receives a consequential answer. Negative: Opening asks who betrayed the sibling; closing never addresses it. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.opening_promises`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/compiler/narrative_intelligence_engine.md`.

## FI-49 — Payoff Quality Engine

**Positive candidate:** A planted broken key later forces the traitor's confession.

**Negative candidate:** Key reappears as nostalgia but has no effect.

**Acceptance:** Positive: A planted broken key later forces the traitor's confession. Negative: Key reappears as nostalgia but has no effect. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.payoff`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/compiler/novel_architecture.md`.

## FI-50 — Ending Without Explanation Law

**Positive candidate:** Final consequence is dramatized in action and silence.

**Negative candidate:** Narrator writes that the ending will be remembered forever.

**Acceptance:** Positive: Final consequence is dramatized in action and silence. Negative: Narrator writes that the ending will be remembered forever. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/compiler/reader_experience.md`.

## FI-51 — Standalone Satisfaction / Series Continuation Test

**Positive candidate:** Primary case closes; a peripheral threat remains for the next book.

**Negative candidate:** Nothing central resolves because the sequel must sell.

**Acceptance:** Positive: Primary case closes; a peripheral threat remains for the next book. Negative: Nothing central resolves because the sequel must sell. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.central_resolution`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/compiler/narrative_intelligence_engine.md`.

## FI-52 — Emotional Center Protection

**Positive candidate:** Climax's technology decision also resolves a mother's loyalty conflict.

**Negative candidate:** Final 80 pages explain machines but forget core relationship.

**Acceptance:** Positive: Climax's technology decision also resolves a mother's loyalty conflict. Negative: Final 80 pages explain machines but forget core relationship. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/compiler/reader_experience.md`.

## FI-53 — Front Matter Separation

**Positive candidate:** Authorial manifesto moves outside the novel's in-world first scene.

**Negative candidate:** Promotional review quotes interrupt an unfolding rescue.

**Acceptance:** Positive: Authorial manifesto moves outside the novel's in-world first scene. Negative: Promotional review quotes interrupt an unfolding rescue. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/diagnostics/scorecard.md`.

## FI-54 — Document Placement Validator

**Positive candidate:** Glossary occurs in back matter with useful cross-references.

**Negative candidate:** Glossary interrupts the decisive confrontation.

**Acceptance:** Positive: Glossary occurs in back matter with useful cross-references. Negative: Glossary interrupts the decisive confrontation. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/diagnostics/scorecard.md`.

## FI-55 — Mathematical and Symbol Rendering Verification

**Positive candidate:** Typeset equation round-trips exactly in exported edition.

**Negative candidate:** Export shows raw '\alpha' and replacement character U+FFFD.

**Acceptance:** Positive: Typeset equation round-trips exactly in exported edition. Negative: Export shows raw '\alpha' and replacement character U+FFFD. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `text.raw_latex`; class `heuristic`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/diagnostics/scorecard.md`.

## FI-56 — Publishing Metadata Completeness

**Positive candidate:** Title, edition and publisher completed; ISBN marked not applicable for draft.

**Negative candidate:** Print release has 'INSERT ISBN' and missing edition.

**Acceptance:** Positive: Title, edition and publisher completed; ISBN marked not applicable for draft. Negative: Print release has 'INSERT ISBN' and missing edition. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `typed.metadata`; class `typed`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/diagnostics/scorecard.md`.

## FI-57 — Timeline and Cross-Book Reference Proofing

**Positive candidate:** Cross-book reference matches verified chapter and timeline anchors.

**Negative candidate:** Book two cites a scene dated years before a character's birth.

**Acceptance:** Positive: Cross-book reference matches verified chapter and timeline anchors. Negative: Book two cites a scene dated years before a character's birth. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/diagnostics/scorecard.md`.

## FI-58 — Typesetting and Pagination Audit

**Positive candidate:** EPUB reflow verified on multiple font sizes; print margins manually checked.

**Negative candidate:** PDF contains clipped notation and unreadable gutters.

**Acceptance:** Positive: EPUB reflow verified on multiple font sizes; print margins manually checked. Negative: PDF contains clipped notation and unreadable gutters. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `review.required`; class `editorial`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/diagnostics/scorecard.md`.

## FI-59 — Independent Reader Evaluation

**Positive candidate:** Consenting independent readers report confusion and attachment against scene anchors.

**Negative candidate:** Creator gives the book a ten based solely on model ratings.

**Acceptance:** Positive: Consenting independent readers report confusion and attachment against scene anchors. Negative: Creator gives the book a ten based solely on model ratings. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `process.reader_study`; class `process`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/compiler/reader_experience.md`.

## FI-60 — Genre-Specific Publication Gate

**Positive candidate:** Release names open artistic concerns, reader evidence, and format proofs.

**Negative candidate:** Publication-ready badge issued from grammar pass alone.

**Acceptance:** Positive: Release names open artistic concerns, reader evidence, and format proofs. Negative: Publication-ready badge issued from grammar pass alone. An evaluator must cite scene or text anchors; a raw score is insufficient.

**Expected mechanism:** `process.release`; class `process`; no inferred pass solely from absence of a signal.

**Canonical owner:** `references/diagnostics/scorecard.md`.
