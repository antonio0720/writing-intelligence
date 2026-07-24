// Claim extraction + classification for the Epistemic Ledger (Pass 5).
// Deterministic rules only. This is the load-bearing safety gate: an unsupported
// factual/numeric claim under a zero-fabrication / citations-required policy blocks delivery.
import { splitSentences, splitParagraphs } from "./text";
import type { EpistemicClaim, EpistemicLedgerV3, ClaimClass, SourceStatus, FabricationRisk } from "../types";

const UNIVERSAL_QUANTIFIERS = /\b(all|every|everyone|everything|always|never|none|no one|nobody|any|entirely|completely|guaranteed)\b/i;
const SUPERLATIVES = /\b(best|worst|most|least|greatest|leading|number one|#1|unmatched|unrivaled|ultimate|premier|finest)\b/i;
const INFLATED_VERBS = /\b(revolutioniz\w*|transform\w*|redefin\w*|disrupt\w*|reinvent\w*|reimagin\w*|supercharg\w*)\b/i;
const NUMERIC = /(\$\s?\d|\d+\s?%|\b\d[\d,.]*\b)/;
const RECOMMENDATION = /\b(should|must|need to|ought to|recommend|we advise|you have to)\b/i;
const CITATION_MARKER = /(\(source[:\s]|according to|per\s+\w+,|\[\d+\]|https?:\/\/|cited in|as reported by|\bsource:\b)/i;
const OPINION_MARKER = /\b(i believe|we believe|i think|we think|in my view|arguably|it feels|it seems)\b/i;

export interface ClaimPolicy {
  citations_required: boolean;
  zero_fabrication: boolean;
  high_stakes: boolean;
  preserve_user_claims: boolean;
}

export function buildLedger(taskId: string, text: string, policy: ClaimPolicy): EpistemicLedgerV3 {
  const paragraphs = splitParagraphs(text);
  const claims: EpistemicClaim[] = [];

  let paraIdx = 0;
  for (const para of paragraphs) {
    paraIdx++;
    const sentences = splitSentences(para);
    let sentIdx = 0;
    for (const sentence of sentences) {
      sentIdx++;
      const claim = classify(sentence, paraIdx, sentIdx, policy, claims.length + 1);
      if (claim) claims.push(claim);
    }
  }

  const summary = summarize(claims);
  const unsafe = summary.unsafe_count;
  const missingFactual = claims.some(
    (c) => (c.class === "observed_fact" || c.class === "sourced_fact") && c.source_status === "missing",
  );
  const gatePolicy = policy.citations_required || policy.zero_fabrication;
  const delivery_block = unsafe > 0 || (missingFactual && gatePolicy);

  const decisions = buildDecisions(claims, policy);

  return {
    task_id: taskId,
    version: "3.0.0",
    claims,
    summary,
    delivery_block,
    decisions,
  };
}

function classify(
  sentence: string,
  paragraph: number,
  sentenceNo: number,
  policy: ClaimPolicy,
  seq: number,
): EpistemicClaim | null {
  const trimmed = sentence.trim();
  if (trimmed.length < 3) return null;

  const hasNumber = NUMERIC.test(trimmed);
  const hasSuperlative = SUPERLATIVES.test(trimmed);
  const hasUniversal = UNIVERSAL_QUANTIFIERS.test(trimmed);
  const hasInflated = INFLATED_VERBS.test(trimmed);
  const hasCitation = CITATION_MARKER.test(trimmed);
  const isOpinion = OPINION_MARKER.test(trimmed);
  const isRecommendation = RECOMMENDATION.test(trimmed);
  const factualAssertion = hasNumber || hasSuperlative || /\b(is|are|was|were|has|have|will|reached|grew|increased|decreased|reduced)\b/i.test(trimmed);

  // Only sentences that assert something checkable enter the ledger.
  const material = hasNumber || hasSuperlative || hasUniversal || hasInflated || isRecommendation || (factualAssertion && !isOpinion);
  if (!material && !isRecommendation) return null;

  let klass: ClaimClass;
  let status: SourceStatus;

  if (isRecommendation) {
    klass = "recommendation";
    status = policy.preserve_user_claims ? "user-provided" : "assumed";
  } else if (isOpinion || (hasInflated && !hasNumber)) {
    klass = "rhetoric";
    status = "assumed";
  } else if (hasNumber || hasSuperlative) {
    // A checkable factual claim.
    klass = hasCitation ? "sourced_fact" : "observed_fact";
    if (hasCitation) status = "verified";
    else if (policy.preserve_user_claims) status = "user-provided";
    else status = "missing";
    // A cite-required or zero-fab policy demotes an unsupported user claim to "missing".
    if (!hasCitation && (policy.citations_required || policy.zero_fabrication)) status = "missing";
  } else {
    klass = "inference";
    status = hasCitation ? "verified" : "inferred";
  }

  // Unsafe: an unsupported universal/superlative factual claim in a high-stakes context.
  const unsupportedFactual = (klass === "observed_fact") && status === "missing";
  if (policy.high_stakes && unsupportedFactual && (hasUniversal || hasSuperlative)) {
    status = "unsafe";
  }

  const fabrication_risk = fabricationRisk(klass, status, hasNumber);

  return {
    claim_id: `c${seq}`,
    text: trimmed,
    location: { paragraph, sentence: sentenceNo },
    class: klass,
    source_status: status,
    sources: hasCitation ? ["user_citation"] : [],
    universal_quantifier_flag: hasUniversal,
    inflated_verb_flag: hasInflated,
    fabrication_risk,
    notes: unsupportedFactual ? "Factual/numeric claim without a source." : undefined,
  };
}

function fabricationRisk(klass: ClaimClass, status: SourceStatus, hasNumber: boolean): FabricationRisk {
  if (status === "unsafe") return "blocked";
  if ((klass === "observed_fact" || klass === "sourced_fact") && status === "missing") {
    return hasNumber ? "high" : "medium";
  }
  if (klass === "rhetoric") return "low";
  if (status === "verified" || status === "user-provided") return "none";
  return "low";
}

function summarize(claims: EpistemicClaim[]) {
  const total = claims.length;
  const pct = (n: number) => (total ? Math.round((n / total) * 1000) / 10 : 0);
  const verified = claims.filter((c) => c.source_status === "verified" || c.source_status === "user-provided").length;
  const sourced = claims.filter((c) => c.class === "sourced_fact").length;
  const inference = claims.filter((c) => c.class === "inference" || c.class === "synthesis").length;
  const rhetoric = claims.filter((c) => c.class === "rhetoric").length;
  const missing = claims.filter((c) => c.source_status === "missing").length;
  const unsafe = claims.filter((c) => c.source_status === "unsafe").length;
  const blocks = claims.filter((c) => c.fabrication_risk === "blocked").length;
  return {
    total_claims: total,
    verified_pct: pct(verified),
    sourced_pct: pct(sourced),
    inference_pct: pct(inference),
    rhetoric_pct: pct(rhetoric),
    missing_source_count: missing,
    unsafe_count: unsafe,
    fabrication_blocks: blocks,
  };
}

function buildDecisions(claims: EpistemicClaim[], policy: ClaimPolicy) {
  const decisions: NonNullable<EpistemicLedgerV3["decisions"]> = [];
  for (const c of claims) {
    if (c.source_status === "unsafe") {
      decisions.push({ claim_id: c.claim_id, action: "user_clarification_required", rationale: "Unsupported absolute claim in a high-stakes context; requires a source or a qualifier." });
    } else if ((c.class === "observed_fact" || c.class === "sourced_fact") && c.source_status === "missing" && (policy.citations_required || policy.zero_fabrication)) {
      decisions.push({ claim_id: c.claim_id, action: "cite_added", rationale: "Numeric/factual claim needs a citation under the active source policy." });
    } else if (c.universal_quantifier_flag && c.source_status === "missing") {
      decisions.push({ claim_id: c.claim_id, action: "claim_qualified", rationale: "Universal quantifier softened to a defensible scope." });
    }
  }
  return decisions;
}
