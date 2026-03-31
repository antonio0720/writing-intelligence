# Gold Outputs

## Purpose

These are before/after pairs showing the compiler's transformations at
sentence, paragraph, and section level. They serve as calibration targets
for output quality.

---

## Sentence-Level Transformations

### Example 1: Removing AI Residue + Adding Specificity

Before:
"In today's rapidly evolving digital landscape, artificial intelligence is
transforming the way businesses operate."

After:
"Amazon cut 27,000 warehouse jobs in 2024 and replaced them with robotic
picking systems that cost 40% less per unit handled."

Score delta: +35 points. The rewrite names an actor, provides a number,
specifies a mechanism, and grounds the claim in verifiable reality.

### Example 2: Deflating Inflated Verbs

Before:
"Our platform revolutionizes how teams collaborate by leveraging cutting-edge
AI to optimize workflow efficiency."

After:
"The platform routes tasks based on each team member's current load and
deadline proximity. Average completion time dropped from 4.2 to 2.8 days
across 340 teams in the pilot."

Score delta: +30 points. "Revolutionizes" → specific mechanism. "Leveraging
cutting-edge AI" → what it actually does. "Optimize workflow efficiency" →
measured outcome.

### Example 3: Variance Injection

Before (uniform — std dev ~3):
"The study examined social media usage patterns. Researchers collected data
from over five thousand participants. The findings revealed significant
correlations. These results suggest important implications for policy."

After (varied — std dev ~11):
"Five thousand participants. That's the dataset. What Twenge's team found in
it should have ended the 'social media is fine' argument: adolescents logging
more than three hours daily showed depressive symptom rates 35% above baseline,
and the curve wasn't linear — it bent sharply at the two-hour mark, suggesting
a threshold effect rather than a dose-response gradient."

Score delta: +40 points. Sentence lengths: 3, 4, 48 words. The variance alone
would shift this from "AI-flagged" to "human-classified" on most detectors.

---

## Paragraph-Level Transformations

### Example 4: Thesis Paragraph

Before:
"Education is an important topic that affects many people around the world.
There are many different perspectives on how education should be approached.
In this essay, I will explore some of the key issues related to education
reform and discuss potential solutions."

After:
"The U.S. spends $15,000 per student annually — more than every G7 nation
except Luxembourg — and ranks 25th in math among OECD countries. Money is not
the constraint. How the money reaches classrooms is. Seventy-three percent of
education funding flows through local property taxes, which means the zip code
a child is born into determines the quality of the education they receive. This
is not an allocation inefficiency. It is a design feature."

Score: 88/100. Specific data. Named mechanism. Clear thesis. Provocative
closing claim. Variance in sentence length (15, 5, 21, 23, 8 words).

### Example 5: Evidence Paragraph

Before:
"Many studies have shown that remote work increases productivity. Workers who
work from home report being happier and more efficient. Companies that adopt
remote work policies tend to see positive results."

After:
"Bloom's 2022 study of 1,612 employees at a major travel agency — the largest
randomized controlled trial on hybrid work to date — found that hybrid workers
(three office days, two remote) showed 35% lower attrition, equivalent
satisfaction scores, and no measurable productivity loss. But Bloom himself
qualifies the finding: the gains concentrated in individual-task roles. For
roles requiring real-time collaboration, the picture was murkier, with
managers reporting a 15-20% increase in coordination costs that didn't appear
in the productivity metrics."

Score: 91/100. Named researcher. Named study design. Specific sample size.
Specific results with qualifiers. Counterpoint from the same source. Honest
about what the evidence doesn't show.

---

## Section-Level Transformations

### Example 6: Strategy Section (Before)

"We need to focus on growth. Our team is aligned on the importance of
expanding our market presence. By leveraging our core competencies and
optimizing our go-to-market strategy, we can drive significant value for
all stakeholders. Moving forward, it will be critical to ensure that our
strategic priorities are properly communicated across the organization."

### Example 6: Strategy Section (After)

"**Current state**: Revenue is $8.4M ARR, flat for three quarters. Net
revenue retention dropped from 108% to 94% since Q1. Two of our top-10
accounts are in active procurement review with competitors.

**Root cause**: Our product serves the mid-market buyer who signed in 2022.
That buyer now has 14 alternatives that didn't exist at signing. We haven't
shipped a feature that changed our competitive position since the dashboard
redesign in September 2024.

**Recommendation**: Ship the API integration layer by June 30. This is the
single feature that 7 of our 10 at-risk accounts have requested. Engineering
estimates 11 weeks. I'm asking for 8 by pulling two engineers from the mobile
project, which can absorb a 6-week delay without revenue impact.

**Risk**: If we don't ship by June 30, the two accounts in procurement review
will likely churn, representing $1.2M in ARR. If we pull the engineers from
mobile, the Q4 mobile launch slips to Q1 2027.

**Decision needed**: Approve the engineering reallocation by Friday. I'll
brief the mobile team Monday."

Score: 93/100. Every claim has a number. Every recommendation has an owner.
Every risk is quantified. Decision point is clear with a deadline.

---

## Dialogue Transformation

### Example 7: Before

"I'm really angry at you," Sarah said angrily. "You betrayed my trust and
I don't know if I can ever forgive you."
"I'm sorry," John replied apologetically. "I never meant to hurt you. I hope
you can find it in your heart to forgive me."
"I don't know if I can," Sarah said sadly.

### Example 7: After

Sarah set her keys on the counter. Not in the bowl where they went. On the
counter. "I called the restaurant."

"Which one?"

"Don't do that." She opened the refrigerator, stared at nothing inside it,
and closed it. "I called Marta's. You told me you were working late."

John pulled out a chair but didn't sit.

"She said you weren't there. That you haven't been there in weeks. She
thought I was funny." Sarah's voice was flat. Not angry. Past angry. "She
actually laughed."

The clock above the stove read 11:40.

"I want you to pack a bag tonight," she said. "We can figure out the rest
when I've decided if there's a rest to figure out."

Score: 92/100. Emotion shown through action (keys on counter, staring into
fridge, clock detail). Subtext (the restaurant call reveals without
explaining). Dialogue compressed. No adverbs on tags. Power dynamic visible.
The final line carries the weight.
