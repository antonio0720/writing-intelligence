# Sentence Surgery Regression Cases — v3.0

These cases stress-test the Sentence Surgeon (Pass 6). Each case has a known sentence-level failure mode. The Surgeon must repair without flattening voice.

## Case SS-01 — Hard Ban Cluster

**Input**: "Here's the thing — at the end of the day, this is a game-changer. Let's be clear: it's not just innovative, it's revolutionary."

**Expected transformations**:
- Remove "Here's the thing"
- Remove "at the end of the day"
- Replace "game-changer" with concrete description
- Remove "Let's be clear"
- Replace "not just innovative, it's revolutionary" with concrete claim

**Voice impact**: should be `increased_fidelity` after restoration.

## Case SS-02 — Cadence Repetition (LinkedIn pattern)

**Input**: "Most people don't realize this. The truth is simple. You need to change. Today is the day. Start now."

**Expected detections**: LinkedIn cadence signature (5 short declaratives, same length, same opening pattern). Should inject variance.

## Case SS-03 — Adverb Stack

**Input**: "She quickly grabbed the keys, slowly turned around, and gently closed the door behind her."

**Expected transformations**: cut all three adverbs unless their removal changes meaning. Replace with action that conveys the manner inherently.

## Case SS-04 — Em Dash Abuse

**Input**: "The result — which we hadn't expected — was clear — we had won — but the cost — measured in months — was high."

**Expected transformations**: collapse to commas or restructure; preserve at most one em dash if it improves timing.

## Case SS-05 — "I" Opening (Non-Personal Essay)

**Input** (memo): "I believe that we should pivot to a different strategy."

**Expected transformations**: Hard-ban "I" as first word of a memo (not a personal essay). Rewrite without weakening claim.

## Case SS-06 — Compression Without Loss

**Input** (2 paragraphs, 400 words): Verbose argument with one core claim and three supporting facts.

**Expected transformations**: compress to 200 words (50%) while preserving claim and all three facts. Log every cut.

## Case SS-07 — Voice Restoration After Cleanup

**Input**: Source voice = sovereign_commander. Pass 6 stripped slop but introduced a flat, neutral register.

**Expected transformations**: Restore avg sentence length variance, compression ratio, authority posture. Voice impact should net `increased_fidelity`.

## Case SS-08 — Rhetorical Question Earned vs. Unearned

**Input** (3 rhetorical questions stacked): "What if I told you the secret to success? Are you ready to change your life? Would you take the leap?"

**Expected transformations**: Cut at least 2 of 3. Keep at most one if it opens genuine tension; rewrite if it's manufactured.

## Case SS-09 — Universal Quantifier Soften (from Pass 5)

**Input**: "All effective leaders communicate directly."

**Expected transformations**: replace "All" with scoped equivalent ("Many" / "Effective leaders typically…") per Pass 5 decision.

## Case SS-10 — Inflated Verb Replace (from Pass 5)

**Input**: "We will leverage cutting-edge technology to revolutionize the customer experience."

**Expected transformations**: replace "leverage cutting-edge technology" with concrete tech name; replace "revolutionize" with specific change ("reduce wait time by 40%," etc.).

## Scoring

Each case scored on:

- All expected detections triggered
- Voice impact net non-negative
- Word count delta within compression target (when specified)
- No new hard-bans introduced
- Rewrite log entry per transformation

Pass rate ≥ 90% required for v3.0 release gate.
