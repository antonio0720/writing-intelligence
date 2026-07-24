// Shared test harness: boot the real app on an ephemeral port, talk to it over HTTP.
import type { Server } from "node:http";
import type { AddressInfo } from "node:net";
import { createApp } from "../src/server.js";

export const DEV_TOKEN = "dev-wi-token";

export interface TestServer {
  base: string;
  close: () => Promise<void>;
}

export async function startServer(): Promise<TestServer> {
  const app = createApp();
  const server: Server = await new Promise((resolve) => {
    const s = app.listen(0, () => resolve(s));
  });
  const { port } = server.address() as AddressInfo;
  return {
    base: `http://127.0.0.1:${port}`,
    close: () => new Promise<void>((resolve) => server.close(() => resolve())),
  };
}

export async function post(base: string, path: string, body: unknown, opts: { token?: string | null; tenant?: string; rawBody?: string } = {}): Promise<{ status: number; json: any; text: string }> {
  const headers: Record<string, string> = { "content-type": "application/json" };
  if (opts.token !== null) headers["authorization"] = `Bearer ${opts.token ?? DEV_TOKEN}`;
  if (opts.tenant) headers["x-wi-tenant"] = opts.tenant;
  const res = await fetch(`${base}${path}`, {
    method: "POST",
    headers,
    body: opts.rawBody ?? JSON.stringify(body),
  });
  const text = await res.text();
  let json: any = null;
  try { json = JSON.parse(text); } catch { /* non-JSON response */ }
  return { status: res.status, json, text };
}

export async function get(base: string, path: string, opts: { token?: string | null } = {}): Promise<{ status: number; json: any; text: string }> {
  const headers: Record<string, string> = {};
  if (opts.token !== null) headers["authorization"] = `Bearer ${opts.token ?? DEV_TOKEN}`;
  const res = await fetch(`${base}${path}`, { headers });
  const text = await res.text();
  let json: any = null;
  try { json = JSON.parse(text); } catch { /* non-JSON */ }
  return { status: res.status, json, text };
}
