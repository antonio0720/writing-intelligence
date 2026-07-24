// Writing Intelligence v3.1 — shared types. Shapes mirror schemas/*.schema.json exactly.

export const VERSION = "3.0.0" as const;

export type Mode =
  | "draft" | "rewrite" | "score" | "redline" | "compress" | "expand" | "audit" | "convert" | "certify";

export type Intent =
  | "inform" | "convert" | "warn" | "teach" | "dignify" | "dominate" | "comfort"
  | "reveal" | "mobilize" | "persuade" | "entertain" | "defend" | "terrify" | "disorient";

export type OutputMode =
  | "clean" | "annotated" | "redline" | "scorecard" | "violations" | "next-pass"
  | "scene-audit" | "epistemic-ledger" | "delivery-bundle" | "voice-drift-report" | "benchmark-result";

export interface IntakeContractV3 {
  task_id: string;
  version: typeof VERSION;
  mode: Mode;
  intent: Intent;
  audience: string;
  voice?: string;
  genre_stack?: string[];
  constraints: {
    word_count_min?: number;
    word_count_max?: number;
    preserve_user_claims?: boolean;
    allow_new_claims?: boolean;
    citations_required?: boolean;
    forbidden_changes?: string[];
    output_mode?: OutputMode[];
  };
  source_policy: {
    user_text_priority?: "highest" | "high" | "normal" | "low" | "ignored";
    memory_allowed?: boolean;
    web_required?: boolean;
    citations_required?: boolean;
    fabrication_tolerance: "zero" | "flag_only";
  };
  arena?: string;
  high_stakes?: boolean;
  success_condition: string;
  ambiguity_flags?: string[];
  created_at?: string;
}

export type ClaimClass =
  | "observed_fact" | "sourced_fact" | "inference" | "synthesis" | "recommendation" | "rhetoric";

export type SourceStatus =
  | "verified" | "user-provided" | "assumed" | "inferred" | "missing" | "unsafe";

export type FabricationRisk = "none" | "low" | "medium" | "high" | "blocked";

export interface EpistemicClaim {
  claim_id: string;
  text: string;
  location?: { paragraph?: number; sentence?: number };
  class: ClaimClass;
  source_status: SourceStatus;
  sources?: string[];
  premises?: string[];
  universal_quantifier_flag?: boolean;
  inflated_verb_flag?: boolean;
  fabrication_risk?: FabricationRisk;
  notes?: string;
}

export interface EpistemicLedgerV3 {
  task_id: string;
  version: typeof VERSION;
  claims: EpistemicClaim[];
  summary?: {
    total_claims: number;
    verified_pct: number;
    sourced_pct: number;
    inference_pct: number;
    rhetoric_pct: number;
    missing_source_count: number;
    unsafe_count: number;
    fabrication_blocks: number;
  };
  delivery_block?: boolean;
  decisions?: Array<{
    claim_id: string;
    action: "cite_added" | "claim_softened" | "claim_removed" | "claim_qualified" | "user_clarification_required";
    rationale: string;
  }>;
}

export type VocabTier = "plain" | "educated" | "scholarly" | "rarefied" | "mixed";

export interface VoiceMetrics {
  avg_sentence_length: number;
  sentence_length_std: number;
  avg_paragraph_length?: number;
  paragraph_length_std?: number;
  compression_ratio?: number;
  abstraction_tolerance?: number;
  metaphor_density?: number;
  question_frequency?: number;
  comma_density?: number;
  vocab_tier: VocabTier;
  domain_vocab_per_500w?: number;
  transition_top5?: string[];
  opening_pattern_repertoire?: string[];
  closing_pattern_repertoire?: string[];
  dominant_syntactic_structures?: string[];
  authority_posture?: number;
}

export interface VoiceFingerprintV3 {
  voice_id: string;
  version: typeof VERSION;
  author?: string;
  baseline_corpus?: string[];
  metrics: VoiceMetrics;
  team_voice?: boolean;
  drift_baseline_id?: string;
  drift_report?: {
    deltas: Record<string, number>;
    direction: "closer_to_baseline" | "further_from_baseline" | "stable";
    explanation: string;
  };
  created_at?: string;
}

export type RewriteOp =
  | "hard_ban_removed" | "soft_ban_removed" | "variance_injected" | "compression"
  | "specificity_added" | "abstract_to_scene" | "voice_restored" | "preserved"
  | "rhetorical_question_kept_earned" | "fragment_kept_earned" | "transition_replaced"
  | "metaphor_added" | "metaphor_removed" | "claim_softened" | "claim_qualified" | "evidence_attached";

export interface ProseRewriteLogV3 {
  task_id: string;
  version: typeof VERSION;
  transformations: Array<{
    transformation_id?: string;
    op: RewriteOp;
    before: string;
    after: string;
    rationale?: string;
    rule_id?: string;
    voice_impact?: "increased_fidelity" | "neutral" | "decreased_fidelity";
  }>;
  summary?: {
    total_transformations: number;
    hard_ban_count: number;
    soft_ban_count: number;
    compressions: number;
    voice_fidelity_delta: number;
  };
}

export type Arena =
  | "memo" | "grant_response" | "sermon" | "caption" | "article" | "chapter" | "email"
  | "pitch_slide" | "youtube_script" | "newsletter" | "government_brief" | "sop" | "speech"
  | "landing_page" | "linkedin_post" | "twitter_thread" | "instagram_caption"
  | "press_release" | "case_study" | "blog_post";

export interface DeliveryBundleV3 {
  task_id: string;
  version: typeof VERSION;
  arena: Arena;
  assets: Array<{
    mode: "clean" | "annotated" | "redline" | "scorecard" | "violations" | "next-pass"
      | "scene-audit" | "epistemic-ledger" | "voice-drift-report" | "benchmark-result";
    content: string;
    format?: "markdown" | "plain_text" | "html" | "json" | "yaml";
    word_count?: number;
    char_count?: number;
  }>;
  channel_constraints?: {
    char_max?: number;
    hashtag_max?: number;
    headline_variants_required?: boolean;
    cta_required?: boolean;
    readability_level?: string;
  };
  constraints_satisfied?: boolean;
  scorecard_summary?: {
    prose_quality?: number;
    chapter_construction?: number;
    dialogue?: number;
    epistemic_integrity?: number;
    arena_fit?: number;
    v3_composite?: number;
  };
  delivery_decision?: "release" | "hold_for_review" | "block";
  blocking_reasons?: string[];
}

export interface Scorecard {
  prose_quality: number;
  epistemic_integrity: number;
  arena_fit: number;
  v3_composite: number;
  auto_fail_triggered: boolean;
  auto_fail_reasons: string[];
  diagnostics: {
    hard_ban_hits: number;
    passive_voice_ratio: number;
    sentence_length_variance: number;
    abstract_noun_density: number;
    em_dash_overuse: boolean;
    ai_opener_detected: boolean;
  };
}

export interface BenchmarkResultV3 {
  case_id: string;
  version: typeof VERSION;
  category?: string;
  v2_baseline_score?: number;
  v3_score: number;
  delta?: number;
  failure_modes_detected?: string[];
  failure_modes_expected?: string[];
  detection_recall?: number;
  score_range_expected?: { min?: number; max?: number };
  score_within_range?: boolean;
  regression_hazards_observed?: string[];
  decision: "PASS" | "CONDITIONAL_PASS" | "FAIL";
  rationale?: string;
  run_id?: string;
  ran_at?: string;
}

// Kernel output (internal), assembled by routes into the API envelope.
export interface KernelResult {
  intake_contract: IntakeContractV3;
  epistemic_ledger: EpistemicLedgerV3;
  prose_rewrite_log: ProseRewriteLogV3;
  voice_fingerprint?: VoiceFingerprintV3;
  delivery_bundle: DeliveryBundleV3;
  scorecard: Scorecard;
  passes_run: number[];
  clean_text: string;
  ambiguity_flags: string[];
}
