import { Router, type Request, type Response } from "express";
import { runBenchmark } from "../runtime/benchmark";
import { contentHash } from "../runtime/ids";
import { resolveTenant } from "../security/tenant";

export const benchmarkRouter = Router();

// POST /benchmark/run — { case_id, against_version? } → BenchmarkResultV3.
benchmarkRouter.post("/benchmark/run", (req: Request, res: Response) => {
  const tenant = resolveTenant(req);
  const body = (req.body ?? {}) as Record<string, unknown>;
  const case_id = body.case_id;
  if (typeof case_id !== "string" || case_id.length === 0) {
    res.status(400).json({ error: "invalid_body", detail: "case_id (non-empty string) is required." });
    return;
  }
  const against_version = typeof body.against_version === "string" ? body.against_version : undefined;

  const ran_at = new Date().toISOString();
  const result = runBenchmark(case_id, against_version, ran_at);
  if (!result) {
    res.status(404).json({ error: "unknown_case", detail: `No benchmark case '${case_id}'. Known: ai_slop_rewrite.` });
    return;
  }

  res.status(200).json({ tenant, ...result, content_hash: contentHash(result) });
});
