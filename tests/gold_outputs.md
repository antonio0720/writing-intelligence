# Gold Outputs

## Purpose

These are before/after pairs showing the compiler's transformations at
sentence, paragraph, and section level. They serve as calibration targets
for output quality. The "Score" lines are illustrative rubric judgments written by
the maintainers for teaching; they are not measured benchmark results and no
v9 quality measurement has been run.

---

## The rule for every example in this file

A rewrite may add only what the author's own material supplies. Each example
below shows the **source card** the author provided; every fact in the
"After" comes from that card, and anything the card does not supply is marked
`[needs source]` rather than invented. The figures on the cards are synthetic
teaching fixtures — they are not claims about any real company, study or
person. (v9 replaced the v8 versions of Examples 1–5, which added named
actors, studies and statistics that no source supplied — the exact
fabrication v4 Law C forbids — and claimed a rewrite would change a detector's
classification.)

---

## Sentence-Level Transformations

### Example 1: Removing Templated Framing + Adding Specificity

Before:
"In today's rapidly evolving digital landscape, artificial intelligence is
transforming the way businesses operate."

Source card (author's notes): *Our warehouse replaced manual picking on two of
six lines with automated pickers in March; cost per order on those lines fell
from $1.10 to $0.70.*

After:
"In March we automated picking on two of our six warehouse lines. Cost per
order on those lines fell from $1.10 to $0.70."

Score delta: +35 points. The rewrite names the actor, the change and the
measured result — all from the author's card. Nothing about other companies
was added.

### Example 2: Deflating Inflated Verbs

Before:
"Our platform revolutionizes how teams collaborate by leveraging cutting-edge
AI to optimize workflow efficiency."

Source card (pilot report): *Tasks are routed by each member's open load and
due date. Pilot: 34 teams, median completion 4.2 → 2.8 days.*

After:
"The platform routes each task by the assignee's open load and due date. In
a 34-team pilot, median completion time fell from 4.2 to 2.8 days."

Score delta: +30 points. "Revolutionizes" → the mechanism. "Leveraging
cutting-edge AI" → what it actually does. "Optimize workflow efficiency" →
the measured outcome, scoped to the pilot that measured it.

### Example 3: Rhythm From Meaning

Before:
"The study examined social media usage patterns. Researchers collected data
from over five thousand participants. The findings revealed significant
correlations. These results suggest important implications for policy."

Source card: *Cohort study, about 5,000 adolescents. Heavier daily use was
associated with more reported depressive symptoms. Design is observational;
the authors state it cannot show cause.*

After:
"About five thousand adolescents, followed over time. Those who used social
media more each day reported more depressive symptoms — an association, not
proof of cause, as the study's authors say themselves. What that means for
policy depends on effect sizes [needs source] the summary does not give."

Score delta: +40 points. The four same-weight sentences became one point
(the association), its limit (observational) and an honest gap
([needs source]). Rhythm changed because the content has a claim, a
qualification and a missing number — not to hit a length pattern. No
researcher, percentage or threshold was invented.

---

## Paragraph-Level Transformations

### Example 4: Thesis Paragraph

Before:
"Education is an important topic that affects many people around the world.
There are many different perspectives on how education should be approached.
In this essay, I will explore some of the key issues related to education
reform and discuss potential solutions."

Source card: *State budget office: per-pupil spending in the top-funded
district is 2.1× the bottom district; most of the gap traces to local
property-tax revenue.*

After:
"In this state, the best-funded district spends 2.1 times as much per pupil
as the worst-funded one, and most of that gap comes from local property
taxes. So the question is not how much the state spends. It is how the
money reaches classrooms — and right now a child's address decides it."

Score: 88/100. A sourced figure, a named mechanism, a clear thesis that the
evidence supports. The comparison to other countries in the v8 version was
removed: no source supplied it.

### Example 5: Evidence Paragraph

Before:
"Many studies have shown that remote work increases productivity. Workers who
work from home report being happier and more efficient. Companies that adopt
remote work policies tend to see positive results."

Source card: *[Citation the author supplies]: randomized trial of hybrid
schedules at one employer; lower attrition in the hybrid group; no measured
productivity loss; authors note results may not generalize to
collaboration-heavy roles.*

After:
"A randomized trial at one employer [citation] found lower attrition among
hybrid workers and no measured productivity loss. The authors limit the
claim themselves: the result may not hold for roles that depend on real-time
collaboration. 'Many studies' becomes one study, scoped to what it tested."

Score: 91/100. One named source in place of "many studies", its result, and
its own stated limit. Effect sizes appear only if the citation supplies
them; the v8 version invented them.

---

## Section-Level Transformations

### Example 6: Strategy Section (Before)

"We need to focus on growth. Our team is aligned on the importance of
expanding our market presence. By leveraging our core competencies and
optimizing our go-to-market strategy, we can drive significant value for
all stakeholders. Moving forward, it will be critical to ensure that our
strategic priorities are properly communicated across the organization."

### Example 6: Strategy Section (After)

Source card (synthetic, the author's operating notes): *$8.4M ARR flat three quarters; NRR 108% → 94%; two top-10 accounts in procurement review; 14 alternatives since 2022; last differentiating release Sept 2024; API layer requested by 7 of 10 at-risk accounts; engineering estimate 11 weeks; mobile can absorb a 6-week delay.* Every figure below comes from this card; the company is invented.

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
Every risk is quantified. Decision point is clear with a deadline. Every
figure here is the author's own operating data (the "before" omitted it); a
rewrite that lacked that data would mark each figure `[needs source]`.

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
