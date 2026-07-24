// The 11-pass compilation kernel. Deterministic end to end. No LLM, no ML, no network.
import { buildIntake, type IntakeOverrides } from "./passes/intake";
import { lockMission } from "./passes/missionLock";
import { runDiagnostics } from "./passes/diagnostic";
import { buildLedger, type ClaimPolicy } from "./claimScan";
import { runSurgery } from "./passes/sentenceSurgery";
import { fingerprintFromText } from "./passes/voice";
import { normalizeArena, checkArena, detectCta } from "./passes/arena";
import { runStress } from "./passes/stress";
import { score } from "./passes/score";
import { buildDelivery } from "./passes/delivery";
import { wordCount } from "./text";
import type { KernelResult, IntakeContractV3, Scorecard, EpistemicLedgerV3 } from "../types";

export interface KernelInput {
  task_id: string;
  request_text: string;
  draft_text?: string;
  overrides?: IntakeOverrides;
  output_modes?: string[];
  created_at: string;
}

function policyFrom(intake: IntakeContractV3): ClaimPolicy {
  return {
    citations_required: Boolean(intake.constraints.citations_required),
    zero_fabrication: intake.source_policy.fabrication_tolerance === "zero",
    high_stakes: Boolean(intake.high_stakes),
    preserve_user_claims: intake.constraints.preserve_user_claims !== false,
  };
}

// The text the kernel actually works on: an explicit draft wins; else the request body.
function processingText(input: KernelInput): string {
  return (input.draft_text ?? input.request_text ?? "").toString();
}

// Pass 1 ambiguity check, exposed so the route can return 422 before compiling.
export function checkAmbiguity(input: KernelInput): { intake: IntakeContractV3; flags: string[] } {
  const intake = buildIntake({
    task_id: input.task_id,
    request_text: input.request_text,
    overrides: input.overrides,
    output_modes: input.output_modes,
    created_at: input.created_at,
  });
  const flags = lockMission(intake, processingText(input));
  return { intake, flags };
}

// Full /compile path — runs all 11 passes and returns every artifact.
export function compile(input: KernelInput): KernelResult {
  const { intake, flags } = checkAmbiguity(input);
  const text = processingText(input);
  const policy = policyFrom(intake);

  // Pass 6 — Sentence Surgery (rewrite). Runs before the clean-text diagnostics.
  const { clean_text, log } = runSurgery(intake.task_id, text);

  // Pass 3 — Diagnostic Scan on the CLEANED asset (what we actually ship gets scored).
  const diagnostics = runDiagnostics(clean_text);

  // Pass 5 — Epistemic Ledger (the safety gate). Claims survive cleaning; the gate is honest.
  const ledger = buildLedger(intake.task_id, clean_text, policy);

  // Pass 7 — Voice Fingerprint of the cleaned asset.
  const voice_fingerprint = fingerprintFromText({
    voice_id: intake.voice ?? "neutral_professional",
    text: clean_text,
    created_at: input.created_at,
  });

  // Pass 8 — Arena Alignment.
  const arena = normalizeArena(intake.arena);
  const cta = detectCta(clean_text);
  const arenaCheck = checkArena(arena, clean_text, cta);

  // Pass 9 — Adversarial Stress Battery.
  const stress = runStress({ diagnostics, ledger, arena: arenaCheck, ambiguity_flags: flags });

  // Pass 10 — Score + Delivery.
  const rawWords = wordCount(text);
  const cleanWords = wordCount(clean_text);
  const retention_ratio = rawWords > 0 ? cleanWords / rawWords : 1;
  const scorecard = score({
    diagnostics,
    ledger,
    arena: arenaCheck,
    high_stakes: Boolean(intake.high_stakes),
    hasClaims: text.length > 0,
    retention_ratio,
  });
  const delivery_bundle = buildDelivery({
    intake, arena, arenaCheck, clean_text, scorecard, ledger, stress,
  });

  return {
    intake_contract: { ...intake, ambiguity_flags: flags },
    epistemic_ledger: ledger,
    prose_rewrite_log: log,
    voice_fingerprint,
    delivery_bundle,
    scorecard,
    passes_run: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    clean_text,
    ambiguity_flags: flags,
  };
}

// /score path — score the RAW draft, no rewrite emitted.
export function scoreOnly(input: KernelInput): {
  intake: IntakeContractV3;
  scorecard: Scorecard;
  ledger: EpistemicLedgerV3;
  passes_run: number[];
} {
  const { intake } = checkAmbiguity(input);
  const text = processingText(input);
  const policy = policyFrom(intake);

  const diagnostics = runDiagnostics(text);
  const ledger = buildLedger(intake.task_id, text, policy);
  const arena = normalizeArena(intake.arena);
  const arenaCheck = checkArena(arena, text, detectCta(text));
  const scorecard = score({
    diagnostics,
    ledger,
    arena: arenaCheck,
    high_stakes: Boolean(intake.high_stakes),
    hasClaims: text.length > 0,
  });

  return { intake, scorecard, ledger, passes_run: [0, 1, 3, 4, 5, 9, 10] };
}
