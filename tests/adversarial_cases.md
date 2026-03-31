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
