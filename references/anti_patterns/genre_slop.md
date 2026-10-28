# Genre Slop

Genre-specific cliché patterns that signal either AI generation or lazy
writing within a particular domain. These extend the general anti-patterns
into domain-specific territory.

---

## Academic Slop

- "Scholars have long debated..."
- "This topic has received considerable attention in the literature..."
- "A growing body of research suggests..."
- "It is beyond the scope of this paper to..."
- Opening with a dictionary definition
- Conclusion that restates the introduction word-for-word
- "More research is needed" as conclusion (unless it genuinely identifies specific research gaps)
- "Since the dawn of civilization" / "Throughout human history" / "Since time immemorial"
- Using "interesting" or "fascinating" as analytical terms
- Block quotes longer than the analysis that follows them
- Literature review organized chronologically instead of thematically
- "This paper will argue that..." repeated in every section

Detection: 3+ of these in a single academic paper = genre slop.

---

## Business / Corporate Slop

- "Move the needle" / "Low-hanging fruit" / "Circle back"
- "Synergy" / "Alignment" / "Stakeholder value"
- "At the end of the day" / "Going forward" / "On a go-forward basis"
- "Leverage our core competencies"
- "Best-in-class" / "World-class" / "Industry-leading"
- "Robust" (when not describing statistical methods)
- "Scalable solution" (without specifying scale parameters)
- "Customer-centric" / "Data-driven" / "Results-oriented"
- Passive voice hiding accountability: "Mistakes were made"
- Bullet points substituting for argument
- "Quick wins" / "Deep dive" / "Touch base"
- Strategy documents that contain zero numbers

Detection: 5+ buzzwords per page = corporate slop.

---

## Self-Help / Motivational Slop

- "Your only limit is you"
- "Be the change you wish to see"
- "Success is a journey, not a destination"
- "Comfort zone" used as if it's an original observation
- "What would you do if you couldn't fail?"
- Any sentence structure: "[Noun] is not [expected thing]. It's [reframing]."
- "Give yourself permission to..."
- "You are worthy of..."
- Lists of habits ("7 habits of..." / "5 things successful people...")
- Morning routine prescriptions
- "Mindset" as a universal explanation
- Vague transformation claims without mechanism

Detection: Pattern of abstract inspiration without specific mechanism = motivational slop.

---

## Tech Blog Slop

- "In this blog post, we'll explore..."
- "Let's dive in!" / "Without further ado..."
- "TL;DR" as a section header in formal writing
- "Bonus tip:" as if the reader won a prize
- Step-by-step tutorials that explain the obvious while skipping the hard parts
- "YAML/JSON configuration" copy-pasted without explanation of WHY each field matters
- "As you can see" (the reader can't see — they're reading)
- Framework comparisons that don't test the same workload
- "It depends" as a conclusion without specifying on what
- Code snippets without context or error handling
- "Happy path" only documentation
- "Simply" before something not simple

Detection: "Let's dive in" + "Without further ado" + "As you can see" = tech blog slop.

---

## Political / Op-Ed Slop

- "Now more than ever"
- "We stand at a crossroads"
- "The American people deserve..."
- "Common-sense solutions"
- "Both sides" framing without substantive analysis of either side
- "Elites" without defining who qualifies
- "The silent majority" / "Real Americans" / "Ordinary people"
- Anecdote → universal claim without intermediate evidence
- "If we don't act now..." without specifying the timeline or consequence
- "Our children and grandchildren" as emotional leverage without policy specifics

Detection: 3+ of these per 500 words = political slop.

---

## Sermon / Spiritual Slop

- "God has a plan for your life" without scriptural or pastoral specificity
- "Just trust the process" as spiritual advice
- "Everything happens for a reason" deployed as comfort for genuine suffering
- Prosperity gospel framing: faithfulness = financial reward
- Generic "seasons" language ("You're in a season of...")
- "God won't give you more than you can handle" (misquoted and misapplied)
- Platitudes replacing pastoral engagement with real pain
- Closing with "Let us pray" after saying nothing specific to pray about
- Name-dropping scripture without engaging with its context or difficulty

Detection: Generic comfort language without specific pastoral engagement = sermon slop.

---

## Fiction Slop

- "Little did they know..."
- "If only they had known..."
- "A chill ran down their spine"
- "Their heart skipped a beat"
- "Time seemed to stand still"
- Eyes described as "orbs"
- Describing a character by having them look in a mirror
- Weather matching mood (rain = sad, sunshine = happy) without irony or complication
- "Said" replaced by a thesaurus of speech verbs: "opined," "exclaimed," "queried," "retorted"
- Internal monologue that sounds like a therapy session
- Villains who explain their plans
- Describing a woman's body through a male gaze POV without narrative awareness

Detection: 3+ clichés per 1000 words = fiction slop.

---

## Sales Copy Slop

- "What if I told you..."
- "Are you tired of [thing]? So were we."
- "But wait, there's more!"
- "Limited time offer" without a real deadline
- "Join thousands of satisfied customers"
- "Risk-free" without specifying the guarantee terms
- Stacking adjectives: "amazing, incredible, life-changing"
- Fake urgency: countdown timers, "only 3 spots left"
- Testimonials that sound written by the same person
- "$10,000 worth of bonuses" for digital content with no marginal cost
- "Valued at $X" for something never sold at that price

Detection: Manufactured urgency + vague proof + adjective stacking = sales slop.

---

## v9: Genre Slop Is a Venue and Source Question

The detection thresholds above ("3+ in a paper", "5+ buzzwords per page") are editing heuristics for a reviewer's attention, not tests of how a text was produced. v9 adds two things: a cross-reference to the editorial phrase catalog and a venue check, because what counts as slop depends on the genre the venue expects.

**Catalog categories.** The experimental 334-rule catalog (`prototypes/wi9/rules/v9_hotphrases.json`) has no genre field; it asks genre-independent questions. Use it as follows.

| Genre section | Catalog categories that overlap |
|---|---|
| Business / Corporate | `marketing_abstraction`, `domainless_solutionism` (who does what, under which conditions, with what observable result?) |
| Tech Blog | `staged_explanation` ("let's dive in", "let's unpack"), `forced_audience_engagement` |
| Self-Help / Motivational, Sales Copy | `performed_candor`, `forced_audience_engagement`, `generic_claim`, `domainless_solutionism` |
| Political / Op-Ed | `generic_claim`, `generic_closure`, `overused_rhetorical_structure` |
| Sermon / Spiritual | `generic_closure`, `empty_metaphor`; see also the sermon voiceprint |
| Academic | `generic_claim`, `qualifier_padding`, `staged_explanation` |
| Fiction | none; fiction slop is a craft judgment and the fiction gates are unchanged by v9 |

A match is an editorial question with legitimate counterexamples. It is not proof about origin and does not call for an automatic rewrite.

### When not to fix

Per genre, one legitimate counterexample (all **synthetic**, written for this page):

- **Academic.** "A growing body of research suggests ..." is fine when the next sentence lists the studies and the paragraph then argues from them; it fails only when nothing follows. Block quotes are ordinary in textual analysis when the analysis that follows is longer.
- **Business.** "Customer-centric" inside a quoted company value statement in an audit is evidence of what the company said.
- **Tech.** "As you can see" in a documentation page with a screenshot directly above is accurate.
- **Self-help.** A fixed morning-routine list is the subject matter of a book about routines.
- **Political.** "Now more than ever" in a verbatim speech excerpt belongs to the speaker.
- **Sermon.** "God has a plan" inside a pastor's own sermon, tied to a named text and a named congregation event, is pastoral speech, not filler; the slop is the version that engages with no text and no person.
- **Sales.** "Limited time offer" with a printed, verifiable end date is a statement of fact.
- **Fiction.** A cliché in a character's mouth may be the characterization.

### Venue contract first

Before cleaning slop out of a pitch, byline or submission, read the venue's rules (principle WI9-G). A human-only venue (a source-quote request, a journalism pitch, a contest) forbids AI-written or AI-rewritten submission copy no matter how clean the result is; the system may help build a research brief, but the submitting text must be the person's own. Cleaning a draft does not change who wrote it.

### Recording a keep/revise decision

For any phrase flagged in a genre section, record the call in the review ledger (`prototypes/wi9/wi9_phrase_review.py`) with one of `retain_as_written`, `revise_for_clarity`, `needs_source` or `not_applicable`, a rationale, a reviewer and an offset-aware time. Decisions are bound to the exact document and rule-pack digests and go stale when the draft changes.
