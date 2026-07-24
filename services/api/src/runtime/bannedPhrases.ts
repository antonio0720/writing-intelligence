// The AI-slop hard-ban bank. 150+ phrases. Each entry: the phrase, a rule_id, and an
// optional deterministic replacement used by Pass 6 (Sentence Surgery). Empty replacement
// means "delete the phrase" (the surrounding sentence is left, trimmed).

export interface BanEntry {
  phrase: string;      // lowercase match target
  rule_id: string;
  replacement: string; // deterministic substitute ("" = remove)
  soft?: boolean;      // soft bans are logged but do not trip the auto-fail cap
}

// Hard bans — the phrases a detector or a discerning reader flags on sight.
export const HARD_BANS: BanEntry[] = [
  { phrase: "in today's fast-paced world", rule_id: "PHRASE-001", replacement: "" },
  { phrase: "in today's digital age", rule_id: "PHRASE-002", replacement: "" },
  { phrase: "in today's ever-changing", rule_id: "PHRASE-003", replacement: "" },
  { phrase: "in today's world", rule_id: "PHRASE-004", replacement: "" },
  { phrase: "in an increasingly", rule_id: "PHRASE-005", replacement: "" },
  { phrase: "unlock the power of", rule_id: "PHRASE-006", replacement: "use" },
  { phrase: "unlock the potential", rule_id: "PHRASE-007", replacement: "reach" },
  { phrase: "unleash the power", rule_id: "PHRASE-008", replacement: "use" },
  { phrase: "harness the power of", rule_id: "PHRASE-009", replacement: "use" },
  { phrase: "it's important to note that", rule_id: "PHRASE-010", replacement: "" },
  { phrase: "it is important to note", rule_id: "PHRASE-011", replacement: "" },
  { phrase: "it's worth noting that", rule_id: "PHRASE-012", replacement: "" },
  { phrase: "it is worth noting", rule_id: "PHRASE-013", replacement: "" },
  { phrase: "needless to say", rule_id: "PHRASE-014", replacement: "" },
  { phrase: "at the end of the day", rule_id: "PHRASE-015", replacement: "" },
  { phrase: "when it comes to", rule_id: "PHRASE-016", replacement: "for" },
  { phrase: "when all is said and done", rule_id: "PHRASE-017", replacement: "" },
  { phrase: "the fact of the matter is", rule_id: "PHRASE-018", replacement: "" },
  { phrase: "let's be clear", rule_id: "PHRASE-019", replacement: "" },
  { phrase: "let's face it", rule_id: "PHRASE-020", replacement: "" },
  { phrase: "let's dive in", rule_id: "PHRASE-021", replacement: "" },
  { phrase: "let's dive into", rule_id: "PHRASE-022", replacement: "" },
  { phrase: "let's delve into", rule_id: "PHRASE-023", replacement: "" },
  { phrase: "dive deep into", rule_id: "PHRASE-024", replacement: "examine" },
  { phrase: "delve into", rule_id: "PHRASE-025", replacement: "examine" },
  { phrase: "delve deeper", rule_id: "PHRASE-026", replacement: "look closer" },
  { phrase: "in conclusion", rule_id: "PHRASE-027", replacement: "" },
  { phrase: "in summary", rule_id: "PHRASE-028", replacement: "" },
  { phrase: "to sum up", rule_id: "PHRASE-029", replacement: "" },
  { phrase: "in a nutshell", rule_id: "PHRASE-030", replacement: "" },
  { phrase: "furthermore", rule_id: "PHRASE-031", replacement: "" },
  { phrase: "moreover", rule_id: "PHRASE-032", replacement: "" },
  { phrase: "in addition to this", rule_id: "PHRASE-033", replacement: "also" },
  { phrase: "on the other hand", rule_id: "PHRASE-034", replacement: "but" },
  { phrase: "that being said", rule_id: "PHRASE-035", replacement: "still" },
  { phrase: "with that being said", rule_id: "PHRASE-036", replacement: "still" },
  { phrase: "leverage", rule_id: "PHRASE-037", replacement: "use" },
  { phrase: "leveraging", rule_id: "PHRASE-038", replacement: "using" },
  { phrase: "seamless", rule_id: "PHRASE-039", replacement: "smooth" },
  { phrase: "seamlessly", rule_id: "PHRASE-040", replacement: "smoothly" },
  { phrase: "robust", rule_id: "PHRASE-041", replacement: "strong" },
  { phrase: "game-changer", rule_id: "PHRASE-042", replacement: "" },
  { phrase: "game changer", rule_id: "PHRASE-043", replacement: "" },
  { phrase: "game-changing", rule_id: "PHRASE-044", replacement: "" },
  { phrase: "game changing", rule_id: "PHRASE-045", replacement: "" },
  { phrase: "navigating the landscape", rule_id: "PHRASE-046", replacement: "" },
  { phrase: "navigate the complexities", rule_id: "PHRASE-047", replacement: "" },
  { phrase: "navigating the complex", rule_id: "PHRASE-048", replacement: "" },
  { phrase: "the ever-evolving landscape", rule_id: "PHRASE-049", replacement: "" },
  { phrase: "ever-evolving", rule_id: "PHRASE-050", replacement: "changing" },
  { phrase: "ever-changing", rule_id: "PHRASE-051", replacement: "changing" },
  { phrase: "a testament to", rule_id: "PHRASE-052", replacement: "proof of" },
  { phrase: "stands as a testament", rule_id: "PHRASE-053", replacement: "proves" },
  { phrase: "in the realm of", rule_id: "PHRASE-054", replacement: "in" },
  { phrase: "in the world of", rule_id: "PHRASE-055", replacement: "in" },
  { phrase: "elevate your", rule_id: "PHRASE-056", replacement: "improve your" },
  { phrase: "take it to the next level", rule_id: "PHRASE-057", replacement: "" },
  { phrase: "to the next level", rule_id: "PHRASE-058", replacement: "" },
  { phrase: "tapestry", rule_id: "PHRASE-059", replacement: "mix" },
  { phrase: "rich tapestry", rule_id: "PHRASE-060", replacement: "mix" },
  { phrase: "underscore", rule_id: "PHRASE-061", replacement: "show" },
  { phrase: "underscores", rule_id: "PHRASE-062", replacement: "shows" },
  { phrase: "underscoring", rule_id: "PHRASE-063", replacement: "showing" },
  { phrase: "pivotal", rule_id: "PHRASE-064", replacement: "key" },
  { phrase: "pivotal role", rule_id: "PHRASE-065", replacement: "key role" },
  { phrase: "plays a pivotal role", rule_id: "PHRASE-066", replacement: "matters" },
  { phrase: "plays a crucial role", rule_id: "PHRASE-067", replacement: "matters" },
  { phrase: "plays a vital role", rule_id: "PHRASE-068", replacement: "matters" },
  { phrase: "crucial", rule_id: "PHRASE-069", replacement: "key" },
  { phrase: "myriad", rule_id: "PHRASE-070", replacement: "many" },
  { phrase: "a myriad of", rule_id: "PHRASE-071", replacement: "many" },
  { phrase: "plethora", rule_id: "PHRASE-072", replacement: "plenty" },
  { phrase: "a plethora of", rule_id: "PHRASE-073", replacement: "many" },
  { phrase: "revolutionize", rule_id: "PHRASE-074", replacement: "change" },
  { phrase: "revolutionizing", rule_id: "PHRASE-075", replacement: "changing" },
  { phrase: "revolutionary", rule_id: "PHRASE-076", replacement: "new" },
  { phrase: "cutting-edge", rule_id: "PHRASE-077", replacement: "new" },
  { phrase: "state-of-the-art", rule_id: "PHRASE-078", replacement: "new" },
  { phrase: "world-class", rule_id: "PHRASE-079", replacement: "" },
  { phrase: "best-in-class", rule_id: "PHRASE-080", replacement: "" },
  { phrase: "next-generation", rule_id: "PHRASE-081", replacement: "new" },
  { phrase: "paradigm shift", rule_id: "PHRASE-082", replacement: "shift" },
  { phrase: "synergy", rule_id: "PHRASE-083", replacement: "fit" },
  { phrase: "synergies", rule_id: "PHRASE-084", replacement: "fits" },
  { phrase: "empower", rule_id: "PHRASE-085", replacement: "help" },
  { phrase: "empowering", rule_id: "PHRASE-086", replacement: "helping" },
  { phrase: "empowers", rule_id: "PHRASE-087", replacement: "helps" },
  { phrase: "passionate professionals", rule_id: "PHRASE-088", replacement: "our team" },
  { phrase: "passionate about", rule_id: "PHRASE-089", replacement: "focused on" },
  { phrase: "dedicated to", rule_id: "PHRASE-090", replacement: "we" },
  { phrase: "committed to delivering", rule_id: "PHRASE-091", replacement: "we deliver" },
  { phrase: "strive to", rule_id: "PHRASE-092", replacement: "" },
  { phrase: "we pride ourselves", rule_id: "PHRASE-093", replacement: "" },
  { phrase: "pleased to share", rule_id: "PHRASE-094", replacement: "" },
  { phrase: "pleased to announce", rule_id: "PHRASE-095", replacement: "" },
  { phrase: "excited to announce", rule_id: "PHRASE-096", replacement: "" },
  { phrase: "thrilled to announce", rule_id: "PHRASE-097", replacement: "" },
  { phrase: "we are pleased to", rule_id: "PHRASE-098", replacement: "we" },
  { phrase: "tremendous growth", rule_id: "PHRASE-099", replacement: "growth" },
  { phrase: "tremendous", rule_id: "PHRASE-100", replacement: "" },
  { phrase: "well-positioned", rule_id: "PHRASE-101", replacement: "ready" },
  { phrase: "significant market share", rule_id: "PHRASE-102", replacement: "market share" },
  { phrase: "execute against", rule_id: "PHRASE-103", replacement: "run" },
  { phrase: "strategic priorities", rule_id: "PHRASE-104", replacement: "priorities" },
  { phrase: "exceptional value", rule_id: "PHRASE-105", replacement: "value" },
  { phrase: "deliver exceptional", rule_id: "PHRASE-106", replacement: "deliver" },
  { phrase: "stakeholders", rule_id: "PHRASE-107", replacement: "" },
  { phrase: "value proposition", rule_id: "PHRASE-108", replacement: "offer" },
  { phrase: "think outside the box", rule_id: "PHRASE-109", replacement: "" },
  { phrase: "outside the box", rule_id: "PHRASE-110", replacement: "" },
  { phrase: "push the envelope", rule_id: "PHRASE-111", replacement: "" },
  { phrase: "move the needle", rule_id: "PHRASE-112", replacement: "" },
  { phrase: "low-hanging fruit", rule_id: "PHRASE-113", replacement: "" },
  { phrase: "boots on the ground", rule_id: "PHRASE-114", replacement: "" },
  { phrase: "circle back", rule_id: "PHRASE-115", replacement: "return" },
  { phrase: "deep dive", rule_id: "PHRASE-116", replacement: "close look" },
  { phrase: "drill down", rule_id: "PHRASE-117", replacement: "focus" },
  { phrase: "transformational change", rule_id: "PHRASE-118", replacement: "change" },
  { phrase: "transformative", rule_id: "PHRASE-119", replacement: "" },
  { phrase: "drive transformational", rule_id: "PHRASE-120", replacement: "drive" },
  { phrase: "cannot be overstated", rule_id: "PHRASE-121", replacement: "" },
  { phrase: "cannot be understated", rule_id: "PHRASE-122", replacement: "" },
  { phrase: "read that again", rule_id: "PHRASE-123", replacement: "" },
  { phrase: "let that sink in", rule_id: "PHRASE-124", replacement: "" },
  { phrase: "here's the thing", rule_id: "PHRASE-125", replacement: "" },
  { phrase: "here's the kicker", rule_id: "PHRASE-126", replacement: "" },
  { phrase: "most people don't realize", rule_id: "PHRASE-127", replacement: "" },
  { phrase: "what most people miss", rule_id: "PHRASE-128", replacement: "" },
  { phrase: "think about it", rule_id: "PHRASE-129", replacement: "" },
  { phrase: "spoiler alert", rule_id: "PHRASE-130", replacement: "" },
  { phrase: "plot twist", rule_id: "PHRASE-131", replacement: "" },
  { phrase: "buckle up", rule_id: "PHRASE-132", replacement: "" },
  { phrase: "the secret to", rule_id: "PHRASE-133", replacement: "" },
  { phrase: "the key takeaway", rule_id: "PHRASE-134", replacement: "" },
  { phrase: "the bottom line is", rule_id: "PHRASE-135", replacement: "" },
  { phrase: "make no mistake", rule_id: "PHRASE-136", replacement: "" },
  { phrase: "rest assured", rule_id: "PHRASE-137", replacement: "" },
  { phrase: "look no further", rule_id: "PHRASE-138", replacement: "" },
  { phrase: "the importance of", rule_id: "PHRASE-139", replacement: "" },
  { phrase: "in this article, we'll explore", rule_id: "PHRASE-140", replacement: "" },
  { phrase: "in this article we will explore", rule_id: "PHRASE-141", replacement: "" },
  { phrase: "in this piece", rule_id: "PHRASE-142", replacement: "" },
  { phrase: "by the end of this", rule_id: "PHRASE-143", replacement: "" },
  { phrase: "comprehensive understanding", rule_id: "PHRASE-144", replacement: "clear picture" },
  { phrase: "comprehensive guide", rule_id: "PHRASE-145", replacement: "guide" },
  { phrase: "transforming every industry", rule_id: "PHRASE-146", replacement: "" },
  { phrase: "changing the way we", rule_id: "PHRASE-147", replacement: "" },
  { phrase: "the way we work, live", rule_id: "PHRASE-148", replacement: "" },
  { phrase: "businesses and consumers alike", rule_id: "PHRASE-149", replacement: "" },
  { phrase: "whether you're a", rule_id: "PHRASE-150", replacement: "" },
  { phrase: "no matter your", rule_id: "PHRASE-151", replacement: "" },
  { phrase: "foster", rule_id: "PHRASE-152", replacement: "build" },
  { phrase: "facilitate", rule_id: "PHRASE-153", replacement: "help" },
  { phrase: "utilize", rule_id: "PHRASE-154", replacement: "use" },
  { phrase: "utilizing", rule_id: "PHRASE-155", replacement: "using" },
  { phrase: "spearhead", rule_id: "PHRASE-156", replacement: "lead" },
  { phrase: "bespoke", rule_id: "PHRASE-157", replacement: "custom" },
  { phrase: "curated", rule_id: "PHRASE-158", replacement: "chosen" },
  { phrase: "holistic", rule_id: "PHRASE-159", replacement: "whole" },
  { phrase: "unprecedented", rule_id: "PHRASE-160", replacement: "" },
  { phrase: "leverages", rule_id: "PHRASE-161", replacement: "uses" },
  { phrase: "empowered", rule_id: "PHRASE-162", replacement: "helped" },
  { phrase: "utilizes", rule_id: "PHRASE-163", replacement: "uses" },
  { phrase: "fosters", rule_id: "PHRASE-164", replacement: "builds" },
  { phrase: "facilitates", rule_id: "PHRASE-165", replacement: "helps" },
];

// Soft bans — hedge/filler words. Logged, replaced, but do not trip the auto-fail cap.
export const SOFT_BANS: BanEntry[] = [
  { phrase: "very", rule_id: "SOFT-001", replacement: "", soft: true },
  { phrase: "really", rule_id: "SOFT-002", replacement: "", soft: true },
  { phrase: "actually", rule_id: "SOFT-003", replacement: "", soft: true },
  { phrase: "basically", rule_id: "SOFT-004", replacement: "", soft: true },
  { phrase: "essentially", rule_id: "SOFT-005", replacement: "", soft: true },
  { phrase: "simply put", rule_id: "SOFT-006", replacement: "", soft: true },
  { phrase: "in order to", rule_id: "SOFT-007", replacement: "to", soft: true },
  { phrase: "a variety of", rule_id: "SOFT-008", replacement: "several", soft: true },
];

// AI-opener patterns (first-sentence tells). Detected in Pass 3, penalized in scoring.
export const AI_OPENERS: string[] = [
  "in today's", "in an increasingly", "in the world of", "in the realm of",
  "as we all know", "we all know that", "picture this", "imagine a world",
  "have you ever", "in this article", "in this post", "in this guide",
  "artificial intelligence is transforming", "the digital age",
];

function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

// Word-boundary matcher shared by the diagnostic scan and sentence surgery, so residual
// counts and rewrites can never disagree (the "leverages vs leverage" class of bug).
export function banRegex(phrase: string): RegExp {
  const escaped = escapeRegExp(phrase);
  const left = /^[a-z0-9]/i.test(phrase) ? "\\b" : "";
  const right = /[a-z0-9]$/i.test(phrase) ? "\\b" : "";
  return new RegExp(left + escaped + right, "gi");
}

export function countBan(text: string, phrase: string): number {
  const m = text.match(banRegex(phrase));
  return m ? m.length : 0;
}

let combined: BanEntry[] | null = null;
export function allBans(): BanEntry[] {
  if (!combined) {
    // Longest phrases first so multi-word bans match before their single-word substrings.
    combined = [...HARD_BANS, ...SOFT_BANS].sort((a, b) => b.phrase.length - a.phrase.length);
  }
  return combined;
}

export function hardBanCount(): number {
  return HARD_BANS.length;
}
