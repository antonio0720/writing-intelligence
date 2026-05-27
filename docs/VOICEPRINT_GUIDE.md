# Voiceprint Guide

How to build a measurable voice fingerprint that meets the v3.0 standard.

## Why Measurable

v2.0 voiceprints described voices: "cold authority, strategic compression." That's useful for human readers, useless for drift detection, team voice enforcement, character voice distinguishability, and machine consumption.

v3.0 voice fingerprints are quantitative. Same descriptive flavor, plus measurements.

## The Fingerprint Schema

See `schemas/voice_fingerprint.schema.json`.

Required measurements:

- `avg_sentence_length` (words per sentence)
- `sentence_length_std` (std dev)
- `vocab_tier` (plain / educated / scholarly / rarefied / mixed)

Strongly recommended:

- `avg_paragraph_length`
- `paragraph_length_std`
- `compression_ratio` (fraction surviving ruthless edit)
- `abstraction_tolerance` (fraction above concrete plane)
- `metaphor_density` (per 500 words)
- `question_frequency` (per 500 words)
- `comma_density` (per 100 words)
- `domain_vocab_per_500w`
- `transition_top5`
- `opening_pattern_repertoire`
- `closing_pattern_repertoire`
- `dominant_syntactic_structures`
- `authority_posture` (0-100)

## How to Build

1. **Collect baseline samples**: minimum 3 samples, 500+ words each. Choose samples that represent the author writing at their best in the target voice. Avoid: outliers, content-driven format changes, drafts the author would disown.

2. **Tokenize and measure**: compute each metric per sample. Aggregate (mean for continuous; mode for categorical).

3. **Describe**: in 1-2 paragraphs of plain language, describe the voice using the measurements. The description is the human-readable summary; the measurements are the machine layer.

4. **Audit against the descriptions of existing voiceprints**: confirm the new voiceprint is distinguishable from the existing 8.

5. **Author 5 sample outputs** demonstrating the voice across different prompts.

6. **Open an RFC** per `governance/RFC_PROCESS.md`. Required attachments: measurements, description, 5 sample outputs, distinguishability audit.

## Distinguishability Test

A new voiceprint must be distinguishable from every existing one on at least 3 measured metrics. If two voiceprints converge within tolerance on most metrics, they are functionally the same voice and should not both exist.

## Building a Custom Voice for a Single User

If a user wants their own voice (not a community-contributed pack), they don't need an RFC. They just need samples:

```
Build a custom voice fingerprint from these 3 samples. Save as
my baseline. Use this for all subsequent work unless I override.

[paste samples]
```

The fingerprint lives in the user's session memory (or persistent storage in builder integrations).

## Voice Drift Detection

Once a baseline exists, the Voice Fingerprinter (Pass 7) computes the fingerprint of every output and compares. Drift thresholds (from `references/voiceprints/voice_fingerprint_engine.md`):

- avg_sentence_length: ±20%
- sentence_length_std: ±25%
- abstraction_tolerance: ±15%
- metaphor_density: ±30%
- authority_posture: ±10 points
- dominant_syntactic_structures: top-3 shift

Drift `direction`:

- `closer_to_baseline`
- `further_from_baseline`
- `stable`

## Team Voice

Set `team_voice: true` to apply a fingerprint across multiple authors. Useful for: brand voice enforcement, multi-author book consistency, newsletter handoffs.

## Character Voices in Fiction

In storyworld work, each character carries their own fingerprint. The Dialogue Commander (Pass 6) uses these to verify "can you tell who's speaking with names removed?"

Each character fingerprint must be distinguishable from every other character in the storyworld on at least 3 metrics. Two characters whose fingerprints converge are dialogue failures and must be redrawn.

## Existing Voiceprints to Read

- `sovereign_commander.md` — cold authority
- `literary_recursive.md` — layered, image-driven
- `sermon_black_church.md` — cadence, dignity
- `investor_precision.md` — data-forward, risk-aware
- `founder_manifesto.md` — vision-heavy
- `academic_rigorous.md` — evidence-first
- `casual_sharp.md` — conversational intelligence
- `courageous_builder.md` — operator persona (v3.0 new)

## Author

Antonio T. Smith Jr. / Density6 LLC
