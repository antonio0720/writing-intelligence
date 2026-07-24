import { Router, type Request, type Response } from "express";
import { fingerprintFromSamples, fingerprintFromText, driftReport } from "../runtime/passes/voice";
import { computeMetrics } from "../runtime/voiceMetrics";
import { contentHash } from "../runtime/ids";
import { resolveTenant } from "../security/tenant";
import { assertWithinLimit, InputTooLargeError } from "../security/limits";
import type { VoiceFingerprintV3, VoiceMetrics } from "../types";

export const voiceRouter = Router();

// POST /voice/fingerprint — build a VoiceFingerprintV3 from { voice_id, samples[] }.
voiceRouter.post("/voice/fingerprint", (req: Request, res: Response) => {
  const tenant = resolveTenant(req);
  const body = (req.body ?? {}) as Record<string, unknown>;
  const voice_id = body.voice_id;
  const samples = body.samples;
  if (typeof voice_id !== "string" || voice_id.length === 0) {
    res.status(400).json({ error: "invalid_body", detail: "voice_id (non-empty string) is required." });
    return;
  }
  if (!Array.isArray(samples) || samples.length === 0 || samples.some((s) => typeof s !== "string")) {
    res.status(400).json({ error: "invalid_body", detail: "samples must be a non-empty array of strings." });
    return;
  }
  try {
    assertWithinLimit({ samples: samples as string[] });
  } catch (e) {
    if (e instanceof InputTooLargeError) { res.status(400).json({ error: "input_too_large", detail: e.message }); return; }
    throw e;
  }

  const author = typeof body.author === "string" ? body.author : undefined;
  const fp = fingerprintFromSamples({ voice_id, samples: samples as string[], author, created_at: new Date().toISOString() });
  res.status(200).json({ tenant, ...fp, content_hash: contentHash(fp) });
});

// POST /voice/drift — { baseline_voice_id?, baseline_fingerprint?, draft_text } → drift_report.
voiceRouter.post("/voice/drift", (req: Request, res: Response) => {
  const tenant = resolveTenant(req);
  const body = (req.body ?? {}) as Record<string, unknown>;
  const draft_text = body.draft_text;
  if (typeof draft_text !== "string" || draft_text.length === 0) {
    res.status(400).json({ error: "invalid_body", detail: "draft_text (non-empty string) is required." });
    return;
  }
  const baselineFp = body.baseline_fingerprint as { metrics?: VoiceMetrics; voice_id?: string } | undefined;
  const baseline_voice_id = typeof body.baseline_voice_id === "string" ? body.baseline_voice_id : undefined;

  let baseline: VoiceFingerprintV3 | null = null;
  if (baselineFp && typeof baselineFp === "object" && baselineFp.metrics) {
    baseline = {
      voice_id: baselineFp.voice_id ?? baseline_voice_id ?? "baseline",
      version: "3.0.0",
      metrics: normalizeMetrics(baselineFp.metrics),
    };
  } else if (baseline_voice_id) {
    // No stored corpus in v1: a neutral baseline is derived from the draft's own structure,
    // so drift is honestly reported as "stable" rather than fabricated against unknown metrics.
    res.status(400).json({
      error: "invalid_body",
      detail: "baseline_fingerprint (with metrics) is required in v1; there is no server-side voice store to resolve baseline_voice_id.",
    });
    return;
  } else {
    res.status(400).json({ error: "invalid_body", detail: "Provide baseline_fingerprint (with metrics), or baseline_voice_id + baseline_fingerprint." });
    return;
  }

  try {
    assertWithinLimit({ draft_text });
  } catch (e) {
    if (e instanceof InputTooLargeError) { res.status(400).json({ error: "input_too_large", detail: e.message }); return; }
    throw e;
  }

  const current = fingerprintFromText({ voice_id: baseline_voice_id ?? "draft", text: draft_text, created_at: new Date().toISOString() });
  const withDrift = driftReport(current, baseline);
  res.status(200).json({ tenant, ...withDrift, content_hash: contentHash(withDrift) });
});

// Fill any missing numeric metrics with 0 and ensure vocab_tier so drift math is safe.
function normalizeMetrics(m: VoiceMetrics): VoiceMetrics {
  const zeroed = computeMetrics(""); // canonical zero shape
  return { ...zeroed, ...m, vocab_tier: m.vocab_tier ?? "plain" };
}
