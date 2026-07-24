import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { startServer, post, type TestServer } from "./helpers.js";

let srv: TestServer;
beforeAll(async () => { srv = await startServer(); });
afterAll(async () => { await srv.close(); });

describe("epistemic delivery gate", () => {
  it("blocks (423) an unsupported numeric claim under citations_required", async () => {
    const r = await post(srv.base, "/compile", {
      request_text: "Rewrite this investor line.",
      draft_text: "Revenue grew 340% last quarter and we captured 87% of the market.",
      intake_overrides: { arena: "memo", high_stakes: true, constraints: { citations_required: true } },
    });
    expect(r.status).toBe(423);
    expect(r.json.error).toBe("delivery_blocked");
    expect(r.json.epistemic_ledger.delivery_block).toBe(true);
    expect(r.json.delivery_bundle.delivery_decision).toBe("block");
    expect(r.json.blocking_reasons.length).toBeGreaterThan(0);
  });

  it("does not block a claim-free draft", async () => {
    const r = await post(srv.base, "/compile", {
      request_text: "Rewrite this note.",
      draft_text: "Thanks for meeting today. I will send the notes and follow up on Thursday about next steps.",
      intake_overrides: { arena: "memo" },
    });
    expect(r.status).toBe(200);
    expect(r.json.epistemic_ledger.delivery_block).toBe(false);
  });

  it("a numeric claim WITHOUT a citation requirement is not force-blocked", async () => {
    const r = await post(srv.base, "/compile", {
      request_text: "Rewrite this casual post.",
      draft_text: "We got 12 signups this week which felt great. Book a call to see how.",
      intake_overrides: { arena: "linkedin_post" },
    });
    // No citations_required, not high-stakes → the numeric claim is user-provided, not blocked.
    expect(r.status).toBe(200);
    expect(r.json.epistemic_ledger.delivery_block).toBe(false);
  });

  it("/score returns a scorecard and an epistemic ledger", async () => {
    const r = await post(srv.base, "/score", {
      draft_text: "We are the best in the industry and everyone agrees we always win.",
      high_stakes: true,
    });
    expect(r.status).toBe(200);
    expect(typeof r.json.scorecard.v3_composite).toBe("number");
    expect(r.json.epistemic_ledger.claims.length).toBeGreaterThan(0);
    expect(r.json.passes_run).toContain(5);
  });
});
