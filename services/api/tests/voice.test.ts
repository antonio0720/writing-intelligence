import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { startServer, post, type TestServer } from "./helpers.js";

let srv: TestServer;
beforeAll(async () => { srv = await startServer(); });
afterAll(async () => { await srv.close(); });

const SAMPLE_A = "Build only what survives. The market does not reward motion. It rewards the thing that still stands after the noise dies. Ship small. Watch closely. Fix fast. Then do it again tomorrow with a sharper edge.";
const SAMPLE_B = "Momentum is a story we tell ourselves. Revenue is the fact. When the two disagree, trust the fact and rebuild the story. Every quarter is a chance to earn the claim you already made.";

describe("voice fingerprint + drift", () => {
  it("builds a fingerprint with real metrics from samples", async () => {
    const r = await post(srv.base, "/voice/fingerprint", { voice_id: "antonio", samples: [SAMPLE_A, SAMPLE_B] });
    expect(r.status).toBe(200);
    expect(r.json.voice_id).toBe("antonio");
    expect(r.json.metrics.avg_sentence_length).toBeGreaterThan(0);
    expect(typeof r.json.metrics.sentence_length_std).toBe("number");
    expect(["plain", "educated", "scholarly", "rarefied", "mixed"]).toContain(r.json.metrics.vocab_tier);
    expect(r.json.content_hash).toMatch(/^[0-9a-f]{64}$/);
  });

  it("400s a fingerprint request with no samples", async () => {
    const r = await post(srv.base, "/voice/fingerprint", { voice_id: "x", samples: [] });
    expect(r.status).toBe(400);
  });

  it("reports drift against a supplied baseline fingerprint", async () => {
    const fp = await post(srv.base, "/voice/fingerprint", { voice_id: "base", samples: [SAMPLE_A, SAMPLE_B] });
    const drift = await post(srv.base, "/voice/drift", {
      baseline_fingerprint: fp.json,
      draft_text: "In today's ever-changing landscape, organizations must leverage synergies to holistically optimize their operational excellence across the enterprise value chain.",
    });
    expect(drift.status).toBe(200);
    expect(drift.json.drift_report).toBeTruthy();
    expect(typeof drift.json.drift_report.deltas.avg_sentence_length).toBe("number");
    expect(["closer_to_baseline", "further_from_baseline", "stable"]).toContain(drift.json.drift_report.direction);
    expect(typeof drift.json.drift_report.explanation).toBe("string");
  });

  it("400s a drift request with no baseline", async () => {
    const r = await post(srv.base, "/voice/drift", { draft_text: "some text" });
    expect(r.status).toBe(400);
  });
});
