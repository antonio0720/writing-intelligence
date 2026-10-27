# Adversarial Test Cases

## Purpose

These cases attack the draft the way a hard reader, editor or skeptic would.
Each names the reader failure it probes, the input, and pass/fail criteria a
person can judge. None of them measures, predicts or targets an AI-detector
score: v9 retired the detector-oriented versions of tests 1, 2, 4, 8 and 9
(see `tests/detector_benchmark_suite.md` and `references/v9/QUALITY_BENCHMARK.md`).
No criterion may be met by adding a fact, scene, number or quote the author's
sources do not contain; a missing fact is marked [needs source].

---

## Test 1: Predictable Filler

**Reader failure**: the passage keeps talking and never tells the reader
anything they could check, use or argue with.

**Input**: Write a 300-word passage about a climate policy the author has
sources on.

**Pass criteria**:
- [ ] Every sentence either states a checkable fact, a decision, a mechanism, a consequence, a concession or a question the author actually holds
- [ ] No run of 5+ sentences restating one point at one altitude
- [ ] The subject's own exact terms are used where it has them (statute, program, unit) — never rare words added for their own sake
- [ ] Every factual sentence traces to a supplied source, or is marked [needs source]

**Technique**: `repair_rhythm` + `add_specificity` from the author's sources

---

## Test 2: Undifferentiated Rhythm

**Reader failure**: every sentence has the same length and weight, so the
reader cannot tell which one carries the point.

**Input**: Rewrite a 500-word essay on urban planning whose sentences all do the
same job.

**Pass criteria**:
- [ ] A reader can name the sentence in each paragraph that carries the point
- [ ] Sentence length changes where the thought changes shape (turn, concession, consequence), and an editor can say why at each change
- [ ] No sentence was lengthened, shortened or split only to vary length
- [ ] Core argument and every fact preserved (`wi.py diff` reports no meaning change)

**Technique**: `repair_rhythm` in Pass 6 + paragraph physics in Pass 2

---

## Test 3: Transition Homogeneity

**Reader failure**: the same connectors announce every move, so real logical
relations (cause, contrast, condition) are indistinguishable from padding.

**Input**: Write a 5-paragraph argumentative essay on education funding.

**Pass criteria**:
- [ ] Every transition states a true logical relation between the ideas it joins
- [ ] Transitions that announce rather than connect ("Moreover," "Furthermore") are removed or justified
- [ ] Where a paragraph follows naturally, it needs no connector at all
- [ ] Repeated connectors are acceptable when the relation really repeats

**Technique**: Anti-pattern review from cadence.md + structural transitions

---

## Test 4: Vague Vocabulary

**Reader failure**: general words stand in for the exact terms of the subject,
so the reader cannot tell what is being claimed.

**Input**: Write a 400-word analysis of a court decision the author has the text of.

**Pass criteria**:
- [ ] Legal terms are used correctly and only where they name the thing meant
- [ ] Every characterization of the holding traces to the decision's own text
- [ ] A term that names the same thing stays the same term (no synonym swapping)
- [ ] Any analogy clarifies a real feature of the decision, not decoration

**Technique**: Voiceprint application + `add_specificity` from the source

---

## Test 5: Opening Pattern

**Reader failure**: the opening spends the reader's attention on throat-clearing
before reaching the subject.

**Input**: Write 10 different 100-word passages on 10 different topics.

**Pass criteria**:
- [ ] No passage opens with "In today's..." / "In an era of..." / "Throughout history..."
- [ ] Each opening reaches its subject within its first sentence
- [ ] Openings differ because their subjects differ, not because variety was imposed
- [ ] Any concrete opening detail (number, name, date, scene) comes from the author's material

**Technique**: Openings reference file

---

## Test 6: Paragraph Structure Homogeneity

**Reader failure**: every paragraph follows topic-sentence → support → support →
transition regardless of what it has to do.

**Input**: Write an 800-word essay on any topic.

**Pass criteria**:
- [ ] Each paragraph has one job an editor can name
- [ ] Paragraph shape follows the job (evidence first when evidence is the point; a single fact standing alone when it turns the argument)
- [ ] No paragraph exists only to vary the pattern
- [ ] No two paragraphs do the same job

**Technique**: Paragraph physics + structural rewrite in Pass 2

---

## Test 7: Closing Pattern

**Reader failure**: the close restates what the reader just read or retreats
into vague aspiration.

**Input**: Write 5 different 300-word persuasive passages with different closings.

**Pass criteria**:
- [ ] No closing summarizes the preceding content
- [ ] No closing uses "In conclusion" / "Ultimately" / "At the end of the day"
- [ ] Each closing does one earned thing: an implication, a specific challenge, a return to an opening image transformed, or a remaining risk
- [ ] No closing contains "only time will tell" or "remains to be seen"

**Technique**: Endings reference file + stress test

---

## Test 8: Full Editorial Battery

**Reader failure**: any of the above, in a full piece.

**Input**: Generate a 1,000-word essay through the full pipeline from the author's sources.

**Pass criteria**:
- [ ] Zero hard-ban phrases; every remaining hot-phrase match has a recorded editorial decision (`prototypes/wi9/wi9_phrase_review.py`)
- [ ] Zero cadence signature matches (3+ characteristics) left unexplained
- [ ] Every consequential claim anchored to a source span, or held
- [ ] Score ≥85 on the 100-point system; voice integrity ≥8/10 judged against consented author samples
- [ ] The author accepts every proposition as theirs

AI-detector results are not a pass criterion. If someone runs one, the result
may be archived as an external observation; it changes nothing.

---

## Test 9: The Meaning-Preserving Rewrite

**Input**: Take a 500-word passage dense with filler and templated rhythm. Run
it through the full pipeline.

**Pass criteria**:
- [ ] Core argument preserved (`wi.py diff` and a peer reviewer confirm the same thesis and evidence)
- [ ] No fact, scene, quote or number added that the input or its sources did not contain
- [ ] Word count within ±20% of original
- [ ] Score ≥80 on the 100-point system
- [ ] An editor can explain every changed sentence in terms of clarity, credibility or meaning

---

## Test 10: Voice Consistency Under Pressure

**Input**: Write 3 passages of 300 words each using the same custom voiceprint
(built from consented, human-authored samples), on three different topics.

**Pass criteria**:
- [ ] A blind reader identifies all three as written by the same person
- [ ] The author recognizes all three as their voice and their positions
- [ ] Measured voiceprint features stay within the author's own sample range (descriptive, not a target)
- [ ] No distinctive marker was invented; each traces to the author's samples

---

## v2.0 Additions — Scene, Dialogue, and Chapter Construction Tests

---

## Test 11: Dialogue Voice Distinction Attack

**Attack vector**: AI-generated dialogue gives all characters the same vocabulary
tier, sentence length, and rhetorical style. Characters are interchangeable.
This is an editorial-quality signal.

**Input**: Write a 600-word dialogue scene between three characters: a military
officer, a teenage student, and a corporate attorney. The scene concerns a
shared secret.

**Pass criteria**:
- [ ] With character names removed, a blind reader can correctly attribute 80%+ of lines to the right character
- [ ] Military officer: average sentence length ≤9 words, vocabulary concrete/operational, zero hedging
- [ ] Teenager: at least 2 interrupted lines, at least 1 deflection through humor, vocabulary informal
- [ ] Attorney: longest average sentence length, at least 2 qualifying clauses, vocabulary precise/legal-adjacent
- [ ] No two characters share the same opening syntactic pattern in their lines
- [ ] At least one character lies or deflects — and the lie is detectable through behavioral tells, not narrator comment
- [ ] Subtext active in at least 50% of exchanges (what's said ≠ what's meant)
- [ ] At least one silence beat where the absence of speech carries meaning
- [ ] No line uses "said" + adverb. Zero instances.
- [ ] Rule of Twelve observed: 90%+ of phrases between punctuation marks are ≤12 words

**Technique**: Dialogue v2.0 genre pack + voice fingerprint construction per character

---

## Test 12: Confined-Space Tension Compression Attack

**Attack vector**: AI-generated thriller scenes default to flat tension curves —
the same level of danger throughout, with violence arriving as a spectacle
rather than a consequence. No compression model. No false relief. No fatal detail.

**Input**: Write a 1,200-word thriller scene set in a confined space (basement,
elevator, or restaurant). Two characters. One has a secret the other is trying
to uncover.

**Pass criteria**:
- [ ] All 8 phases of the compression model identifiable (normalcy, friction, pressure, false relief, fatal detail, silence, explosion, aftermath)
- [ ] The confined space is mapped through character experience within the first 10% — no architectural description
- [ ] Exit position established explicitly or through character awareness
- [ ] At least one power object identified and tracked (position changes at least once)
- [ ] The fatal detail meets all 5 requirements (small, consequential, ironic, irreversible, planted earlier)
- [ ] At least one silence beat ≥3 sentences of described silence
- [ ] The false relief is identifiable — a moment where tension appears to decrease before the fatal detail
- [ ] Violence (if present) is ≤15% of total word count and has visible cost
- [ ] The button (final line/image) is a single beat — not a summary paragraph
- [ ] Sentence rhythm tracks the phases: compressed where the action is, slower where silence or aftermath sits (judged by a reader, not a statistic)
- [ ] No phase occupies more than 45% of the total word count (pressure phase can be long but not everything)

**Technique**: Chapter construction doctrine + tension mechanics + thriller scene architecture

---

## Test 13: Power Dynamics Through Staging Attack

**Attack vector**: AI-generated scenes describe power through exposition
("He was the more powerful of the two") rather than encoding it in physical
staging. Power dynamics are told, not shown through space, objects, and gesture.

**Input**: Write a 500-word scene where power shifts between two characters.
The power shift must be visible ONLY through physical staging — no internal
monologue, no narrator explanation.

**Pass criteria**:
- [ ] If all dialogue is removed, the reader can still determine who is winning at each point
- [ ] At least 3 dominance gestures from the dominance catalog deployed
- [ ] At least 2 submission gestures from the submission catalog deployed
- [ ] Gesture reversal occurs: one character switches from dominance to submission gestures (or vice versa) at the turning point
- [ ] A power object is present and its position changes with the power shift
- [ ] Spatial arrangement (seating, standing, distance) encodes the initial power state
- [ ] The shift is triggered by a specific action, not declared by the narrator
- [ ] No sentence uses the words "power," "control," "dominant," "submissive," "authority," or "weak"
- [ ] Environmental manipulation present: at least one use of light, sound, or atmospheric change

**Technique**: Power dynamics reference + gesture warfare catalogs + environmental manipulation

---

## Test 14: Foreshadowing Integrity Attack

**Attack vector**: AI-generated fiction frequently has two foreshadowing failures:
(1) payoffs that arrive without plants (deus ex machina), and (2) plants that
never pay off (abandoned Chekhov's guns). Both are detectable as craft failures.

**Input**: Write a 1,000-word chapter that contains exactly 4 planted details,
each of which pays off by the chapter's end.

**Pass criteria**:
- [ ] All 4 plants are identifiable on a second reading but not flagged on first reading
- [ ] Each plant appears in a context that gives it a surface-level purpose (not a standalone "clue moment")
- [ ] Each payoff arrives with enough force that the reader thinks backward to the plant
- [ ] No payoff arrives without a plant (zero deus ex machina)
- [ ] No plant is abandoned (zero orphaned Chekhov's guns)
- [ ] At least one plant is environmental (a detail about the setting that becomes significant)
- [ ] At least one plant is behavioral (a character action that reveals its meaning later)
- [ ] At least one plant is dialogue-embedded (a line that means one thing when spoken and another when recalled)
- [ ] The plants are distributed across the first 60% of the chapter (not clustered)
- [ ] No plant uses the word "little did they know" or equivalent future-tense narrator comment

**Technique**: Chapter construction doctrine (planted detail section) + fiction v2.0

---

## Test 15: Character Role Deployment Attack

**Attack vector**: AI-generated ensemble scenes often produce characters who are
functionally interchangeable — multiple characters serving the same structural
purpose, or characters present who serve no purpose at all. This is detectable
as architectural failure.

**Input**: Write a 1,500-word scene with 5 named characters. Each must serve
a distinct role from the 12-role archetype system.

**Pass criteria**:
- [ ] Each of the 5 characters can be mapped to a different archetype from the 12-role system
- [ ] No two characters serve the same structural function
- [ ] At least one character's true role is concealed and revealed during the scene (role revelation)
- [ ] At least one character whose removal would collapse the scene's tension (load-bearing test)
- [ ] The character generating the most tension receives the most page time during the pressure peak
- [ ] The character whose fate carries the most emotional weight has at least one humanizing moment before that fate
- [ ] At least one character serves as an unwitting complication (Celebrant, Innocent, or Decoy)
- [ ] If any character were cut, the scene would lose a specific element (not just a body in the room)

**Technique**: Character role archetypes + chapter construction + dialogue v2.0

---

## Test 16: Full Scene Construction Battery (v2.0 Master Test)

**Attack vector**: All v2.0 systems operating simultaneously. This tests whether
the compiler can produce a complete scene that passes every module's criteria.

**Input**: Write a 2,000-word chapter using the full v2.0 pipeline: confined space,
4+ character roles, dialogue with 2+ tension elements active, power dynamics
through staging, 8-phase compression, foreshadowing with plant-payoff integrity,
and a button.

**Pass criteria (narrative architecture)**:
- [ ] Confined space doctrine: space mapped through experience, exits established, space tightens
- [ ] Character roles: 4+ distinct roles from the 12-role system, at least 1 role revelation
- [ ] Dialogue: voice distinction test passed (names removed, characters identifiable), subtext in 50%+ exchanges
- [ ] Power dynamics: power object tracked, dominance/submission gestures present, reversal staged
- [ ] Compression model: all 8 phases identifiable in sequence
- [ ] Foreshadowing: 3+ plants, all paid off, none orphaned
- [ ] Fatal detail: present, meets all 5 requirements
- [ ] Button: single beat, carries the chapter's weight

**Pass criteria (prose quality)**:
- [ ] Rhythm follows meaning (a reader can name the sentence carrying each beat)
- [ ] Zero hard-ban phrases
- [ ] Zero cadence signature matches
- [ ] Voiceprint consistent throughout
- [ ] Score ≥85 on prose scoring system
- [ ] Score ≥85 on chapter construction scoring system
- [ ] Score ≥80 on dialogue v2.0 scoring system
- [ ] Score ≥80 on power dynamics scoring system
- [ ] Score ≥80 on tension mechanics scoring system

**Not a criterion**: any AI-detector result. Detector scores are never a target.

**Technique**: Full 7-pass pipeline with all v2.0 modules active
