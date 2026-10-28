# Custom Voiceprint Builder

## Purpose

Build a unique voiceprint from a writer's existing samples. This is the
highest-leverage voice-fidelity tool in the system. A custom voiceprint
produces output that sounds like a specific person, built only from samples
that person supplied and consented to. It is a craft instrument, not a way
to make a document evade a detector or misrepresent who wrote it
(`references/v4/NON_GOALS.md`).

---

## Requirements

- Minimum 3 writing samples from the same author
- Minimum 500 words per sample (1,000+ preferred)
- Samples should represent the author's natural voice, not their most polished work
- Samples from different dates/contexts are better than samples from one session

---

## Extraction Protocol

### Step 1: Sentence Metrics

For each sample, compute:

- **Mean sentence length** (words)
- **Sentence length standard deviation**
- **Minimum sentence length**
- **Maximum sentence length**
- **Percentage of sentences ≤8 words**
- **Percentage of sentences ≥25 words**

Average across samples. This becomes the cadence target.

### Step 2: Paragraph Metrics

- **Mean paragraph length** (sentences)
- **Paragraph length standard deviation**
- **Frequency of 1-sentence paragraphs**
- **Frequency of 6+ sentence paragraphs**
- **Most common opening word/structure per paragraph**

### Step 3: Vocabulary Profile

- **Vocabulary tier**: Count unique words per 500 words. Below 150 = accessible.
  150-200 = standard. Above 200 = elevated.
- **Favorite verbs**: Top 10 non-auxiliary verbs by frequency
- **Favorite adjectives**: Top 5 (if any — sparse adjective use is a marker)
- **Favorite transitions**: How does the author move between ideas?
- **Domain-specific terms**: Words that signal the author's field or interest
- **Avoided words**: Common words the author never uses (this is a strong fingerprint)
- **Contraction frequency**: Percentage of possible contractions that ARE contracted

### Step 4: Structural Patterns

- **Opening preference**: How does the author typically begin a piece?
  (Scene, claim, question, anecdote, data, declaration)
- **Closing preference**: How do pieces end?
  (Implication, challenge, image, question, quiet close, action step)
- **Evidence integration**: Does the author front-load evidence, weave it, or append it?
- **Counterargument style**: Concede-and-pivot? Dismiss? Steelman? Ignore?
- **List usage**: Does the author use bullet points, inline lists, or never lists?

### Step 5: Personality Markers

- **Humor frequency**: How often does humor appear? What type?
  (Dry, observational, self-deprecating, dark, absurdist, none)
- **Question frequency**: How often does the author ask questions?
  (Never, rarely, frequently as rhetorical device, frequently as genuine inquiry)
- **First person frequency**: How often does "I" appear per 1000 words?
- **Emotional display**: Does the author name emotions directly or show them through action/evidence?
- **Certainty level**: Does the author hedge or declare? Where on the spectrum?
- **Formality band**: On a 1-10 scale (1 = text message, 10 = legal brief), where does the author sit?

### Step 6: Distinctive Tics

Every writer has patterns they don't consciously control:

- **Punctuation habits**: Heavy comma user? Colon lover? Dash-dependent? Semicolon-friendly?
- **Sentence starters**: Does the author favor certain opening words? ("The," "It," "She," proper nouns?)
- **Paragraph enders**: Does the author end paragraphs with questions? Short sentences? Long ones?
- **Favorite constructions**: "Not X but Y"? "The kind of X that Y"? "What Z really means is..."?
- **Rhythm signature**: Is there a consistent short-long or long-short pattern?

---

## Output Format

Compile findings into a voiceprint file matching the format of existing
voiceprints in `references/voiceprints/`:

```markdown
# Voiceprint: [Author Name / Alias]

## Identity
[One paragraph capturing the essence of this voice]

## Parameters
[Table with all 8 dimensions]

## Sentence Characteristics
[Metrics and patterns]

## Paragraph Characteristics
[Metrics and patterns]

## Vocabulary
[Tier, favorites, avoided words]

## Distinctive Markers
[5-7 unique identifiers]

## Anti-Patterns for This Voice
[Things this author would NEVER do]
```

---

## Calibration Test

After building the voiceprint, write a 200-word passage using it. Then:

1. Place it alongside the original samples
2. Check: Could a reader familiar with this author's work believe this passage
   came from the same person?
3. If not, identify which parameters are off and adjust

---

## Ongoing Refinement

As more samples become available:
- Recalculate metrics with larger corpus
- Identify seasonal or contextual voice shifts (the author may write differently
  in emails vs. essays vs. fiction)
- Build sub-voiceprints for different contexts if needed
- Track vocabulary evolution over time

---

## Integration

Once a custom voiceprint is built:
1. Save it to `references/voiceprints/custom_[name].md`
2. Reference it in Pass 0 (Mission Lock) when the author is the intended voice
3. Apply it in Pass 4 (Voice Restoration) after cleanup
4. Use it as the calibration target in Pass 5 (Stress Test) — every sentence
   must be plausible as this author's work

---

## v9: Voice Is Evidence (WI9-B)

In v9 a voiceprint is a measurement of a person's consented writing. It is not a costume and not a proof of who wrote a given text. The experimental reference kernel (`prototypes/wi9/wi9_core.py voice`, PR #8 proposal, not a release) enforces the minimums below; the withdrawal and vault steps are policy this file asks for, not features that exist yet (WI9-02 and WI9-03 are PLANNED and PROTOTYPE, and no consented author corpus has been collected).

### Eligibility of a sample

A sample counts only if all of these are true. The kernel records them per sample and returns HOLD for any that fails:

- **Human-authored origin** (`origin: human_authored`), declared by the person. A paragraph a model wrote and the author lightly edited is not a voice sample, however it reads. This is a self-declaration; nothing authenticates it.
- **Explicit consent** (`consent: true`) from the person whose voice it is, for this use. Writing found online, a colleague's emails or a deceased author's papers do not qualify by being available.
- **A pinned sha256 digest** of the exact file, so a later edit to the sample is detected (`VOICE_DIGEST_MISMATCH`).
- **At least 500 words** each, and **at least three distinct samples** per baseline. The requirement above is **per genre**: a baseline mixing, say, a eulogy and a grant narrative is refused (`VOICE_GENRE_MIX`). Build one voiceprint per genre, each with three or more samples of 500 or more words.

One caution: choose samples that show how the author actually writes, including the plain and unfinished-feeling stretches. Selecting only the most polished pieces produces a profile of the editor, not the author.

### What a voiceprint may and may not do

- **Similarity is a diagnostic.** Closeness to the baseline means the draft resembles the samples. It does not mean the author wrote it, and distance does not mean someone else did. Use it to find where an edit drifted from the author's habits, then ask the author.
- **No voice theft.** Do not build a voiceprint of a person who has not consented, and do not use any voiceprint to write something a venue requires the person to have written themselves. A human-only venue gets a research brief at most (principle WI9-G); the submission copy must be the person's own.
- **A voice does not change the origin label.** `human_authored`, `ai_assisted` and `ai_generated` are separate declarations (WI9-F); text produced in the author's voice by a model stays AI-generated.
- **Measure, then ask.** A voiceprint proposes edits that the author accepts or rejects; it does not authorize publication.

### Withdrawal

The author may withdraw consent at any time. On withdrawal: stop using the voiceprint, delete the derived profile and any copied sample text held outside the author's own files, and note the date in the voiceprint's header. Past drafts already delivered are not rewritten silently; list them so the author can decide. Because no vault exists yet, this is a manual obligation on whoever holds the files.
