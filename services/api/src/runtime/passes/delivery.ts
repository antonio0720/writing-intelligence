// Pass 10 (delivery half) — assemble the DeliveryBundleV3 and decide release/hold/block.
import type {
  DeliveryBundleV3, IntakeContractV3, EpistemicLedgerV3, Scorecard, Arena, OutputMode,
} from "../../types";
import type { ArenaCheck } from "./arena";
import type { StressReport } from "./stress";
import { wordCount } from "../text";

// Which output modes map to a delivery-bundle asset mode.
const ASSET_MODES: Record<string, DeliveryBundleV3["assets"][number]["mode"] | undefined> = {
  clean: "clean",
  annotated: "annotated",
  redline: "redline",
  scorecard: "scorecard",
  violations: "violations",
  "next-pass": "next-pass",
  "scene-audit": "scene-audit",
  "epistemic-ledger": "epistemic-ledger",
  "voice-drift-report": "voice-drift-report",
  "benchmark-result": "benchmark-result",
};

export function buildDelivery(params: {
  intake: IntakeContractV3;
  arena: Arena;
  arenaCheck: ArenaCheck;
  clean_text: string;
  scorecard: Scorecard;
  ledger: EpistemicLedgerV3;
  stress: StressReport;
}): DeliveryBundleV3 {
  const { intake, arena, arenaCheck, clean_text, scorecard, ledger, stress } = params;

  const decision = decide(scorecard, ledger, stress);
  const requested = intake.constraints.output_mode ?? (["clean"] as OutputMode[]);
  const assets = buildAssets(requested, { clean_text, scorecard, ledger, stress });

  return {
    task_id: intake.task_id,
    version: "3.0.0",
    arena,
    assets,
    channel_constraints: arenaCheck.constraints,
    constraints_satisfied: arenaCheck.satisfied,
    scorecard_summary: {
      prose_quality: scorecard.prose_quality,
      epistemic_integrity: scorecard.epistemic_integrity,
      arena_fit: scorecard.arena_fit,
      v3_composite: scorecard.v3_composite,
    },
    delivery_decision: decision,
    blocking_reasons: stress.blocking_reasons,
  };
}

function decide(
  scorecard: Scorecard,
  ledger: EpistemicLedgerV3,
  stress: StressReport,
): "release" | "hold_for_review" | "block" {
  if (ledger.delivery_block || stress.blocking_reasons.length > 0) return "block";
  if (scorecard.v3_composite < 70 || stress.soft_flags.length > 0 || scorecard.auto_fail_triggered) {
    return "hold_for_review";
  }
  return "release";
}

function buildAssets(
  requested: OutputMode[],
  data: { clean_text: string; scorecard: Scorecard; ledger: EpistemicLedgerV3; stress: StressReport },
): DeliveryBundleV3["assets"] {
  const assets: DeliveryBundleV3["assets"] = [];
  const seen = new Set<string>();

  // A clean asset is always present so the delivery is never empty.
  const modes: OutputMode[] = requested.includes("clean") ? requested : ["clean", ...requested];

  for (const mode of modes) {
    const assetMode = ASSET_MODES[mode];
    if (!assetMode || seen.has(assetMode)) continue;
    seen.add(assetMode);

    switch (assetMode) {
      case "clean":
      case "annotated":
      case "next-pass":
      case "scene-audit":
        assets.push(textAsset(assetMode, data.clean_text));
        break;
      case "redline":
        assets.push(textAsset("redline", data.clean_text));
        break;
      case "scorecard":
        assets.push(jsonAsset("scorecard", data.scorecard));
        break;
      case "epistemic-ledger":
        assets.push(jsonAsset("epistemic-ledger", data.ledger));
        break;
      case "violations":
        assets.push({
          mode: "violations",
          content: JSON.stringify({ blocking_reasons: data.stress.blocking_reasons, soft_flags: data.stress.soft_flags }, null, 2),
          format: "json",
        });
        break;
      case "voice-drift-report":
      case "benchmark-result":
        // These modes are produced by their own endpoints, not the compile bundle.
        break;
    }
  }
  return assets;
}

function textAsset(mode: DeliveryBundleV3["assets"][number]["mode"], content: string): DeliveryBundleV3["assets"][number] {
  return { mode, content, format: "markdown", word_count: wordCount(content), char_count: content.length };
}

function jsonAsset(mode: DeliveryBundleV3["assets"][number]["mode"], obj: unknown): DeliveryBundleV3["assets"][number] {
  const content = JSON.stringify(obj, null, 2);
  return { mode, content, format: "json", char_count: content.length };
}
