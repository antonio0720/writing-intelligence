# Voice Drift Test Cases — v3.0

These cases stress-test the Voice Fingerprinter (Pass 7). Each case provides a baseline fingerprint, a target output, and the expected drift direction.

## Case VOICE-DRIFT-01 — Sovereign Commander to Casual

**Baseline**: `sovereign_commander` — avg sentence length 18, std 14, authority_posture 85, abstraction_tolerance 0.3.

**Output**: A draft rewritten in casual_sharp voice without explicit user permission.

**Expected detection**: drift direction `further_from_baseline` on `authority_posture` (drop > 20 points), `avg_sentence_length` (drop > 25%), `compression_ratio` (drop). Pass 7 should restore or flag.

## Case VOICE-DRIFT-02 — Founder Manifesto Flattening

**Baseline**: `founder_manifesto` — high metaphor_density (6.0/500w), authority_posture 80, vocab_tier mixed.

**Output**: A draft post-Pass-6 with metaphor_density dropped to 1.5 and authority_posture dropped to 60.

**Expected detection**: drift direction `further_from_baseline` on metaphor_density (>30%) and authority_posture (>10 points). Sentence Surgeon's rewrite log should show metaphor removals tagged `decreased_fidelity`.

## Case VOICE-DRIFT-03 — Academic to Activist

**Baseline**: `academic_rigorous` — comma_density 5.5/100w, abstraction_tolerance 0.55, question_frequency 0.5/500w.

**Output**: A draft with comma_density dropped to 2.1, question_frequency up to 3.0, exclamations introduced.

**Expected detection**: drift on comma_density (>25%), question_frequency (>30%). Pass 7 should restore academic register.

## Case VOICE-DRIFT-04 — Character Voice Convergence (Fiction)

**Baseline**: Two characters, A and B, with distinct fingerprints.

**Output**: Dialogue where their fingerprints converge within tolerance on avg_sentence_length, dominant_syntactic_structures, and authority_posture.

**Expected detection**: Dialogue Commander flags the convergence. Voice distinction score drops below 70.

## Case VOICE-DRIFT-05 — Cross-Arena Drift

**Baseline**: One voice fingerprint applied to a memo.

**Output**: Cross-arena repackage (memo → LinkedIn → Twitter → YouTube → newsletter) where fingerprint drifts on each arena.

**Expected detection**: Delivery Packager flags each arena's drift. Successful runs preserve fingerprint within tolerance across all arenas.

## v9 preview rules: consented samples (proposal — PR #8)

Drift is measured against a baseline. Under the v9 proposal a *personal* baseline is evidence only when it meets these rules; otherwise the case is not run against an individual author.

## Case VOICE-DRIFT-06 — Baseline Without Consent

**Baseline**: Samples from an author who has not consented to their use.

**Expected**: no personal voiceprint is built. The run uses a stated genre voice instead and says so.

## Case VOICE-DRIFT-07 — Baseline Too Thin

**Baseline**: Two samples, or three samples under 500 words each.

**Expected**: `VOICE_BASELINE_INSUFFICIENT` (advisory in the authorship checker). A personal voiceprint needs at least three consented, human-authored samples of at least 500 words, in the genre being drifted-tested. Short-sample statistics are not reported as a fingerprint.

## Case VOICE-DRIFT-08 — Baseline Contains Assisted Text

**Baseline**: A sample that was model-drafted and lightly edited, declared `human_authored`.

**Expected**: the declaration is recorded as self-reported; it cannot be authenticated. The sample's presence cannot raise a finding about who wrote the new draft.

## Case VOICE-DRIFT-09 — Style Match Cannot Change Origin

**Baseline**: A strong, consented voiceprint.

**Output**: An AI-generated draft revised until it matches the voiceprint closely.

**Expected**: origin stays `ai_generated` or `ai_assisted`. A close match is not authorship; it does not clear a human-only venue. Drift magnitude can be reported; it cannot be offered as provenance.

## Case VOICE-DRIFT-10 — The Author Reviews

**Expected**: the voiceprint and each restoration are reviewed by the author; a measurement alone does not decide "that sounds like me".

Per-genre note: samples in one genre are not a baseline for another. Statistics only; no authentication; no corpus of consented author samples exists yet, so none of VOICE-DRIFT-06 to 10 has been run against real data (WI9-03 is a prototype).

## Scoring

Each case scored on:

- Correct drift direction identified (yes / no)
- Correct dimension identified (yes / no)
- Restoration action proposed (yes / no)
- Drift magnitude reported accurately (within ±10%)

Pass rate ≥ 80% required for v3.0 release gate.
