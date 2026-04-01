# Writing Intelligence v2.0 — User Guide

**From first install to signature-grade prose. From blank page to masterpiece chapter.**

A complete guide to using Writing Intelligence, the 7-pass writing compiler created by **Antonio T. Smith Jr. / Density6 LLC**.

58 files. 68,770 words. 16 genres. 8 voices. 7 scoring systems. Free forever.

**v2.0** adds the Fiction Intelligence Engine — chapter construction, 12 character role archetypes, dialogue warfare (22 techniques, 9 tension elements), power dynamics, tension mechanics, thriller scene architecture, and transmedia character deepening.

Repository: [github.com/antonio0720/writing-intelligence](https://github.com/antonio0720/writing-intelligence)

---

## Table of Contents

1. [Installation](#1-installation)
2. [Your First 5 Minutes](#2-your-first-5-minutes)
3. [Beginner Guide](#3-beginner-guide)
4. [Intermediate Guide](#4-intermediate-guide)
5. [Advanced Guide](#5-advanced-guide)
6. [Expert Guide](#6-expert-guide)
7. [Prompt Library — By Task](#7-prompt-library--by-task)
8. [Prompt Library — By Genre](#8-prompt-library--by-genre)
9. [Prompt Library — By Voice](#9-prompt-library--by-voice)
10. [Scoring & Diagnostics](#10-scoring--diagnostics)
11. [Academic Mode](#11-academic-mode)
12. [Style Transfer](#12-style-transfer)
13. [Longform & Multi-Session](#13-longform--multi-session)
14. [Fiction & Chapter Construction](#14-fiction--chapter-construction) *(v2.0)*
15. [Character Roles & Dialogue Mastery](#15-character-roles--dialogue-mastery) *(v2.0)*
16. [Thriller & Suspense Craft](#16-thriller--suspense-craft) *(v2.0)*
17. [Transmedia & Storyworld Deepening](#17-transmedia--storyworld-deepening) *(v2.0)*
18. [Worldbuilding Prompts](#18-worldbuilding-prompts) *(v2.0)*
19. [Troubleshooting](#19-troubleshooting)
20. [FAQ](#20-faq)
21. [Quick Reference Card](#21-quick-reference-card)

---

## 1. Installation

### Claude.ai (Easiest)

1. Download `writing-intelligence.skill` from [Releases](https://github.com/antonio0720/writing-intelligence/releases)
2. Open Claude.ai → Settings → Skills
3. Click "Install from file"
4. Select the `.skill` file
5. Start a new conversation. The skill is now active.

### Claude Code

```
git clone https://github.com/antonio0720/writing-intelligence .claude/skills/writing-intelligence
```

### Claude Projects

1. Create a new project or open an existing one
2. Go to Project Knowledge
3. Upload `SKILL.md`
4. Upload the entire `references/` folder
5. The skill is now active in every conversation within that project

### Any Other LLM (ChatGPT, Gemini, etc.)

1. Copy the contents of `SKILL.md`
2. Paste it into your system prompt or custom instructions
3. For deeper functionality, also paste relevant reference files as needed

---

## 2. Your First 5 Minutes

### Prompt 1 — Clean Up AI-Sounding Text

```
Rewrite this paragraph to sound like a real person wrote it:

"In today's rapidly evolving digital landscape, artificial intelligence has emerged as a transformative force that is reshaping industries across the globe. It's worth noting that the impact extends far beyond mere automation."
```

### Prompt 2 — Score a Piece of Writing

```
Score this passage on the 100-point Writing Intelligence scale and tell me what's wrong:

"The company experienced significant growth in recent years. By leveraging our core competencies, we can drive stakeholder value."
```

### Prompt 3 — Write Something From Scratch

```
Write a 300-word opening for a strategy memo about why our company should stop using contractors and hire full-time engineers. Use the sovereign commander voice. Score it when done.
```

### Prompt 4 — Write a Fiction Scene *(v2.0)*

```
Write a 500-word scene where two old friends meet for coffee and one of them is about to deliver devastating news. Show the tension through objects, silence, and what they DON'T say. Score it on both prose quality and dialogue.
```

### Prompt 5 — Audit Your Chapter *(v2.0)*

```
Run a full scene audit on this chapter. Check: Does the setting act as a force? Do props serve dual purposes? Are character roles structurally distinct? Does the pacing follow the compression model? Does every planted detail pay off?

[paste your chapter]
```

If the output is specific, varied in sentence length, architecturally sound, and scores 80+, the skill is working.

---

## 3. Beginner Guide

### What the Skill Does Automatically

Once installed, Writing Intelligence activates whenever you ask Claude to write, edit, rewrite, score, or build fiction. You don't need to invoke it by name. These trigger it automatically:

- "Write me a..." / "Rewrite this..." / "Edit this for..."
- "Score this..." / "Grade my writing..."
- "Write a chapter..." / "Write a scene..." / "Write dialogue..."
- "Build a character..." / "Audit this chapter..."
- "Make this sound more human..."

### The 7 Passes (Simple Version)

1. **Mission Lock** — Figures out what you're doing, who you're writing for, what voice to use
2. **Diagnostic Scan** — Identifies everything wrong: AI phrases, weak arguments, flat rhythm
3. **Structural Rewrite** — Fixes the order: right paragraphs in the right sequence
4. **Sentence Surgery** — Cleans each sentence: removes filler, varies length, adds specificity
5. **Scene & Chapter Audit** — *(v2.0)* For fiction: checks setting, props, roles, power dynamics, pacing, foreshadowing
6. **Stress Test** — Asks: would a smart reader buy this? What feels generic?
7. **Output Modes** — Returns the final draft in your requested format

### 12 Beginner Prompts

```
Rewrite this to remove AI patterns and make it sound human: [paste text]
```

```
Write a professional email to my manager requesting a meeting about my promotion. Under 100 words. Direct, no filler.
```

```
Write a compelling opening paragraph for a blog post about why most small businesses fail at social media marketing.
```

```
Score this writing on the 100-point scale: [paste text]
```

```
Compress this by 40% without losing any meaning: [paste text]
```

```
Raise the intelligence of this passage without adding jargon: [paste text]
```

```
The opening of this piece is weak. Rewrite just the first paragraph to hook the reader: [paste text]
```

```
This ending just summarizes. Rewrite the final paragraph to leave the reader with something unforgettable: [paste text]
```

```
This is too vague. Rewrite with specific names, numbers, dates, and examples: [paste text]
```

```
Edit for clarity and polish. Don't change the structure or voice: [paste text]
```

```
Write a short scene where a father tells his daughter he lost his job. Show it — don't tell it. No emotion words allowed.
```

```
Write dialogue between two coworkers. One is lying. The reader should know, but the other character shouldn't. Use subtext.
```

---

## 4. Intermediate Guide

### Choosing a Voice

| Voice | When to Use It | What It Sounds Like |
|---|---|---|
| `sovereign commander` | Strategy docs, executive comms | Cold, precise, declarative. Zero filler. |
| `academic rigorous` | Papers, research, scholarly writing | Evidence-first, qualified, citation-dense |
| `casual sharp` | Blog posts, newsletters, smart content | Conversational, witty, no hand-holding |
| `literary recursive` | Fiction, creative nonfiction, layered narratives | Image-driven, varied rhythm, subtext-heavy |
| `sermon black church` | Sermons, inspirational speeches | Cadence-built, dignified, call-response |
| `investor precision` | Pitch memos, financial communication | Data-forward, no adjectives |
| `founder manifesto` | Vision statements, rallying cries | Conviction-dense, future-claiming |

```
Write a 500-word essay on why remote work is failing mid-level managers. Use the casual sharp voice.
```

```
Rewrite this investor update in the investor precision voice. Cut all adjectives. Replace them with numbers.
```

### Choosing a Genre Pack

| Genre | What It Optimizes For |
|---|---|
| `academic` | Citations, rubric compliance, claim-evidence binding |
| `strategy` | Situation-complication-recommendation, owners, timelines |
| `fiction` | Scene architecture, show-don't-tell, character deployment *(v2.0)* |
| `dialogue` | Voice distinction, subtext, 9 tension elements *(v2.0)* |
| `thriller_scene_architecture` | Confined space, compression, WWGW framework *(v2.0)* |
| `transmedia_character` | Cross-format character deepening *(v2.0)* |
| `sales` | Hook-story-offer-proof-close |
| `email` | Compression, action clarity |
| `sermon` | Cadence, scriptural grounding, dignity |
| `cinematic_narration` | Shot-based prose, pacing, sensory density |
| `speech` | Delivery rhythm, landing lines |
| `pitch_deck` | Data density, narrative arc, ask clarity |
| `legal_positioning` | Precision, IRAC structure |
| `government_brief` | BLUF, plain language |
| `medical_writing` | IMRAD, evidence hierarchy |
| `patent_claims` | Claim structure, enablement |

### 15 Intermediate Prompts

```
Write a 600-word analysis of subscription fatigue killing SaaS. Sovereign commander voice. Strategy genre. Score it.
```

```
This was written in corporate voice. Rewrite in casual sharp without losing content: [paste text]
```

```
The argument in this piece is soft. Strengthen it: add evidence, address the strongest counterargument: [paste text]
```

```
Diagnose every paragraph: what job does it do? Does it actually do that job? [paste text]
```

```
Give me 5 different openings for an essay about income inequality in education. Each a different technique.
```

```
Give me 4 different closings for this piece: extend, challenge, return to opening, end quietly. [paste text]
```

```
This passage makes claims without backing. Rewrite with specific evidence. If you don't have exact data, tell me what to find: [paste text]
```

```
Compress this 800-word piece to 400 words. Same argument, half the words. Score both: [paste text]
```

```
This passage has flat rhythm. Rewrite with dramatic sentence-length variation. One under 6 words. One over 30: [paste text]
```

```
Remove every trace of corporate voice. No "leverage," no "synergy," no passive voice hiding accountability: [paste text]
```

```
Write a fiction scene where power shifts between two characters. I should be able to track the shift through objects and body language alone — no internal monologue.
```

```
This dialogue sounds like one person talking to themselves. Rewrite so each character has a distinct voice: [paste text]
```

```
Write a scene set in a confined space — an elevator stuck between floors. Two strangers. One has a secret. Build tension using the 8-phase compression model.
```

```
Analyze the cadence of this writing. Does it fall into AI-typical rhythm patterns? Identify and break them: [paste text]
```

```
Rewrite this in 3 voices: sovereign commander, casual sharp, founder manifesto. Score all three. [paste text]
```

---

## 5. Advanced Guide

### Rewrite Operators

| Operator | What It Does |
|---|---|
| `compress(N%)` | Reduce word count by N% without losing meaning |
| `raise_intelligence` | Sharper ideas, not bigger words |
| `add_specificity` | Replace abstractions with names, numbers, examples |
| `abstract_to_scene` | Convert concepts into grounded narrative |
| `sharpen_thesis` | Make the core claim more precise |
| `strip_corporate` | Remove institutional voice |
| `make_colder` | Reduce warmth, increase analytical distance |
| `make_warmer` | Increase empathy without sentimentality |
| `make_executable` | Convert insight into action steps |
| `genre_transfer(from, to)` | Rewrite in target genre conventions |
| `audience_shift(from, to)` | Adjust register for different reader |
| `inject_variance` | Add sentence-length and vocabulary unpredictability |
| `kill_padding` | Remove every sentence that doesn't earn its place |
| `strengthen_closing` | Rewrite final paragraph for maximum impact |
| `scene_audit` | Run chapter construction checklist *(v2.0)* |
| `role_audit` | Map every character to structural archetype *(v2.0)* |
| `dialogue_stress_test` | Score against 9 tension elements + 22 techniques *(v2.0)* |
| `power_map` | Track power object migration and control shifts *(v2.0)* |
| `plant_audit` | Verify foreshadowing plants have payoffs *(v2.0)* |

```
Apply the scene_audit operator to this chapter. Show me every checklist item: [paste chapter]
```

```
Apply the role_audit operator. Map every character to one of the 12 archetypes. Flag any that serve no structural function: [paste scene]
```

```
Apply the dialogue_stress_test. Can I tell who's speaking with names removed? Is subtext active in 50%+ of exchanges? [paste dialogue]
```

```
Apply the power_map operator. Track the power object through the scene. Where does it start, when does it move, where does it end? [paste scene]
```

```
Apply the plant_audit operator. List every detail that pays off later. List every payoff that wasn't planted. [paste chapter]
```

### Chaining Operators

```
Apply these in order:
1. kill_padding
2. raise_intelligence
3. inject_variance
4. scene_audit
5. strengthen_closing

Show the result after each step: [paste text]
```

### Custom Voiceprint Builder

```
I'm giving you 3 samples of my writing. Build a custom voiceprint — extract sentence-length patterns, vocabulary tier, metaphor density, emotional temperature, cadence profile, formality band, distinctive habits. Use it for everything you write for me.

Sample 1: [paste 500+ words]
Sample 2: [paste 500+ words]
Sample 3: [paste 500+ words]
```

### 10 Advanced Prompts

```
Write 1,000 words arguing standardized testing destroys creative thinking. Academic rigorous voice. Academic genre. Full 7-pass pipeline. Scorecard with rationale for each category.
```

```
Run the adversarial stress test on this. Check sentence-length std dev, cadence signatures, vocabulary predictability, transition homogeneity. Flag and fix everything: [paste text]
```

```
Audit the section architecture. For each section: what job does it declare? Does it perform it? Is it in the right position? [paste document]
```

```
Transfer this academic essay into a sermon. Same argument, different delivery. Sermon black church voiceprint: [paste text]
```

```
This was written for experts. Rewrite for a general audience without dumbing it down: [paste text]
```

```
Audit the argument topology: claim sequence, premise strength, hidden assumptions, evidence-to-assertion ratio, escalation logic: [paste text]
```

```
Run paragraph physics on every paragraph: entry force, variety, midpoint turn, exit type, purpose, overlap, compression opportunity: [paste text]
```

```
Write a 2,000-word thriller chapter using the full v2.0 pipeline. Confined space. 4+ character roles. 8-phase compression. Foreshadowing integrity. Score on all 5 systems when done.
```

```
Cross-document voice check: compare these two documents for sentence stats, vocabulary tier, formality, emotional register. Flag inconsistencies: [paste doc 1] [paste doc 2]
```

```
Diagnose every failure mode in this piece. Use the full 25-mode taxonomy. Total penalty and final score: [paste text]
```

---

## 6. Expert Guide

### Running the Pipeline Manually

For maximum control, run each pass step-by-step:

```
Run only Pass 1 (Diagnostic Scan). Don't rewrite. Just show me everything wrong: [paste text]
```

```
Now Pass 2 (Structural Rewrite). Show me the restructured outline before writing prose.
```

```
Now Pass 3 (Sentence Surgery). Show what you changed and why for each fix.
```

```
Now Pass 4 (Voice Restoration) using the [voice] voiceprint. Reinject personality.
```

```
Now Pass 5 (Scene & Chapter Audit). Check setting, props, roles, power dynamics, pacing, foreshadowing.
```

```
Now Pass 6 (Stress Test). For every paragraph: what would a skeptic attack? What feels generic? What could be cut?
```

```
Now all Pass 7 outputs: clean draft, annotated draft, scorecard, violations, scene audit, next-pass recommendations.
```

### Expert Fiction Pipeline

```
I'm writing a masterpiece chapter. Walk me through the full chapter construction doctrine:

1. What's the catalytic positioning? (Where does this chapter sit in the arc?)
2. What's the deceptively simple mission? (What seems easy but will go wrong?)
3. Is the setting an active antagonist? (Does the space compress, threaten, trap?)
4. Are props dual-purpose? (What objects serve narrative + character + thematic functions?)
5. Who are the characters by role? (Map each to one of the 12 archetypes)
6. Where's the power object? (Track its migration)
7. What's the fatal detail? (Small trigger, enormous consequence, ironic)
8. Does the pacing follow the 8-phase compression model?
9. Where are the silence beats?
10. What's the button? (Final line/image — the scar the chapter leaves)

Here's my chapter: [paste chapter]
```

---

## 7. Prompt Library — By Task

### Rewriting

```
Rewrite this to sound human: [paste text]
```
```
Rewrite in half the words: [paste text]
```
```
Rewrite for a [specific audience]: [paste text]
```
```
Rewrite just the opening — hook the reader in one sentence: [paste text]
```
```
Rewrite just the closing — make it unforgettable: [paste text]
```

### Scoring & Diagnosis

```
Score on the 100-point system: [paste text]
```
```
Run full diagnostic — violations, AI risk, statistical profile: [paste text]
```
```
3 biggest problems with this piece: [paste text]
```
```
Which paragraphs are weakest? Why? [paste text]
```
```
Is this detectable as AI? What specifically would trigger a detector? [paste text]
```

### Writing From Scratch

```
Write a [length] [type] about [topic]. Voice: [voice]. Genre: [genre].
```
```
Write a [type] that scores 90+ about [topic].
```
```
Give me 3 versions: cold, warm, conversational. Score all three.
```
```
Write the strongest argument for [position]. Then against it. Score both.
```

### Fiction *(v2.0)*

```
Write a scene where [event]. Show everything through action and dialogue. No emotion words.
```
```
Write a chapter opening that drops the reader into the middle of tension. No setup. No preamble.
```
```
Write dialogue between [characters] about [topic]. They disagree. Each has a distinct voice and a hidden agenda.
```
```
Write a scene where power shifts between two people. Track it through objects and space, not words.
```
```
Write the final 500 words of a chapter. Make the button (last line) the strongest line in the piece.
```

---

## 8. Prompt Library — By Genre

### Fiction *(v2.0)*

```
Write a scene where [character] discovers [revelation] through action and dialogue only. No internal monologue.
```
```
Write a 1,000-word chapter using the 8-phase compression model. Start with normalcy, end with aftermath.
```
```
Write a conversation where one character is hiding something. The reader knows. The other character suspects. Use subtext throughout.
```
```
Write a cold open — drop the reader into a scene already in crisis. Orient them through immersion, not exposition.
```

### Thriller *(v2.0)*

```
Write a thriller scene in a confined space. Establish exits early. Use the space against the characters. Follow the 5 structural beats: setup, complication, escalation, break, aftermath.
```
```
Write an interrogation scene. The questioner is charming. Every question is a trap. The protagonist cannot answer safely.
```
```
Write a scene where the fatal detail is a hand gesture. Build 1,000 words of tension leading up to a 3-second mistake that changes everything.
```

### Dialogue *(v2.0)*

```
Write a conversation between [3 characters]. Each has a different vocabulary tier, sentence length, and verbal habit. I should know who's speaking with the names removed.
```
```
Write a scene where two characters argue without raising their voices. The tension comes from subtext, not volume.
```
```
Write dialogue where one character uses the Rule of Twelve (under 12 words between punctuation) and the other speaks in long, circling sentences. The difference in rhythm IS the characterization.
```

### Transmedia *(v2.0)*

```
Write a character diary entry from [character]'s perspective. Include sensory detail, emotional depth, and at least one "unseen moment" not in the primary text. 800 words.
```
```
Design a 10-clue digital scavenger hunt based on [story world]. Each clue should require knowledge of the lore to solve. Include the narrative wrapper that justifies the hunt.
```
```
Write the script for a 15-minute audio drama episode set during [event from the story]. Dialogue-driven. Sound cues in brackets. Each character's voice must be immediately distinguishable.
```

### Academic

```
Write a thesis paragraph arguing [position]. Include claim, scope, stakes, roadmap.
```
```
Write a counterargument that steelmans the opposition, concedes what's true, then pivots.
```
```
Convert rough notes into an evidence paragraph with claim-evidence-interpretation structure: [paste notes]
```

### Strategy

```
Write a strategy memo in SCIR format about [topic]. Include owners, timelines, risk analysis.
```

### Sales

```
Write a sales page using Hook → Story → Offer → Proof → Close for [product]. Specific guarantee. Clear CTA.
```

### Sermon

```
Write a 12-minute sermon on [scripture]. Build from observation to conviction. Include one testimony and one silence.
```

### Email

```
Write an email to [recipient] about [topic]. Purpose in the first sentence. One ask. One deadline. Under 100 words.
```

---

## 9. Prompt Library — By Voice

### Sovereign Commander
```
Write this like a general briefing a war room. Cold. Precise. Every sentence is a fact, conclusion, or command: [topic]
```

### Academic Rigorous
```
Write as a scholar — evidence-first, qualified, named sources. Confident on data, hedged on projections: [topic]
```

### Casual Sharp
```
Write like a smart friend over coffee. Conversational, witty, no hand-holding: [topic]
```

### Literary Recursive
```
Write layered prose — image-driven, subtext-heavy, dramatic rhythm. The important things are said obliquely: [topic]
```

### Sermon Black Church
```
Write for a congregation. Build from observation to conviction. Cadence matters — rhythm IS meaning: [topic]
```

### Investor Precision
```
Write for investors. Data-first. No adjectives — only numbers. State assumptions. Quantify risk: [topic]
```

### Founder Manifesto
```
Write as a founder addressing the world. Hot conviction, cold execution. Name the broken system. Declare what you're building: [topic]
```

---

## 10. Scoring & Diagnostics

### 7 Scoring Systems *(v2.0)*

| System | Points | When to Use |
|---|---|---|
| **Prose Quality** | 100 | Any writing |
| **Chapter Construction** | 100 | Fiction chapters, narrative scenes |
| **Dialogue** | 100 | Any scene with character speech |
| **Power Dynamics** | 100 | Scenes with competing characters |
| **Tension Mechanics** | 100 | Suspense, thriller, high-stakes scenes |
| **Thriller Scene** | 100 | Thriller/suspense genre specifically |
| **Transmedia** | 100 | Cross-format character content |

### Quick Score

```
Score this on the 100-point scale. Total and breakdown: [paste text]
```

### Full Multi-System Score *(v2.0)*

```
Score this chapter on ALL applicable systems: prose quality, chapter construction, dialogue, power dynamics, tension mechanics. Give me 5 separate scores with breakdowns: [paste chapter]
```

### Full Diagnostic

```
Run the full auto-diagnostic:
1. Prose score (100-point, all 10 categories)
2. Auto-fail check
3. Violation heatmap by paragraph
4. AI detection risk by paragraph
5. Top 3 violations with fixes
6. Top 3 strengths
7. Recommended next actions ranked by impact

[paste text]
```

### Grade Thresholds

- **95–100**: Signature-grade — could only come from this author
- **90–94**: Elite — distinctive, defensible, memorable
- **80–89**: Strong — publishable with minor polish
- **70–79**: Usable but soft — needs tightening
- **Below 70**: Significant revision required

---

## 11. Academic Mode

### Before Writing: Rubric Analysis

```
Here's my assignment prompt. Extract what verbs it uses, what the rubric rewards, expected evidence type, what's prohibited, citation style, target depth. Build me a rubric-mapped outline: [paste prompt]
```

### Writing the Paper

```
Write a [word count] paper on [topic] for [course]. The professor values [what]. Academic genre pack. Include: thesis as position not topic, claim-evidence-interpretation paragraphs, one counterargument at its strongest, conclusion that extends not summarizes.
```

### Anti-Hallucination Check

```
Flag: any potentially fabricated quotes, statistics without named sources, study references not specific enough to verify, wrong page numbers, "many scholars" without names. Replace each with [VERIFY: description]: [paste paper]
```

### Authorship Defense

```
Generate 10 questions a professor would ask about this paper if they suspected AI. Write my answers grounded in the specific sources and reasoning: [paste paper]
```

---

## 12. Style Transfer

```
Transfer from [source genre] to [target genre]. Preserve content. Rebuild structure, voice, conventions: [paste text]
```

```
Transfer this academic essay into a blog post. Keep the argument. Change the voice.
```

```
Transfer this strategy memo into a pitch deck narrative. Same data. Different delivery.
```

```
Transfer this sales page into an academic paper. Same claims. Add evidence standards.
```

```
Transfer this email into a speech. Expand compressed points. Add breathing room and landing lines.
```

---

## 13. Longform & Multi-Session

### Starting a Book Project

```
I'm starting a book. Details:
- Title: [title]
- Genre: [genre]
- Central thesis/premise: [one sentence]
- Target reader: [who]
- Voice: [voiceprint]
- Planned chapters: [list]

Create a Project Memory File. Track voice, terminology, metaphors, thesis, character roles, power objects, and foreshadowing ledger across sessions. Session 1.
```

### Continuing

```
Session [N] of [project]. Last session I wrote [chapter/section]. Here's where we stopped: [paste last paragraph]. Continue. Check continuity first.
```

### End-of-Session

```
End session for [project]. Update the Project Memory File. Note new terms, metaphors, character developments. Flag unresolved threads. Tell me what the next session should accomplish.
```

---

## 14. Fiction & Chapter Construction *(v2.0)*

This is the crown jewel of v2.0. A complete structural engineering system for fiction.

### The Chapter Construction Checklist

Use this prompt to audit any chapter you've written or are planning:

```
Run the full chapter construction checklist on this chapter:

- [ ] Does the setting function as an active force, not a backdrop?
- [ ] Can the reader map the space from character movement alone?
- [ ] Does every prop serve at least two narrative functions?
- [ ] Is there a power object whose position tracks the shifting dynamics?
- [ ] Does dialogue operate on 2+ layers (surface + subtext)?
- [ ] Is there at least one strategic interruption serving 3+ functions?
- [ ] Does pacing follow the compression model (normalcy → friction → pressure → false relief → fatal detail → silence → explosion → aftermath)?
- [ ] Is there a silence beat carrying more weight than the dialogue around it?
- [ ] Does every planted detail pay off? Does every payoff have a plant?
- [ ] Does each character's first action foreshadow their arc?
- [ ] Are 4+ character roles deployed?
- [ ] Is there a power reversal that feels surprising but inevitable?
- [ ] Does the chapter begin simple and end irreversibly complex?
- [ ] Is the final image/line the strongest in the chapter?

[paste chapter]
```

### Build a Chapter From Scratch

```
I want to build a masterpiece chapter. Walk me through it:

1. PLACEMENT: Where does this chapter sit in the arc? What irreversible change does it trigger?
2. MISSION: What's the deceptively simple objective that spirals into disaster?
3. SETTING: Design the space as an active antagonist. What are the constraints? Where are the exits?
4. PROPS: What objects will serve dual purposes? What's the power object?
5. CHARACTERS: Who's in the room? Map each to one of the 12 archetypes.
6. PACING: Walk me through all 8 phases of the compression model with specific beats.
7. FATAL DETAIL: What's the small mistake with enormous consequences?
8. FORESHADOWING: What needs to be planted in the first 60% that pays off at the climax?
9. BUTTON: What's the final image that burns into the reader's memory?

My chapter is about: [describe the scenario]
```

### Setting as Active Force

```
This scene is set in [location]. Right now it's just a backdrop. Redesign the setting to function as an active antagonist. Show me how the space compresses, threatens, or traps the characters. Establish exits. Make the environment act on the characters, not just contain them.
```

### Props as Narrative Weapons

```
List every named object in this scene. For each, tell me: what narrative function does it serve beyond its literal one? Does it reveal character? Foreshadow? Track power? Argue theme? If it only serves one function, tell me how to deepen it or cut it: [paste scene]
```

### The 8-Phase Compression Model

```
Analyze this chapter against the 8-phase compression model:

1. Ambient normalcy (2-5%)
2. First friction (5-15%)
3. Sustained pressure (15-60%)
4. False relief (60-70%)
5. Fatal detail (70-80%)
6. Silence before storm (80-85%)
7. Explosive release (85-95%)
8. Aftermath resonance (95-100%)

Mark where each phase starts and ends. Flag any missing phases. Flag any phase that overstays its welcome: [paste chapter]
```

### Foreshadowing Audit

```
Run the plant_audit operator on this chapter:
- List every detail that's planted early and pays off later
- List every payoff that arrives without a plant (deus ex machina)
- List every plant that never pays off (orphaned Chekhov's gun)
- Rate each plant: invisible on first read? Visible on second read?

[paste chapter]
```

---

## 15. Character Roles & Dialogue Mastery *(v2.0)*

### The 12 Character Role Archetypes

| Role | Function | Tension Contribution |
|---|---|---|
| **Covert Operative** | Facade linchpin | Sustained dread — when will the mask slip? |
| **Double Agent** | Dual-loyalty conduit | Trust uncertainty — whose side are they on? |
| **Interrogator** | Psychological pressure engine | Every question is a trap |
| **Enforcer** | Physical threat counterweight | Ticking bomb — restraint eroding |
| **Celebrant** | Unwitting chaos agent | Unpredictable innocence disrupts control |
| **Observer** | Paranoia amplifier | Being watched by unknown allegiance |
| **Overlooked Ally** | Hidden resource | The furniture that suddenly matters |
| **Innocent** | Consequence generator | Ordinary actions with extraordinary fallout |
| **Ghost** | Emotional depth charge | Past forces present to confront history |
| **Shadow** | Invisible architect | Events shaped by someone outside the frame |
| **Fall Guy** | Sacrificial pawn | Reader sees the trap before the character does |
| **Decoy** | Misdirection engine | Forces the wrong conclusion |

### Deploy Character Roles

```
I have a scene with these characters: [list characters and brief descriptions]. Map each to one of the 12 archetypes. Tell me which roles are missing that would increase tension. Suggest which characters could stack two roles.
```

```
Write a scene with exactly 5 characters, each serving a distinct role from the 12 archetypes. At least one role should be concealed and revealed during the scene.
```

### Dialogue Voice Distinction

```
Write a conversation between 3 characters. Rules:
- Each has a different vocabulary tier, sentence length pattern, and verbal habit
- One speaks in fragments. One speaks in qualifications. One speaks in questions.
- Remove the names. I should still know who's speaking.
- At least one character lies. The lie should be detectable through behavior, not narrator comment.
```

### The 9 Dialogue Tension Elements

Use these to inject tension into any conversation:

```
Write a dialogue scene and deploy at least 3 of these tension elements:
1. Personality clash (incompatible communication styles)
2. Opposing conversational goals (each trying to steer toward what they want)
3. Pre-loaded emotions (one character enters already upset about something else)
4. Bias (one expects the conversation to go badly)
5. Insecurities (one reads insults into harmless comments)
6. Incorrect assumptions (one assumes the other knows something they don't)
7. Small annoyances (accumulated friction)
8. Cultural differences (gestures, norms, expectations mismatched)
9. Active subtext (what's said ≠ what's meant)

Scenario: [describe the conversation]
```

### Dialogue Stress Test

```
Run the full dialogue stress test on this scene:
- Voice distinction: can I tell who's speaking with names removed?
- Subtext depth: what percentage of exchanges have a gap between said and meant?
- Tension elements: which of the 9 elements are active?
- Rule of Twelve: are most phrases under 12 words between punctuation?
- Attribution technique: tags invisible? Action beats instead of adverbs?
- Exposition handling: is information delivered through conflict, not recitation?
- Silence: does wordlessness carry weight at any point?
Score on the dialogue v2.0 rubric (100 points).

[paste dialogue]
```

---

## 16. Thriller & Suspense Craft *(v2.0)*

### Confined-Space Scene

```
Write a thriller scene set in [confined space: basement, elevator, restaurant, interrogation room]. Requirements:
- Map the space through character experience in the first 10%
- Establish exits and who's between the characters and the exit
- Use the space to compress tension — it should feel smaller as the scene progresses
- When violence erupts, the space becomes a kill box
- The very features that made the space atmospheric now make it lethal
```

### The Fatal Detail

```
Write a 1,000-word scene that builds to a fatal detail — a single small mistake (a gesture, an accent, a cultural error) that collapses everything. Requirements:
- The detail must be planted earlier (invisible at planting, devastating at payoff)
- The most prepared character makes the mistake (ironic)
- The mistake is irreversible
- The scene's tension doubles in the 50 words after the detail lands
```

### Power Dynamics Through Staging

```
Write a scene where the power balance shifts. Rules:
- No internal monologue
- No narrator explanation of who's winning
- The shift must be visible purely through: object positions, body language, spatial arrangement, who asks questions vs. who answers, gesture patterns
- Include at least one power object whose position changes with the shift

[describe the scenario]
```

### The WWGW Diagnostic

```
Run the WWGW (What Was Going Wrong) diagnostic on this thriller chapter. At every 15% interval, tell me what's going wrong. If the same thing is going wrong at two consecutive checkpoints, the scene has stalled: [paste chapter]
```

### Psychological Warfare Scene

```
Write an interrogation scene where the antagonist never raises their voice, never threatens directly, and is genuinely charming. The menace comes entirely from:
- Questions that are impossible to answer safely
- Knowledge they shouldn't possess (delivered casually)
- Physical comfort that contrasts with lethal stakes
- Silence held longer than socially comfortable

The protagonist must navigate without breaking cover.
```

---

## 17. Transmedia & Storyworld Deepening *(v2.0)*

### Character Diary

```
Write a character diary entry for [character]. Requirements:
- Voice must match the character's speech patterns, education, emotional range
- Include sensory detail and emotional response, not plot summary
- Explore an "unseen moment" not covered in the primary narrative
- Include at least one insight that recontextualizes a scene from the main story
- 800-1200 words. Date-stamped.
```

### Lore Bible Construction

```
I'm building the lore bible for [story world]. Help me construct:
- Complete timeline (historical + character-personal)
- Cultural norms and taboos
- Mythological system (creation myth, prophecies, supernatural rules)
- 5 artifacts with provenance (who made them, what they do, where they are)
- Naming conventions and etymologies

Start with the timeline and cultural norms. We'll build the rest in subsequent sessions.
```

### Audio Drama Script

```
Write a 15-minute audio drama episode. Rules:
- Set during [event from the story]
- Dialogue-driven — all information through speech and sound
- Sound cues in brackets: [Door slams. Footsteps on wet stone. Silence.]
- Each character's voice immediately distinguishable (age, accent, rhythm, vocabulary)
- Complete arc: setup, complication, turn, resolution
```

### Interactive Web Serial Design

```
Design a 10-episode interactive web serial based on [story]. For each episode:
- Summary of events
- The decision point (what the reader votes on)
- 2-3 options with emotionally different consequences
- What fixed events happen regardless of the vote
- How each option affects the next episode
```

### Transmedia Launch Sequence

```
I have [story/book/series]. Design a transmedia launch sequence using the effort-impact matrix:
- Phase 1 (Foundation): What low-cost content establishes the transmedia presence?
- Phase 2 (Expansion): What medium-cost content builds community?
- Phase 3 (Immersion): What high-cost content deepens engagement?
- Phase 4 (Event): What event-driven content ties to major releases?

Match each format to my resources: [describe budget/team/timeline]
```

---

## 18. Worldbuilding Prompts *(v2.0)*

```
Design a setting that functions as an active antagonist. It should compress tension, limit options, and force characters into proximity they'd avoid. Give me: physical description, exit locations, atmospheric details, and 3 ways the space gets "smaller" as the scene progresses.
```

```
Create 5 objects for this scene. Each must serve its literal function PLUS at least one of: character revelation, foreshadowing, power signaling, or thematic argument. Show me the dual-purpose mapping.
```

```
Design the drink/food culture for [fictional setting]. What people consume should reveal their class, allegiance, and psychological state. Create a consumption guide with at least 5 items and what ordering each one signals.
```

```
Build the gesture language for [character culture]. What are the dominance gestures? Submission gestures? What gesture mistakes would betray an outsider pretending to belong?
```

```
Design 3 confined spaces for my story world: one for interrogation, one for celebration that turns dangerous, one for transit. For each: physical layout, exit positions, acoustic properties, what makes it feel smaller over time.
```

```
Create the foreshadowing architecture for my chapter. I need: 4 details to plant in the first 60%, each serving a surface purpose at planting. Show me the plant and the payoff for each. None should be obvious on first read.
```

---

## 19. Troubleshooting

**"The skill doesn't seem to be doing anything different."**
Start a new conversation after installing. Skills activate on new conversations. Try one of the prompts from Section 2.

**"The output still sounds like AI."**
Be more specific. Instead of "write about X," try: "Write 400 words about X. Casual sharp voice. No AI clichés. Vary sentence lengths. One sentence under 6 words."

**"The scoring seems harsh."**
It's calibrated against published, edited prose — not AI output. 75 is usable professional writing. 85 is strong. 95+ is rare.

**"The fiction tools feel overwhelming."**
Start with one system at a time. First use the dialogue stress test on existing work. Then try the scene_audit operator. Build up to the full chapter construction checklist.

**"I want to use this with ChatGPT / Gemini."**
Copy `SKILL.md` into your system prompt. For deeper features, also paste specific reference files. Designed for Claude, but the principles work with any LLM.

**"How do I pass Turnitin?"**
Adversarial stress test (Section 5). Key factors: sentence-length variation (std dev ≥8), vocabulary unpredictability, no transition repetition, no cadence signatures. Academic mode + inject_variance + custom voiceprint is the strongest combination.

---

## 20. FAQ

**Q: Is this just "anti-slop" with more files?**
No. Anti-slop removes AI patterns (subtractive). Writing Intelligence removes patterns AND constructs quality — voice, argument, evidence, structure, scene architecture, character deployment, power dynamics, tension mechanics (compiler). v2.0 adds a complete fiction engineering system that no other writing tool has.

**Q: What's actually new in v2.0?**
A fiction intelligence engine. Chapter construction doctrine. 12 character role archetypes. Dialogue system with 22 techniques and 9 tension elements. Power dynamics through objects, space, and gesture. Tension mechanics with 8-phase compression. Thriller scene architecture. Transmedia character deepening. 7 independent scoring systems instead of 1. 5 new rewrite operators. 6 new adversarial tests.

**Q: Can I use this to write a novel?**
Yes. Use the longform multi-session system (Section 13) for continuity tracking. Use the fiction tools (Section 14) for chapter construction. Use the character roles (Section 15) for ensemble management. Use the dialogue system for every conversation scene. Use the foreshadowing ledger to track plants and payoffs across the entire manuscript.

**Q: Will this work for screenplays?**
The dialogue system, character roles, scene architecture, and pacing mechanics all apply directly to screenwriting. The cinematic narration genre pack was built for shot-based prose that translates to screen.

**Q: Can I use this commercially?**
Yes. MIT license. Use it in your products, courses, agency, workflow. Credit appreciated.

**Q: Who built this?**
Antonio T. Smith Jr., Founder & CEO of Density6 LLC. Inventor of OMC and ERI. Built because the world needed a writing system that compiles quality, not just cleans surfaces — and a fiction system that treats stories as engineering, not decoration.

**Q: Why is it free?**
Because language is how the poor build power and the middle class keep it. The student at 2 AM and the executive before the board meeting deserve the same tool. So does the novelist at 3 AM and the screenwriter before the pitch.

---

## 21. Quick Reference Card

| I Want To... | Prompt Starts With... |
|---|---|
| Clean up AI text | "Rewrite this to sound human..." |
| Score my writing | "Score on the 100-point scale..." |
| Write from scratch | "Write [length] [type] about [topic]. Voice: [voice]. Genre: [genre]." |
| Fix weak opening | "Rewrite just the first paragraph..." |
| Fix weak closing | "Rewrite the final paragraph..." |
| Make it shorter | "Compress by [N]%..." |
| Make it smarter | "Apply raise_intelligence..." |
| Change the voice | "Rewrite in [voice] voice..." |
| Transfer genres | "Transfer from [A] to [B]..." |
| Check AI risk | "Run adversarial stress test..." |
| Full diagnostic | "Run full auto-diagnostic..." |
| Build my voice | "Build voiceprint from these 3 samples..." |
| **Write a scene** | **"Write a scene where [event]. Show everything. No emotion words."** |
| **Build a chapter** | **"Walk me through chapter construction doctrine for [scenario]."** |
| **Audit a chapter** | **"Run scene_audit on this chapter. Full checklist."** |
| **Map character roles** | **"Run role_audit. Map each character to the 12 archetypes."** |
| **Test dialogue** | **"Run dialogue_stress_test. Names removed — can I tell who's speaking?"** |
| **Track power dynamics** | **"Run power_map. Where's the power object? When does it shift?"** |
| **Audit foreshadowing** | **"Run plant_audit. Every plant. Every payoff. Every orphan."** |
| **Write thriller scene** | **"Write in confined space. 8-phase compression. Fatal detail."** |
| **Design transmedia** | **"Design transmedia launch sequence for [story]."** |
| **Build storyworld** | **"Design setting as active antagonist. Exits. Atmosphere. Compression."** |
| **Write character diary** | **"Write diary entry for [character]. Unseen moment. 800 words."** |

---

*Built by Antonio T. Smith Jr. / [Density6 LLC](https://densitysix.com)*

*Writing should sound like a person wrote it. Fiction should feel like a person lived it. This makes sure both happen.*

*[github.com/antonio0720/writing-intelligence](https://github.com/antonio0720/writing-intelligence)*
