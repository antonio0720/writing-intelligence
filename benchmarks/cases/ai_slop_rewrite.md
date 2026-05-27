# Benchmark Category — AI Slop Rewrite

Five cases. Each takes a generic, AI-flavored draft and demands an authored rewrite that preserves the claim while restoring voice.

---

## SLOP-01 — LinkedIn Thought-Leader Post

**Input**:

> In today's fast-paced world, the importance of authentic leadership cannot be overstated. Game-changing leaders are those who think outside the box and leverage their unique perspectives to drive transformational change. Let's be clear: at the end of the day, it's not just about what you do — it's about who you are. Read that again.

**Task Contract**: rewrite, persuade, founder-audience, courageous_builder voice, `social_media` + `linkedin_post`, arena = `linkedin_post`, success: "The reader recognizes themselves and feels the move, not the hype."

**Expected Detections**: hard-ban "In today's", "game-changing", "Let's be clear", "at the end of the day", "It's not just X, it's Y", "Read that again", cadence flag (LinkedIn cadence), abstraction flatness.

**Expected Range**: 78-92. **v2 baseline**: 71. **v3 target**: 88.

---

## SLOP-02 — Corporate "About Us" Page

**Input**:

> At [Company], we are dedicated to revolutionizing the way our customers experience our world-class solutions. Our team of passionate professionals leverages cutting-edge technology and decades of combined experience to deliver game-changing results that empower our clients to achieve their goals.

**Task Contract**: rewrite, inform + persuade, customer audience, `small_business_operator` + `sales`, arena = `landing_page`, success: "A skeptical first-time visitor knows what the company actually does and who runs it."

**Expected Detections**: "revolutionizing", "world-class", "passionate professionals", "cutting-edge", "game-changing", "empower", inflated verbs, missing operator name, no real numbers.

**Expected Range**: 80-90. **v2 baseline**: 74. **v3 target**: 87.

---

## SLOP-03 — "Tips" Blog Post Opener

**Input**:

> Want to improve your writing? Here's the thing — most people don't realize that the secret to great writing isn't talent. It's something much more important. Think about it. The question isn't whether you have what it takes. The question is whether you're willing to put in the work. Spoiler alert: most people aren't.

**Task Contract**: rewrite, teach, general audience, casual_sharp voice, `newsletter`, arena = `blog_post`, success: "Reader keeps reading and trusts the writer."

**Expected Detections**: "Here's the thing", "most people don't realize", "Think about it", "The question isn't X — it's Y", "Spoiler alert", question-stacking, fake profundity.

**Expected Range**: 78-90. **v2 baseline**: 70. **v3 target**: 86.

---

## SLOP-04 — Investor Update

**Input**:

> We are pleased to share that the company is experiencing tremendous growth and is well-positioned to capture significant market share in the coming year. Our team continues to execute against our strategic priorities and we remain confident in our ability to deliver exceptional value to our stakeholders.

**Task Contract**: rewrite, inform, investor audience, investor_precision voice, `email` + `investor_update`, arena = `memo`, success: "Investor knows the actual numbers and the actual risks."

**Expected Detections**: "pleased to share", "tremendous growth", "well-positioned", "significant market share", "execute against strategic priorities", "exceptional value", "stakeholders", missing numbers, missing risks.

**Expected Range**: 82-92. **v2 baseline**: 76. **v3 target**: 89.

---

## SLOP-05 — Educational AI Content

**Input**:

> Artificial intelligence is transforming every industry and changing the way we work, live, and interact. In this article, we'll explore the key trends shaping AI in 2026 and discuss what they mean for businesses and consumers alike. By the end of this piece, you'll have a comprehensive understanding of where AI is headed.

**Task Contract**: rewrite, teach, professional audience, academic_rigorous voice, `journalism`, arena = `article`, success: "Reader trusts the article and reads past the second paragraph."

**Expected Detections**: "transforming every industry", "changing the way we", "In this article, we'll explore", "comprehensive understanding", missing thesis, missing nut graf, missing source.

**Expected Range**: 78-90. **v2 baseline**: 72. **v3 target**: 86.

---

## Scoring Rubrics Applied

- Prose Quality (100)
- Arena Fit (100)
- Epistemic Integrity (100) for SLOP-04 and SLOP-05

## Regression Hazards

- Risk: Rewrite becomes too aggressive, dropping a claim the user made.
- Risk: Voice restoration introduces hard-bans of its own.
- Risk: Compression below `word_count_min` if contract specifies one.
