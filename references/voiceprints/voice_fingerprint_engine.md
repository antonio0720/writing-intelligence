# Voice Fingerprint Engine

**Purpose**: Upgrade voiceprints from descriptive docs into measurable authorial profiles.

**Schema**: `schemas/voice_fingerprint.schema.json` (`VoiceFingerprintV3`)

**Agent**: Voice Fingerprinter (`agents/voice_fingerprinter.md`)

---

## What v3.0 Adds

v2.0 voiceprints described voices: "cold authority, strategic compression, zero filler." Useful for human readers, opaque to machines. v3.0 measures voices so:

- A scorecard can say *why* voice is weak (cadence uniform, metaphor density low, register mismatched)
- A drift report can detect *which direction* the voice has drifted
- Team voice can be enforced via shared fingerprints
- Character voices in fiction can be measured for distinguishability

## Measured Dimensions

| Metric | Definition | How Measured |
|---|---|---|
| `avg_sentence_length` | Mean words per sentence | Tokenize, divide |
| `sentence_length_std` | Standard deviation of sentence length | Standard formula |
| `avg_paragraph_length` | Mean words per paragraph | Tokenize, divide |
| `paragraph_length_std` | Std dev of paragraph length | Standard formula |
| `compression_ratio` | Fraction of words surviving ruthless edit | Run `compress(20%)`, measure surviving claims |
| `abstraction_tolerance` | Fraction of sentences operating above concrete plane | Concreteness classifier (concrete = named actor / number / image; abstract = otherwise) |
| `metaphor_density` | Metaphors per 500 words | Metaphor classifier |
| `question_frequency` | Questions per 500 words | Count `?` |
| `comma_density` | Commas per 100 words | Count `,` |
| `vocab_tier` | plain / educated / scholarly / rarefied / mixed | Vocabulary classifier |
| `domain_vocab_per_500w` | Domain-specific words per 500 words | Domain dictionary match |
| `transition_top5` | Top 5 transition words/phrases | Frequency count |
| `opening_pattern_repertoire` | Common opening structures | First-sentence pattern extraction |
| `closing_pattern_repertoire` | Common closing structures | Last-sentence pattern extraction |
| `dominant_syntactic_structures` | Top-N syntactic patterns | Parse tree pattern extraction |
| `authority_posture` | 0 (warm) — 100 (dominant) | Warmth/dominance classifier |

## Baseline Construction

Build a baseline from **3+ samples, 500+ words each**. The samples should represent the author writing at their best in their target voice.

Procedure:

1. Tokenize each sample.
2. Compute each metric per sample.
3. Aggregate (mean for continuous metrics; mode for categorical metrics).
4. Record as the canonical fingerprint with `voice_id`.

## Drift Detection

After every compilation, the Voice Fingerprinter (Pass 7) computes the fingerprint of the output and compares to the baseline. Drift is the per-metric delta.

| Metric | Drift Threshold | Action if Exceeded |
|---|---|---|
| avg_sentence_length | ±20% | Surface for review |
| sentence_length_std | ±25% | Surface |
| abstraction_tolerance | ±15% | Surface |
| metaphor_density | ±30% | Surface |
| authority_posture | ±10 points | Surface |
| dominant_syntactic_structures | Top-3 shift | Surface |

Drift `direction` is one of: `closer_to_baseline`, `further_from_baseline`, `stable`.

The Sentence Surgeon's voice impact log (Pass 6) feeds into this. A run with negative voice fidelity delta and drifting fingerprint = Pass 7 must restore.

## Team Voice

Set `team_voice: true` to use the same fingerprint across multiple authors. Useful for:

- Brand voice enforcement
- Multi-author book consistency
- Editorial style guide automation
- Newsletter handoffs between contributors

When team_voice is active, each author's output is fingerprinted and compared. The team voice fingerprint is the canonical reference.

## Custom Voice Build

To build a custom fingerprint, the user provides 3+ samples. The engine returns a `VoiceFingerprintV3` artifact. From then on, that fingerprint can be referenced in any intake contract.

## Definition of Done

The Voice Fingerprinter emits a fingerprint that:

- Validates against `voice_fingerprint.schema.json`
- Carries every measured metric
- Identifies its baseline corpus
- Computes drift against the baseline when invoked at Pass 7
- Surfaces every drift exceeding thresholds

If any of the above fails, Pass 7 has not completed.

---

## v9: What a Fingerprint Is Allowed to Claim (WI9-B)

The fingerprint is a statistical description of consented samples. The v9 reference kernel (`prototypes/wi9/wi9_core.py voice`; released in 9.0.0 proposal) implements a simpler form than the `VoiceFingerprintV3` above: mean sentence length, its spread, type-token ratio and first-person rate, over eligible samples only. The full 16-metric profile in this file is the v3 design; do not describe it as validated.

- **Baseline eligibility.** Three or more distinct samples, 500 or more words each, in **one genre**, each declared `human_authored`, consented, and pinned by sha256. Mixed-genre input is refused rather than averaged. Duplicate samples are refused. The earlier phrase "the author writing at their best" is amended to "the author writing in the target genre as they really write."
- **Drift detection measures change, not origin.** A draft that drifts from the baseline may have been edited by someone else, written on a bad day, or written for a different reader. The drift report asks the author; it does not accuse. Neither a close match nor a far one is evidence of who produced the text.
- **Team voice and character voice** use the same rule: each contributor's baseline needs that contributor's consent. For fiction characters, distinctiveness is a craft measure and is unaffected by v9.
- **Digests and replay.** Store each sample's sha256 in the fingerprint's baseline record so a later reader can tell whether the baseline was built from the files now on disk.
- **Withdrawal.** If a contributor withdraws, remove their baseline and rebuild any team fingerprint without them; do not keep a derived profile of a person who has withdrawn. Policy only: no automated vault enforces this.
- **Not a detector.** Do not report a fingerprint distance as a probability of human or machine authorship, and do not tune a draft to move a distance for its own sake. Change a sentence because the author's meaning or voice calls for it.

The Definition of Done above is unchanged; add one condition: the fingerprint record states the consent basis and the genre of its baseline.
