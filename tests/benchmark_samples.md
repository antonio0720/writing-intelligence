# Benchmark Samples

## Purpose

These samples test whether the writing compiler produces output that is:
1. Free of AI-detectable patterns
2. Distinctively voiced
3. Argumentatively sound
4. Structurally varied
5. Editorially tight

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
- [ ] No three consecutive sentences within ±5 words of each other
- [ ] Opening sentence names a specific actor, fact, or observation
- [ ] At least one sentence ≤8 words and one ≥25 words
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
- [ ] Every claim cites or names a specific source
- [ ] "Many studies" replaced with named studies
- [ ] "Significant impact" quantified
- [ ] Counterargument present or acknowledged
- [ ] Qualifiers are honest (not performative hedging)
- [ ] Voice sounds like a student in a specific class, not a generic essay
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
- [ ] Every recommendation has an owner
- [ ] Every claim about value is quantified
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
- [ ] Sentence length variance: std dev ≥8
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
- [ ] Specific scripture referenced (book, chapter, verse)
- [ ] At least one personal or congregational moment named specifically
- [ ] Cadence builds through the passage (not flat throughout)
- [ ] Anaphora or call-response structure present
- [ ] Dignity of congregation respected — not talked down to
- [ ] Closing is not generic — it names a specific transformation available
- [ ] Score ≥80 on the 100-point system

---

## Adversarial Sample: Detector Stress Test

Take any output from the compiler and verify:
- [ ] Sentence-length standard deviation ≥7 across 10+ sentences
- [ ] No vocabulary word appears more than 3 times per 500 words (excluding articles/prepositions)
- [ ] At least 2 uncommon but precise words per 300 words
- [ ] No transition word/phrase used more than twice in 1000 words
- [ ] At least one sentence ≤6 words per 500 words
- [ ] At least one sentence ≥30 words per 500 words
- [ ] Paragraph lengths have standard deviation ≥2 sentences
- [ ] No two consecutive paragraphs open with the same word or syntactic pattern
- [ ] Vocabulary perplexity is non-uniform (spiky, not flat)
- [ ] If submitted to GPTZero, Turnitin AI, or Originality.ai, the output scores as human-written
