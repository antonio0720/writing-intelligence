# Language Tiers

Law C applied to internationalization: an unavailable metric is reported as unavailable, never faked with an English-shaped substitute.

Read this when working in any language other than English, or on multilingual documents.

---

## The problem

The v3 voiceprint metrics — average sentence length in words, sentence-length variance, question frequency, lexical richness — are built on assumptions that do not travel:

- **Chinese, Japanese, Thai, Khmer** have no word delimiters. "Words per sentence" is undefined without a tokenizer, and a whitespace count returns nonsense.
- **German, Finnish, Turkish** compound and agglutinate. Word counts undercount information density relative to English by a large and variable factor.
- **Thai and Khmer** have no sentence-final punctuation convention. Splitting on periods returns one sentence for a whole document.
- **Arabic, Hebrew, Persian, Urdu** run right-to-left, and diff rendering that ignores this scrambles mixed-direction text.
- **Japanese** uses `。`; Arabic uses `؟` and `،`. A period-and-space rule finds nothing.

Computing an English metric on such text and reporting a number is worse than reporting nothing, because the number looks like the ones that mean something.

## The tiers

**Tier 1 — full metric set.** English, Spanish, French, German, Portuguese, Italian, Dutch. Space-delimited, conventional sentence punctuation, metrics behave as the v3 voiceprint system assumes.

**Tier 2 — structural metrics only.** Chinese (Hans/Hant), Japanese, Korean, Arabic, Hebrew, Hindi, Bengali, Russian, Turkish, Vietnamese, Indonesian, Thai, Swahili, Persian, Urdu, Polish, Greek.

Available: paragraph rhythm, repetition, structural balance, sentence count where punctuation permits, compression relative to a supplied baseline in the same language.
Unavailable: word-based length, lexical richness, and anything requiring lemmatization or reliable word segmentation.

**Tier 3 — craft only.** Everything else. All v3 craft doctrine applies: anti-patterns, structure, evidence discipline, genre packs, the full accountability layer. No voiceprint metrics.

## What to say

Never silently omit. State it once, in the report:

> Voice metrics for Thai are not calibrated here, so this scorecard covers structure, evidence, and craft rather than voice measurement. Everything else in the audit works normally.

An author writing in a Tier 3 language loses voice scoring and nothing else. Claim extraction, quotation verification, numeric and date checks, proposal discipline, source hygiene, and the release gate all work — the deterministic checks are language-independent because they compare strings and numbers rather than parse grammar.

## Comparison across languages

Do not compare a metric computed in one language against a baseline built in another. A voiceprint from English samples says nothing about the author's Japanese. If an author has samples in both, build and score separately, and say which is which.

## Translation work

A translated document carries the source document's claims. Verification does not survive translation automatically — the translated sentence must be checked against the source passage, and if the source passage is in a third language, say so and mark the support `cross-language` so a reviewer knows they need to read two languages to check it.

Preserve the original alongside the translation, always. Law B applies with extra force here, because a translation error is invisible to a monolingual reader in a way a rewrite error is not.
