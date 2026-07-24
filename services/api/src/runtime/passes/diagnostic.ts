// Pass 3 — Diagnostic Scan. Deterministic slop + cadence metrics used by scoring.
import { HARD_BANS, SOFT_BANS, AI_OPENERS, countBan } from "../bannedPhrases";
import { splitSentences, words, stddev, round } from "../text";

export interface BanHit {
  phrase: string;
  rule_id: string;
  count: number;
  soft: boolean;
}

export interface Diagnostics {
  hard_ban_hits: number;
  soft_ban_hits: number;
  hard_ban_detail: BanHit[];
  soft_ban_detail: BanHit[];
  passive_voice_ratio: number;
  sentence_length_variance: number;
  abstract_noun_density: number;
  em_dash_overuse: boolean;
  ai_opener_detected: boolean;
  perplexity_flatness_run: number; // longest run of same-ish-length consecutive sentences
  fragment_ratio: number;          // fraction of sentences under 4 words (deletion debris)
  grammar_seam_per_100w: number;   // adjacent duplicate words + dangling terminal function words
}

const PASSIVE = /\b(was|were|is|are|been|being|be)\s+\w+(ed|en)\b/i;
const ABSTRACT_NOUN = /\b\w+(tion|ment|ness|ity|ance|ence|ism|ology)\b/gi;
// Deletion seams: an adjacent duplicated word ("our team of our"), or a sentence that ends
// on a dangling function word ("deliver value to our.") — both are marks of rule-based cuts.
const DUP_WORD = /\b(\w+)\s+\1\b/gi;
const DANGLING_TERMINAL = /\b(to|of|the|a|an|and|our|in|for|with|is|are|we|that)\s*[.!?]/gi;

export function runDiagnostics(text: string): Diagnostics {
  const lower = text.toLowerCase();
  const sentences = splitSentences(text);
  const allWords = words(text);
  const wc = Math.max(allWords.length, 1);

  const hard_ban_detail: BanHit[] = [];
  for (const b of HARD_BANS) {
    const count = countBan(lower, b.phrase);
    if (count > 0) hard_ban_detail.push({ phrase: b.phrase, rule_id: b.rule_id, count, soft: false });
  }
  const soft_ban_detail: BanHit[] = [];
  for (const b of SOFT_BANS) {
    const count = countBan(lower, b.phrase);
    if (count > 0) soft_ban_detail.push({ phrase: b.phrase, rule_id: b.rule_id, count, soft: true });
  }

  const hard_ban_hits = hard_ban_detail.reduce((a, h) => a + h.count, 0);
  const soft_ban_hits = soft_ban_detail.reduce((a, h) => a + h.count, 0);

  const passiveCount = sentences.filter((s) => PASSIVE.test(s)).length;
  const passive_voice_ratio = round(sentences.length ? passiveCount / sentences.length : 0);

  const sentLens = sentences.map((s) => words(s).length);
  const sentence_length_variance = round(stddev(sentLens));

  const abstractMatches = (text.match(ABSTRACT_NOUN) ?? []).length;
  const abstract_noun_density = round((abstractMatches / wc) * 100);

  const emDashes = (text.match(/—|--/g) ?? []).length;
  const em_dash_overuse = emDashes >= 3 && sentences.length > 0 && emDashes / sentences.length > 0.5;

  const firstSentence = (sentences[0] ?? "").toLowerCase();
  const ai_opener_detected = AI_OPENERS.some((o) => firstSentence.startsWith(o) || firstSentence.includes(o));

  const perplexity_flatness_run = longestFlatRun(sentLens);

  const fragments = sentences.filter((s) => words(s).length < 4).length;
  const fragment_ratio = round(sentences.length ? fragments / sentences.length : 0);
  const dupWords = (text.match(DUP_WORD) ?? []).length;
  const dangling = (text.match(DANGLING_TERMINAL) ?? []).length;
  const grammar_seam_per_100w = round(((dupWords + dangling) / wc) * 100);

  return {
    hard_ban_hits,
    soft_ban_hits,
    hard_ban_detail,
    soft_ban_detail,
    passive_voice_ratio,
    sentence_length_variance,
    abstract_noun_density,
    em_dash_overuse,
    ai_opener_detected,
    perplexity_flatness_run,
    fragment_ratio,
    grammar_seam_per_100w,
  };
}

// Longest run of consecutive sentences whose lengths differ by <= 2 words (cadence flatness).
function longestFlatRun(lens: number[]): number {
  if (lens.length === 0) return 0;
  let best = 1;
  let cur = 1;
  for (let i = 1; i < lens.length; i++) {
    if (Math.abs(lens[i] - lens[i - 1]) <= 2) {
      cur++;
      best = Math.max(best, cur);
    } else {
      cur = 1;
    }
  }
  return best;
}
