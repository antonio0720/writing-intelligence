// Pass 11 — Benchmark runtime. Implements the `ai_slop_rewrite` case for real: it detects
// the expected slop failure modes on the raw inputs, rewrites, and scores the rewrite.
import { runDiagnostics } from "./passes/diagnostic";
import { compile } from "./Kernel";
import { taskId } from "./ids";
import type { BenchmarkResultV3 } from "../types";

interface BenchCase {
  case_id: string;
  category: BenchmarkResultV3["category"];
  inputs: string[];
  // Expected failure modes are phrase substrings the scanner must catch on the raw inputs.
  expected_failure_modes: string[];
  v2_baseline: number;
  range: { min: number; max: number };
  arena: string;
}

// The five SLOP cases from benchmarks/cases/ai_slop_rewrite.md, embedded verbatim.
const AI_SLOP: BenchCase = {
  case_id: "ai_slop_rewrite",
  category: "ai_slop_rewrite",
  // blog_post carries no CTA/hashtag requirement, so the score isolates rewrite quality
  // (slop removal + cadence + epistemic) rather than arena packaging.
  arena: "blog_post",
  inputs: [
    "In today's fast-paced world, the importance of authentic leadership cannot be overstated. Game-changing leaders are those who think outside the box and leverage their unique perspectives to drive transformational change. Let's be clear: at the end of the day, it's not just about what you do — it's about who you are. Read that again.",
    "At our company, we are dedicated to revolutionizing the way our customers experience our world-class solutions. Our team of passionate professionals leverages cutting-edge technology and decades of combined experience to deliver game-changing results that empower our clients to achieve their goals.",
    "Want to improve your writing? Here's the thing — most people don't realize that the secret to great writing isn't talent. Think about it. The question isn't whether you have what it takes. Spoiler alert: most people aren't.",
    "We are pleased to share that the company is experiencing tremendous growth and is well-positioned to capture significant market share in the coming year. Our team continues to execute against our strategic priorities and we remain confident in our ability to deliver exceptional value to our stakeholders.",
    "Artificial intelligence is transforming every industry and changing the way we work, live, and interact. In this article, we'll explore the key trends shaping AI in 2026. By the end of this piece, you'll have a comprehensive understanding of where AI is headed.",
  ],
  expected_failure_modes: [
    "in today's fast-paced world",
    "cannot be overstated",
    "game-changing",
    "think outside the box",
    "leverage",
    "let's be clear",
    "at the end of the day",
    "read that again",
    "revolutionizing",
    "world-class",
    "passionate professionals",
    "cutting-edge",
    "empower",
    "here's the thing",
    "most people don't realize",
    "think about it",
    "spoiler alert",
    "pleased to share",
    "tremendous growth",
    "well-positioned",
    "execute against",
    "exceptional value",
    "stakeholders",
    "transforming every industry",
    "in this article, we'll explore",
    "comprehensive understanding",
  ],
  v2_baseline: 73,
  range: { min: 78, max: 92 },
};

const CASES: Record<string, BenchCase> = {
  ai_slop_rewrite: AI_SLOP,
  "SLOP-ALL": AI_SLOP,
};

export function knownBenchmarkCase(caseId: string): boolean {
  return caseId in CASES;
}

export function runBenchmark(caseId: string, againstVersion: string | undefined, ranAt: string): BenchmarkResultV3 | null {
  const bench = CASES[caseId];
  if (!bench) return null;

  const rawText = bench.inputs.join("\n\n");

  // Detection: which expected failure modes does the scanner actually catch on the raw input?
  const rawDiag = runDiagnostics(rawText);
  const detectedPhrases = new Set(rawDiag.hard_ban_detail.map((h) => h.phrase));
  const detected = bench.expected_failure_modes.filter((p) => detectedPhrases.has(p));
  const detection_recall = bench.expected_failure_modes.length
    ? Math.round((detected.length / bench.expected_failure_modes.length) * 1000) / 1000
    : 1;

  // Rewrite + score the cleaned output through the real kernel.
  const tid = taskId({ benchmark: caseId }, "benchmark");
  const result = compile({
    task_id: tid,
    request_text: "Rewrite these drafts to remove AI slop while preserving the claim.",
    draft_text: rawText,
    overrides: { arena: bench.arena, voice: "courageous_builder", intent: "persuade", mode: "rewrite" },
    output_modes: ["clean", "scorecard"],
    created_at: ranAt,
  });

  const v3_score = result.scorecard.v3_composite;
  const within = v3_score >= bench.range.min && v3_score <= bench.range.max;

  // Regression hazards from the case file: did the rewrite reintroduce slop, or empty the draft?
  const cleanDiag = runDiagnostics(result.clean_text);
  const regression_hazards: string[] = [];
  if (cleanDiag.hard_ban_hits > 0) regression_hazards.push("voice_restoration_reintroduced_hard_bans");
  if (result.clean_text.trim().length === 0) regression_hazards.push("rewrite_emptied_the_draft");

  const decision: BenchmarkResultV3["decision"] =
    within && detection_recall >= 0.6 && regression_hazards.length === 0
      ? "PASS"
      : detection_recall >= 0.6 && regression_hazards.length === 0
        ? "CONDITIONAL_PASS"
        : "FAIL";

  return {
    case_id: bench.case_id,
    version: "3.0.0",
    category: bench.category,
    v2_baseline_score: bench.v2_baseline,
    v3_score,
    delta: Math.round((v3_score - bench.v2_baseline) * 10) / 10,
    failure_modes_detected: detected,
    failure_modes_expected: bench.expected_failure_modes,
    detection_recall,
    score_range_expected: bench.range,
    score_within_range: within,
    regression_hazards_observed: regression_hazards,
    decision,
    rationale: `Detected ${detected.length}/${bench.expected_failure_modes.length} expected slop modes (recall ${detection_recall}); rewrite scored ${v3_score} (expected ${bench.range.min}-${bench.range.max}). Compared against v${againstVersion ?? "2.0"} baseline ${bench.v2_baseline}.`,
    run_id: tid,
    ran_at: ranAt,
  };
}
