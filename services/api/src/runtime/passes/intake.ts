// Pass 0 — Intake Contract. Deterministic defaults; user overrides always win.
import type { IntakeContractV3, Mode, Intent, OutputMode } from "../../types";

export interface IntakeOverrides {
  mode?: Mode;
  intent?: Intent;
  audience?: string;
  voice?: string;
  genre_stack?: string[];
  arena?: string;
  high_stakes?: boolean;
  success_condition?: string;
  constraints?: IntakeContractV3["constraints"];
  source_policy?: Partial<IntakeContractV3["source_policy"]>;
}

const HIGH_STAKES_TERMS = [
  "investor", "medical", "legal", "grant", "nofo", "financial", "government",
  "compliance", "regulatory", "clinical", "securities", "audit", "diagnosis",
];

const MODE_RULES: Array<[RegExp, Mode]> = [
  [/\b(rewrite|revise|edit|redline|clean up|de-slop|fix)\b/i, "rewrite"],
  [/\b(score|grade|evaluate|assess)\b/i, "score"],
  [/\b(compress|shorten|tighten|trim)\b/i, "compress"],
  [/\b(expand|lengthen|flesh out)\b/i, "expand"],
  [/\b(audit|review)\b/i, "audit"],
  [/\b(convert|repackage|reformat)\b/i, "convert"],
];

const INTENT_RULES: Array<[RegExp, Intent]> = [
  [/\b(sell|persuade|convert|pitch|close|cta)\b/i, "persuade"],
  [/\b(teach|explain|guide|educate|how to)\b/i, "teach"],
  [/\b(warn|caution|risk)\b/i, "warn"],
  [/\b(update|report|inform|brief)\b/i, "inform"],
  [/\b(mobilize|rally|activate)\b/i, "mobilize"],
];

const OUTPUT_MODE_MAP: Record<string, OutputMode> = {
  clean: "clean",
  annotated: "annotated",
  redline: "redline",
  scorecard: "scorecard",
  violations: "violations",
  "next-pass": "next-pass",
  "scene-audit": "scene-audit",
  "epistemic-ledger": "epistemic-ledger",
  "delivery-bundle": "delivery-bundle",
  "voice-drift-report": "voice-drift-report",
  "benchmark-result": "benchmark-result",
};

export function buildIntake(params: {
  task_id: string;
  request_text: string;
  overrides?: IntakeOverrides;
  output_modes?: string[];
  created_at: string;
}): IntakeContractV3 {
  const { task_id, request_text, overrides = {}, output_modes = [], created_at } = params;
  const req = request_text ?? "";

  const mode = overrides.mode ?? detectMode(req);
  const intent = overrides.intent ?? detectIntent(req);

  const citationsRequired =
    overrides.constraints?.citations_required ??
    overrides.source_policy?.citations_required ??
    false;

  const high_stakes =
    overrides.high_stakes ??
    (citationsRequired || HIGH_STAKES_TERMS.some((t) => req.toLowerCase().includes(t)));

  const outputModes = normalizeOutputModes(output_modes, overrides.constraints?.output_mode);

  const constraints: IntakeContractV3["constraints"] = {
    preserve_user_claims: true,
    allow_new_claims: false,
    ...overrides.constraints,
    // Resolved values stay authoritative over whatever the override object carried.
    citations_required: citationsRequired,
    output_mode: outputModes,
  };

  const source_policy: IntakeContractV3["source_policy"] = {
    user_text_priority: overrides.source_policy?.user_text_priority ?? "highest",
    memory_allowed: overrides.source_policy?.memory_allowed ?? false,
    web_required: overrides.source_policy?.web_required ?? false,
    citations_required: citationsRequired,
    fabrication_tolerance:
      overrides.source_policy?.fabrication_tolerance ??
      (high_stakes || citationsRequired ? "zero" : "flag_only"),
  };

  return {
    task_id,
    version: "3.0.0",
    mode,
    intent,
    audience: overrides.audience ?? "general audience",
    voice: overrides.voice ?? "neutral_professional",
    genre_stack: overrides.genre_stack && overrides.genre_stack.length > 0 ? overrides.genre_stack : ["general"],
    constraints,
    source_policy,
    arena: overrides.arena ?? "memo",
    high_stakes,
    success_condition:
      overrides.success_condition ??
      "The reader trusts the writing and the intended action is unmistakable.",
    created_at,
  };
}

function detectMode(text: string): Mode {
  for (const [re, mode] of MODE_RULES) if (re.test(text)) return mode;
  return "draft";
}

function detectIntent(text: string): Intent {
  for (const [re, intent] of INTENT_RULES) if (re.test(text)) return intent;
  return "inform";
}

function normalizeOutputModes(requested: string[], fromConstraints?: OutputMode[]): OutputMode[] {
  const source = [...(fromConstraints ?? []), ...requested];
  const mapped = source.map((m) => OUTPUT_MODE_MAP[m]).filter((m): m is OutputMode => Boolean(m));
  const unique = [...new Set(mapped)];
  return unique.length > 0 ? unique : ["clean", "scorecard", "epistemic-ledger"];
}
