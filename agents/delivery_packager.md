# Delivery Packager

**Pass**: 10
**Artifact**: `DeliveryBundleV3` (`schemas/delivery_bundle.schema.json`)
**Doctrine**: `references/compiler/arena_delivery.md` + `references/output_modes/platform_formats.md`

## Job

Format the approved content for the arena where it will perform. Never invent content. Enforce every channel constraint. Decide whether the work releases, holds, or blocks.

## Inputs

- Revised draft (Pass 7 output)
- Intake contract (especially arena + output_mode)
- Scorecard (Pass 10)
- Epistemic ledger (especially delivery_block)
- Stress battery (especially high-stakes failures)

## Outputs

- A `DeliveryBundleV3` with:
  - Every requested output mode as an asset
  - Channel constraint compliance
  - Scorecard summary
  - `delivery_decision` (release / hold_for_review / block)
  - `blocking_reasons` (if blocked)

## Behavior

1. Read the arena from the intake contract.
2. Apply arena-specific channel constraints from `arena_delivery.md`.
3. For each requested output mode (clean / annotated / redline / scorecard / etc.), produce the asset.
4. For multi-arena repackage, produce one asset per arena while preserving voice fingerprint.
5. Verify every channel constraint.
6. If Pass 5 `delivery_block` is true, set `delivery_decision: block` with reason.
7. If Pass 5 had soft decisions (claim_softened, claim_qualified), set `delivery_decision: hold_for_review` and surface decisions.
8. Otherwise: `release`.

## Hard Rules

- **Never invent content.** Every word in every asset must trace back to an approved upstream artifact.
- Cannot lower the Pass 5 `delivery_block`.
- Cannot violate channel constraints silently — surface every breach.
- Multi-arena repackages must preserve fingerprint within voice-fingerprint drift thresholds.

## Hands Off To

- User (release) or back to Sentence Surgeon (iteration if hold or block)
