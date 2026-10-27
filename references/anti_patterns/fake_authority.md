# Fake Authority Patterns

These patterns create the illusion of expertise, credibility, or insider
knowledge without actually providing it. They are especially common in AI
output because LLMs are trained to sound authoritative.

---

## The Unnamed Expert

"Experts agree that..." / "Research shows that..." / "Studies have found..."

No expert is named. No study is cited. The plural form creates an impression
of consensus that may not exist.

Fix: Name the expert. Cite the study. If you can't, the claim is unsupported.

---

## The False Consensus

"Everyone knows that..." / "It's widely accepted that..." / "The general
consensus is..."

These phrases smuggle a disputed claim past the reader by asserting agreement
that may not exist.

Fix: State the claim directly and provide evidence. If there IS a consensus,
cite the body that established it. If there isn't, acknowledge the debate.

---

## The Authority Stack

Listing multiple credentials, titles, or institutions without connecting them
to the specific claim being made.

"As a Harvard-trained economist, bestselling author, and former White House
advisor, I can tell you that..."

The credentials may be real, but they don't substitute for evidence on the
specific point. A Harvard economist can still be wrong about a particular
market prediction.

Fix: Lead with the evidence. Credentials are context, not proof.

---

## The Historical Invoke

"History teaches us that..." / "As history has shown..." / "If history is
any guide..."

This treats "history" as a unified authority rather than a contested, complex
record that supports multiple interpretations.

Fix: Name the specific historical event or period. Acknowledge the specific
parallel and its limits. "The 1997 Asian financial crisis — specifically
Thailand's decision to unpeg the baht — illustrates what happens when..."

---

## The Quantitative Bluff

"Significantly" / "Substantially" / "Dramatically" — used without numbers.

"Our efficiency improved dramatically." How much? 3%? 300%? The word
"dramatically" hides the absence of data.

Fix: Provide the number. If you don't have it, say "by an amount we haven't
quantified" or remove the claim.

---

## The Framework Drop

Invoking a named framework, model, or theory as if mentioning it constitutes
an argument.

"Using a Porter's Five Forces analysis..." followed by a generic assessment
that doesn't actually apply the five forces.

"From a Maslow's hierarchy perspective..." followed by a point that has
nothing to do with hierarchical needs.

Fix: If you invoke a framework, apply it rigorously. Show the specific
analytical steps. If the framework doesn't add analytical value, drop it.

---

## The Certainty Escalator

Gradually increasing certainty across a passage without adding evidence.

Sentence 1: "This may contribute to..." (hedged)
Sentence 2: "This likely plays a role in..." (more certain)
Sentence 3: "This drives the outcome of..." (certain)
Sentence 4: "This is the primary cause of..." (causal claim)

The evidence didn't change. The language did.

Fix: Match certainty level to evidence level. If the evidence supports "may
contribute," don't escalate to "is the primary cause" without new evidence.

---

## The Jargon Shield

Using technical vocabulary to create an impression of expertise while
obscuring the actual argument.

"The paradigmatic shift in our ontological framework necessitates a
recalibration of the epistemological underpinnings of our strategic
operational methodology."

Translation: "We need to change how we think about this."

Fix: State the idea plainly first. Then add technical precision where it
genuinely adds meaning. If the plain version says the same thing, the
jargon was a shield.

---

## The Experience Claim

"In my experience..." / "Having worked in this field for X years..."

Experience is context, not evidence. Twenty years of doing something wrong
doesn't make it right. And "In my experience" written for someone who has
no such experience is not hollow, it is false: a model, a ghostwriter without
the client's notes, or a template can produce the sentence, but only the person
can supply the event behind it.

Fix: State the observation. Provide supporting evidence. If personal
experience is genuinely relevant, give a specific example with details
that prove you were actually there.

---

## v9: Source Before Style, and the Catalog Cross-Reference

Fake authority is a **source** problem before it is a wording problem. Rewriting "Experts agree" into a more elegant sentence fixes nothing if there is no expert behind it. v9 therefore treats these patterns as questions about evidence.

**Catalog categories.** The 334-rule editorial catalog (`prototypes/wi9/rules/v9_hotphrases.json`, experimental, proposed on PR #8) puts "studies show", "research shows", "experts agree", "it is widely known" under `generic_claim`, with the question *can you identify an actual source, date, sample or bounded observation?* A hit is an editorial question. It is not evidence of how the passage was produced, and it never triggers an automatic rewrite.

| Pattern in this file | v9 handling |
|---|---|
| Unnamed Expert, False Consensus | `generic_claim`. Answer with a source the author actually holds, or mark the claim `needs_source`. Do not invent a study or an expert to fill the gap. |
| Quantitative Bluff, Certainty Escalator | Supply the number from a source or lower the claim. In an authorship dossier the claim-coverage check requires an anchored evidence span under each consequential claim. |
| Experience Claim | A first-person "I saw / I measured / I decided" needs an author-supplied event. A planned, hypothetical or modelled scene cannot support it (`experience_state`, principle WI9-E). |
| Authority Borrow, Historical Invoke | Verify the quotation and the event. Never supply a plausible attribution from memory. |
| Authority Stack, Framework Drop | Credentials and frameworks are context. They do not count as support for the specific claim. |

### When not to fix

Leave the wording, or add the source and keep the wording, when:

- **The citation follows.** "Research shows that sleep loss impairs recall [source]" in a literature review is a summary with its anchor in the next clause. (Synthetic example; the bracket stands for a real citation the author must supply.)
- **It is a quoted maxim or a source's own words.** A profile that quotes a coach saying "everybody knows you can't coach speed" reports her claim as hers; the sentence is attributed, not asserted.
- **The consensus is documented.** "It is widely accepted that ..." is acceptable when the next sentence names the standard-setting body and the document.
- **The credentials are the subject.** In a biography or speaker introduction, listing titles is the content.
- **Firsthand experience is real and supplied.** "In my fourth year running the intake desk I saw ..." is the opposite of this pattern, if the author supplied it and can answer questions about it.

### Recording a keep/revise decision

Record the call in the phrase review ledger (`prototypes/wi9/wi9_phrase_review.py`): `retain_as_written` for a legitimate use with the reason, `needs_source` when the author has to find or confirm a source, `revise_for_clarity` when the support exists and the sentence hides it. The ledger binds each decision to the exact document and rule-pack digests, so a later edit makes it stale and forces a fresh look. The reviewer identity is self-declared; the ledger proves a decision was recorded, not that the claim is true.
