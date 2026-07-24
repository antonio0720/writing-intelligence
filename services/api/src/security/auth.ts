// Bearer-token auth. Reads WI_API_TOKENS (comma-separated). If unset, a single dev token
// is allowed and a warning is logged. Missing/blank/wrong token => 401.
import type { Request, Response, NextFunction } from "express";
import { timingSafeEqual } from "node:crypto";

const DEV_TOKEN = "dev-wi-token";

let cachedTokens: Set<string> | null = null;
let warnedDev = false;

export function loadTokens(): Set<string> {
  if (cachedTokens) return cachedTokens;
  const raw = process.env.WI_API_TOKENS?.trim();
  if (raw) {
    cachedTokens = new Set(raw.split(",").map((t) => t.trim()).filter((t) => t.length > 0));
  } else {
    cachedTokens = new Set([DEV_TOKEN]);
    if (!warnedDev) {
      console.warn("[wi-api] WI_API_TOKENS not set — allowing dev token 'dev-wi-token'. Set WI_API_TOKENS in production.");
      warnedDev = true;
    }
  }
  return cachedTokens;
}

// For tests: force a re-read of env.
export function resetTokenCache(): void {
  cachedTokens = null;
  warnedDev = false;
}

function constantTimeHas(tokens: Set<string>, candidate: string): boolean {
  // Compare against every token in constant time to avoid leaking length/first-mismatch.
  let matched = false;
  const candBuf = Buffer.from(candidate);
  for (const token of tokens) {
    const tokenBuf = Buffer.from(token);
    if (tokenBuf.length === candBuf.length && timingSafeEqual(tokenBuf, candBuf)) {
      matched = true;
    }
  }
  return matched;
}

export function requireAuth(req: Request, res: Response, next: NextFunction): void {
  const header = req.header("authorization") ?? "";
  const match = /^Bearer\s+(.+)$/i.exec(header.trim());
  const token = match?.[1]?.trim() ?? "";
  if (!token) {
    res.status(401).json({ error: "unauthorized", detail: "Missing or malformed Authorization header. Use 'Bearer <token>'." });
    return;
  }
  const tokens = loadTokens();
  if (!constantTimeHas(tokens, token)) {
    res.status(401).json({ error: "unauthorized", detail: "Invalid token." });
    return;
  }
  next();
}
