import { Router, type Request, type Response } from "express";
import { normalizeArena, checkArena, detectCta } from "../runtime/passes/arena";
import { taskId, contentHash } from "../runtime/ids";
import { resolveTenant } from "../security/tenant";
import { assertWithinLimit, InputTooLargeError } from "../security/limits";
import { wordCount } from "../runtime/text";
import type { DeliveryBundleV3 } from "../types";

export const repackageRouter = Router();

// POST /repackage — Pass 8 only. Repackage already-approved content for each target arena.
repackageRouter.post("/repackage", (req: Request, res: Response) => {
  const tenant = resolveTenant(req);
  const body = (req.body ?? {}) as Record<string, unknown>;
  const approved_text = body.approved_text;
  const target_arenas = body.target_arenas;

  if (typeof approved_text !== "string" || approved_text.length === 0) {
    res.status(400).json({ error: "invalid_body", detail: "approved_text (non-empty string) is required." });
    return;
  }
  if (!Array.isArray(target_arenas) || target_arenas.length === 0 || target_arenas.some((a) => typeof a !== "string")) {
    res.status(400).json({ error: "invalid_body", detail: "target_arenas must be a non-empty array of strings." });
    return;
  }

  try {
    assertWithinLimit({ approved_text });
  } catch (e) {
    if (e instanceof InputTooLargeError) { res.status(400).json({ error: "input_too_large", detail: e.message }); return; }
    throw e;
  }

  const cta = detectCta(approved_text);
  const bundles: DeliveryBundleV3[] = (target_arenas as string[]).map((raw) => {
    const arena = normalizeArena(raw);
    const check = checkArena(arena, approved_text, cta);
    const task_id = taskId({ approved_text, arena }, tenant);
    return {
      task_id,
      version: "3.0.0",
      arena,
      assets: [{
        mode: "clean",
        content: approved_text,
        format: "markdown",
        word_count: wordCount(approved_text),
        char_count: approved_text.length,
      }],
      channel_constraints: check.constraints,
      constraints_satisfied: check.satisfied,
      delivery_decision: check.satisfied ? "release" : "hold_for_review",
      blocking_reasons: check.violations,
    };
  });

  res.status(200).json({ tenant, bundles, content_hash: contentHash(bundles) });
});
