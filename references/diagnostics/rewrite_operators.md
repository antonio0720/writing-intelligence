# Rewrite Operators

## Usage

Operators are applied individually or chained. Each operator has a trigger
syntax, a description of what it does, and examples of before/after.

---

## compress(N%)

Reduce word count by N% without losing meaning or argument structure.

Method:
1. Identify recursive restatements — keep the strongest version
2. Remove ornamental adverbs and adjectives
3. Collapse multi-clause sentences where one clause adds nothing
4. Merge paragraphs with overlapping content
5. Replace circumlocutions with direct statements

Before (62 words):
"It is absolutely essential that we take the time to carefully consider all of
the various different factors that might potentially impact the final outcome
of this particular decision, because the consequences of making the wrong choice
could be quite significant and far-reaching for the organization as a whole."

After compress(70%) — 18 words:
"This decision has significant consequences. We need to evaluate every factor
before committing."

---

## raise_intelligence

Increase sophistication of thought without increasing jargon. The text should
feel smarter because the IDEAS are sharper, not because the WORDS are bigger.

Method:
1. Replace surface observations with causal analysis
2. Add specificity — named mechanisms, concrete examples, precise numbers
3. Acknowledge complexity where the original oversimplifies
4. Introduce one non-obvious connection per 500 words
5. Tighten logical transitions so the argument's architecture becomes visible

Before:
"Social media has changed how people communicate. This has both good and bad
effects on society."

After:
"Social media compressed the feedback loop between expression and response from
days to seconds. That compression rewired social incentives: visibility became
currency, and the fastest path to visibility was provocation. The platforms that
profited from engagement had no structural reason to penalize the dynamic."

---

## add_specificity

Replace every abstraction with a named actor, concrete number, specific example,
or verifiable observation.

Before:
"The company experienced significant growth in recent years."

After:
"Stripe processed $817 billion in payment volume in 2023, up from $640 billion
in 2022 — a 28% increase driven primarily by expansion into 15 new markets."

---

## abstract_to_scene

Convert a conceptual passage into grounded narrative. The idea becomes visible
through a specific moment, place, and set of actions.

Before:
"Burnout is a growing problem in the tech industry, with many workers
experiencing chronic stress and exhaustion."

After:
"At 11:40 PM on a Tuesday, a senior engineer at a Series C startup in Austin
pushed a commit, closed her laptop, and sat in the dark for nine minutes before
she could stand up. She'd shipped code every day for 23 consecutive days. Her
Slack status said 'focused.' Her hands were shaking."

---

## sharpen_thesis

Make the core claim more precise, more falsifiable, and more defensible.

Before:
"Education needs to be reformed to better serve students."

After:
"The current K-12 funding model, which ties school budgets to local property
taxes, ensures that the students with the fewest resources attend the schools
with the least money — a structural guarantee of inequality that no curriculum
reform can fix without addressing revenue allocation."

---

## strip_corporate

Remove institutional voice patterns. Replace passive, hedged, committee-written
prose with direct, human-sounding sentences.

Indicators of corporate voice:
- Passive constructions hiding accountability
- "Stakeholder," "leverage," "synergy," "alignment," "operationalize"
- Sentences that could appear in any company's annual report
- Hedging that avoids commitment: "We are committed to exploring..."

Before:
"We are pleased to announce that we have successfully completed the strategic
realignment of our organizational priorities to better leverage our core
competencies and drive stakeholder value."

After:
"We reorganized. Three teams merged into one. We cut two product lines that
weren't working. The team that remains is focused on the three things that
actually make us money."

---

## make_colder

Reduce warmth. Increase analytical distance. Remove emotional appeals. The text
should feel like a briefing, not a conversation.

Method:
- Remove first-person emotional language
- Replace "we" framing with third-person analytical framing
- Cut reassurance and encouragement
- Increase data density
- Reduce metaphor density
- Shorten sentences

---

## make_warmer

Increase empathy signals without sentimentality. The text should feel like it
was written by someone who understands the reader's situation.

Method:
- Add second-person address where appropriate
- Include one specific acknowledgment of the reader's likely experience
- Replace clinical language with accessible equivalents
- Add one concrete human example
- Do NOT add performative empathy ("I see you"). Add real understanding.

---

## make_executable

Convert insight into action steps. Every observation becomes an instruction.

Before:
"Team communication is critical for project success. When teams communicate
effectively, they avoid misunderstandings and deliver better results."

After:
"Run a 15-minute daily standup. Each person answers three questions: what did I
finish yesterday, what am I doing today, what's blocking me. If a blocker
surfaces, assign an owner and a deadline before the standup ends. No blocker
leaves the room unowned."

---

## genre_transfer(from, to)

Rewrite content in the conventions of a target genre while preserving the
core argument or content.

Example — genre_transfer(academic, sermon):

Before (academic):
"Research indicates that social isolation correlates with increased mortality
risk at rates comparable to smoking 15 cigarettes per day (Holt-Lunstad, 2015)."

After (sermon):
"Loneliness will kill you. Not metaphorically — medically. The researchers
measured it. Being alone, truly alone, does the same damage to your body as
smoking fifteen cigarettes every single day. Fifteen. And nobody's putting a
warning label on an empty apartment."

---

## audience_shift(from, to)

Adjust register, vocabulary, and evidence expectations for a different reader.

Example — audience_shift(expert, general_public):

Before:
"The attenuation of dopaminergic signaling in the mesocortical pathway is
implicated in the anhedonic presentation characteristic of major depressive
disorder."

After:
"Depression doesn't just make you sad. It dulls your brain's reward system — the
part that makes you want things, enjoy things, look forward to things. The
chemistry that drives motivation literally stops working at normal levels."

---

## inject_variance

Add sentence-length and vocabulary unpredictability. This is the anti-detector
operator. It specifically targets the statistical signatures that AI detectors use.

Method:
1. Identify any span of 3+ sentences within ±5 words of each other → break the pattern
2. Insert one sentence ≤6 words per 500 words
3. Insert one sentence ≥30 words per 500 words
4. Replace any word used 3+ times in 500 words with a synonym or restructure
5. Vary paragraph opening syntax — no two consecutive paragraphs start the same way
6. Introduce one uncommon but precise word per 300 words

---

## kill_padding

Remove every sentence that doesn't advance the argument, deepen the scene,
or provide evidence.

Test per sentence: "If I delete this sentence, does the paragraph lose anything
the reader needs?" If no, delete it.

---

## strengthen_closing

Rewrite the final paragraph for maximum residue.

Method:
1. Delete any summary content
2. Identify the single most important implication of the entire piece
3. Express it in a way that extends beyond what was argued — into consequence, challenge, or image
4. End on a sentence the reader will carry. Not a question. Not a platitude. A landing.
