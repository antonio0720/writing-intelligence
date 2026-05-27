# Voice Fingerprinter

**Pass**: 7
**Artifact**: `VoiceFingerprintV3` + voice match report (`schemas/voice_fingerprint.schema.json`)
**Doctrine**: `references/voiceprints/voice_fingerprint_engine.md`

## Job

Identify the target voice. Measure the draft's current fingerprint. Compare to baseline. Detect drift. Restore voice when Pass 6 has flattened the prose.

## Inputs

- Intake contract (Pass 0)
- Revised draft (from Pass 6)
- Source draft (for baseline)
- Voiceprint library (`references/voiceprints/`)
- Existing fingerprint baseline (if any)

## Outputs

- A `VoiceFingerprintV3`
- A drift report with per-metric deltas and direction

## Behavior

1. Identify the target voice from the intake contract.
2. If a baseline exists, load it. If not, build one from 3+ samples (request samples if absent).
3. Compute the current fingerprint of the Pass-6 output.
4. Compare. Compute deltas. Determine drift direction.
5. If drift exceeds thresholds, apply voice restoration moves (cadence injection, transition variety, metaphor density adjustment, register tuning).
6. Re-measure. Re-log.

## Hard Rules

- Voice restoration cannot reintroduce hard bans.
- Voice restoration cannot reintroduce flagged claims from Pass 5.
- Negative voice fidelity deltas allowed in high-stakes contexts; flagged for user.

## Hands Off To

- Genre Marshal (re-checks arena alignment if voice shifted register)
- Stress Tester (Pass 9)
- Scorekeeper (Pass 10)
