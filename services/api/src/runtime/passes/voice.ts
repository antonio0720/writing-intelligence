// Pass 7 — Voice Restoration / Fingerprinting. Wraps the deterministic metric engine.
import { computeMetrics, computeDrift } from "../voiceMetrics";
import type { VoiceFingerprintV3 } from "../../types";

export function fingerprintFromText(params: {
  voice_id: string;
  text: string;
  author?: string;
  baseline_corpus?: string[];
  created_at: string;
  team_voice?: boolean;
}): VoiceFingerprintV3 {
  return {
    voice_id: params.voice_id,
    version: "3.0.0",
    author: params.author,
    baseline_corpus: params.baseline_corpus,
    metrics: computeMetrics(params.text),
    team_voice: params.team_voice ?? false,
    created_at: params.created_at,
  };
}

export function fingerprintFromSamples(params: {
  voice_id: string;
  samples: string[];
  author?: string;
  created_at: string;
}): VoiceFingerprintV3 {
  // Joined corpus keeps the computation deterministic and order-stable.
  const corpusText = params.samples.join("\n\n");
  return {
    voice_id: params.voice_id,
    version: "3.0.0",
    author: params.author,
    baseline_corpus: params.samples.map((_s, i) => `sample_${i + 1}`),
    metrics: computeMetrics(corpusText),
    team_voice: false,
    created_at: params.created_at,
  };
}

export function driftReport(
  fingerprint: VoiceFingerprintV3,
  baseline: VoiceFingerprintV3,
): VoiceFingerprintV3 {
  const report = computeDrift(fingerprint.metrics, baseline.metrics);
  return {
    ...fingerprint,
    drift_baseline_id: baseline.voice_id,
    drift_report: report,
  };
}
