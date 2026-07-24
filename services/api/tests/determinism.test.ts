import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { startServer, post, type TestServer } from "./helpers.js";
import { contentHash, taskId, stripTimestamps } from "../src/runtime/ids.js";

let srv: TestServer;
beforeAll(async () => { srv = await startServer(); });
afterAll(async () => { await srv.close(); });

const BODY = {
  request_text: "Rewrite this for investors.",
  draft_text: "We shipped the export feature and three teams adopted it in a week.",
  intake_overrides: { arena: "memo" },
  output_modes: ["clean", "scorecard", "epistemic-ledger"],
};

describe("determinism", () => {
  it("same input yields the same task_id and content_hash across runs", async () => {
    const a = await post(srv.base, "/compile", BODY);
    const b = await post(srv.base, "/compile", BODY);
    expect(a.status).toBe(200);
    expect(b.status).toBe(200);
    expect(a.json.task_id).toBe(b.json.task_id);
    expect(a.json.content_hash).toBe(b.json.content_hash);
  });

  it("two tenants get distinct task_ids for the same body", async () => {
    const a = await post(srv.base, "/compile", BODY, { tenant: "alpha" });
    const b = await post(srv.base, "/compile", BODY, { tenant: "beta" });
    expect(a.json.task_id).not.toBe(b.json.task_id);
  });

  it("content_hash ignores timestamps (created_at / ran_at)", () => {
    const t1 = { a: 1, created_at: "2020-01-01T00:00:00Z", nested: { ran_at: "2020-01-01T00:00:00Z", v: 2 } };
    const t2 = { a: 1, created_at: "2099-12-31T23:59:59Z", nested: { ran_at: "2099-12-31T23:59:59Z", v: 2 } };
    expect(contentHash(t1)).toBe(contentHash(t2));
    expect(stripTimestamps(t1)).toEqual(stripTimestamps(t2));
  });

  it("content_hash is stable regardless of key order", () => {
    expect(contentHash({ a: 1, b: 2 })).toBe(contentHash({ b: 2, a: 1 }));
  });

  it("taskId is a pure function of request + tenant", () => {
    expect(taskId({ x: 1 }, "t1")).toBe(taskId({ x: 1 }, "t1"));
    expect(taskId({ x: 1 }, "t1")).not.toBe(taskId({ x: 1 }, "t2"));
    expect(taskId({ x: 1 }, "t1")).toMatch(/^wi_v3_[0-9a-f]{16}$/);
  });
});
