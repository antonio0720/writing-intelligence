# Anti-Pattern Structures

## Table of Contents
1. Binary Contrast Structures
2. List-Masquerading-As-Argument
3. The False Build
4. Narrative Distance Patterns
5. Sentence-Length Uniformity
6. Paragraph Homogeneity
7. The Recursive Restatement
8. The Hollow Framework
9. Performative Complexity

---

## 1. Binary Contrast Structures

Pattern: "It's not X — it's Y" / "Less about X, more about Y" / "The real question isn't X, it's Y"

Why it flags: LLMs default to binary reframing as a substitute for actual analysis. The structure sounds insightful but often just relabels the same idea.

Detection: Two nouns or noun phrases connected by a contrast operator where the second term is not genuinely different from the first.

Fix: If the contrast is real, state both sides with evidence. If the contrast is cosmetic, delete the structure and make the actual claim directly.

---

## 2. List-Masquerading-As-Argument

Pattern: A numbered or bulleted list presented as if the items build on each other, but each item is actually independent and could appear in any order.

Why it flags: LLMs generate lists because they are structurally easy. Humans making an argument sequence their points for cumulative force.

Detection:
- Reorder the list items randomly. If the text reads identically, it's a list, not an argument.
- Check whether later items reference or build on earlier ones. If not, it's a list.

Fix: Either (a) restructure as prose with logical connectors showing how each point builds, or (b) acknowledge it's a list and format it as one honestly — but only if a list is the appropriate format.

---

## 3. The False Build

Pattern: "First... Second... Third... And finally..." where the final item is either the most obvious or least impactful.

Why it flags: LLMs enumerate in order of generation, not order of force. Human writers save the strongest point for last or lead with it.

Detection: Rank the items by argumentative weight. If the strongest is buried in the middle or the weakest is positioned as the climax, the build is false.

Fix: Reorder for escalation (weakest → strongest) or lead with the strongest and defend it through the section.

---

## 4. Narrative Distance Patterns

Pattern: Describing events or ideas from a consistent observer distance without ever zooming in or zooming out.

Why it flags: LLMs maintain a stable narrative distance because they process text at uniform granularity. Human writing zooms between satellite view and ground level.

Detection: Check whether the prose stays at one altitude throughout. Does it ever give a specific moment, a close detail, a personal observation? Or does it hover at summary altitude for the entire passage?

Fix: Introduce at least one zoom-in per 500 words: a specific moment, a named detail, a scene, a quote, a sensory observation. Alternate between wide-angle claims and close-range evidence.

---

## 5. Sentence-Length Uniformity

Pattern: Consecutive sentences within ±5 words of each other in length, across 4+ sentences.

Why it flags: This is the single strongest statistical signal for AI generation. Human sentence lengths have high variance (standard deviation typically 8-15 words). LLM output clusters around a mean with low variance (standard deviation typically 3-6 words).

Detection: Count words per sentence in any paragraph. If the standard deviation is below 5 across 5+ sentences, flag it.

Fix: Deliberately vary. Follow a 22-word sentence with a 7-word one. Then 31. Then 11. Then 45. Then 5. The pattern should look random — because human writing IS random at this level.

---

## 6. Paragraph Homogeneity

Pattern: Every paragraph is 3-5 sentences, opens with a topic sentence, develops with 2-3 supporting sentences, and closes with a transition.

Why it flags: This is the five-paragraph essay structure applied fractally. Real prose has paragraphs of wildly different lengths, purposes, and internal structures.

Detection: Map paragraph lengths across a document. If they cluster within ±1 sentence of each other, flag it. Also check whether every paragraph opens with the same syntactic structure.

Fix:
- Include at least one 1-sentence paragraph per 800 words
- Include at least one 6+ sentence paragraph per 1000 words
- Vary opening structures: start with a quote, a question, a scene detail, a number, a contrast, a concession — not always a topic sentence

---

## 7. The Recursive Restatement

Pattern: Saying the same thing three ways in consecutive sentences without adding information.

Example: "This approach offers significant value. The benefits are substantial. Organizations that adopt it see meaningful results."

Why it flags: LLMs pad for length by restating. Humans either add detail or move on.

Detection: If deleting 2 of 3 consecutive sentences loses no information, it's recursive restatement.

Fix: Keep the strongest version. Delete the others. Use the recovered space for evidence or a new point.

---

## 8. The Hollow Framework

Pattern: Presenting a framework (3 pillars, 4 principles, 5 steps) where the categories are vague enough to contain anything.

Example: "The three pillars of success are: Strategy, Execution, and Culture."

Why it flags: LLMs generate frameworks because they organize output. But the frameworks are often so broad they communicate nothing specific.

Detection: Ask whether the framework categories could be guessed without reading the text. If someone could predict "Strategy, Execution, Culture" before seeing the document, the framework adds no information.

Fix: Either (a) make the framework specific and non-obvious, or (b) delete the framework and present the actual content in prose.

---

## 9. Performative Complexity

Pattern: Using complex sentence structures, multi-clause constructions, and academic vocabulary not to convey complex ideas but to signal sophistication.

Example: "The multifaceted implications of this paradigmatic shift necessitate a comprehensive reevaluation of our fundamental assumptions regarding the interconnected nature of these systemic dynamics."

Translation: "This changes how we think about the system."

Why it flags: LLMs optimize for sounding smart over being clear. The complexity is structural, not intellectual.

Detection: Rewrite the sentence in plain language. If the plain version says exactly the same thing in half the words, the original was performative.

Fix: Default to the plainest structure that preserves meaning. Complexity should come from the idea, not the syntax.
