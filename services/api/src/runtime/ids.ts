// Deterministic identity + content hashing. No Date/timestamp ever feeds a hash.
import { createHash } from "node:crypto";

// Keys that are timestamps or non-deterministic envelope metadata; stripped before hashing.
const TIMESTAMP_KEYS = new Set(["created_at", "ran_at"]);

// Canonical JSON: recursively sort object keys so key order never changes the hash.
export function canonicalJSON(value: unknown): string {
  return JSON.stringify(canonicalize(value));
}

function canonicalize(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(canonicalize);
  if (value && typeof value === "object") {
    const src = value as Record<string, unknown>;
    const out: Record<string, unknown> = {};
    for (const key of Object.keys(src).sort()) {
      out[key] = canonicalize(src[key]);
    }
    return out;
  }
  return value;
}

// Strip timestamp keys recursively so a hash is stable across runs.
export function stripTimestamps(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(stripTimestamps);
  if (value && typeof value === "object") {
    const src = value as Record<string, unknown>;
    const out: Record<string, unknown> = {};
    for (const key of Object.keys(src)) {
      if (TIMESTAMP_KEYS.has(key)) continue;
      out[key] = stripTimestamps(src[key]);
    }
    return out;
  }
  return value;
}

export function sha256Hex(input: string): string {
  return createHash("sha256").update(input, "utf8").digest("hex");
}

// content_hash = sha256(canonicalJSON(artifact-minus-timestamps)).
export function contentHash(artifact: unknown): string {
  return sha256Hex(canonicalJSON(stripTimestamps(artifact)));
}

// task_id = "wi_v3_" + sha256(canonical(request)).slice(0,16). Tenant is folded in as a salt.
export function taskId(request: unknown, tenant: string): string {
  const canonical = canonicalJSON({ tenant, request });
  return "wi_v3_" + sha256Hex(canonical).slice(0, 16);
}
