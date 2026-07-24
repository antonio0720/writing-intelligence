import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { startServer, post, get, type TestServer } from "./helpers.js";

let srv: TestServer;
beforeAll(async () => { srv = await startServer(); });
afterAll(async () => { await srv.close(); });

describe("service surface", () => {
  it("GET /health needs no auth and reports healthy", async () => {
    const r = await get(srv.base, "/health", { token: null });
    expect(r.status).toBe(200);
    expect(r.json.status).toBe("healthy");
    expect(typeof r.json.version).toBe("string");
  });

  it("rejects a missing token with 401", async () => {
    const r = await post(srv.base, "/compile", { request_text: "hi" }, { token: null });
    expect(r.status).toBe(401);
  });

  it("rejects a wrong token with 401", async () => {
    const r = await post(srv.base, "/compile", { request_text: "hi" }, { token: "nope" });
    expect(r.status).toBe(401);
  });

  it("compiles a benign draft to a released bundle (200)", async () => {
    const draft = "We shipped the new export button on Monday. Three users tried it that afternoon. Two hit a timeout, so we raised the limit and shipped a fix the same day. No data was lost.";
    const r = await post(srv.base, "/compile", {
      request_text: "Rewrite this update.",
      draft_text: draft,
      intake_overrides: { arena: "memo" },
      output_modes: ["clean", "scorecard", "epistemic-ledger"],
    });
    expect(r.status).toBe(200);
    expect(r.json.task_id).toMatch(/^wi_v3_[0-9a-f]{16}$/);
    expect(r.json.passes_run).toHaveLength(12);
    expect(r.json.content_hash).toMatch(/^[0-9a-f]{64}$/);
    expect(r.json.prose_rewrite_log).toBeTruthy();
    expect(r.json.voice_fingerprint.metrics.avg_sentence_length).toBeGreaterThan(0);
    expect(r.json.delivery_bundle.delivery_decision).toBe("release");
    expect(typeof r.json.duration_ms).toBe("number");
  });

  it("returns 400 when neither request_text nor draft_text is present", async () => {
    const r = await post(srv.base, "/compile", { intake_overrides: {} });
    expect(r.status).toBe(400);
    expect(r.json.error).toBe("invalid_body");
  });

  it("returns 400 on non-JSON body", async () => {
    const r = await post(srv.base, "/compile", null, { rawBody: "{not json" });
    expect(r.status).toBe(400);
    expect(r.json.error).toBe("invalid_json");
  });

  it("returns 422 with ambiguity_flags on empty input", async () => {
    const r = await post(srv.base, "/compile", { request_text: "" });
    expect(r.status).toBe(422);
    expect(r.json.error).toBe("ambiguity");
    expect(Array.isArray(r.json.ambiguity_flags)).toBe(true);
    expect(r.json.ambiguity_flags.length).toBeGreaterThan(0);
  });

  it("returns 404 for an unknown route", async () => {
    const r = await get(srv.base, "/nope");
    expect(r.status).toBe(404);
  });

  it("serves the parsed manifest with a git sha", async () => {
    const r = await get(srv.base, "/manifest");
    expect(r.status).toBe(200);
    expect(r.json.git_sha).toBe("dev");
    expect(Array.isArray(r.json.manifest.agents)).toBe(true);
    expect(r.json.manifest.agents.length).toBeGreaterThanOrEqual(10);
    expect(r.json.manifest.agents[0].id).toBe("intake_architect");
  });

  it("serves a known schema and 404s an unknown one", async () => {
    const ok = await get(srv.base, "/schemas/intake_contract");
    expect(ok.status).toBe(200);
    expect(ok.json.title).toBe("IntakeContractV3");
    const bad = await get(srv.base, "/schemas/does_not_exist");
    expect(bad.status).toBe(404);
  });

  it("repackages approved content per arena", async () => {
    const r = await post(srv.base, "/repackage", {
      approved_text: "Book a call today and we will map your first funnel in twenty minutes.",
      target_arenas: ["linkedin_post", "twitter_thread", "email"],
    });
    expect(r.status).toBe(200);
    expect(r.json.bundles).toHaveLength(3);
    const arenas = r.json.bundles.map((b: any) => b.arena);
    expect(arenas).toEqual(["linkedin_post", "twitter_thread", "email"]);
  });
});
