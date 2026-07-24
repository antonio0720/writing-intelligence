// Deterministic text-analysis primitives shared across passes. Pure functions, no state.

export function splitSentences(text: string): string[] {
  if (!text.trim()) return [];
  // Split on sentence-ending punctuation followed by whitespace. Keep it simple + deterministic.
  const raw = text
    .replace(/\s+/g, " ")
    .trim()
    .split(/(?<=[.!?])\s+/);
  return raw.map((s) => s.trim()).filter((s) => s.length > 0);
}

export function splitParagraphs(text: string): string[] {
  return text
    .split(/\n\s*\n/)
    .map((p) => p.trim())
    .filter((p) => p.length > 0);
}

export function words(text: string): string[] {
  const matched = text.toLowerCase().match(/[a-z0-9']+/g);
  return matched ?? [];
}

export function wordCount(text: string): number {
  return words(text).length;
}

export function mean(nums: number[]): number {
  if (nums.length === 0) return 0;
  return nums.reduce((a, b) => a + b, 0) / nums.length;
}

export function stddev(nums: number[]): number {
  if (nums.length === 0) return 0;
  const m = mean(nums);
  const variance = mean(nums.map((n) => (n - m) ** 2));
  return Math.sqrt(variance);
}

// Round to 3 decimals so hashes stay stable and JSON stays tidy.
export function round(n: number, places = 3): number {
  const f = 10 ** places;
  return Math.round(n * f) / f;
}

export function countMatches(haystack: string, needle: string): number {
  if (!needle) return 0;
  let count = 0;
  let idx = haystack.indexOf(needle);
  while (idx !== -1) {
    count++;
    idx = haystack.indexOf(needle, idx + needle.length);
  }
  return count;
}
