# Proof Protocol

How claims get found, classified, verified, and gated. This is the mechanism behind Law D (support means a verbatim span) and Law E (under-claim).

Read this whenever the work involves sources, citations, fact-checking, or a document whose claims could be challenged.

---

## 1. Find the claims

Walk the text and mark every sentence that asserts something checkable. The signal is **checkable content**, not assertive tone:

numerals · dates and date ranges · quantities and units · currency · percentages · named entities · superlatives ("the largest," "the first") · comparatives ("twice as," "more than") · causal assertions ("X caused Y") · attributions ("according to," "X said") · quotations · categorical statements ("all," "no," "never")

A sentence with none of these is rhetoric or framing. It carries no verification burden. Do not flag it — over-flagging trains authors to ignore the flags.

## 2. Split into atoms

One sentence often makes several separable assertions. Verification operates on the smallest independently checkable unit, because that is what tells the author *which half of the sentence* is the problem.

> "Between 2019 and 2023, the program served 12,400 households and cut wait times by 38%."

Three atoms: the date range · the household count · the wait-time reduction. Each supportable on its own. A sentence where two atoms hold and one does not is `partially supported`, and saying so is far more useful than a single verdict on the whole sentence.

## 3. Classify

| Class | Definition | Verification burden |
|---|---|---|
| `sourced_fact` | Asserts an external, checkable fact | Needs a verbatim span |
| `observed_fact` | Something the author directly did, saw, built, or owns | Author's own assertion; label it, do not demand a source |
| `synthesis` | Combines multiple sources into a new statement | Each input needs support; the combination is the author's |
| `inference` | Reasons beyond what any source states | Label as reasoning; never present as fact |
| `recommendation` | Prescribes an action | Its factual premises need support; the recommendation does not |
| `rhetoric` | Framing with no checkable content | None |

Misclassification cuts both ways. Treating an author's own operating experience as an unsupported claim is insulting and wrong. Treating an inference as a sourced fact is the failure that matters.

## 4. Verify — the span lock

**For each `sourced_fact` atom, find a passage in the supplied sources and reproduce it verbatim.**

Verbatim means: exact characters, exact numbers, exact names. Whitespace may be normalized. Nothing else.

The span goes in the output next to the claim. The author can see with their own eyes whether the quoted sentence supports the claim it sits beside — which means the verification is checkable by someone who does not trust the system.

**If the span cannot be produced, the claim is `needs_source`.** No exceptions, and specifically no exception for claims that are obviously true. "Water boils at 100°C" without a supplied source is still `needs_source` under strict mode — because the discipline only holds if it holds when it feels unnecessary.

**Verification statuses:**

| Status | Meaning |
|---|---|
| `quote_verified` | The text quotes the source, and the quotation is verbatim present |
| `supported` | A verbatim span entails the atom |
| `partially_supported` | Some atoms in the sentence supported, others not |
| `author_asserted` | Author's own observation, labeled as such |
| `inference` | Reasoning beyond the sources, labeled as such |
| `needs_source` | No verbatim span found |
| `conflicted` | A source says something incompatible |
| `unsafe` | Citation resolves to nothing, or an approved source directly contradicts |
| `stale` | Verified earlier, but the sentence changed since |

## 5. Deterministic checks that always run

These need no model judgment and no network. They work in any language and they catch the errors that hurt most. Run them even in `light` mode.

**Quotation check.** Every quoted string in the text must appear verbatim in a source. A misquotation is the most common serious error in sourced writing and the easiest to catch.

**Numeric check.** Every number in a claim, against the number in the passage cited for it. `12,400` vs `12,400` passes. `12,400` vs `about 12,000` is a mismatch — flag it, and offer the qualification that would make it true.

**Date check.** Ranges and points, canonicalized. "Since 2019" against a source saying "beginning in 2021" is a contradiction, not a rounding.

**Entity check.** If none of the claim's named entities appear in the passage, that passage does not support that claim regardless of how topically similar it reads.

**Citation resolution.** Every citation-shaped construction resolves to a supplied source, or it is `unsafe`. This is the fabrication check.

On a filesystem, `scripts/wi.py verify` runs all five mechanically. Prefer the script over doing it by eye — it does not get tired on page 40, and its output is reproducible.

## 6. Staleness

A verification belongs to a specific wording. Change the sentence, and the verification is gone until re-run.

This applies within a single conversation. If a claim was verified, then the author revised that sentence, the claim is `stale` — say so rather than carrying the old status forward. Silently inherited verification is how a system ends up asserting that an edited sentence was checked.

## 7. The gate

Produce a verdict with reasons and repairs. See `OUTPUT_TEMPLATES.md` for exact format.

```
BLOCK   ← unresolvable citation, or approved source contradicts
HOLD    ← unsupported claims, conflicts, or stale verifications, under strict/regulated
RELEASE ← nothing outstanding
```

Under `standard`, unsupported claims produce advisory notes, not a hold. Under `strict`, they hold. Under `regulated`, conflicts block and every proceed-anyway needs a stated reason recorded in the report.

## 8. Waivers

An author may proceed past a hold. Record it: which claim, what reason, what disclosure appears in the final text if any. Waivers belong in the report, because the report is the artifact that gets handed to counsel or a program officer.

A waiver dies when its sentence changes. You cannot waive a claim and then rewrite it under the waiver.

## 9. What this protocol does not do

**It does not verify truth.** It verifies *support within the sources the author supplied*. If the source is wrong, a claim will read `supported` and be false. Say this plainly the first time a proof report appears in a conversation — an author who thinks the system checks reality will trust it in exactly the situation where it cannot help them.

**It does not adjudicate source quality.** Surface what is knowable — date, origin, conflicts with other supplied sources — and leave the judgment with the author and their reviewers.

**It does not search for sources.** If no source supports a claim, the answer is `needs_source`, not a constructed citation. Offering to search, where searching is available, is fine. Inventing is never.
