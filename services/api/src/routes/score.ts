import { Router, type Request, type Response } from "express";
import { scoreOnly, type KernelInput } from "../runtime/Kernel";
import { taskId } from "../runtime/ids";
import { resolveTenant } from "../security/tenant";
import { assertWithinLimit, InputTooLargeError } from "../security/limits";
import type { IntakeOverrides } from "../runtime/passes/intake";

export const scoreRouter = Router();

scoreRouter.post("/score", (req: Request, res: Response) => {
  const tenant = resolveTenant(req);
  const body = (req.body ?? {}) as Record<string, unknown>;
  if (typeof body !== "object" || body === null) {
    res.status(400).json({ error: "invalid_body", detail: "Body must be a JSON object." });
    return;
  }
  const draft_text = body.draft_text;
  if (typeof draft_text !== "string" || draft_text.length === 0) {
    res.status(400).json({ error: "invalid_body", detail: "draft_text (non-empty string) is required." });
    return;
  }
  const genre_stack = Array.isArray(body.genre_stack) && body.genre_stack.every((g) => typeof g === "string")
    ? (body.genre_stack as string[]) : undefined;

  try {
    assertWithinLimit({ draft_text });
  } catch (e) {
    if (e instanceof InputTooLargeError) {
      res.status(400).json({ error: "input_too_large", detail: e.message });
      return;
    }
    throw e;
  }

  const overrides: IntakeOverrides = {
    mode: "score",
    voice: typeof body.voice === "string" ? body.voice : undefined,
    genre_stack,
    high_stakes: typeof body.high_stakes === "boolean" ? body.high_stakes : undefined,
    arena: typeof body.arena === "string" ? body.arena : undefined,
  };

  const created_at = new Date().toISOString();
  const canonicalRequest = { draft_text, genre_stack: genre_stack ?? null, voice: overrides.voice ?? null, high_stakes: overrides.high_stakes ?? null, arena: overrides.arena ?? null };
  const task_id = taskId(canonicalRequest, tenant);
  const input: KernelInput = { task_id, request_text: "Score this draft.", draft_text, overrides, created_at };

  const { scorecard, ledger, passes_run } = scoreOnly(input);
  res.status(200).json({ task_id, tenant, scorecard, epistemic_ledger: ledger, passes_run });
});
