import { Router, type Request, type Response } from "express";
import { readFileSync } from "node:fs";
import { loadManifest } from "../runtime/manifest";
import { repoPath } from "../paths";
import { SERVICE_VERSION, gitSha } from "../version";

export const manifestRouter = Router();

// GET /manifest — the agent manifest as JSON + build identity.
manifestRouter.get("/manifest", (_req: Request, res: Response) => {
  const manifest = loadManifest();
  res.status(200).json({ version: SERVICE_VERSION, git_sha: gitSha(), manifest });
});

const SCHEMA_IDS = new Set([
  "intake_contract", "epistemic_ledger", "voice_fingerprint", "delivery_bundle",
  "prose_rewrite_log", "benchmark_result", "genre_stack", "architecture_graph",
  "corpus_map", "storyworld_memory", "agent_task",
]);
const SCHEMA_ID_RE = /^[a-z0-9_]+$/;

// GET /schemas/:id — return the matching JSON Schema (404 if unknown).
manifestRouter.get("/schemas/:id", (req: Request, res: Response) => {
  const id = req.params.id;
  if (!SCHEMA_ID_RE.test(id) || !SCHEMA_IDS.has(id)) {
    res.status(404).json({ error: "unknown_schema", detail: `No schema '${id}'.` });
    return;
  }
  try {
    const raw = readFileSync(repoPath("schemas", `${id}.schema.json`), "utf8");
    res.status(200).type("application/json").send(raw);
  } catch {
    res.status(404).json({ error: "unknown_schema", detail: `Schema file for '${id}' not found.` });
  }
});
