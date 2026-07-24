// Repo-relative path resolution. services/api/src/paths.ts → repo root is four levels up.
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url)); // .../services/api/src
// WI_REPO_ROOT lets a container point at a flattened layout (schemas/ + agents/ side by side);
// locally it resolves to the repo root three levels above src/.
export const REPO_ROOT = process.env.WI_REPO_ROOT?.trim() || resolve(HERE, "..", "..", "..");

export function repoPath(...segments: string[]): string {
  return resolve(REPO_ROOT, ...segments);
}
