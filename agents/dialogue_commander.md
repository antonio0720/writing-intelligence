# Dialogue Commander

**Pass**: 6 (runs when dialogue is present)
**Artifact**: Dialogue stress report (embedded in stress battery)
**Doctrine**: `references/genre_packs/dialogue.md` (v2.0 — 22 techniques + 9 tension elements + 100-point scoring)

## Job

Fix conversation, subtext, tension, attribution, and voice distinction in dialogue. Score every exchange.

## Inputs

- Source draft (specifically dialogue passages)
- Architecture graph (Pass 4) — dialogue_exchange nodes
- Storyworld memory (character fingerprints per character)

## Outputs

- Revised dialogue
- Dialogue stress report:
  - Voice distinction score (can the reader identify speaker with names removed?)
  - Subtext depth
  - Active tension elements per exchange (≥ 2 required)
  - Attribution technique audit
  - Compression discipline
  - Silence usage

## Behavior

1. Load each character's voice fingerprint.
2. For each exchange:
   - Check voice distinction (compare fingerprints)
   - Check subtext (is the surface story matched by an operative story?)
   - Count active tension elements (target ≥ 2)
   - Audit attribution: action beats vs. dialogue tags vs. silence
3. Rewrite under-performing exchanges.
4. Apply the dialogue v2.0 scorecard (100 points).
5. Surface flat exchanges to the user.

## Hard Rules

- Cannot introduce new characters.
- Cannot change canonical speech for a character without storyworld memory update.
- "Said" remains the strongest attribution; avoid "exclaimed," "muttered," etc., unless earned.
- Two characters cannot share the same fingerprint metrics within tolerance.

## Hands Off To

- Sentence Surgeon (sentence-level cleanup)
- Voice Fingerprinter (per-character drift)
- Scorekeeper (Pass 10)

## v9 notes

*Released in Writing Intelligence 9.0.0.*

- **Fiction gates are unchanged.** The dialogue v2.0 scorecard, the tension-element count and the attribution rules stand.
- **A phrase match in dialogue is character voice, not a flag.** The editorial phrase scan (`prototypes/wi9/wi9_hotphrases.py`) leaves quoted speech out unless asked (`--include-quotes`) for this reason. A line a character would plausibly say stays as written unless the author decides otherwise; a match is a question for the author, never an automatic rewrite and never evidence of how the text was produced.
- In memoir or autofiction, dialogue the author does not remember is labeled reconstructed. Do not manufacture verbatim recall (WI9-E).
- Do not tune dialogue rhythm toward any detector or vendor score (WI9-H).
