import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { startServer, post, type TestServer } from "./helpers.js";
import { runBenchmark } from "../src/runtime/benchmark.js";

let srv: TestServer;
beforeAll(async () => { srv = await startServer(); });
afterAll(async () => { await srv.close(); });

describe("ai_slop_rewrite benchmark", () => {
  it("PASSes: detects the expected slop and scores inside the expected range", async () => {
    const r = await post(srv.base, "/benchmark/run", { case_id: "ai_slop_rewrite", against_version: "2.0" });
    expect(r.status).toBe(200);
    expect(r.json.category).toBe("ai_slop_rewrite");
    expect(r.json.decision).toBe("PASS");
    expect(r.json.score_within_range).toBe(true);
    expect(r.json.v3_score).toBeGreaterThanOrEqual(r.json.score_range_expected.min);
    expect(r.json.v3_score).toBeLessThanOrEqual(r.json.score_range_expected.max);
    expect(r.json.detection_recall).toBeGreaterThanOrEqual(0.6);
    expect(r.json.failure_modes_detected.length).toBeGreaterThan(0);
    expect(r.json.regression_hazards_observed).toHaveLength(0);
  });

  it("404s an unknown case", async () => {
    const r = await post(srv.base, "/benchmark/run", { case_id: "not_a_case" });
    expect(r.status).toBe(404);
  });

  it("is deterministic across runs (same score + run_id)", () => {
    const a = runBenchmark("ai_slop_rewrite", "2.0", "2020-01-01T00:00:00Z")!;
    const b = runBenchmark("ai_slop_rewrite", "2.0", "2099-12-31T23:59:59Z")!;
    expect(a.v3_score).toBe(b.v3_score);
    expect(a.run_id).toBe(b.run_id);
    expect(a.detection_recall).toBe(b.detection_recall);
  });
});
