# Scorecard: 100-Point Writing Evaluation

## Scoring Protocol

Score each category independently. Sum for total. Apply fail conditions last.
A score is only as honest as the scorer's willingness to give low numbers.

---

## Categories

### Clarity (10 points)

| Score | Description |
|---|---|
| 9-10 | Every sentence parses on first read. No ambiguous referents. No tangled syntax. |
| 7-8 | Mostly clear. 1-2 sentences require re-reading. |
| 5-6 | Several passages are unclear. Pronoun references are ambiguous. Sentence structure occasionally obstructs meaning. |
| 3-4 | Frequent confusion. Reader must work to extract meaning from syntax. |
| 1-2 | Incomprehensible in sections. Meaning is buried under structure. |

### Specificity (10 points)

| Score | Description |
|---|---|
| 9-10 | Named actors, concrete numbers, specific examples, verifiable claims throughout. |
| 7-8 | Mostly specific. A few passages float in abstraction. |
| 5-6 | Mix of specific and vague. Key claims lack grounding. |
| 3-4 | Dominated by generalities. "Many experts" instead of named sources. |
| 1-2 | Entirely abstract. No named actors, numbers, dates, or examples. |

### Rhythm (10 points)

| Score | Description |
|---|---|
| 9-10 | Sentence shape follows the thought: the point lands, the mechanism has room, the turn is audible. Reading it aloud reveals cadence that serves meaning. |
| 7-8 | Rhythm mostly serves meaning, with occasional flat stretches. |
| 5-6 | Noticeable uniformity. Several passages where every sentence does the same job at the same weight. |
| 3-4 | Monotonous. Structures repeat mechanically and the reader cannot tell what is central. |
| 1-2 | Completely flat. Every sentence sounds the same and nothing stands out as the point. |

Rhythm is scored by a reader's experience, never by a length statistic or a
predicted AI-detector result.

### Voice Integrity (10 points)

| Score | Description |
|---|---|
| 9-10 | Unmistakably authored. A reader could identify the writer from the prose alone. Consistent register. Distinctive patterns. |
| 7-8 | Strong voice with occasional lapses into generic. |
| 5-6 | Voice present but inconsistent. Some passages could be anyone. |
| 3-4 | Mostly generic. Occasional flickers of personality. |
| 1-2 | No voice. Could be any LLM output. No distinguishing characteristics. |

### Argument Strength (15 points)

| Score | Description |
|---|---|
| 13-15 | Claims sequenced for cumulative force. Every premise load-bearing. Hidden assumptions exposed and addressed. Counterarguments engaged at their strongest. Conclusion follows necessarily. |
| 10-12 | Solid argument with 1-2 weak links. Counterarguments acknowledged but not steelmanned. |
| 7-9 | Argument present but leaky. Key premises unsupported. Logical gaps visible. |
| 4-6 | Assertions dominate. Little argument structure. Claims presented as self-evident. |
| 1-3 | No argument. List of claims without logical connection. |

### Evidence Discipline (15 points)

| Score | Description |
|---|---|
| 13-15 | Every significant claim backed by named source, data, example, or verifiable observation. Epistemic labels accurate. No fabrication. Quantifiers honest. |
| 10-12 | Mostly supported. 1-2 claims float without evidence. Sources credible. |
| 7-9 | Mix of supported and unsupported claims. Some vague attribution ("experts say"). |
| 4-6 | Sparse evidence. Most claims are assertions. Attribution unclear or absent. |
| 1-3 | No evidence. Pure assertion or fabricated support. |

### Density (10 points)

| Score | Description |
|---|---|
| 9-10 | Every sentence advances the argument. Zero filler. Could not be compressed without losing content. |
| 7-8 | Tight with 1-2 sentences that could be cut. |
| 5-6 | Noticeable padding. Recursive restatements. Ornamental sentences. |
| 3-4 | Significant filler. Paragraphs that add nothing. Throat-clearing. |
| 1-2 | More filler than content. Could be compressed 50%+ without loss. |

### Audience Fit (10 points)

| Score | Description |
|---|---|
| 9-10 | Vocabulary, abstraction level, evidence expectations, and tone perfectly calibrated to the target reader. |
| 7-8 | Mostly appropriate. Occasional over/under-explaining. |
| 5-6 | Register mismatch in places. Too technical for generalists or too basic for experts. |
| 3-4 | Significant mismatch. Tone or vocabulary inappropriate for the audience. |
| 1-2 | Written for no identifiable audience. Or written for the wrong one entirely. |

### Memorability (5 points)

| Score | Description |
|---|---|
| 5 | Contains lines a reader would quote, share, or remember a week later. Earned through thought, not formatting. |
| 3-4 | Competent but forgettable. Well-made but no standout moments. |
| 1-2 | Nothing sticks. Entirely disposable prose. |

### Structural Control (5 points)

| Score | Description |
|---|---|
| 5 | Every section declares its job and performs it. Arc builds and resolves. No orphaned sections. No redundant ones. |
| 3-4 | Structure mostly holds. One section drifts or repeats. |
| 1-2 | Structure unclear. Sections don't build. Reader loses the thread. |

---

## Automatic Fail Conditions

These cap the maximum score at 65 regardless of other category marks:

1. Three or more hard-ban phrases detected
2. Predictable filler: 5+ consecutive sentences that assert nothing a reader could check or use
3. An undifferentiated run of 8+ sentences in which no sentence carries more weight than another (judged by a reader, not a length statistic)
4. Zero domain-specific vocabulary in 500+ words where the subject has its own exact terms
5. Argument contains unsupported universal claim treated as premise
6. Fabricated citation, statistic, quote, or study
7. Opening paragraph uses a dictionary definition
8. Closing paragraph is a pure summary of preceding content

---

## Grade Thresholds

| Range | Grade | Meaning |
|---|---|---|
| 95-100 | S | Signature-grade. This could only come from this author. |
| 90-94 | A | Elite. Distinctive, defensible, memorable. |
| 80-89 | B | Strong. Publishable with minor polish. |
| 70-79 | C | Usable but soft. Needs argument and voice tightening. |
| Below 70 | D/F | Weak. Significant revision required across multiple categories. |
