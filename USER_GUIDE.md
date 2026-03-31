# Writing Intelligence — User Guide

**From first install to signature-grade prose.**

A complete guide to using Writing Intelligence, the 6-pass writing compiler created by **Antonio T. Smith Jr. / Density6 LLC**.

52 files. 42,264 words. 14 genres. 8 voices. 100-point scoring. Free forever.

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
11. [Academic Mode — Complete Guide](#11-academic-mode--complete-guide)
12. [Style Transfer](#12-style-transfer)
13. [Longform & Multi-Session](#13-longform--multi-session)
14. [Troubleshooting](#14-troubleshooting)
15. [FAQ](#15-faq)

---

## 1. Installation

### Claude.ai (Easiest)
1. Download `writing-intelligence-v1.0.skill` from [Releases](https://github.com/antonio0720/writing-intelligence/releases)
2. Open Claude.ai → Settings → Skills
3. Click "Install from file"
4. Select the `.skill` file
5. Start a new conversation. The skill is now active.

### Claude Code
```bash
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
3. For deeper functionality, also paste the relevant reference files (anti-patterns, voiceprints, genre packs) as needed

---

## 2. Your First 5 Minutes

Once installed, try these three prompts to see the skill in action immediately:

### Prompt 1 — Clean Up AI-Sounding Text
```
Rewrite this paragraph to sound like a real person wrote it:

"In today's rapidly evolving digital landscape, artificial intelligence has emerged as a transformative force that is reshaping industries across the globe. It's worth noting that the impact extends far beyond mere automation, fundamentally altering how we approach problem-solving."
```

### Prompt 2 — Score a Piece of Writing
```
Score this passage on the 100-point Writing Intelligence scale and tell me what's wrong:

"The company experienced significant growth in recent years. Our team is aligned on the importance of expanding our market presence. By leveraging our core competencies, we can drive stakeholder value. Moving forward, it will be critical to ensure our strategic priorities are communicated across the organization."
```

### Prompt 3 — Write Something From Scratch
```
Write a 300-word opening for a strategy memo about why our company should stop using contractors and hire full-time engineers. Use the sovereign commander voice. Score it when done.
```

If the output is specific, varied in sentence length, free of buzzwords, and scores 80+, the skill is working.

---

## 3. Beginner Guide

### What the Skill Does Automatically

Once installed, Writing Intelligence activates whenever you ask Claude to write, edit, rewrite, or score text. You don't need to invoke it by name. Just write naturally and the 6-pass pipeline runs in the background.

These trigger it automatically:
- "Write me a..."
- "Rewrite this..."
- "Edit this for..."
- "Make this sound more..."
- "Clean this up..."
- "Score this..."
- "Grade my writing..."

### The 6 Passes (Simple Version)

Think of it as an assembly line for your writing:

1. **Mission Lock** — The skill figures out what you're trying to do, who you're writing for, and what voice to use
2. **Diagnostic Scan** — It identifies everything wrong: AI phrases, weak arguments, repetitive rhythm, vague claims
3. **Structural Rewrite** — It fixes the order: are your paragraphs in the right sequence? Is your thesis in the right place?
4. **Sentence Surgery** — It cleans each sentence: removes filler, varies length, adds specificity
5. **Voice Restoration** — It makes sure the cleanup didn't flatten your personality
6. **Stress Test** — It asks: would a smart reader buy this? What feels generic? What could be cut?

### 10 Beginner Prompts (Copy-Paste Ready)

**1. Basic Cleanup**
```
Rewrite this to remove AI patterns and make it sound human:

[paste your text here]
```

**2. Email Writing**
```
Write a professional email to my manager requesting a meeting to discuss my promotion timeline. Keep it under 100 words. Direct, no filler.
```

**3. Blog Post Opening**
```
Write a compelling opening paragraph for a blog post about why most small businesses fail at social media marketing. Don't start with "In today's..." or any AI cliché.
```

**4. Simple Scoring**
```
Score this writing on the 100-point scale:

[paste your text here]
```

**5. Make It Shorter**
```
Compress this by 40% without losing any meaning:

[paste your text here]
```

**6. Make It Smarter**
```
Raise the intelligence of this passage without adding jargon. Make the ideas sharper, not the words bigger:

[paste your text here]
```

**7. Fix a Weak Opening**
```
The opening of this piece is weak. Rewrite just the first paragraph to hook the reader immediately:

[paste your text here]
```

**8. Fix a Weak Closing**
```
This ending just summarizes what was already said. Rewrite the final paragraph to leave the reader with something they'll remember:

[paste your text here]
```

**9. Add Specificity**
```
This is too vague. Rewrite it with specific names, numbers, dates, and examples:

[paste your text here]
```

**10. Quick Grammar and Polish**
```
Edit this for clarity and polish. Don't change the structure or voice, just clean the sentences:

[paste your text here]
```

---

## 4. Intermediate Guide

### Choosing a Voice

The skill has 7 built-in voiceprints. Specifying one changes how the output sounds:

| Voice | When to Use It | What It Sounds Like |
|---|---|---|
| `sovereign commander` | Strategy docs, executive comms, authority pieces | Cold, precise, declarative. Zero filler. |
| `academic rigorous` | Papers, research, scholarly writing | Evidence-first, qualified, citation-dense |
| `casual sharp` | Blog posts, newsletters, friendly-but-smart content | Conversational, witty, respects the reader |
| `literary recursive` | Fiction, creative nonfiction, layered narratives | Image-driven, varied rhythm, subtext-heavy |
| `sermon black church` | Sermons, inspirational speeches, pastoral content | Cadence-built, dignified, builds to declaration |
| `investor precision` | Pitch memos, board updates, financial communication | Data-forward, risk-aware, no adjectives |
| `founder manifesto` | Vision statements, company manifestos, rallying cries | Conviction-dense, future-claiming, morally urgent |

### How to Specify a Voice

Just name it in your prompt:

```
Write a 500-word essay on why remote work is failing mid-level managers. Use the casual sharp voice.
```

```
Rewrite this investor update in the investor precision voice. Cut all adjectives. Replace them with numbers.
```

```
Write the opening of a sermon about forgiveness after betrayal. Use the sermon black church voice.
```

### Choosing a Genre Pack

Genre packs adjust the rules for specific types of writing:

| Genre | What It Optimizes For |
|---|---|
| `academic` | Citations, rubric compliance, claim-evidence binding |
| `strategy` | Situation-complication-recommendation, owners, timelines |
| `fiction` | Scene, dialogue, show-don't-tell, sensory detail |
| `sales` | Hook-story-offer-proof-close, objection handling |
| `email` | Compression, action clarity, scannable structure |
| `speech` | Delivery rhythm, landing lines, applause architecture |
| `sermon` | Cadence arc, scriptural grounding, dignity |
| `pitch deck` | Data density, 12-slide architecture, ask clarity |
| `legal positioning` | Precision, IRAC structure, statutory citation |
| `cinematic narration` | Shot-based prose, pacing, sensory density |
| `dialogue` | Character voice distinction, subtext, attribution |
| `government brief` | BLUF, plain language, agency calibration |
| `medical writing` | IMRAD, evidence hierarchy, clinical precision |
| `patent claims` | Claim structure, antecedent basis, enablement |

### How to Specify a Genre

```
Write a 400-word pitch for our Series A deck. Use the pitch deck genre pack.
```

```
Draft a government brief recommending the approval of a $12M water infrastructure grant. Use the government brief genre pack.
```

### 15 Intermediate Prompts

**1. Voice + Genre Combo**
```
Write a 600-word analysis of why subscription fatigue is killing SaaS companies. Use the sovereign commander voice and the strategy genre pack. Score it when done.
```

**2. Rewrite with Voice Change**
```
This was written in a corporate voice. Rewrite it in the casual sharp voice without losing any content:

[paste your text here]
```

**3. Argument Strengthening**
```
The argument in this piece is soft. Strengthen it: add evidence, address the strongest counterargument, and make the conclusion go further than the introduction:

[paste your text here]
```

**4. Paragraph-Level Diagnosis**
```
Diagnose every paragraph in this piece. For each one, tell me: what job does it do? Does it actually do that job? What's weak?

[paste your text here]
```

**5. Opening Variations**
```
Give me 5 different openings for an essay about income inequality in American education. Each opening should use a different technique: data spike, counterintuitive claim, scene drop, authority declaration, and question that bites.
```

**6. Closing Variations**
```
Give me 4 different closings for this piece. One that extends the argument into implication, one that issues a challenge, one that returns to the opening image, and one that ends quietly:

[paste your text here]
```

**7. Evidence Integration**
```
This passage makes claims but doesn't back them up. Rewrite it with specific evidence: named sources, real data, concrete examples. If you don't have the exact data, tell me what data I should find:

[paste your text here]
```

**8. Compression Challenge**
```
Compress this 800-word piece to 400 words. Same argument, same evidence, half the words. Score both versions:

[paste your text here]
```

**9. Sentence-Length Variation**
```
This passage has flat rhythm — every sentence is roughly the same length. Rewrite it with dramatic sentence-length variation. Include at least one sentence under 6 words and one over 30 words:

[paste your text here]
```

**10. Strip Corporate Voice**
```
Remove every trace of corporate voice from this document. No "leverage," no "synergy," no "stakeholders," no passive voice hiding accountability. Make a human being sound like they wrote this:

[paste your text here]
```

**11. Epistemic Audit**
```
Go through this piece sentence by sentence. Label each one as: observed fact, sourced fact, inference, synthesis, recommendation, or rhetoric. Then flag every sentence that claims to be fact but isn't backed by a source:

[paste your text here]
```

**12. Cadence Diagnosis**
```
Analyze the cadence of this writing. Does it fall into any AI-typical rhythm patterns? LinkedIn cadence? LLM list rhythm? Startup guru cadence? Identify the pattern and show me how to break it:

[paste your text here]
```

**13. Fiction Scene Rewrite**
```
This fiction passage tells instead of shows. Rewrite it so the emotion comes through action, dialogue, and sensory detail — never named directly:

[paste your text here]
```

**14. Dialogue Polish**
```
This dialogue sounds like the same person is speaking every line. Rewrite it so each character has a distinct voice — different vocabulary, different sentence length, different verbal habits:

[paste your text here]
```

**15. Multi-Output Request**
```
Rewrite this passage three ways:
1. Sovereign commander voice (cold, strategic)
2. Casual sharp voice (conversational, smart)
3. Founder manifesto voice (conviction-dense, future-claiming)

Score all three.

[paste your text here]
```

---

## 5. Advanced Guide

### Using Rewrite Operators

Rewrite operators are specific transformation commands. Use them by name:

```
Apply the compress(40%) operator to this piece:

[paste your text here]
```

```
Apply the raise_intelligence operator. Make the ideas sharper without making the words bigger:

[paste your text here]
```

```
Apply the abstract_to_scene operator. Convert this conceptual paragraph into a grounded narrative moment:

[paste your text here]
```

#### Full Operator List

| Operator | What It Does |
|---|---|
| `compress(N%)` | Reduce word count by N% without losing meaning |
| `raise_intelligence` | Sharper ideas, not bigger words |
| `add_specificity` | Replace abstractions with names, numbers, examples |
| `abstract_to_scene` | Convert concepts into grounded narrative |
| `sharpen_thesis` | Make the core claim more precise and defensible |
| `strip_corporate` | Remove institutional voice patterns |
| `make_colder` | Reduce warmth, increase analytical distance |
| `make_warmer` | Increase empathy without sentimentality |
| `make_executable` | Convert insight into action steps |
| `genre_transfer(from, to)` | Rewrite in target genre conventions |
| `audience_shift(from, to)` | Adjust register for different reader |
| `inject_variance` | Add sentence-length and vocabulary unpredictability |
| `kill_padding` | Remove every sentence that doesn't advance the argument |
| `strengthen_closing` | Rewrite final paragraph for maximum impact |

### Chaining Operators

You can apply multiple operators in sequence:

```
Apply these operators in order to this piece:
1. kill_padding
2. raise_intelligence
3. inject_variance
4. strengthen_closing

Show me the result after each step so I can see the transformation:

[paste your text here]
```

### Using the Auto-Diagnostic Report

Request the full structured audit:

```
Run a full auto-diagnostic report on this piece. I want:
- Score summary (100-point)
- Auto-fail check
- Violation heatmap by paragraph
- Statistical profile (sentence lengths, vocabulary)
- AI detection risk assessment
- Critical violations with fixes
- Strength callouts
- Recommended next actions

[paste your text here]
```

### Building a Custom Voiceprint

If you want the skill to write in YOUR specific voice:

```
I'm going to give you 3 samples of my writing. Analyze them and build a custom voiceprint — extract my sentence length patterns, vocabulary tier, metaphor density, emotional temperature, cadence profile, formality band, and distinctive habits. Then use that voiceprint for everything you write for me going forward.

Sample 1:
[paste 500+ words of your writing]

Sample 2:
[paste 500+ words of your writing]

Sample 3:
[paste 500+ words of your writing]
```

### 10 Advanced Prompts

**1. Full Pipeline with Scoring**
```
Write a 1,000-word essay arguing that standardized testing destroys creative thinking in public schools. Run the full 6-pass pipeline. Use the academic rigorous voice and the academic genre pack. Output the clean draft followed by the full 100-point scorecard with rationale for each category.
```

**2. Adversarial Stress Test**
```
I need this piece to pass AI detection. Run the adversarial stress test:
- Check sentence-length standard deviation (target: ≥8)
- Check for cadence signature matches
- Check vocabulary predictability
- Check transition homogeneity
- Check opening and closing patterns
Flag everything that would trigger a detector and fix it:

[paste your text here]
```

**3. Section Architecture Audit**
```
Analyze the section architecture of this document. For each section, tell me:
1. What job does it declare (or imply)?
2. Does it perform that job?
3. If not, what's missing?
4. Is it in the right position?
5. Does it overlap with another section?

[paste your text here]
```

**4. Genre Transfer**
```
Transfer this academic essay into a sermon. Preserve the core argument and evidence but rebuild the structure, cadence, and voice for a congregation. Use the sermon black church voiceprint:

[paste your text here]
```

**5. Audience Shift**
```
This piece was written for experts. Rewrite it for a general audience with no background in the field. Don't dumb it down — make it accessible while keeping the substance:

[paste your text here]
```

**6. Argument Topology Audit**
```
Audit the argument topology of this piece:
- Are claims sequenced for cumulative force?
- Is every premise load-bearing?
- What hidden assumptions exist?
- What's the evidence-to-assertion ratio?
- Does the argument escalate or plateau?
- Is the conclusion stronger than the introduction?

[paste your text here]
```

**7. Paragraph Physics Audit**
```
Run a paragraph physics audit on every paragraph:
- Entry force (does the first sentence compel reading?)
- Sentence variety within the paragraph
- Midpoint turn (does something shift mid-paragraph?)
- Exit type (launch, land, or hang?)
- Purpose (what job does this paragraph do?)
- Overlap with the previous paragraph
- Compression opportunity

[paste your text here]
```

**8. Competitive Rewrite**
```
This is a competitor's sales page. Rewrite it using the Writing Intelligence framework: sharper hook, better story structure, stronger offer stack, more specific proof, clearer CTA. Use the sales genre pack. Score both versions:

[paste competitor text here]
```

**9. Cross-Document Voice Check**
```
I'm going to give you two documents I've written. Check whether my voice is consistent across both. Compare sentence-length stats, vocabulary tier, formality level, and emotional register. Flag any inconsistencies:

Document 1:
[paste text]

Document 2:
[paste text]
```

**10. Failure Mode Diagnosis**
```
Diagnose every failure mode in this piece. Use the full 25-mode taxonomy:
- Critical failures (auto-fail conditions)
- Severe failures (score capped at 75)
- Moderate failures (point penalties)
- Minor failures (polish issues)

Give me the total penalty and final score:

[paste your text here]
```

---

## 6. Expert Guide

### Running the Full Compilation Pipeline Manually

For maximum control, run each pass explicitly:

```
I'm going to give you a piece of writing. Do NOT rewrite it yet. Run only Pass 1 (Diagnostic Scan) and give me the complete findings:
- AI residue detected
- Contradictions
- Vagueness spots
- Cadence repetition
- Argument gaps
- Evidence gaps
- Tone drift
- Perplexity flatness
- Burstiness deficit

[paste your text here]
```

Then:
```
Now run Pass 2 (Structural Rewrite) based on the diagnostics. Fix section order, paragraph sequence, and thesis placement. Show me the restructured outline before you write prose.
```

Then:
```
Now run Pass 3 (Sentence Surgery). Apply all anti-pattern rules. Show me what you changed and why for each fix.
```

Then:
```
Now run Pass 4 (Voice Restoration) using the [voice name] voiceprint. The cleanup may have flattened the prose. Reinject personality.
```

Then:
```
Now run Pass 5 (Stress Test). For every paragraph, answer:
1. What would a skeptic attack?
2. What feels generic?
3. What could be cut?
4. What line actually lands?
```

Then:
```
Now give me all Pass 6 outputs: clean draft, annotated draft, scorecard, violations list, and next-pass recommendations.
```

### Multi-Session Longform Project Setup

For books, doctrine documents, or multi-part series:

```
I'm starting a longform project. Create a Project Memory File with:
- Project title: [title]
- Type: [book / doctrine / series]
- Voiceprint: [name or "build from samples"]
- Central thesis: [one sentence]
- Planned sections/chapters: [list]
- Terminology lock: [terms that must be consistent]

This is session 1. Track everything across sessions.
```

### Cross-Document Audit

```
I'm going to give you 3 documents from the same project. Run a full cross-document consistency audit:
- Voice consistency (sentence stats, vocabulary, formality)
- Terminology consistency
- Factual consistency (do any claims contradict?)
- Argument continuity
- Audience consistency

[paste document 1]
[paste document 2]
[paste document 3]
```

### Detector Benchmark Prep

```
I need this piece to pass Turnitin, GPTZero, and Originality.ai. Run the full detector preparation:

1. Statistical profile (sentence-length std dev, vocabulary analysis)
2. Cadence signature scan (check against all 59 patterns)
3. Perplexity uniformity check
4. Burstiness analysis
5. Transition homogeneity check
6. AI detection risk rating per paragraph

Fix everything flagged as medium or high risk. Show me the before/after statistical comparison:

[paste your text here]
```

### Expert Prompts — The Hardest Challenges

**1. Write Something Undetectable (Full Protocol)**
```
Write a 1,500-word academic essay arguing that social media regulation should be treated as a public health issue, not a free speech issue. Requirements:
- Use the academic rigorous voice
- Use the academic genre pack
- Include at least 5 real, named sources (tell me which ones to verify)
- Sentence-length standard deviation must exceed 8
- Zero hard-ban phrases
- Zero cadence signature matches at 3+ level
- At least 2 uncommon but precise words per 300 words
- No transition word used more than once
- Opening must NOT be a context-setter
- Closing must NOT be a summary
- Score must exceed 85
- Run the adversarial detection check when done and confirm all clear
```

**2. Build a Complete Voice from Scratch**
```
I'm going to give you 5 writing samples from [person]. Build a complete voiceprint with all 8 dimensions, sentence characteristics, paragraph characteristics, vocabulary profile, distinctive markers, and anti-patterns. Then write a 500-word passage on [topic] in that voice. Score the voice fidelity: would a reader of this person's work believe they wrote it?

[paste 5 samples]
```

**3. Genre Transfer Chain**
```
Take this strategy memo and transfer it through 3 genres in sequence:
1. Strategy → Sermon (same argument, different delivery)
2. Sermon → Sales copy (same truth, different mechanism)
3. Sales copy → Academic essay (same claim, different evidence standard)

Show me all 3 versions. Score each one in its target genre.

[paste strategy memo]
```

**4. The Rewrite Gauntlet**
```
This passage scores 95%+ AI-probability on GPTZero. Run it through the full 6-pass pipeline and produce output that:
- Preserves the core argument and all evidence
- Scores <20% AI-probability
- Scores ≥85 on the 100-point system
- A human reader would not suspect AI involvement

Show me the statistical comparison before and after:

[paste AI-generated text]
```

**5. Compile a Complete Document**
```
I need a 3,000-word strategy document on [topic]. Compile it from scratch using the full pipeline:

Pass 0: Declare mission, audience (board of directors), voice (sovereign commander), genre (strategy)
Pass 1: Skip (new writing)
Pass 2: Build the section architecture first — show me the outline with each section's declared job before writing
Pass 3-4: Write with anti-slop and voice enforcement active
Pass 5: Stress-test every section
Pass 6: Deliver clean draft + scorecard + 3 recommended improvements

Go.
```

---

## 7. Prompt Library — By Task

### Rewriting
```
Rewrite this to sound human, not AI-generated: [paste text]
```
```
Rewrite this in half the words without losing meaning: [paste text]
```
```
Rewrite this for a [specific audience]: [paste text]
```
```
Rewrite just the opening — make it hook the reader in one sentence: [paste text]
```
```
Rewrite just the closing — make it unforgettable: [paste text]
```

### Scoring & Diagnosis
```
Score this on the 100-point system: [paste text]
```
```
Run a full diagnostic — violations, AI risk, statistical profile: [paste text]
```
```
What are the 3 biggest problems with this piece? [paste text]
```
```
Which paragraphs are weakest? Why? [paste text]
```
```
Is this detectable as AI? What specifically would trigger a detector? [paste text]
```

### Writing From Scratch
```
Write a [word count] [type of piece] about [topic]. Voice: [voice]. Genre: [genre].
```
```
Write a [type] that scores 90+ on the Writing Intelligence scale about [topic].
```
```
Give me 3 different versions of [piece]: one cold, one warm, one conversational.
```
```
Write the strongest possible argument for [position]. Then write the strongest possible argument against it. Score both.
```

### Editing
```
Edit this for clarity only. Don't change the structure or voice: [paste text]
```
```
This is 80% there. Find the 20% that's weak and fix it: [paste text]
```
```
Make this tighter. Every sentence should earn its place: [paste text]
```

### Evidence & Research
```
This passage makes claims without evidence. Tell me exactly what evidence I need to find for each claim: [paste text]
```
```
Integrate these sources into this passage naturally: [paste text + sources]
```

---

## 8. Prompt Library — By Genre

### Academic
```
Write a thesis paragraph for a paper arguing [position]. Include the claim, scope, stakes, and roadmap.
```
```
Write a counterargument paragraph that steelmans the opposition to [my position], concedes what's true, then pivots to why my argument still holds.
```
```
Convert my rough notes into an evidence paragraph with proper claim-evidence-interpretation structure: [paste notes]
```
```
Generate 10 questions a professor would ask about this paper: [paste paper]
```

### Strategy
```
Write a strategy memo in SCIR format (Situation, Complication, Implication, Recommendation) about [topic]. Include owners, timelines, and risk analysis.
```

### Sales
```
Write a sales page using Hook → Story → Offer → Proof → Close for [product/service]. Include a specific guarantee and clear CTA.
```

### Fiction
```
Write a scene where [character A] discovers [revelation] through action and dialogue only. No internal monologue. No emotion words. Show everything.
```

### Sermon
```
Write a 12-minute sermon on [scripture passage]. Build from observation to conviction to altar call. Include one specific testimony and one moment of silence.
```

### Email
```
Write an email to [recipient] about [topic]. State the purpose in the first sentence. Include one clear ask with a deadline. Under 100 words.
```

### Pitch Deck
```
Write the speaker notes for a 12-slide Series A pitch deck for [company]. Slide 1: Title. Slide 2: Problem. Slide 3: Solution. Slide 4: Why Now. Slide 5: Market. Slide 6: Product. Slide 7: Traction. Slide 8: Business Model. Slide 9: Competition. Slide 10: Team. Slide 11: Ask. Slide 12: Close.
```

### Legal
```
Write a position memo on [legal issue]. Use IRAC structure: Issue, Rule, Application, Conclusion. Include statutory citations.
```

### Medical
```
Write an IMRAD-structured summary of [clinical scenario]. Introduction with research gap, Methods, Results, Discussion with limitations.
```

### Government
```
Write a decision brief on [issue]. BLUF format. Include options with pros/cons, fiscal impact, and a specific recommendation with implementation timeline.
```

### Dialogue
```
Write a conversation between [character A] and [character B] about [topic]. They disagree. Each must have a distinct voice — different vocabulary, sentence length, and verbal habits. Use subtext — neither character says exactly what they mean.
```

### Speech
```
Write a 7-minute speech for [occasion/audience] about [topic]. Include a cold open, three main points with landing lines, a turn, a climax with repetition, and a quiet close.
```

---

## 9. Prompt Library — By Voice

### Sovereign Commander
```
Write this like a general briefing a war room. Cold. Precise. Every sentence is either a fact, a conclusion, or a command. Zero filler:

[topic or text to rewrite]
```

### Academic Rigorous
```
Write this as a scholar would — evidence-first, properly qualified, with named sources. Confident on data-backed claims, explicitly hedged on projections:

[topic or text to rewrite]
```

### Casual Sharp
```
Write this like a smart friend explaining it over coffee. Conversational but intelligent. Contractions, personality, no hand-holding:

[topic or text to rewrite]
```

### Literary Recursive
```
Write this as layered prose — image-driven, subtext-heavy, with dramatic sentence-length variation. The most important things are said obliquely:

[topic or text to rewrite]
```

### Sermon Black Church
```
Write this for a congregation. Build from observation to conviction. Cadence matters — rhythm IS meaning. Specific testimony, not generic comfort. Dignity throughout:

[topic or text to rewrite]
```

### Investor Precision
```
Write this for investors. Data-first. No adjectives — only numbers. State assumptions explicitly. Quantify risk. Name what you don't know:

[topic or text to rewrite]
```

### Founder Manifesto
```
Write this as a founder addressing the world. Hot conviction, cold execution. Name the broken system. Declare what you're building. State the timeline. End with irreversibility:

[topic or text to rewrite]
```

---

## 10. Scoring & Diagnostics

### Quick Score
```
Score this on the Writing Intelligence 100-point scale. Give me the total and the breakdown:

[paste text]
```

### Full Diagnostic
```
Run the full auto-diagnostic on this piece:
1. Score (100-point, all 10 categories)
2. Auto-fail check (all 8 conditions)
3. Violation heatmap (by paragraph)
4. AI detection risk (by paragraph)
5. Top 3 violations with fixes
6. Top 3 strengths
7. Recommended next actions (ranked by impact)

[paste text]
```

### Grade Thresholds Reference
- **95-100**: Signature-grade — could only come from this author
- **90-94**: Elite — distinctive, defensible, memorable
- **80-89**: Strong — publishable with minor polish
- **70-79**: Usable but soft — needs tightening
- **Below 70**: Significant revision required
- **Auto-fail (capped at 65)**: 3+ hard-ban phrases, perplexity flatness, fabricated citations, sentence-length uniformity, zero domain vocabulary, unsupported universals, dictionary opening, summary conclusion

---

## 11. Academic Mode — Complete Guide

### Before You Write: Rubric Analysis
```
Here's my assignment prompt. Extract:
1. What verbs does it use? (argue, analyze, compare, evaluate?)
2. What does the rubric actually reward?
3. What's the expected evidence type?
4. What's prohibited?
5. What citation style?
6. What's the target depth?

Then build me an outline that maps every rubric criterion to a section:

[paste assignment prompt]
```

### Writing the Paper
```
Write a [word count] paper on [topic] for my [course name] class. The professor values [what they value]. Use the academic genre pack. Include:
- A thesis that states a position, not a topic
- Evidence paragraphs with claim-evidence-interpretation structure
- At least one counterargument engaged at its strongest
- A conclusion that extends, not summarizes
- All sources I should verify (flag them)
```

### Anti-Hallucination Check
```
Go through this paper and flag:
- Any quote that might be fabricated
- Any statistic without a named source
- Any study reference that isn't specific enough to verify
- Any page number that might be wrong
- Any "many scholars believe" without named scholars

Replace each flagged item with [VERIFY: description of what to look up]:

[paste paper]
```

### Authorship Defense Prep
```
Generate 10 questions my professor would likely ask about this paper if they suspected AI wrote it. Then write my answers — grounded in the specific sources and reasoning in the paper:

[paste paper]
```

### Discipline-Specific Reasoning
```
I'm writing for a [discipline: e.g., sociology / philosophy / history] class. What are the discipline-specific reasoning primitives I should be using? Show me what strong writing looks like in this field vs. what weak writing looks like.
```

---

## 12. Style Transfer

### Basic Transfer
```
Transfer this from [source genre] to [target genre]. Preserve all content and argument. Rebuild the structure, voice, and conventions:

[paste text]
```

### Transfer Examples
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
Transfer this email into a speech. Expand the compressed points. Add breathing room and landing lines.
```

---

## 13. Longform & Multi-Session

### Starting a Book Project
```
I'm starting a book project. Here are the details:
- Title: [title]
- Genre: [fiction / nonfiction / memoir / etc.]
- Central thesis or premise: [one sentence]
- Target reader: [who]
- Voice: [voiceprint name or "build from my samples"]
- Planned chapters: [list]

Create a Project Memory File. Track voice consistency, terminology, metaphors, and thesis continuity across every session. This is session 1.
```

### Continuing a Session
```
This is session [N] of [project name]. Last session I wrote [chapter/section]. Here's where we left off:

[paste the last paragraph or summary of where you stopped]

Continue from here. Check continuity against the Project Memory File before writing.
```

### End-of-Session Protocol
```
End of session for [project name]. Before we stop:
1. Update the Project Memory File with what was written today
2. Note any new terms, metaphors, or character developments
3. Flag any unresolved threads
4. Tell me what the next session should accomplish
```

---

## 14. Troubleshooting

**"The skill doesn't seem to be doing anything different."**
Start a new conversation after installing. Skills activate on new conversations, not mid-conversation. Then try one of the prompts from Section 2.

**"The output still sounds like AI."**
Be more specific in your prompt. Instead of "write me something about X," try: "Write 400 words about X using the casual sharp voice. No AI clichés. Vary sentence lengths dramatically. Include at least one sentence under 6 words."

**"The scoring seems harsh."**
It's calibrated against published, edited prose — not AI output. A score of 75 is usable professional writing. 85 is strong. 95+ is rare. If your writing scores 70, that's not a failure of the skill — it's the skill doing its job by showing you where to improve.

**"I want to use this with ChatGPT / Gemini / other LLMs."**
Copy `SKILL.md` into your system prompt or custom instructions. For deeper features, also paste the specific reference files you need (anti-patterns, voiceprints, genre packs). The skill was designed for Claude but the principles work with any LLM.

**"How do I make my writing pass Turnitin?"**
Use the adversarial stress test prompt from Section 5. The key factors: sentence-length variation (std dev ≥8), vocabulary unpredictability, no transition repetition, no cadence signatures, and no opening/closing clichés. The academic mode + inject_variance operator + custom voiceprint is the strongest combination.

---

## 15. FAQ

**Q: Is this just "anti-slop" with more files?**
No. Anti-slop tools remove AI patterns (subtractive). Writing Intelligence removes patterns AND constructs quality — voice, argument, evidence, structure, audience calibration, genre compliance (compiler). The difference is a spell-checker vs. a compiler.

**Q: Will this work for languages other than English?**
The principles (argument structure, paragraph physics, evidence discipline) are universal. The specific phrase bans and cadence signatures are English-focused. Community contributions for other languages are welcome.

**Q: Can I use this commercially?**
Yes. MIT license. Use it in your products, your courses, your agency, your workflow. Credit appreciated.

**Q: How do I contribute?**
See [CONTRIBUTING.md](https://github.com/antonio0720/writing-intelligence/blob/main/CONTRIBUTING.md). New anti-patterns, voiceprints, genre packs, examples, and detector benchmark results all improve the system.

**Q: Who built this?**
Antonio T. Smith Jr., Founder & CEO of Density6 LLC. Inventor of Operational Machine Consciousness (OMC) and Existential Recursive Intelligence (ERI). Built because the world needed a writing system that compiles quality, not just cleans surfaces.

**Q: Why is it free?**
Because language is how the poor build power and the middle class keep it. The student at 2 AM and the executive before the board meeting deserve the same tool.

---

## Quick Reference Card

| I Want To... | Prompt Starts With... |
|---|---|
| Clean up AI-sounding text | "Rewrite this to sound human..." |
| Score my writing | "Score this on the 100-point scale..." |
| Write something new | "Write a [length] [type] about [topic]. Voice: [voice]. Genre: [genre]." |
| Fix a weak opening | "Rewrite just the first paragraph to hook the reader..." |
| Fix a weak closing | "Rewrite the final paragraph for maximum impact..." |
| Make it shorter | "Compress this by [N]% without losing meaning..." |
| Make it smarter | "Apply the raise_intelligence operator..." |
| Add specifics | "Apply the add_specificity operator..." |
| Change the voice | "Rewrite this in the [voice name] voice..." |
| Transfer genres | "Transfer this from [genre A] to [genre B]..." |
| Check for AI detection risk | "Run the adversarial stress test on this..." |
| Full diagnostic | "Run the full auto-diagnostic report..." |
| Build my custom voice | "Build a custom voiceprint from these 3 samples..." |
| Academic paper | "Write using the academic genre pack and academic rigorous voice..." |
| Score a draft | "Score this and tell me the 3 highest-impact fixes..." |

---

*Built by Antonio T. Smith Jr. / [Density6 LLC](https://density6.com)*

*Writing should sound like a person wrote it. This makes sure it does.*

*[github.com/antonio0720/writing-intelligence](https://github.com/antonio0720/writing-intelligence)*
