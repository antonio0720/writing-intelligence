// Output sanitation. Never echo a bearer token; never leak a stack trace to the client.
const BEARER_RE = /Bearer\s+[A-Za-z0-9._\-]+/gi;

export function scrub(text: string): string {
  return text.replace(BEARER_RE, "Bearer [redacted]");
}

// A safe 500 body — the real error is logged server-side, never returned.
export function serverError(): { error: "server_error" } {
  return { error: "server_error" };
}
