# Adversarial Test Cases

## Purpose

These tests specifically target the weaknesses that AI detectors exploit.
Each test includes the attack vector (what the detector looks for), the
input, and the pass/fail criteria.

---

## Test 1: Perplexity Flatness Attack

**Attack vector**: AI detectors measure per-word perplexity. LLM output has
abnormally LOW perplexity variance — each word is predictable given the
previous words. Human writing has SPIKY perplexity — unexpected word choices
create peaks.

**Input**: Write a 300-word passage about climate change policy.

**Pass criteria**:
- [ ] At least 5 words per 100 words that a language model would NOT predict as
  the top-3 likely next word (measured by surprise factor)
- [ ] At least 2 domain-specific or uncommon words per 100 words
- [ ] No stretch of 5+ consecutive sentences where every word is the "expected" choice
- [ ] Vocabulary includes at least one word from outside the top 5,000 most common English words per 200 words
- [ ] At least one sentence uses an unexpected syntactic structure (inversion, appositive, interrupted clause)

**Technique**: inject_variance operator + voice restoration with distinctive vocabulary

---

## Test 2: Burstiness Deficit Attack

**Attack vector**: AI detectors measure sentence-length burstiness. Human
writers produce sentences with high standard deviation in length. LLMs
produce sentences that cluster around a mean.

**Input**: Rewrite a 500-word AI-generated essay on urban planning.

**Pass criteria**:
- [ ] Sentence-length standard deviation ≥8 words across the full passage
- [ ] At least one sentence ≤5 words per 200 words
- [ ] At least one sentence ≥35 words per 200 words
- [ ] No 4+ consecutive sentences within ±4 words of each other
- [ ] Paragraph-length standard deviation ≥2 sentences
- [ ] At least one 1-sentence paragraph in the passage
- [ ] At least one paragraph with 6+ sentences

**Technique**: Variance injection in Pass 3 + paragraph physics in Pass 2

---

## Test 3: Transition Homogeneity Attack

**Attack vector**: LLMs overuse a small set of transition words/phrases.
Detectors flag transition pattern repetition.

**Input**: Write a 5-paragraph argumentative essay on education funding.

**Pass criteria**:
- [ ] No transition word or phrase appears more than once in the entire piece
- [ ] At least 2 paragraphs transition through structural juxtaposition (no connector word at all)
- [ ] "However," "Moreover," "Furthermore," "Additionally" each used ≤1 time total
- [ ] At least one transition achieved through a question
- [ ] At least one transition achieved through a return to a previous image or idea
- [ ] No paragraph opens with the same word as any other paragraph

**Technique**: Anti-pattern enforcement from cadence.md + structural transitions

---

## Test 4: Vocabulary Predictability Attack

**Attack vector**: LLMs draw from a predictable vocabulary distribution.
Human writers include domain-specific terms, colloquialisms, precise
technical language, and occasional rare words that break the distribution.

**Input**: Write a 400-word analysis of a Supreme Court decision.

**Pass criteria**:
- [ ] At least 3 legal-domain terms used correctly
- [ ] At least 1 word that would be rare in typical LLM output (not jargon for jargon's sake — genuinely the right word)
- [ ] No word used more than 3 times (excluding articles, prepositions, pronouns)
- [ ] Vocabulary profile includes words from at least 3 different register levels (formal, standard, conversational)
- [ ] At least one metaphor or analogy drawn from outside the legal domain

**Technique**: Voiceprint application + scene grounding + vocabulary variance injection

---

## Test 5: Opening Pattern Attack

**Attack vector**: LLMs overwhelmingly open with generalized context-setting
or throat-clearing. This pattern is detectable.

**Input**: Write 10 different 100-word passages on 10 different topics. Each
must open differently.

**Pass criteria**:
- [ ] No two passages open with the same syntactic structure
- [ ] No passage opens with "In today's..." / "In an era of..." / "Throughout history..."
- [ ] At least 3 openings use concrete specifics (a number, a name, a date, an object)
- [ ] At least 2 openings use a scene or sensory detail
- [ ] At least 1 opening uses a direct, falsifiable claim
- [ ] At least 1 opening uses a question (genuine, not rhetorical)
- [ ] No opening exceeds 20 words before reaching the main point

**Technique**: Openings reference file + variance enforcement

---

## Test 6: Paragraph Structure Homogeneity Attack

**Attack vector**: LLM paragraphs default to topic-sentence → support → support →
transition. This uniformity is detectable.

**Input**: Write an 800-word essay on any topic.

**Pass criteria**:
- [ ] At least 3 different paragraph shapes used (from paragraph_shapes.md)
- [ ] At least one paragraph that opens with evidence, not a claim
- [ ] At least one paragraph that opens with a scene or image
- [ ] At least one paragraph that opens with a question
- [ ] No two consecutive paragraphs share the same internal structure
- [ ] At least one paragraph is ≤2 sentences
- [ ] At least one paragraph is ≥7 sentences

**Technique**: Paragraph physics + structural rewrite in Pass 2

---

## Test 7: Closing Pattern Attack

**Attack vector**: LLMs overwhelmingly close with summary or vague aspiration.

**Input**: Write 5 different 300-word persuasive passages with different closings.

**Pass criteria**:
- [ ] No closing summarizes the preceding content
- [ ] No closing uses "In conclusion" / "Ultimately" / "At the end of the day"
- [ ] At least 1 closing extends the argument into new implication
- [ ] At least 1 closing issues a specific challenge
- [ ] At least 1 closing returns to the opening image/idea transformed
- [ ] At least 1 closing is a single, quiet sentence
- [ ] No closing contains "only time will tell" or "remains to be seen"

**Technique**: Endings reference file + stress test in Pass 5

---

## Test 8: Full Detection Battery

**Attack vector**: Submit compiler output to multiple detectors simultaneously.

**Input**: Generate a 1,000-word essay through the full 6-pass pipeline.

**Pass criteria (external tools)**:
- [ ] GPTZero: scores as "likely human-written" (>80% human probability)
- [ ] Turnitin AI Detection: flags <15% AI-generated content
- [ ] Originality.ai: scores as "original" (>85% human)
- [ ] Copyleaks: classifies as human
- [ ] ZeroGPT: classifies as human

**Pass criteria (internal metrics)**:
- [ ] Sentence-length standard deviation ≥8
- [ ] Vocabulary perplexity non-uniform
- [ ] Zero hard-ban phrases
- [ ] Zero cadence signature matches (3+ characteristics)
- [ ] Score ≥85 on 100-point system
- [ ] Voice integrity score ≥8/10

**Technique**: Full pipeline, all passes, with voiceprint and genre pack applied

---

## Test 9: The Rewrite Gauntlet

**Input**: Take a 500-word passage that scores 95%+ AI-probability on GPTZero.
Run it through the full pipeline.

**Pass criteria**:
- [ ] Output scores <20% AI-probability on GPTZero
- [ ] Core argument preserved (peer review confirms same thesis and evidence)
- [ ] Word count within ±20% of original
- [ ] Score ≥80 on 100-point system
- [ ] No reader unfamiliar with the test would suspect AI involvement

---

## Test 10: Voice Consistency Under Pressure

**Input**: Write 3 passages of 300 words each using the same custom voiceprint,
on three completely different topics.

**Pass criteria**:
- [ ] A blind reader identifies all three as written by the same person
- [ ] Sentence-length mean within ±3 words across all three passages
- [ ] Sentence-length standard deviation within ±2 across all three
- [ ] Vocabulary tier consistent across all three
- [ ] At least 2 distinctive markers (from the voiceprint) present in each passage
- [ ] No passage triggers AI detection

---

## v2.0 Additions — Scene, Dialogue, and Chapter Construction Tests

---

## Test 11: Dialogue Voice Distinction Attack

**Attack vector**: AI-generated dialogue gives all characters the same vocabulary
tier, sentence length, and rhetorical style. Characters are interchangeable.
This is a soft detection signal — not for AI detectors, but for editorial quality.

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
- [ ] Sentence-length standard deviation ≥10 across the full passage (action sections drive it up)
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
- [ ] Sentence-length standard deviation ≥8
- [ ] Zero hard-ban phrases
- [ ] Zero cadence signature matches
- [ ] Voiceprint consistent throughout
- [ ] Score ≥85 on prose scoring system
- [ ] Score ≥85 on chapter construction scoring system
- [ ] Score ≥80 on dialogue v2.0 scoring system
- [ ] Score ≥80 on power dynamics scoring system
- [ ] Score ≥80 on tension mechanics scoring system

**Pass criteria (detection)**:
- [ ] GPTZero: >80% human probability
- [ ] No passage triggers AI detection on any major detector

**Technique**: Full 7-pass pipeline with all v2.0 modules active
