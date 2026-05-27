# Writing Intelligence v3.0 — User Guide

The complete how-to. 250+ prompts. Organized by operator tier (beginner → expert), domain, voice, and use case.

**For the kernel doctrine, read `SKILL.md`.**
**For the one-page summary, read `CHEATSHEET.md`.**

---

## Table of Contents

1. [Getting Started — 5 Essential Prompts](#getting-started)
2. [The 11-Pass Kernel In Practice](#kernel-in-practice)
3. [By Tier — Beginner / Operator / Architect](#by-tier)
4. [By Domain — 26 Genre Packs](#by-domain)
5. [By Voice — 8 Voiceprints + Custom](#by-voice)
6. [Cross-Arena Repackaging](#cross-arena)
7. [Fiction & Storyworld](#fiction)
8. [High-Stakes Discipline](#high-stakes)
9. [Multi-Agent Orchestration](#multi-agent)
10. [Diagnostics & Debugging](#diagnostics)

---

<a id="getting-started"></a>
## 1. Getting Started — 5 Essential Prompts

### Prompt 1 — Make AI prose sound human

```
Rewrite this to sound like a real person wrote it. Run the full
Writing Intelligence v3.0 kernel. Show me the clean version and
a brief scorecard.

[paste text]
```

### Prompt 2 — Build a custom voice

```
Build a measurable voice fingerprint from these three writing
samples. Output the canonical fingerprint JSON and a one-paragraph
description I can use as a quick reference.

[paste 3 samples, 500+ words each]
```

### Prompt 3 — Score what I just wrote

```
Apply all relevant Writing Intelligence v3.0 scoring rubrics to
this draft. Show me the per-rubric scores, the v3.0 composite,
the auto-fail flags if any, and the top 3 things to fix.

[paste draft]
```

### Prompt 4 — Repackage one piece for multiple arenas

```
Take this approved memo. Run Pass 8 (Arena Delivery) and produce
delivery bundles for: LinkedIn post (1,200 chars), Twitter thread
(8 tweets), YouTube short script (90 seconds), newsletter section
(450 words), internal Slack BLUF (200 words). Preserve voice
fingerprint across all five.

[paste memo]
```

### Prompt 5 — Audit a chapter at full depth

```
Run the full 11-pass kernel on this chapter as fiction. Apply
prose quality + chapter construction + dialogue + power dynamics
+ tension mechanics scoring. Emit the scene graph and update the
storyworld memory if one exists.

[paste chapter]
```

---

<a id="kernel-in-practice"></a>
## 2. The 11-Pass Kernel In Practice

### When to ask for specific passes

| Want | Ask For |
|---|---|
| Quick cleanup | "Run Passes 3 and 6 only" |
| Audit without rewriting | "Run audit mode: Passes 3, 4, 5, 9, 10. Output: scorecard + epistemic ledger + violations." |
| Just the contract | "Run Pass 0 and stop. Show me the intake contract." |
| Just the architecture | "Run through Pass 4 and stop. Show me the architecture graph." |
| Just the ledger | "Run through Pass 5 and stop. Show me the epistemic ledger." |
| Voice diagnosis | "Run Pass 7 against this baseline fingerprint. Show me the drift report." |
| Channel formatting | "Run Pass 8 only. Format this approved content for LinkedIn / YouTube / etc." |
| Benchmark | "Run benchmark case [ID] against v2 baseline. Show me the result." |

### Combining passes with operators

```
Run the kernel through Pass 6 only. Then apply compress(40%),
add_specificity, and strengthen_closing. Show me the rewrite log.
```

---

<a id="by-tier"></a>
## 3. By Tier

### Beginner (Apprentice path)

10 prompts for someone using the skill for the first time:

1. *Rewrite this to sound less like AI.*
2. *Score this and tell me what to fix first.*
3. *Make this more specific.*
4. *Cut this in half without losing the main point.*
5. *Make the opening earn the read.*
6. *Make the closing leave residue.*
7. *Add evidence to claim #2.*
8. *Show me where I'm hedging.*
9. *Show me where I'm padding.*
10. *Pick a voiceprint that fits and rewrite in that voice.*

### Operator (mid-tier)

20 prompts for someone running the system on real work:

11. *Build the intake contract from this messy request.*
12. *Run the corpus audit on these three attached documents.*
13. *Resolve the genre collision between sales and academic.*
14. *Apply the dialogue stress test. Score on the v2.0 dialogue rubric.*
15. *Run power_map and plant_audit on this scene.*
16. *Repackage this newsletter section as a LinkedIn post + Twitter thread.*
17. *Build a team voice fingerprint from these three contributors.*
18. *Check voice drift against this baseline.*
19. *Find every universal quantifier and decide soften / source / remove.*
20. *Build the architecture graph. Surface unsupported claims.*
21. *Run the storyworld memory audit on these 5 chapters.*
22. *Run scenes 1-3 through the dialogue commander. Compare per-character fingerprints.*
23. *Apply grant_nofo + church_leadership stack. Resolve collisions.*
24. *Apply technical_documentation pack to this README.*
25. *Score this against the journalism rubric. Surface composite scenes.*
26. *Apply the loan_officer pack with TRID compliance check.*
27. *Apply real_estate pack and run the local-knowledge check.*
28. *Build a voiceprint for this character. Compare to other characters in the storyworld.*
29. *Run the regression matrix against the prior version of this piece.*
30. *Run the full 11-pass kernel and emit every artifact.*

### Architect (advanced)

20 prompts for someone extending the system:

31. *Propose a new genre pack for [domain]. Include the 15-section schema and 5 benchmark cases.*
32. *Build a new voiceprint with measurable fingerprint and add it to the matrix.*
33. *Extend the architecture graph with a new node type for [purpose].*
34. *Propose a new rewrite operator and demonstrate it on 5 examples.*
35. *Propose a new scoring rubric and show how it interacts with v3.0 Composite.*
36. *Propose a new agent role and demonstrate the handoff.*
37. *Author 5 benchmark cases for a new category.*
38. *Identify a gap in the collision matrix and propose the resolution.*
39. *Propose a schema extension that's backwards compatible.*
40. *Build a multi-agent orchestration script using the agent_manifest.*
41. *Audit the current benchmark gates and propose tighter thresholds.*
42. *Propose a multilingual extension for [language].*
43. *Build an MCP server reference implementation skeleton.*
44. *Build a CLI binary skeleton for the kernel.*
45. *Author an ADR for [decision]. Walk the alternatives.*
46. *Propose a deprecation path for [legacy capability].*
47. *Build a certification audit script.*
48. *Build the team voice enforcement workflow.*
49. *Propose a series escalation curve refinement.*
50. *Open an RFC for [structural change]. Walk through the spec.*

---

<a id="by-domain"></a>
## 4. By Domain — 26 Genre Packs

For each pack, see `references/genre_packs/<pack>.md` for the full doctrine. Here are 5 example prompts per category.

### Grant Writing / NOFO

```
51. Apply grant_nofo. Rewrite this Statement of Need.
52. Build the logic model. Distinguish outputs from outcomes.
53. Audit the budget narrative against the program narrative.
54. Audit for funder fit (RFP attached).
55. Audit the sustainability plan for specificity.
```

### Technical Documentation

```
56. Rewrite this API endpoint doc per technical_documentation pack.
57. Audit code examples — do they run?
58. Add an error documentation block.
59. Refactor for scannability.
60. Apply the runbook structure.
```

### Journalism / Feature

```
61. Write the nut graf for this draft.
62. Audit sources. Surface unattributed claims.
63. Balance scene and exposition.
64. Add the counter-perspective.
65. Refactor the lede.
```

### Resume / Cover Letter

```
66. Quantify every bullet.
67. ATS-keyword-align this resume to the attached JD.
68. Rewrite the cover letter opening (no "I hope this finds you well").
69. Run the 6-second test.
70. Trim to 1 page.
```

### Social Media

```
71. Repackage as LinkedIn post (1,200 chars).
72. Repackage as Twitter thread (8 tweets).
73. Repackage as Instagram caption.
74. Test the hook against the preview cutoff.
75. Cut every CTA except one.
```

### YouTube Script

```
76. Rewrite the first 7 seconds.
77. Identify retention drop points and add beat changes.
78. Add open loops at 90-second intervals.
79. Earn the subscribe CTA.
80. Score the hook against the retention curve.
```

### Newsletter

```
81. Rewrite the subject line + preview text.
82. Cut the "Hey friends" opener.
83. Surface the single CTA.
84. Verify voice consistency against last 3 issues.
85. Strengthen the P.S.
```

### Real Estate

```
86. Replace every cliche with a measurement.
87. Audit for fair housing compliance.
88. Add the comps.
89. Build the investor memo with cap rate.
90. Write the open-house follow-up.
```

### Loan Officer

```
91. Audit for TRID / RESPA / ECOA compliance.
92. Pair every rate with APR.
93. Rewrite without "lowest" / "guaranteed" / "best".
94. Build the refinance break-even.
95. Build the pre-approval letter.
```

### Church Leadership

```
96. Sermon notes — three movements with applications.
97. Bible study guide with discussion questions.
98. Weekly devotional (300-500 words).
99. Bulletin announcement.
100. Pastoral letter (hard news).
```

### Small Business Operator

```
101. Hero copy with the operator's name.
102. About page that sounds like the actual operator.
103. Founder outreach email.
104. Hiring post for first / second / third hire.
105. Investor / lender memo for small business capital.
```

### v2.0 Packs (preserved)

```
106-110. Strategy memo (use strategy.md)
111-115. Fiction scene (use fiction.md)
116-120. Sales page (use sales.md)
121-125. Academic paragraph (use academic.md)
126-130. Speech (use speech.md)
131-135. Sermon (use sermon.md)
136-140. Email (use email.md)
141-145. Pitch deck (use pitch_deck.md)
146-150. Legal positioning (use legal_positioning.md)
151-155. Cinematic narration (use cinematic_narration.md)
156-160. Dialogue v2.0 (use dialogue.md)
161-165. Government brief (use government_brief.md)
166-170. Medical writing (use medical_writing.md)
171-175. Patent claims (use patent_claims.md)
176-180. Thriller scene architecture (use thriller_scene_architecture.md)
181-185. Transmedia (use transmedia_character.md)
```

(Each pack file contains 5 worked examples; see those files for verbatim prompts.)

---

<a id="by-voice"></a>
## 5. By Voice — 8 Voiceprints + Custom

```
186. Rewrite in sovereign_commander voice.
187. Rewrite in literary_recursive voice.
188. Rewrite in sermon_black_church voice.
189. Rewrite in investor_precision voice.
190. Rewrite in founder_manifesto voice.
191. Rewrite in academic_rigorous voice.
192. Rewrite in casual_sharp voice.
193. Rewrite in courageous_builder voice.
194. Build a custom voice fingerprint from these 3 samples.
195. Detect voice drift against this baseline.
```

---

<a id="cross-arena"></a>
## 6. Cross-Arena Repackaging

```
196. Memo → LinkedIn + Twitter + YouTube short + newsletter + Slack.
197. Sermon → social posts + newsletter devotional + bulletin announcement.
198. Grant narrative → 1-page executive summary + funder pitch deck slide.
199. Chapter excerpt → social teaser + newsletter preview + audio drama script.
200. Investor update → board memo + LinkedIn announcement + press release.
```

---

<a id="fiction"></a>
## 7. Fiction & Storyworld

```
201. Run scene_audit on this chapter.
202. Run role_audit and map characters to the 12 archetypes.
203. Run dialogue_stress_test on these exchanges.
204. Run power_map on this confined-space scene.
205. Run plant_audit across the last 5 chapters.
206. Initialize a storyworld memory for this novel.
207. Update the storyworld memory after this chapter.
208. Audit series escalation across 3 books.
209. Check character voice fingerprint stability across appearances.
210. Resolve the canon vs. sanctioned conflict.
211. Build a character voice fingerprint distinguishable from every other character.
212. Audit the foreshadowing ledger. Surface orphaned plants.
213. Audit the terminology lock across the series.
214. Build the lore bible from the storyworld memory.
215. Convert this novel chapter to an audio drama script.
```

---

<a id="high-stakes"></a>
## 8. High-Stakes Discipline

```
216. Mandatory epistemic ledger run on this academic paragraph.
217. Source every numeric claim in this grant narrative.
218. Block fabrication: find every "studies show" without studies.
219. Run universal-quantifier sweep. Surface every all/every/never/always.
220. Run inflated-verb sweep. Surface every revolutionize/transform/disrupt.
221. Audit citation honesty (no invented sources, no misattributed quotes).
222. Mandatory delivery block check: any unsafe sources?
223. Audit this medical write-up for clinical precision.
224. Audit this legal brief for hedging discipline.
225. Audit this financial disclosure for inflation language.
226. Cap the score if delivery_block is true.
227. Surface every ambiguity for user clarification before proceeding.
228. Confirm the success_condition was actually met.
229. Audit against the channel constraints.
230. Build the steel-man counter-argument for the strongest claim.
```

---

<a id="multi-agent"></a>
## 9. Multi-Agent Orchestration

```
231. Run all 12 agents on this draft. Show me each artifact.
232. Run only Intake Architect + Corpus Auditor + Evidence Prosecutor (audit mode).
233. Run only Voice Fingerprinter + Sentence Surgeon + Scorekeeper (voice repair).
234. Run only Narrative Architect + Dialogue Commander (fiction mode).
235. Surface every agent conflict and how it was resolved.
236. Show me the handoff graph (which agent fed which).
237. Block delivery if any agent flagged unsafe.
238. Run benchmark mode: full agent board on case GRANT-04 against v2.
239. Run iteration: take Stress Tester findings, hand back to Sentence Surgeon.
240. Build the delivery bundle (Pass 10) only after Pass 5 ledger clears.
```

---

<a id="diagnostics"></a>
## 10. Diagnostics & Debugging

```
241. Show me where the rewrite log says voice_impact: decreased_fidelity.
242. Show me the orphan nodes from the architecture graph.
243. Show me the unpaid plants from the storyworld memory.
244. Show me every conflict in the corpus map.
245. Show me every ambiguity_flag from the intake contract.
246. Show me the genre stack and its collision resolutions.
247. Show me the v2 vs. v3 score delta for this piece.
248. Show me the channel-constraint violations.
249. Show me the unsafe sources.
250. Show me the fabrication_risk: blocked claims.
251. Show me which auto-fail condition triggered the cap.
252. Show me what the steel-man counter-argument is.
253. Show me which pass took the longest.
254. Show me what would change if I switched voiceprint.
255. Show me the regression hazards for this benchmark case.
```

---

## Beyond 255

The prompts above are starting points. The skill activates on any writing, editing, scoring, fiction, dialogue, grant, sermon, social, journalism, technical, or longform task. Read the SKILL.md for the kernel. Read the genre packs for domain depth. Read the schemas for the machine layer.

**Build what compounds. Ship what survives. The 11-pass kernel is the floor — your voice is the ceiling.**

— Antonio T. Smith Jr. / Density6 LLC
