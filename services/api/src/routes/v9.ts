// v9 preview routes. They run the one Python implementation (scripts/wi-authorship.py,
// prototypes/wi9/wi9_hotphrases.py) instead of re-implementing it, inside a private
// temporary directory, with a time limit. `release` is not served: it reads authority
// from a v6 store the operator names, and a network caller is not the operator.
import { Router, type Request, type Response } from "express";
import { execFile } from "node:child_process";
import { mkdtemp, mkdir, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join, posix, resolve, sep } from "node:path";
import { repoPath } from "../paths";
import { assertWithinLimit, InputTooLargeError } from "../security/limits";

export const v9Router = Router();

const PYTHON = process.env.WI_PYTHON?.trim() || "python3";
const TIMEOUT_MS = Number(process.env.WI_V9_TIMEOUT_MS ?? 30_000);
const MAX_FILES = 50;
const SAFE_NAME = /^[A-Za-z0-9_][A-Za-z0-9_.-]*(\/[A-Za-z0-9_][A-Za-z0-9_.-]*)*$/;

type RunResult = { code: number; stdout: string } | { unavailable: string } | { timeout: true };

function runTool(script: string, args: string[]): Promise<RunResult> {
  return new Promise((resolve) => {
    execFile(PYTHON, ["-I", repoPath(...script.split("/")), ...args],
      { timeout: TIMEOUT_MS, maxBuffer: 8 * 1024 * 1024, env: { PATH: process.env.PATH ?? "" } },
      (err, stdout) => {
        const e = err as (NodeJS.ErrnoException & { killed?: boolean; code?: number | string }) | null;
        if (e && e.code === "ENOENT") return resolve({ unavailable: `${PYTHON} not found` });
        if (e && e.killed) return resolve({ timeout: true });
        resolve({ code: typeof e?.code === "number" ? e.code : 0, stdout: String(stdout) });
      });
  });
}

function relayed(res: Response, r: RunResult): void {
  if ("unavailable" in r) {
    res.status(503).json({ error: "v9_runtime_unavailable", detail: `The v9 tools need Python 3.8+ (${r.unavailable}).` });
    return;
  }
  if ("timeout" in r) {
    res.status(504).json({ error: "v9_timeout", detail: `The v9 check exceeded ${TIMEOUT_MS} ms and was stopped.` });
    return;
  }
  let report: unknown;
  try { report = JSON.parse(r.stdout); } catch {
    res.status(500).json({ error: "v9_bad_output", detail: "The v9 tool did not return JSON." });
    return;
  }
  // The report's own status (REVIEW, HOLD) is the answer; HTTP 200 means the check ran.
  res.status(200).json({ exit_code: r.code, report, release_authorized: false });
}

function tooLarge(res: Response, fields: Record<string, unknown>): boolean {
  try { assertWithinLimit(fields); return false; } catch (e) {
    if (e instanceof InputTooLargeError) { res.status(400).json({ error: "input_too_large", detail: e.message }); return true; }
    throw e;
  }
}

v9Router.post("/v9/authorship/audit", async (req: Request, res: Response) => {
  const body = (req.body ?? {}) as Record<string, unknown>;
  const dossier = body.dossier;
  const files = body.files ?? {};
  if (typeof dossier !== "object" || dossier === null || Array.isArray(dossier)) {
    res.status(400).json({ error: "invalid_body", detail: "dossier (object) is required." });
    return;
  }
  if (typeof files !== "object" || files === null || Array.isArray(files)) {
    res.status(400).json({ error: "invalid_body", detail: "files must be an object of relative path to UTF-8 text." });
    return;
  }
  const entries = Object.entries(files as Record<string, unknown>);
  if (entries.length > MAX_FILES) {
    res.status(400).json({ error: "invalid_body", detail: `At most ${MAX_FILES} files.` });
    return;
  }
  for (const [name, text] of entries) {
    if (typeof text !== "string" || !SAFE_NAME.test(name) || name.split("/").includes("..")
        || name === "dossier.json") {
      res.status(400).json({ error: "invalid_body", detail: `files[${JSON.stringify(name)}] must be a plain relative path to a string.` });
      return;
    }
  }
  if (tooLarge(res, { dossier: JSON.stringify(dossier), files: entries.map(([, t]) => t as string) })) return;

  const dir = await mkdtemp(join(tmpdir(), "wi9-audit-"));
  try {
    for (const [name, text] of entries) {
      const target = resolve(dir, ...posix.normalize(name).split("/"));
      if (!target.startsWith(resolve(dir) + sep)) {
        res.status(400).json({ error: "invalid_body", detail: `files[${JSON.stringify(name)}] leaves the working directory.` });
        return;
      }
      await mkdir(dirname(target), { recursive: true });
      await writeFile(target, text as string, { encoding: "utf8", flag: "wx" });
    }
    await writeFile(join(dir, "dossier.json"), JSON.stringify(dossier), { encoding: "utf8", flag: "wx" });
    relayed(res, await runTool("scripts/wi-authorship.py", ["audit", "--input", join(dir, "dossier.json")]));
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
});

v9Router.post("/v9/hotphrases/scan", async (req: Request, res: Response) => {
  const body = (req.body ?? {}) as Record<string, unknown>;
  const text = body.text;
  if (typeof text !== "string" || text.length === 0) {
    res.status(400).json({ error: "invalid_body", detail: "text (non-empty string) is required." });
    return;
  }
  if (tooLarge(res, { text })) return;
  const dir = await mkdtemp(join(tmpdir(), "wi9-scan-"));
  try {
    const input = join(dir, "input.txt");
    await writeFile(input, text, { encoding: "utf8", flag: "wx" });
    const args = ["scan", "--input", input, "--format", "json"];
    if (body.include_quotes === true) args.push("--include-quotes");
    relayed(res, await runTool("prototypes/wi9/wi9_hotphrases.py", args));
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
});

v9Router.post("/v9/authorship/release", (_req: Request, res: Response) => {
  res.status(403).json({
    error: "release_is_local",
    detail: "Release authority is read from a v6 grant store the operator names on their own machine "
      + "(wi authorship release --authority-store). It is not offered over the network.",
  });
});
