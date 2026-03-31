# Example 1: AI Slop → Human Prose

**Transformation**: Generic AI output → Specific, voiced, human-sounding writing
**Passes used**: Full pipeline (all 6 passes)
**Voice**: casual sharp
**Score delta**: 31 → 87

---

## Before (Score: 31/100)

In today's rapidly evolving digital landscape, artificial intelligence has emerged as a transformative force that is reshaping industries across the globe. From healthcare to finance, AI is revolutionizing the way we work, live, and interact with the world around us. However, this technological revolution also brings with it a host of challenges and ethical considerations that we must carefully navigate.

It's worth noting that the impact of AI extends far beyond mere automation. At its core, AI represents a fundamental shift in how we approach problem-solving and decision-making. As we stand at this crossroads, it's crucial that we consider both the immense potential and the significant risks that AI presents for our collective future.

Furthermore, the democratization of AI tools has created new opportunities for businesses of all sizes. Small companies can now leverage cutting-edge technology that was previously only available to large enterprises. This paradigm shift is creating a more level playing field, though it also raises important questions about data privacy and algorithmic bias.

### Violations Found
- Hard-ban phrases: "In today's rapidly evolving," "It's worth noting," "At its core," "paradigm shift," "leverage," "democratization"
- Cadence: LLM list rhythm (all sentences 18-22 words, identical S-V-O structure)
- Sentence-length std dev: 2.8 (target: ≥8)
- Zero specific claims — no names, numbers, dates, or examples
- Every paragraph opens with a generalization
- Closing is a vague gesture at "important questions"

---

## After (Score: 87/100)

OpenAI laid off its entire safety team in May 2024. Not downsized. Dissolved. The people whose job it was to make sure the technology didn't cause harm were removed by the company building the technology most likely to cause harm. That fact alone should end the "AI companies will regulate themselves" argument. It didn't.

Six months later, the same company released a model that could generate a human-sounding voice from a 15-second sample. No consent architecture. No opt-out mechanism. The product shipped because the market rewarded speed and the regulatory vacuum allowed it.

The small-business story is real but more complicated than the brochure version. A bakery in Waco, Texas can now run targeted ads using the same machine learning stack that Coca-Cola uses. That access costs $50/month instead of $500,000/year. The trade: every customer interaction feeds a data pipeline the bakery owner doesn't control, can't audit, and agreed to in paragraph 47 of a terms-of-service document nobody reads. Cheap tools aren't free tools. The currency is just different.

### What Changed
- Opening: specific event, named company, specific date, specific action
- Sentence lengths: 6, 3, 26, 5, 24, 13, 29, 18, 25, 7, 5 (std dev: 9.1)
- Zero hard-ban phrases
- Three named entities (OpenAI, Waco Texas, Coca-Cola)
- Specific numbers ($50/month, $500,000/year, 15-second, paragraph 47)
- Closing sentence: 5 words. Lands.
- Voice: casual sharp — conversational, opinionated, respects the reader

---

*Try it yourself: paste the "Before" text into Claude with Writing Intelligence installed and ask it to rewrite.*
