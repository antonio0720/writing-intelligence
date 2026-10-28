import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { createHash } from "node:crypto";
import { startServer, post, type TestServer } from "./helpers.js";

let srv: TestServer;
beforeAll(async () => { srv = await startServer(); });
afterAll(async () => { await srv.close(); });

const NOTES = "I built a miniature town in my garage in 2024.";
const sha = (t: string) => createHash("sha256").update(t, "utf8").digest("hex");

function dossier(overrides: Record<string, unknown> = {}) {
  return {
    schema: "wi9-authorship-2",
    document: { path: "draft.txt", origin: "human_authored", arena: "journalism",
                venue_policy: "human_only", intended_use: "submission", expected_sha256: sha(NOTES) },
    contribution_log: [{ kind: "human_original" }],
    evidence: [{ id: "e1", claim: "The author built a miniature town.", kind: "firsthand",
                 source_path: "notes.txt", sha256: sha(NOTES), exact_excerpt: NOTES,
                 source_origin: "human_authored", experience_state: "observed", consent: true }],
    document_claim_anchors: [{ exact_excerpt: NOTES, evidence_id: "e1" }],
    ...overrides,
  };
}
const files = { "draft.txt": NOTES, "notes.txt": NOTES };

describe("v9 authorship audit over REST", () => {
  it("relays REVIEW from the Python checker, never as permission", async () => {
    const r = await post(srv.base, "/v9/authorship/audit", { dossier: dossier(), files });
    expect(r.status).toBe(200);
    expect(r.json.exit_code).toBe(0);
    expect(r.json.report.status).toBe("REVIEW");
    expect(r.json.report.declaration_status).toBe("self_reported");
    expect(r.json.release_authorized).toBe(false);
  });

  it("relays HOLD with its reason code and exit 3", async () => {
    const d = dossier();
    (d.document as Record<string, unknown>).origin = "ai_generated";
    const r = await post(srv.base, "/v9/authorship/audit", { dossier: d, files });
    expect(r.json.exit_code).toBe(3);
    expect(r.json.report.status).toBe("HOLD");
    expect(r.json.report.findings.map((f: { code: string }) => f.code)).toContain("HUMAN_ONLY_CONFLICT");
  });

  it("refuses file names that could leave the private directory", async () => {
    for (const name of ["../x.txt", "/etc/hosts", "a/../../x", "dossier.json", ".hidden"]) {
      const r = await post(srv.base, "/v9/authorship/audit", { dossier: dossier(), files: { ...files, [name]: "x" } });
      expect(r.status, name).toBe(400);
    }
  });

  it("refuses a body without a dossier object", async () => {
    const r = await post(srv.base, "/v9/authorship/audit", { dossier: [], files });
    expect(r.status).toBe(400);
  });

  it("refuses an oversized body", async () => {
    const r = await post(srv.base, "/v9/authorship/audit", { dossier: dossier(), files: { "draft.txt": "a".repeat(250_000) } });
    expect(r.status).toBe(400);
    expect(r.json.error).toBe("input_too_large");
  });

  it("does not offer release over the network", async () => {
    const r = await post(srv.base, "/v9/authorship/release", { dossier: dossier(), files });
    expect(r.status).toBe(403);
    expect(r.json.error).toBe("release_is_local");
  });

  it("still requires a token", async () => {
    const r = await post(srv.base, "/v9/authorship/audit", { dossier: dossier(), files }, { token: null });
    expect(r.status).toBe(401);
  });
});

describe("v9 hot-phrase scan over REST", () => {
  it("returns editorial findings with digests and no release authority", async () => {
    const r = await post(srv.base, "/v9/hotphrases/scan", { text: "That matters because the invoice was 32 days late." });
    expect(r.status).toBe(200);
    expect(r.json.report.rule_count).toBe(334);
    expect(r.json.report.findings[0].id).toBe("empty_emphasis_001");
    expect(r.json.report.release_authorized).toBe(false);
  });

  it("refuses empty text", async () => {
    const r = await post(srv.base, "/v9/hotphrases/scan", { text: "" });
    expect(r.status).toBe(400);
  });
});
