// Pass 10 (scoring half) — deterministic composite scorecard.
// Scores whatever text's diagnostics are handed in: /compile scores the CLEANED asset,
// /score scores the RAW draft. Same math, different input — honest by construction.
import type { Diagnostics } from "./diagnostic";
import type { EpistemicLedgerV3, Scorecard } from "../../types";
import type { ArenaCheck } from "./arena";
import { round } from "../text";

function clamp(n: number, lo = 0, hi = 100): number {
  return Math.max(lo, Math.min(hi, n));
}

export function score(params: {
  diagnostics: Diagnostics;
  ledger: EpistemicLedgerV3;
  arena: ArenaCheck;
  high_stakes: boolean;
  hasClaims: boolean;
  // clean_words / raw_words for a rewrite. 1 = nothing deleted (or no rewrite happened).
  retention_ratio?: number;
}): Scorecard {
  const { diagnostics: d, ledger, arena, high_stakes } = params;
  const retention = params.retention_ratio ?? 1;

  // --- Prose quality (100) ---
  let prose = 100;
  prose -= d.hard_ban_hits * 8;
  prose -= d.soft_ban_hits * 1.5;
  prose -= d.passive_voice_ratio * 20;
  prose -= Math.max(0, 5 - d.sentence_length_variance) * 3; // reward burstiness
  prose -= Math.max(0, d.abstract_noun_density - 8) * 1.5;
  if (d.em_dash_overuse) prose -= 5;
  if (d.ai_opener_detected) prose -= 6;
  // Deletion debris: rule-based cutting can leave dangling seams and stubby fragments.
  // A well-formed human draft scores ~0 here; an aggressively gutted rewrite pays for it.
  prose -= d.grammar_seam_per_100w * 4;
  prose -= d.fragment_ratio * 20;
  // Deletion aggressiveness: a rule-based rewrite that removed a large share of the words
  // carries editorial risk a human would smooth. Zero when nothing was cut.
  const deletion = Math.max(0, 1 - retention);
  prose -= deletion * 60;
  prose = clamp(prose);

  // --- Epistemic integrity (100) ---
  const summary = ledger.summary;
  let epistemic: number;
  if (!summary || summary.total_claims === 0) {
    epistemic = 85; // nothing checkable asserted — neutral-good
  } else {
    epistemic = 100;
    epistemic -= summary.missing_source_count * 12;
    epistemic -= summary.unsafe_count * 30;
    epistemic -= summary.fabrication_blocks * 20;
    epistemic = clamp(epistemic);
  }
  if (ledger.delivery_block) epistemic = Math.min(epistemic, 60);

  // --- Arena fit (100) ---
  let arenaFit = 100 - arena.violations.length * 20;
  arenaFit = clamp(arenaFit);

  // --- Automatic fail conditions (cap at 65) ---
  const auto_fail_reasons: string[] = [];
  if (d.hard_ban_hits >= 3) auto_fail_reasons.push("3+ hard-ban phrases detected.");
  if (d.perplexity_flatness_run >= 5) auto_fail_reasons.push("Perplexity flatness across 5+ consecutive sentences.");
  const unsupportedUniversal = ledger.claims.some((c) => c.universal_quantifier_flag && c.source_status === "missing");
  if (unsupportedUniversal) auto_fail_reasons.push("Argument contains an unsupported universal claim.");
  if ((summary?.fabrication_blocks ?? 0) > 0) auto_fail_reasons.push("Fabricated/unsafe citation or statistic detected.");
  if (high_stakes && summary && summary.total_claims === 0 && params.hasClaims) {
    auto_fail_reasons.push("High-stakes domain with unclassified claims.");
  }
  const auto_fail_triggered = auto_fail_reasons.length > 0;

  // --- Composite (0-100) ---
  const weights = high_stakes
    ? { prose: 0.35, epistemic: 0.4, arena: 0.25 }
    : { prose: 0.5, epistemic: 0.2, arena: 0.3 };
  let composite = prose * weights.prose + epistemic * weights.epistemic + arenaFit * weights.arena;
  composite = clamp(composite);

  if (auto_fail_triggered) {
    prose = Math.min(prose, 65);
    composite = Math.min(composite, 65);
  }

  return {
    prose_quality: round(prose, 1),
    epistemic_integrity: round(epistemic, 1),
    arena_fit: round(arenaFit, 1),
    v3_composite: round(composite, 1),
    auto_fail_triggered,
    auto_fail_reasons,
    diagnostics: {
      hard_ban_hits: d.hard_ban_hits,
      passive_voice_ratio: d.passive_voice_ratio,
      sentence_length_variance: d.sentence_length_variance,
      abstract_noun_density: d.abstract_noun_density,
      em_dash_overuse: d.em_dash_overuse,
      ai_opener_detected: d.ai_opener_detected,
    },
  };
}
