// Tenant boundary. The optional x-wi-tenant header namespaces results and salts the task_id
// so two tenants never collide on the same body. v1 is stateless — no cross-tenant store exists.
import type { Request } from "express";

const DEFAULT_TENANT = "public";
const TENANT_RE = /^[a-zA-Z0-9_-]{1,64}$/;

export function resolveTenant(req: Request): string {
  const raw = req.header("x-wi-tenant")?.trim();
  if (!raw) return DEFAULT_TENANT;
  if (!TENANT_RE.test(raw)) return DEFAULT_TENANT; // reject junk rather than trust it
  return raw;
}
