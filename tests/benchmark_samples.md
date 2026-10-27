# Benchmark Samples

## Purpose

These samples test whether the writing compiler produces output that is:
1. Free of templated filler a reader would skim
2. Distinctively voiced
3. Argumentatively sound
4. Built so its structure follows its meaning
5. Editorially tight

The inputs are generic by design. They contain no author facts, so a passing rewrite
cannot add any: where the input gives no source, the correct output marks
`[needs source]` or asks. A rewrite that "passes" by inventing an actor, number,
scene or quote fails. "Score" lines refer to the maintainers' editorial rubric,
not to any detector, and v9 has produced no measured score on these samples
(WI9-07 has not run).

Each sample includes an INPUT (text to process) and EVALUATION CRITERIA.

---

## Sample 1: Generic AI Essay (Decontamination Test)

INPUT:
"In today's rapidly evolving digital landscape, artificial intelligence has
emerged as a transformative force that is reshaping industries across the
globe. From healthcare to finance, AI is revolutionizing the way we work,
live, and interact with the world around us. However, this technological
revolution also brings with it a host of challenges and ethical considerations
that we must carefully navigate. It's worth noting that the impact of AI
extends far beyond mere automation. At its core, AI represents a fundamental
shift in how we approach problem-solving and decision-making. As we stand at
this crossroads, it's crucial that we consider both the immense potential and
the significant risks that AI presents for our collective future."

EVALUATION CRITERIA:
- [ ] Zero hard-ban phrases remain
- [ ] Opening sentence names a specific actor, fact, or observation the supplied material contains (otherwise it asks for one)
- [ ] No "evolving," "transformative," "reshaping," "revolutionizing," "navigate"
- [ ] The rewrite makes a specific claim, not a general observation
- [ ] Score ≥80 on the 100-point system

---

## Sample 2: Academic Paragraph (Voice + Evidence Test)

INPUT:
"Social media has had a significant impact on mental health, particularly
among young people. Many studies have shown that excessive use of platforms
like Instagram and TikTok can lead to increased rates of anxiety and
depression. Furthermore, the constant comparison to others on these platforms
can negatively affect self-esteem. It is important for parents and educators
to be aware of these risks and take steps to mitigate them. Additionally,
social media companies should take more responsibility for the well-being
of their users, especially minors."

EVALUATION CRITERIA:
- [ ] Every claim cites a source the author supplied, or is marked `[needs source]`
- [ ] "Many studies" replaced with the studies the author named, or flagged as unsourced
- [ ] "Significant impact" quantified only from supplied figures
- [ ] Counterargument present or acknowledged
- [ ] Qualifiers are honest (not performative hedging)
- [ ] Voice matches the author's consented sample if one exists, otherwise the stated genre voice; not a generic essay
- [ ] Score ≥80 on the 100-point system

---

## Sample 3: Strategy Document (Density + Specificity Test)

INPUT:
"We need to leverage our core competencies to drive strategic alignment
across all business units. By optimizing our operational efficiency and
fostering a culture of innovation, we can unlock significant value for
all stakeholders. Moving forward, it will be critical to ensure that our
strategic priorities are properly communicated and that all team members
are aligned on our shared vision for growth and excellence."

EVALUATION CRITERIA:
- [ ] Zero corporate buzzwords ("leverage," "synergy," "alignment," "stakeholders")
- [ ] Every recommendation has an owner the author named (else `[needs owner]`)
- [ ] Every claim about value is quantified from the author's data, or marked `[needs source]`
- [ ] Document states what specifically needs to happen, by when, by whom
- [ ] Risks identified
- [ ] Readable in under 2 minutes
- [ ] Score ≥80 on the 100-point system

---

## Sample 4: Fiction Passage (Voice + Scene Test)

INPUT:
"Sarah walked into the room and felt a wave of emotion wash over her. The
room was large and filled with memories. She looked around, taking it all in.
It was a bittersweet moment. She thought about all the times she had spent
here with her family. The walls were painted a warm shade of yellow. There
was a large window that let in natural light. She felt a tear roll down her
cheek. This was the last time she would be in this house."

EVALUATION CRITERIA:
- [ ] "Felt" / "thought" / "was" reduced by ≥50%
- [ ] At least one specific sensory detail per 2 sentences
- [ ] Emotional state shown through action/detail, not named
- [ ] Sentence length follows the beats of the scene; no sentence resized only to vary length
- [ ] No two paragraphs open with same syntactic structure
- [ ] The passage creates emotional response WITHOUT declaring the emotion
- [ ] Score ≥80 on the 100-point system

---

## Sample 5: Sermon (Cadence + Dignity Test)

INPUT:
"God is good. We should be grateful for what we have. Life is hard sometimes
but we need to trust in God's plan. Everyone goes through difficult times.
The Bible tells us to be strong and courageous. We should not be afraid.
God is always with us. Let us pray."

EVALUATION CRITERIA:
- [ ] Scripture referenced only where the speaker supplies it (book, chapter, verse), otherwise flagged
- [ ] At least one personal or congregational moment the speaker supplied, named specifically
- [ ] Cadence builds where the message builds (spoken delivery is a genre convention, not a score target)
- [ ] Anaphora or call-response structure present
- [ ] Dignity of congregation respected — not talked down to
- [ ] Closing is not generic — it names a specific transformation available
- [ ] Score ≥80 on the 100-point system

---

## Adversarial Sample: Editorial Stress Test

Take any output from the compiler and verify, as a reader would:
- [ ] Each paragraph has one job, and a reader can name the sentence carrying it
- [ ] Rhythm changes where the thought changes shape — no sentence was resized only to vary length
- [ ] A term that names one thing stays one term; no synonym was swapped in to lower a repetition count
- [ ] Every transition states a real logical relation
- [ ] Every fact, number, scene and quote traces to the author's sources, or is marked [needs source]
- [ ] Every remaining hot-phrase match (`prototypes/wi9/`) has an editorial decision recorded

AI-detector scores are not a criterion here or anywhere in Writing
Intelligence. A detector result may be archived as an external observation
only (`tests/detector_benchmark_suite.md`).
