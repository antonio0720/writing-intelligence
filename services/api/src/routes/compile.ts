import { Router, type Request, type Response } from "express";
import { compile, checkAmbiguity, type KernelInput } from "../runtime/Kernel";
import { taskId, contentHash } from "../runtime/ids";
import { resolveTenant } from "../security/tenant";
import { assertWithinLimit, InputTooLargeError } from "../security/limits";
import type { IntakeOverrides } from "../runtime/passes/intake";

export const compileRouter = Router();

interface CompileBody {
  request_text?: unknown;
  draft_text?: unknown;
  intake_overrides?: unknown;
  output_modes?: unknown;
}

function validate(body: CompileBody): { ok: true; input: Omit<KernelInput, "task_id" | "created_at"> } | { ok: false; detail: string } {
  if (typeof body !== "object" || body === null) return { ok: false, detail: "Body must be a JSON object." };
  const { request_text, draft_text, intake_overrides, output_modes } = body;
  if (request_text !== undefined && typeof request_text !== "string") return { ok: false, detail: "request_text must be a string." };
  if (draft_text !== undefined && typeof draft_text !== "string") return { ok: false, detail: "draft_text must be a string." };
  if (request_text === undefined && draft_text === undefined) return { ok: false, detail: "One of request_text or draft_text is required." };
  if (output_modes !== undefined && (!Array.isArray(output_modes) || output_modes.some((m) => typeof m !== "string"))) {
    return { ok: false, detail: "output_modes must be an array of strings." };
  }
  if (intake_overrides !== undefined && (typeof intake_overrides !== "object" || intake_overrides === null || Array.isArray(intake_overrides))) {
    return { ok: false, detail: "intake_overrides must be an object." };
  }
  return {
    ok: true,
    input: {
      request_text: (request_text as string) ?? "",
      draft_text: draft_text as string | undefined,
      overrides: intake_overrides as IntakeOverrides | undefined,
      output_modes: output_modes as string[] | undefined,
    },
  };
}

compileRouter.post("/compile", (req: Request, res: Response) => {
  const tenant = resolveTenant(req);
  const parsed = validate(req.body ?? {});
  if (!parsed.ok) {
    res.status(400).json({ error: "invalid_body", detail: parsed.detail });
    return;
  }

  try {
    assertWithinLimit({
      request_text: parsed.input.request_text,
      draft_text: parsed.input.draft_text,
      overrides: JSON.stringify(parsed.input.overrides ?? {}),
    });
  } catch (e) {
    if (e instanceof InputTooLargeError) {
      res.status(400).json({ error: "input_too_large", detail: e.message });
      return;
    }
    throw e;
  }

  const started = Date.now();
  const created_at = new Date().toISOString();
  const canonicalRequest = {
    request_text: parsed.input.request_text,
    draft_text: parsed.input.draft_text ?? null,
    intake_overrides: parsed.input.overrides ?? null,
    output_modes: parsed.input.output_modes ?? null,
  };
  const task_id = taskId(canonicalRequest, tenant);
  const input: KernelInput = { ...parsed.input, task_id, created_at };

  // Pass 1 — ambiguity gate → 422.
  const { flags } = checkAmbiguity(input);
  if (flags.length > 0) {
    res.status(422).json({ error: "ambiguity", task_id, tenant, ambiguity_flags: flags });
    return;
  }

  const result = compile(input);
  const duration_ms = Date.now() - started;

  const blocked = result.epistemic_ledger.delivery_block || result.delivery_bundle.delivery_decision === "block";

  if (blocked) {
    res.status(423).json({
      error: "delivery_blocked",
      task_id,
      tenant,
      delivery_bundle: result.delivery_bundle,
      blocking_reasons: result.delivery_bundle.blocking_reasons ?? [],
      epistemic_ledger: result.epistemic_ledger,
    });
    return;
  }

  const artifacts = {
    intake_contract: result.intake_contract,
    delivery_bundle: result.delivery_bundle,
    scorecard: result.scorecard,
    epistemic_ledger: result.epistemic_ledger,
    prose_rewrite_log: result.prose_rewrite_log,
    voice_fingerprint: result.voice_fingerprint,
    passes_run: result.passes_run,
  };
  const content_hash = contentHash(artifacts);

  res.status(200).json({
    task_id,
    tenant,
    ...artifacts,
    content_hash,
    duration_ms,
  });
});
