// Voice Fingerprint Engine (Pass 7). Deterministic metric extraction from text.
// Where a metric is a heuristic (metaphor density, vocab tier, authority posture) it is
// labelled as such in the code and the README — these are v1 approximations, not ground truth.
import { splitSentences, splitParagraphs, words, mean, stddev, round } from "./text";
import type { VoiceMetrics, VocabTier } from "../types";

const TRANSITIONS = [
  "however", "therefore", "moreover", "furthermore", "meanwhile", "consequently",
  "nevertheless", "thus", "hence", "instead", "besides", "still", "yet", "also",
  "then", "so", "but", "and", "because", "although", "while", "since",
];

const HEDGES = ["maybe", "perhaps", "might", "could", "possibly", "somewhat", "arguably", "seems", "i think", "we think"];
const IMPERATIVE_STARTERS = ["do", "stop", "build", "ship", "know", "understand", "remember", "listen", "watch", "read", "look", "start", "make", "take", "give", "own"];
const METAPHOR_MARKERS = ["like a", "as if", "as though", "is a", "are the", "a kind of", "a form of"];

export function computeMetrics(text: string): VoiceMetrics {
  const sentences = splitSentences(text);
  const paragraphs = splitParagraphs(text);
  const allWords = words(text);
  const wc = Math.max(allWords.length, 1);

  const sentLens = sentences.map((s) => words(s).length);
  const paraLens = paragraphs.map((p) => words(p).length);

  const commas = (text.match(/,/g) ?? []).length;
  const questions = sentences.filter((s) => s.trim().endsWith("?")).length;

  // Compression ratio: fraction of words that survive a ruthless edit (drop hedges/fillers).
  const fillers = allWords.filter((w) => ["very", "really", "actually", "basically", "essentially", "just", "quite", "that"].includes(w)).length;
  const compression = round((wc - fillers) / wc);

  // Abstraction tolerance: fraction of sentences with an abstract-noun suffix and no concrete number.
  const abstractSentences = sentences.filter((s) => /\b\w+(tion|ment|ness|ity|ance|ence|ism|ology)\b/i.test(s) && !/\d/.test(s)).length;
  const abstraction = round(sentences.length ? abstractSentences / sentences.length : 0);

  // Metaphor density (heuristic): marker hits per 500 words.
  const lower = text.toLowerCase();
  let metaphorHits = 0;
  for (const m of METAPHOR_MARKERS) metaphorHits += (lower.split(m).length - 1);
  const metaphorDensity = round((metaphorHits / wc) * 500);

  const questionFreq = round((questions / wc) * 500);
  const commaDensity = round(sentences.length ? commas / sentences.length : 0);

  // Vocab tier (heuristic): driven by long-word ratio + average word length.
  const longWords = allWords.filter((w) => w.length >= 9).length;
  const longRatio = longWords / wc;
  const avgWordLen = mean(allWords.map((w) => w.length));
  const vocab_tier = vocabTier(longRatio, avgWordLen);

  // Domain vocab per 500w (heuristic): distinct long words as a proxy for specialized terms.
  const distinctLong = new Set(allWords.filter((w) => w.length >= 9)).size;
  const domainVocab = round((distinctLong / wc) * 500);

  // Authority posture (heuristic): 0 = warm/hedged, 100 = dominant/imperative.
  const authority = authorityPosture(sentences, allWords);

  const transitionTop5 = topTransitions(allWords);
  const openings = repertoire(sentences.map((s) => firstWord(s)));
  const closings = repertoire(sentences.map((s) => lastWord(s)));

  return {
    avg_sentence_length: round(mean(sentLens)),
    sentence_length_std: round(stddev(sentLens)),
    avg_paragraph_length: round(mean(paraLens)),
    paragraph_length_std: round(stddev(paraLens)),
    compression_ratio: compression,
    abstraction_tolerance: abstraction,
    metaphor_density: metaphorDensity,
    question_frequency: questionFreq,
    comma_density: commaDensity,
    vocab_tier,
    domain_vocab_per_500w: domainVocab,
    transition_top5: transitionTop5,
    opening_pattern_repertoire: openings,
    closing_pattern_repertoire: closings,
    dominant_syntactic_structures: dominantStructures(sentences),
    authority_posture: authority,
  };
}

function vocabTier(longRatio: number, avgWordLen: number): VocabTier {
  if (longRatio >= 0.22) return "rarefied";
  if (longRatio >= 0.15) return "scholarly";
  if (longRatio >= 0.08 || avgWordLen >= 5) return "educated";
  if (longRatio >= 0.04) return "mixed";
  return "plain";
}

function authorityPosture(sentences: string[], allWords: string[]): number {
  if (sentences.length === 0) return 50;
  const imperatives = sentences.filter((s) => IMPERATIVE_STARTERS.includes(firstWord(s))).length;
  const hedgeHits = allWords.filter((w) => HEDGES.includes(w)).length;
  const impRatio = imperatives / sentences.length;
  const hedgeRatio = hedgeHits / Math.max(allWords.length, 1);
  // Center at 50, push up for imperatives, down for hedging.
  const score = 50 + impRatio * 60 - hedgeRatio * 400;
  return round(Math.max(0, Math.min(100, score)), 1);
}

function topTransitions(allWords: string[]): string[] {
  const counts = new Map<string, number>();
  for (const w of allWords) {
    if (TRANSITIONS.includes(w)) counts.set(w, (counts.get(w) ?? 0) + 1);
  }
  return [...counts.entries()]
    .sort((a, b) => (b[1] - a[1]) || a[0].localeCompare(b[0]))
    .slice(0, 5)
    .map(([w]) => w);
}

function repertoire(tokens: string[]): string[] {
  const counts = new Map<string, number>();
  for (const t of tokens) {
    if (!t) continue;
    counts.set(t, (counts.get(t) ?? 0) + 1);
  }
  return [...counts.entries()]
    .sort((a, b) => (b[1] - a[1]) || a[0].localeCompare(b[0]))
    .slice(0, 5)
    .map(([t]) => t);
}

function dominantStructures(sentences: string[]): string[] {
  const structs = new Set<string>();
  if (sentences.some((s) => words(s).length <= 4)) structs.add("short_declarative");
  if (sentences.some((s) => words(s).length >= 30)) structs.add("long_compound");
  if (sentences.some((s) => s.includes(";"))) structs.add("semicolon_joined");
  if (sentences.some((s) => s.trim().endsWith("?"))) structs.add("interrogative");
  if (sentences.some((s) => /^(and|but|so|because)\b/i.test(s.trim()))) structs.add("conjunction_opener");
  return [...structs].sort();
}

function firstWord(sentence: string): string {
  const w = words(sentence);
  return w.length ? w[0] : "";
}

function lastWord(sentence: string): string {
  const w = words(sentence);
  return w.length ? w[w.length - 1] : "";
}

// Drift: per-metric numeric deltas (current minus baseline) + direction + explanation.
export function computeDrift(
  current: VoiceMetrics,
  baseline: VoiceMetrics,
): { deltas: Record<string, number>; direction: "closer_to_baseline" | "further_from_baseline" | "stable"; explanation: string } {
  const numericKeys: (keyof VoiceMetrics)[] = [
    "avg_sentence_length", "sentence_length_std", "avg_paragraph_length", "paragraph_length_std",
    "compression_ratio", "abstraction_tolerance", "metaphor_density", "question_frequency",
    "comma_density", "domain_vocab_per_500w", "authority_posture",
  ];
  const deltas: Record<string, number> = {};
  let totalAbs = 0;
  for (const key of numericKeys) {
    const c = (current[key] as number) ?? 0;
    const b = (baseline[key] as number) ?? 0;
    const d = round(c - b);
    deltas[key] = d;
    totalAbs += Math.abs(d);
  }
  // Normalize magnitude against sentence-length scale to pick a direction band.
  const magnitude = round(totalAbs);
  let direction: "closer_to_baseline" | "further_from_baseline" | "stable";
  if (magnitude <= 2) direction = "stable";
  else direction = "further_from_baseline";

  const biggest = Object.entries(deltas).sort((a, b) => Math.abs(b[1]) - Math.abs(a[1]))[0];
  const explanation = magnitude <= 2
    ? `Voice is stable against baseline (aggregate metric drift ${magnitude}).`
    : `Voice diverges from baseline (aggregate drift ${magnitude}); largest shift is ${biggest[0]} (${biggest[1] >= 0 ? "+" : ""}${biggest[1]}).`;
  return { deltas, direction, explanation };
}
