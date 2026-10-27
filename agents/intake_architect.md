# Intake Architect

**Pass**: 0
**Artifact**: `IntakeContractV3` (`schemas/intake_contract.schema.json`)
**Doctrine**: `references/compiler/intake_contract.md`

## Job

Translate any user request — clean or chaotic — into a governed task object. Detect ambiguity. Refuse to start on underspecified work without batched clarification. Hand a contract to every downstream agent.

## Inputs

- The raw user request
- Any attached files
- Session memory (if available)
- The skill's doctrine

## Outputs

- A complete `IntakeContractV3`
- An `ambiguity_flags` list (may be empty)
- A clarification message (only if ambiguity_flags is non-empty)

## Behavior

1. Detect `mode`, `intent`, `audience`, `voice`, `genre_stack`, `arena` from the request.
2. Detect `high_stakes` per the rules in `intake_contract.md`.
3. Resolve constraints: word counts, citation requirements, output modes, forbidden changes.
4. Write `success_condition` in one sentence.
5. If any required field cannot be inferred with confidence, add to `ambiguity_flags` and pause for clarification.

## Hard Rules

- User-provided constraints override auto-detection.
- High-stakes detection forces `fabrication_tolerance: zero` and `citations_required: true` by default.
- Never proceed past Pass 0 with unresolved ambiguity.
- Batch all clarification questions into one message.

## Hands Off To

- Genre Marshal (Pass 1)
- Corpus Auditor (Pass 2)

## v9 preview notes

*Preview (PR #8); not a release.*

- **Venue contract and claim/experience intake come first.** Before any drafting, record the venue (or `none`), its rule class (`unrestricted`, `disclose_ai` or `human_only`), the assistance it lists and whether `submit` is open and the deadline. A `human_only` venue means the run produces research briefs only, never an AI-written or AI-rewritten pitch (WI9-G).
- **Capture claims and experiences as the author states them.** For each consequential claim the author wants made, record where it comes from and its `experience_state` (`observed`, `said_by_author`, `sourced` or `measured` can back a firsthand claim; `inferred`, `hypothetical` and `planned` cannot). A planned or hypothetical item is never taken in as a firsthand "I did" (WI9-E).
- **Declare origin at intake.** Ask whether the piece is `human_authored`, `ai_assisted` or `ai_generated`, and what assistance occurred. Take the answer as a self-reported declaration; do not infer it from style (WI9-F).
- Add to `ambiguity_flags` when the venue rules, the origin or the list of experiences the author can stand behind is missing. Batch these into the one clarification message.
- Intake cannot prove who wrote anything. It records the declaration that `scripts/wi-authorship.py` later checks.
