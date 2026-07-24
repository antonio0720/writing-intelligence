// Service version + build identity. git_sha is injected at deploy; "dev" locally.
export const SERVICE_VERSION = "3.1.0";
export const DOCTRINE_VERSION = "3.0.0";

export function gitSha(): string {
  return process.env.WI_GIT_SHA?.trim() || "dev";
}
