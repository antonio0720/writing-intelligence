// Pass 8 — Genre & Arena Alignment. Per-arena channel constraint table + satisfaction check.
import type { Arena, DeliveryBundleV3 } from "../../types";
import { wordCount } from "../text";

export type ChannelConstraints = NonNullable<DeliveryBundleV3["channel_constraints"]>;

// The canonical arena constraint table. char_max = 0 means "no hard character cap".
const ARENA_TABLE: Record<Arena, ChannelConstraints> = {
  memo: { char_max: 0, hashtag_max: 0, headline_variants_required: false, cta_required: false, readability_level: "grade_10" },
  grant_response: { char_max: 0, hashtag_max: 0, headline_variants_required: false, cta_required: false, readability_level: "grade_12" },
  sermon: { char_max: 0, hashtag_max: 0, headline_variants_required: false, cta_required: false, readability_level: "grade_8" },
  caption: { char_max: 2200, hashtag_max: 10, headline_variants_required: false, cta_required: true, readability_level: "grade_6" },
  article: { char_max: 0, hashtag_max: 0, headline_variants_required: true, cta_required: false, readability_level: "grade_9" },
  chapter: { char_max: 0, hashtag_max: 0, headline_variants_required: false, cta_required: false, readability_level: "grade_8" },
  email: { char_max: 5000, hashtag_max: 0, headline_variants_required: true, cta_required: true, readability_level: "grade_7" },
  pitch_slide: { char_max: 600, hashtag_max: 0, headline_variants_required: true, cta_required: false, readability_level: "grade_8" },
  youtube_script: { char_max: 0, hashtag_max: 0, headline_variants_required: true, cta_required: true, readability_level: "grade_7" },
  newsletter: { char_max: 0, hashtag_max: 0, headline_variants_required: true, cta_required: true, readability_level: "grade_8" },
  government_brief: { char_max: 0, hashtag_max: 0, headline_variants_required: false, cta_required: false, readability_level: "grade_12" },
  sop: { char_max: 0, hashtag_max: 0, headline_variants_required: false, cta_required: false, readability_level: "grade_9" },
  speech: { char_max: 0, hashtag_max: 0, headline_variants_required: false, cta_required: true, readability_level: "grade_6" },
  landing_page: { char_max: 0, hashtag_max: 0, headline_variants_required: true, cta_required: true, readability_level: "grade_7" },
  linkedin_post: { char_max: 3000, hashtag_max: 5, headline_variants_required: false, cta_required: true, readability_level: "grade_7" },
  twitter_thread: { char_max: 280, hashtag_max: 3, headline_variants_required: false, cta_required: false, readability_level: "grade_6" },
  instagram_caption: { char_max: 2200, hashtag_max: 30, headline_variants_required: false, cta_required: true, readability_level: "grade_6" },
  press_release: { char_max: 0, hashtag_max: 0, headline_variants_required: true, cta_required: false, readability_level: "grade_10" },
  case_study: { char_max: 0, hashtag_max: 0, headline_variants_required: true, cta_required: true, readability_level: "grade_9" },
  blog_post: { char_max: 0, hashtag_max: 0, headline_variants_required: true, cta_required: false, readability_level: "grade_8" },
};

const VALID_ARENAS = new Set<string>(Object.keys(ARENA_TABLE));

// Aliases from intake vocabulary (which allows arenas the delivery enum spells differently).
const ARENA_ALIASES: Record<string, Arena> = {
  grant: "grant_response",
  investor_update: "memo",
  article_body: "article",
};

export function normalizeArena(raw: string | undefined): Arena {
  if (!raw) return "memo";
  const lower = raw.toLowerCase();
  if (VALID_ARENAS.has(lower)) return lower as Arena;
  if (ARENA_ALIASES[lower]) return ARENA_ALIASES[lower];
  return "memo";
}

export function constraintsFor(arena: Arena): ChannelConstraints {
  return ARENA_TABLE[arena];
}

export interface ArenaCheck {
  constraints: ChannelConstraints;
  satisfied: boolean;
  violations: string[];
}

// Deterministically check the compiled asset against the arena's channel constraints.
export function checkArena(arena: Arena, content: string, ctaPresent: boolean): ArenaCheck {
  const constraints = ARENA_TABLE[arena];
  const violations: string[] = [];

  if (constraints.char_max && constraints.char_max > 0 && content.length > constraints.char_max) {
    violations.push(`char_max_exceeded: ${content.length} > ${constraints.char_max}`);
  }
  const hashtags = (content.match(/#[a-z0-9_]+/gi) ?? []).length;
  if (constraints.hashtag_max !== undefined && constraints.hashtag_max >= 0 && hashtags > constraints.hashtag_max && constraints.hashtag_max > 0) {
    violations.push(`hashtag_max_exceeded: ${hashtags} > ${constraints.hashtag_max}`);
  }
  // hashtag_max === 0 means hashtags are not expected in this arena at all.
  if (constraints.hashtag_max === 0 && hashtags > 0) {
    violations.push(`hashtags_not_allowed: found ${hashtags}`);
  }
  if (constraints.cta_required && !ctaPresent) {
    violations.push("cta_missing: arena requires a call to action.");
  }
  // Empty content in an arena that expects prose is a violation.
  if (wordCount(content) === 0) {
    violations.push("empty_content: no deliverable prose was produced.");
  }

  return { constraints, satisfied: violations.length === 0, violations };
}

const CTA_MARKERS = /\b(book|buy|sign up|subscribe|register|call|reply|click|download|start|join|get started|contact us|learn more|schedule)\b/i;
export function detectCta(content: string): boolean {
  return CTA_MARKERS.test(content);
}
