# Your voice baseline

**For:** every person who uses Writing Intelligence v9. **Ships with v9:** no samples at all. Each writer measures their own voice from their own writing, kept on their own machine.

A voice baseline is a few numbers taken from writing you did yourself: sentence length and its spread, vocabulary range, how often you write in the first person, and how you argue — how often you qualify, intensify or disagree, how much concrete detail you use, and whether you reach for an example, a reason, a concession or a question. v9 compares an edit against them to tell you when an edit has drifted from how you write. A baseline describes your style. It never proves who wrote a text, and v9 never uses it that way.

## 1. Choose your samples

- At least three pieces you wrote yourself, without a model drafting them or substantially rewriting them.
- Each at least 500 words.
- All the same kind of writing (essay, speech, letters, fiction). Make a separate baseline for each kind.
- Pieces from different occasions describe you better than three parts of one piece.

## 2. Keep them private

Put them in a folder outside any repository, for example `~/wi9-private/voice/essay/`, as plain UTF-8 text files. Nothing in v9 uploads, commits or bundles them, and a test in this repository fails if a voice manifest or review is ever committed.

## 3. Describe them in `voice.json`, in the same folder

```json
{
  "samples": [
    {"id": "essay-1", "path": "essay-1.txt", "genre": "essay",
     "origin": "human_authored", "consent": true,
     "sha256": "<output of: shasum -a 256 essay-1.txt>"}
  ]
}
```

`origin` and `consent` are your own declaration about your own writing. The `sha256` fingerprint lets v9 notice if a file changes after you described it.

## 4. Measure

```bash
wi authorship voice --root ~/wi9-private/voice/essay --input voice.json
```

`REVIEW` (exit 0) returns per-sample and mean measurements, a `baseline_digest`, and `held_out_stability`: each sample is left out in turn and checked against the band built from the others. A measure marked `stable: false` is one your own samples do not agree on, so drift on it later tells you little; a sample by somebody else mixed in usually shows up here. `HOLD` (exit 3) names each problem: `VOICE_SAMPLE_SHORT`, `VOICE_SAMPLE_COUNT`, `VOICE_GENRE_MIX`, `VOICE_DIGEST_MISMATCH`, `VOICE_DUPLICATED_SAMPLE`, `VOICE_SAMPLES_TOO_SIMILAR` (near-copies of one passage describe that passage, not you), `VOICE_SOURCE_INELIGIBLE`.

## 5. Review it yourself

Read the measurements. Then record your decision:

```bash
wi authorship voice-review --root ~/wi9-private/voice/essay --input voice.json \
  --decision approve --note "Sentence length fits; first-person rate is lower than I expected"
```

This writes `voice-review-<digest>.json` into the same private folder, readable only by you. It is bound to the exact samples: change one and the digest changes, so the old review no longer applies. A review is never overwritten. `--decision reject` is recorded too, and is not an approval. A baseline that does not qualify cannot be approved.

## 6. Compare a draft with your baseline

```bash
wi authorship voice-compare --root ~/wi9-private/voice/essay --input voice.json --text draft.txt
```

Each measure outside your band is listed with its direction and whether that measure is stable for you. Drift is a question — perhaps the draft needs a qualifier you would use, perhaps the occasion is different. Sitting inside every band proves nothing about who wrote the draft: a careful imitation can match these numbers, and v9 never treats a match as authorship.

## Withdrawing

Delete the folder. v9 keeps no other copy.
