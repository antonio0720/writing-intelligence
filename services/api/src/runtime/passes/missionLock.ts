// Pass 1 — Mission Lock. Confirms the success condition and surfaces unresolved ambiguity.
// A non-empty ambiguity list drives the 422 path in /compile.
import type { IntakeContractV3 } from "../../types";

export function lockMission(contract: IntakeContractV3, processingText: string): string[] {
  const flags: string[] = [];

  if (!processingText.trim()) {
    flags.push("empty_input: no request_text or draft_text was provided to work on.");
  }

  const min = contract.constraints.word_count_min;
  const max = contract.constraints.word_count_max;
  if (typeof min === "number" && typeof max === "number" && min > max) {
    flags.push(`contradictory_word_count: word_count_min (${min}) exceeds word_count_max (${max}).`);
  }

  if (contract.mode === "compress" && typeof min === "number" && typeof max === "number" && min === max && min > 0) {
    // Compression to an exact count with no room is not resolvable without loss guidance.
    flags.push("compress_target_ambiguous: exact word target leaves no compression band.");
  }

  // Note: citations_required is intentionally NOT an ambiguity. Missing citations are
  // resolved by the Epistemic Ledger (Pass 5) and the delivery gate (Pass 10) — a 423,
  // never a 422. Fabrication is refused, not silently guessed.

  return flags;
}
