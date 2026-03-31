# Expanded Cadence Library

## Purpose

50+ identifiable cadence patterns that signal AI generation, lazy writing,
or genre-specific cliché. Each entry includes the pattern signature,
detection threshold, and fix protocol.

The original cadence.md covers 9 major signatures. This library extends
into subtler, more specialized patterns that sophisticated detectors and
experienced editors catch.

---

## Category A: Structural Cadences (sentence/paragraph level)

### A01: The Uniform Trio
Three consecutive sentences of 14-18 words each, all Subject-Verb-Object.
Detection: 3 consecutive S-V-O sentences within ±4 words.
Fix: Break the middle sentence into a fragment. Invert the third.

### A02: The Paragraph Template
Every paragraph: topic sentence → 2-3 support sentences → transition.
Detection: 4+ consecutive paragraphs with identical internal structure.
Fix: Open one paragraph with evidence. Open another with a question. Let one be a single sentence.

### A03: The Bullet Point Essay
Prose that reads like a numbered list with the numbers removed.
Detection: 5+ consecutive paragraphs beginning with parallel structure ("First..." "Second..." or equivalent).
Fix: Weave points into an argument with causal, contrastive, or temporal connections.

### A04: The Identical Opening
3+ paragraphs in a piece beginning with the same word.
Detection: Pattern match on first word of each paragraph.
Fix: Vary aggressively. Name, number, question, scene, contrast.

### A05: The Metronomic Paragraph
All paragraphs within ±1 sentence of each other in length.
Detection: Paragraph-length standard deviation below 1.5 across 5+ paragraphs.
Fix: Include at least one 1-sentence paragraph and one 6+ sentence paragraph.

### A06: The Bookend Trap
Opening sentence and closing sentence of every paragraph are short declaratives, with longer sentences sandwiched between.
Detection: Consistent short-long-long-short paragraph architecture across 3+ paragraphs.
Fix: Vary exit types. Some paragraphs end long. Some end mid-thought.

### A07: The Clause Stack
Sentence with 3+ subordinate clauses, all of similar length, creating a monotonous nested rhythm.
Detection: Comma-separated or conjunction-separated clauses where each clause is 5-8 words.
Fix: Break into multiple sentences or make clauses dramatically different lengths.

---

## Category B: Transitional Cadences

### B01: The Bridge Word
"However," "Moreover," "Furthermore," "Additionally" appearing at 3+ paragraph openings.
Detection: Count formal transition words at position 1 of paragraphs.
Fix: Delete the transition. Let the paragraph's content create the connection.

### B02: The Cause-Chain
"This leads to... which causes... resulting in... which means..."
Detection: 3+ consecutive causal connectors in a sequence.
Fix: Break the chain. State the end-state first, then explain the mechanism.

### B03: The Enumeration March
"First... Second... Third... Finally..."
Detection: Ordinal sequence spanning 3+ paragraphs.
Fix: Integrate the strongest point first. Subsume weaker points into the discussion.

### B04: The Echo Transition
Repeating the last phrase of the previous paragraph as the opening of the next.
Detection: >4 words repeated across a paragraph boundary.
Fix: Allowed once per 2000 words as intentional echo. More than that is a pattern.

### B05: The Question Bridge
"But what does this mean? Let's explore." / "So how do we solve this? The answer lies in..."
Detection: Rhetorical question + self-answer as paragraph transition.
Fix: Delete both sentences. Start the next paragraph with the answer directly.

### B06: The Meta-Narrator
"Now let's turn to..." / "Having established X, we can now examine Y."
Detection: Narrator announcing the next move instead of making it.
Fix: Just make the move. The reader follows structure, not announcements.

### B07: The Pivot Cliché
"But here's where it gets interesting."
Detection: Excitement annotation before a point that should be interesting on its own.
Fix: Delete. If it's interesting, the reader will notice.

---

## Category C: Emotional/Rhetorical Cadences

### C01: The Inspiration Ramp
Sentences getting progressively more emotionally elevated without corresponding evidence elevation.
Detection: Adjective intensity increasing across 4+ sentences without new data.
Fix: Match emotional intensity to evidence strength. Conviction requires proof.

### C02: The Empathy Sandwich
Acknowledgment → reassurance → call to action, repeated identically across sections.
Detection: Same 3-part emotional structure appearing 2+ times.
Fix: Vary the structure. Sometimes lead with the action. Sometimes let the acknowledgment stand alone.

### C03: The Dramatic Fragment Chain
"Not anymore." / "Not this time." / "Not like this."
Detection: 3+ consecutive fragment sentences for dramatic effect.
Fix: One is powerful. Two is pattern. Three is formula.

### C04: The Anaphora Overload
"We need to... We need to... We need to..." extending beyond 3 repetitions.
Detection: Same opening phrase 4+ times consecutively.
Fix: Anaphora earns its place at 2-3 repetitions. Beyond that, find a new construction.

### C05: The False Crescendo
Building intensity toward a conclusion that doesn't deliver anything new.
Detection: Sentence length and emotional language increasing toward a final sentence that restates the opening.
Fix: The ending must go FURTHER than the opening. Not louder — further.

### C06: The Parenthetical Habit
(Like this) appearing in 3+ sentences per 500 words.
Detection: Count parenthetical asides per 500 words.
Fix: Convert to separate sentences or integrate into the main clause.

### C07: The Colon Addiction
"Here's the truth:" / "The answer:" / "One word:" appearing 3+ times per 1000 words.
Detection: Colon-terminated setup phrases.
Fix: Reduce to one per 1000 words. The colon announces; overuse dulls the announcement.

---

## Category D: Genre-Specific Cadences

### D01: The LinkedIn Loop
Short sentence. Line break. Short sentence. Line break. "And that changes everything."
(Extended from cadence.md with additional variants)
Variants: "That's the difference." / "Read that twice." / "This is the way."

### D02: The Thread Cadence
"Thread (1/12):" → numbered listicle with each item as a sentence or two.
Detection: Numbered sequential posts with uniform length.
Fix: Develop 3 points deeply instead of 12 points shallowly.

### D03: The Newsletter Cadence
"Hey [name]," → one anecdote → "Here's what I learned:" → bullet list → CTA.
Detection: Recurring structure across emails.
Fix: Vary the entry. Not every newsletter needs to open with an anecdote.

### D04: The Podcast Transcript Cadence
"So basically what happened was..." / "I mean, it's like..." / "Right? And so..."
Detection: Conversational filler that works in speech but dies in print.
Fix: Remove verbal tics. Tighten the structure. Written casual ≠ transcribed speech.

### D05: The Substack Cadence
Bold claim → "Let me explain." → 5-paragraph essay → subscriber CTA.
Detection: "Let me explain" or equivalent as the second sentence.
Fix: The explanation should make the claim self-evident. Don't announce it.

### D06: The AI Assistant Cadence
"Great question!" → organized response → "I hope this helps!" / "Let me know if you need anything else!"
Detection: Affirmation + structured answer + closing pleasantry.
Fix: Drop the affirmation. Drop the closing. Answer the question.

### D07: The Case Study Cadence
"[Company] was struggling with [problem]. Then they [solution]. Now they [result]."
Detection: Problem-solution-result in 3 sentences, repeated for multiple examples.
Fix: Develop one case deeply. Show the mess, the decisions, the tradeoffs.

---

## Category E: Academic-Specific Cadences

### E01: The Five-Paragraph Ghost
Introduction with thesis → 3 body paragraphs → conclusion restating thesis.
Even in longer papers, this skeleton is visible.
Detection: Thesis in final sentence of intro, repeated in first sentence of conclusion.
Fix: Let the thesis evolve through the paper. The conclusion should go beyond the introduction.

### E02: The Quote Crutch
Block quote → "This shows that..." → Block quote → "This demonstrates..."
Detection: Alternating block quotes and single-sentence interpretations.
Fix: Paraphrase more. Quote only when exact words matter. Interpret at length.

### E03: The Hedge Stack
"It could be argued that it is possible that some evidence might suggest..."
Detection: 3+ hedge terms in a single sentence.
Fix: One hedge per sentence maximum. Be specific about what's uncertain.

### E04: The Source Parade
"Smith (2019) argues... Jones (2020) contends... Lee (2021) finds..."
Detection: 3+ consecutive sentences each opening with a different author citation.
Fix: Synthesize. What do they agree on? Where do they diverge? That's the paragraph.

### E05: The Circular Introduction
Paragraph that returns to its opening claim without having advanced it.
Detection: Final sentence semantically equivalent to first sentence.
Fix: The paragraph must END further than it STARTED.

---

## Category F: Subtle Statistical Patterns

### F01: Vocabulary Ceiling
No word in the passage falls outside the 10,000 most common English words.
Detection: Vocabulary analysis showing zero rare-word usage.
Fix: Introduce 2-3 precise, domain-appropriate uncommon words per 500 words.

### F02: Comma Regularity
Commas appearing at statistically regular intervals (e.g., every 8-10 words).
Detection: Comma interval standard deviation below 3 across 10+ sentences.
Fix: Vary sentence structure. Some sentences with no commas. Some with 3+.

### F03: Conjunction Monotony
"And" is the only conjunction used across 500+ words.
Detection: Count unique conjunctions. Fewer than 3 types in 500 words = monotony.
Fix: Use "but," "yet," "so," "while," "although," "unless," "because" — each earns different logical work.

### F04: Pronoun Density Flatness
"It" / "they" / "this" appearing at uniform density without variance.
Detection: Pronoun frequency per sentence remains constant across 10+ sentences.
Fix: Alternate between naming the subject and using pronouns. Vary referent clarity.

### F05: Perfect Parallelism
Every list item, every comparison, every pair follows identical grammatical structure.
Detection: 4+ parallel structures in 500 words with zero variation.
Fix: Break one parallel for emphasis. Intentional asymmetry signals human craft.

---

## Detection Thresholds (Summary)

| Severity | Threshold |
|---|---|
| **Flag** | Any single pattern detected |
| **Warn** | 3+ patterns from the same category in one piece |
| **Critical** | 5+ patterns from any categories in one piece |
| **Auto-fail** | 3+ Category F (statistical) patterns simultaneously |

---

## Integration

This library extends `references/anti_patterns/cadence.md`. When running
Pass 1 (Diagnostic Scan), check against BOTH the original 9 signatures
AND this expanded library. The expanded library catches patterns that
unsophisticated detectors miss but experienced editors and advanced
AI classifiers identify.
