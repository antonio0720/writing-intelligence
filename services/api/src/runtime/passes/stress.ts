// Pass 9 — Adversarial Stress Battery. Reader / editor / skeptic / detector checks that
// contribute blocking reasons. Deterministic; operates on the cleaned draft + upstream artifacts.
import type { Diagnostics } from "./diagnostic";
import type { EpistemicLedgerV3 } from "../../types";
import type { ArenaCheck } from "./arena";

export interface StressReport {
  blocking_reasons: string[];
  soft_flags: string[];
}

export function runStress(params: {
  diagnostics: Diagnostics;      // diagnostics of the CLEANED text
  ledger: EpistemicLedgerV3;
  arena: ArenaCheck;
  ambiguity_flags: string[];
}): StressReport {
  const { diagnostics, ledger, arena, ambiguity_flags } = params;
  const blocking_reasons: string[] = [];
  const soft_flags: string[] = [];

  // Skeptic / detector: epistemic block is a hard blocker.
  if (ledger.delivery_block) {
    blocking_reasons.push("epistemic_block: unsupported factual/numeric or unsafe claim under the active source policy.");
  }
  if ((ledger.summary?.unsafe_count ?? 0) > 0) {
    blocking_reasons.push("unsafe_claim: an absolute claim in a high-stakes context lacks a source.");
  }

  // Editor: arena fit failure is a hard blocker for a packaged delivery.
  if (!arena.satisfied) {
    for (const v of arena.violations) blocking_reasons.push(`arena_fit_failure: ${v}`);
  }

  // Unresolved ambiguity means we should not have produced a final at all.
  for (const flag of ambiguity_flags) blocking_reasons.push(`unresolved_ambiguity: ${flag}`);

  // Detector: residual hard bans in the cleaned draft are a hard blocker (the rewrite failed).
  if (diagnostics.hard_ban_hits > 0) {
    blocking_reasons.push(`residual_hard_bans: ${diagnostics.hard_ban_hits} slop phrase(s) survived the rewrite.`);
  }

  // Soft flags — quality concerns that route to hold_for_review, not a block.
  if (diagnostics.perplexity_flatness_run >= 5) {
    soft_flags.push(`cadence_flatness: ${diagnostics.perplexity_flatness_run} consecutive same-length sentences.`);
  }
  if (diagnostics.passive_voice_ratio > 0.4) {
    soft_flags.push(`passive_voice_high: ${diagnostics.passive_voice_ratio}`);
  }
  if (diagnostics.abstract_noun_density > 12) {
    soft_flags.push(`abstraction_high: ${diagnostics.abstract_noun_density} abstract nouns / 100 words.`);
  }
  if (diagnostics.ai_opener_detected) {
    soft_flags.push("ai_opener: the opening still reads like a generic AI lead.");
  }

  return { blocking_reasons, soft_flags };
}
