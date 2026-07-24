import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { startServer, post, type TestServer } from "./helpers.js";
import { HARD_BANS } from "../src/runtime/bannedPhrases.js";
import { runSurgery } from "../src/runtime/passes/sentenceSurgery.js";
import { runDiagnostics } from "../src/runtime/passes/diagnostic.js";

let srv: TestServer;
beforeAll(async () => { srv = await startServer(); });
afterAll(async () => { await srv.close(); });

const SLOP = "In today's fast-paced world, we leverage cutting-edge synergy to unlock the power of game-changing results. It's important to note that our world-class team is dedicated to revolutionizing everything. Book a call today.";

describe("banned-phrase engine", () => {
  it("ships a bank of at least 150 hard bans", () => {
    expect(HARD_BANS.length).toBeGreaterThanOrEqual(150);
  });

  it("/score sees hard-ban hits on a raw slop draft", async () => {
    const r = await post(srv.base, "/score", { draft_text: SLOP });
    expect(r.status).toBe(200);
    expect(r.json.scorecard.diagnostics.hard_ban_hits).toBeGreaterThan(0);
  });

  it("/compile removes every hard ban from the clean asset", async () => {
    const r = await post(srv.base, "/compile", {
      request_text: "Rewrite this.",
      draft_text: SLOP,
      intake_overrides: { arena: "blog_post" },
      output_modes: ["clean"],
    });
    expect([200, 423]).toContain(r.status);
    const bundle = r.json.delivery_bundle;
    const clean = bundle.assets.find((a: any) => a.mode === "clean").content.toLowerCase();
    for (const phrase of ["game-changing", "leverage", "cutting-edge", "world-class", "in today's fast-paced world"]) {
      expect(clean).not.toContain(phrase);
    }
    expect(r.json.prose_rewrite_log.summary.hard_ban_count).toBeGreaterThan(0);
  });

  it("surgery is idempotent — a second pass finds nothing to remove (fixpoint)", () => {
    const first = runSurgery("t", SLOP);
    expect(runDiagnostics(first.clean_text).hard_ban_hits).toBe(0);
    const second = runSurgery("t", first.clean_text);
    expect(second.log.summary?.hard_ban_count).toBe(0);
    expect(second.clean_text).toBe(first.clean_text);
  });
});
