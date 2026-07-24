// Writing Intelligence v3.1 — deterministic REST reference runtime. Express, ESM, tsx.
import express, { type Request, type Response, type NextFunction } from "express";
import { pathToFileURL } from "node:url";
import { requireAuth } from "./security/auth";
import { resolveTenant } from "./security/tenant";
import { rateLimitOk } from "./security/limits";
import { scrub, serverError } from "./security/sanitize";
import { SERVICE_VERSION, gitSha } from "./version";
import { compileRouter } from "./routes/compile";
import { scoreRouter } from "./routes/score";
import { voiceRouter } from "./routes/voice";
import { repackageRouter } from "./routes/repackage";
import { benchmarkRouter } from "./routes/benchmark";
import { manifestRouter } from "./routes/manifest";

export function createApp(): express.Express {
  const app = express();
  app.disable("x-powered-by");
  app.use(express.json({ limit: "2mb" }));

  // /health — no auth.
  app.get("/health", (_req: Request, res: Response) => {
    res.status(200).json({ status: "healthy", version: SERVICE_VERSION, git_sha: gitSha() });
  });

  // Everything below requires a valid bearer token.
  app.use(requireAuth);

  // Per token+tenant sliding-window rate limit → 429.
  app.use((req: Request, res: Response, next: NextFunction) => {
    const tenant = resolveTenant(req);
    const token = (req.header("authorization") ?? "").replace(/^Bearer\s+/i, "").trim();
    const key = `${tenant}:${token}`;
    if (!rateLimitOk(key)) {
      res.status(429).json({ error: "rate_limit", detail: "Too many requests; retry after the window resets." });
      return;
    }
    next();
  });

  app.use(compileRouter);
  app.use(scoreRouter);
  app.use(voiceRouter);
  app.use(repackageRouter);
  app.use(benchmarkRouter);
  app.use(manifestRouter);

  // 404 for anything unmatched.
  app.use((_req: Request, res: Response) => {
    res.status(404).json({ error: "not_found" });
  });

  // Central error handler. Body-parse + size errors → 400; everything else → sanitized 500.
  app.use((err: unknown, _req: Request, res: Response, _next: NextFunction) => {
    const e = err as { type?: string; status?: number; message?: string };
    if (e?.type === "entity.parse.failed" || err instanceof SyntaxError) {
      res.status(400).json({ error: "invalid_json", detail: "Request body is not valid JSON." });
      return;
    }
    if (e?.type === "entity.too.large") {
      res.status(400).json({ error: "input_too_large", detail: "Request body exceeds the size limit." });
      return;
    }
    console.error("[wi-api] unhandled error:", scrub(String(e?.message ?? err)));
    res.status(500).json(serverError());
  });

  return app;
}

const PORT = Number(process.env.PORT ?? 4090);

// Start listening only when run directly (not when imported by tests).
const isMain = process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href;
if (isMain) {
  const app = createApp();
  app.listen(PORT, () => {
    console.log(`[wi-api] Writing Intelligence v${SERVICE_VERSION} (git ${gitSha()}) listening on :${PORT}`);
  });
}
