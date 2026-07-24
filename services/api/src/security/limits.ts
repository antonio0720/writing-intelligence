// Input limits + a simple in-process rate limiter (per token+tenant sliding window).
export const MAX_INPUT_CHARS = 200_000;

export class InputTooLargeError extends Error {
  readonly field: string;
  readonly total: number;
  constructor(field: string, total: number) {
    super(`Input exceeds ${MAX_INPUT_CHARS} chars (field=${field}, total=${total}).`);
    this.field = field;
    this.total = total;
  }
}

// Sum the character weight of all text fields; throw if the combined size is too large.
export function assertWithinLimit(fields: Record<string, unknown>): void {
  let total = 0;
  for (const [name, value] of Object.entries(fields)) {
    if (typeof value === "string") {
      total += value.length;
    } else if (Array.isArray(value)) {
      for (const item of value) if (typeof item === "string") total += item.length;
    }
    if (total > MAX_INPUT_CHARS) throw new InputTooLargeError(name, total);
  }
}

interface Bucket {
  count: number;
  windowStart: number;
}

const WINDOW_MS = 60_000;
const MAX_PER_WINDOW = Number(process.env.WI_RATE_LIMIT ?? 120);
const buckets = new Map<string, Bucket>();

// Returns true if the caller is within budget; false if rate-limited.
export function rateLimitOk(key: string, now = Date.now()): boolean {
  const bucket = buckets.get(key);
  if (!bucket || now - bucket.windowStart >= WINDOW_MS) {
    buckets.set(key, { count: 1, windowStart: now });
    return true;
  }
  bucket.count++;
  return bucket.count <= MAX_PER_WINDOW;
}

export function resetRateLimits(): void {
  buckets.clear();
}
