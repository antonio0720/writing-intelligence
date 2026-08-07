# Non-Goals

What Writing Intelligence v5 refuses to do, and why each refusal is load-bearing rather than decorative.

A non-goal is not a gap in the roadmap. It is a decision that has already been made, with reasoning attached, so that it does not have to be re-litigated every time someone arrives with a plausible reason to cross the line. The plausible reason is the point — none of these refusals exist to block bad ideas. They exist to block good-sounding ones.

The v4 non-goals carry forward with their full reasoning, strengthened where v5's machinery makes them sharper. The originals: [`../v4/NON_GOALS.md`](../v4/NON_GOALS.md).

---

## Table of contents

**Carried forward from v4**

1. Detector evasion
2. Source generation and citation invention
3. Truth verification
4. Absolute quality scores
5. Also preserved without change

**New in v5**

6. No hosted-account dependency
7. No proprietary-model dependency
8. No vector database as the truth layer
9. No blockchain
10. No public transparency log by default
11. No autonomous source approval
12. No automatic legal or medical adjudication
13. No claim of invention over prior art

**Operating with refusals**

14. How to decline without being useless
15. What a non-goal is not

---

## Carried forward from v4

### Detector evasion

**Anti-slop is a craft objective, not a laundering service.**

The goal is writing that does not pattern-match to machine prose because it is actually better constructed — earned specificity, real structure, sentences that carry weight. That is a legitimate objective and it is what the craft kernel does. Requests framed as *"make this pass an AI detector"* get the craft work and a plain statement that detector evasion is not the goal. The craft work usually satisfies the underlying need; the framing is what gets declined.

**Why the refusal is load-bearing in v5.** v5 makes this refusal structural rather than merely stated. A v5 release bundle records what happened to a document — sources, atoms, anchors, decisions, transformations, provenance. A system built to produce a machine-checkable account of how a document came to exist cannot also be a system for concealing how a document came to exist. Those are opposite products. Building the evasion feature would require the release bundle to lie, and a bundle that lies once is worth nothing forever.

### Source generation and citation invention

**Never construct a citation. Ever.**

If a claim needs support and none exists in the supplied material, the output is `needs_source`. Offering to search, where search is available, is fine. Inventing a plausible reference is the single most damaging thing this system could do, and Law D exists specifically so that it cannot happen quietly.

**Why the refusal is load-bearing in v5.** A fabricated citation is uniquely destructive because it is self-concealing: it looks exactly like a real one, it survives casual review, and it is usually found by the one reader who was going to decide something. v5 hardens the refusal by making support a *resolvable anchor* rather than a *string that looks like a reference*. An anchor either resolves into a specific version of a specific ingested source at a specific location, or it does not exist. There is no code path in which a well-formed anchor can be produced for a source that was never ingested — which is a stronger guarantee than asking a generator to behave.

### Truth verification

**Support within supplied sources is not truth.**

The proof protocol verifies support within the sources the author supplied. If the source is wrong, a claim reads `supported` and is false. This is stated the first time proof output appears, because an author who believes reality is being checked will trust the system in exactly the situation where it cannot help.

**Why the refusal is load-bearing in v5.** v5 makes the proof output much stronger, and that is precisely what makes this refusal more urgent, not less. A `.wiab` bundle that verifies offline, cryptographically, on a stranger's machine is an extremely convincing artifact. It proves that the document's claims are anchored to the sources supplied, that the anchors resolve, that the decisions were recorded, and that nothing drifted since. It proves nothing whatsoever about whether those sources are correct.

Source quality is a human editorial judgment. v5 gives it a place to live — source approval is an actor-attributed decision under Law J, so a reader can at least see *who* vouched for the source and when. That is accountability for the choice. It is not verification of the content, and no amount of graph machinery will convert one into the other.

### Absolute quality scores

**There is no universal writing number.**

Scores are relative to a stated profile, arena and mission. Presenting a context-free quality number is the fake-authority pattern the v3 doctrine already names.

**Why the refusal is load-bearing in v5.** v5 adds a fourth reliability type and a graph full of countable things, which makes a single headline number more tempting than it has ever been — every dashboard wants one. It is still forbidden, and now for a second reason: a blended score would average across the reliability types, which is the one operation that destroys the information those types exist to carry. See [`RELIABILITY_TYPES.md`](RELIABILITY_TYPES.md). Counts with visible denominators are legitimate. A number that stands in for the counts is not.

### Also preserved without change

Three further v4 refusals carry into v5 untouched, because v5 gives each of them stronger machinery rather than a new argument.

**Ghostwriting that erases authorship.** Every change is a proposal. An author who cannot see what changed is not the author. v5 makes the proposal a machine-readable object with a recorded decision (Laws A and J), so "the author approved this" becomes a checkable statement rather than an assumption.

**Unauthorized voice modeling.** Modeling a real, named person's voice requires a stated consent basis. See [`../v4/VOICE_CONSENT.md`](../v4/VOICE_CONSENT.md). v5 adds nothing permissive here; the consent basis is an actor-attributed record like any other decision.

**Silent memory.** Preferences inferred across a session get stated before they are applied. An unstated standing rule the author never granted is a silent rewrite moved up a level — Law A defeated by being applied to policy instead of prose.

---

## New in v5

### No hosted-account dependency

**v5.0 works local-first and offline. Nothing constitutional requires a server.**

`wi init`, `ingest`, `atomize`, `anchor`, `graph`, `impact`, `diff --semantic`, `test`, `explain`, `bundle`, `verify-release` and `doctor` all run on one machine with no network, from a single stdlib-only Python file.

**Why it is load-bearing.** The documents that most need this system are the ones that cannot leave the building: sealed bids, pre-publication investigations, patient material, privileged legal work, unannounced filings, classified review. A tool that requires an account excludes exactly the users whose stakes justify it. Worse, a hosted dependency puts a company between an author and their own evidence — and companies get acquired, change terms, deprecate endpoints and go out of business, at which point every release bundle they were required to validate becomes unverifiable. A proof that expires when a vendor does is not a proof.

Hosted collaboration may exist later as an option. It will never be a precondition for a single constitutional guarantee.

### No proprietary-model dependency

**The deterministic tier is model-independent by construction. Judgment providers are replaceable and named in every record.**

Every check in `scripts/wi.py` today is a comparison — strings, numbers, dates, digests, offsets. No model is invoked, and none can be. When the judgment tier arrives, it will be an interface with named, swappable providers, and Law L requires every judgment record to carry its provider and model identifier.

**Why it is load-bearing.** A verification system whose answers depend on a specific vendor's specific model has not eliminated trust; it has relocated it somewhere the reader cannot audit and the author cannot control. Models are also non-stationary — the same prompt to the same product name returns different output across versions, and a proof that silently changes underneath you is not a proof. The deterministic tier gives the same answer today, next year, and in an air-gapped room in 2039, which is the only basis on which a release bundle can promise anything.

Models are third-party infrastructure here, on the same footing as a PDF decoder. Named so they can be replaced, audited and disagreed with. Never authors, never contributors, never signers.

### No vector database as the truth layer

**Embeddings are candidate retrieval. They are never evidence.**

High cosine similarity is not support. Retrieval scores never become proof scores. No record typed `verified` may cite a similarity value as its basis, and no similarity value may be rendered as a confidence, a coverage figure or a support strength.

**Why it is load-bearing.** Embedding proximity measures distributional similarity, which is not entailment and is frequently its opposite. "The program served 12,400 households" and "the program served 11,800 households" are neighbors in embedding space and are a career-ending difference in a grant narrative. Negation barely moves a vector. Attribution swaps barely move a vector. Date shifts barely move a vector. Every failure this system was built to catch is a small distance in exactly the space a similarity search is scoring — which makes similarity not merely a weak proxy for support but a proxy that is *blind in the specific direction of the risk*.

Retrieval is genuinely useful, in its place. The correct pipeline:

```
embedding / BM25 search        find plausible passages, fast, over a large corpus
        ↓                      output: candidates, ranked. Not evidence.
candidate anchor               a proposed pointer into a specific source version
        ↓                      output: a hypothesis to be tested
exact source locator           byte offsets · page + bbox · sheet + range · time interval · JSON Pointer
        ↓                      output: a resolvable, inspectable location
deterministic checks           exact string, numeric, date, citation resolution, digest match
        ↓                      output: verified / failed. This is where support is decided.
judgment, only if required     paraphrase and entailment, provider named, marked `judged`
        ↓                      output: a reasoned opinion, never a verification
proof record                   typed, dependency-bound, invalidated by Law I
```

The retrieval score exists only in the first row and it never propagates. It is a search ranking. It does not appear in the proof record, in the bundle, or in any rendered output as a measure of support.

**Right:**

```
candidate  c0002  →  needs_assessment.txt @ bytes 4102–4260   (retrieval rank 1 of 8)
  status: unverified. Retrieval proposed this passage; nothing has checked it.
  next:   `wi anchor` to bind, then `wi verify` to compare.
```

**Wrong:**

```
c0002 — supported (similarity 0.94)
```

The second line asserts support on the strength of a distance measurement, and prints a number with two decimal places to say so. It would report `supported` for 11,800 against a claim of 12,400 — the exact fixture this project ships to prove the point.

### No blockchain

**Not the core problem.**

A distributed ledger cannot tell you whether the source supports the claim. It cannot tell you whether a rewrite changed the meaning. It cannot tell you whether the author approved the change. It cannot tell you whether an anchor points at the right region of the right page. It cannot tell you whether a source is stale.

It timestamps a digest. That is a real and narrow service, and this system already produces the digests it would timestamp.

**Why it is load-bearing.** Every hard problem in accountable authorship is a *semantic* problem — meaning, support, invalidation, human decision, realm. Ledger technology addresses ordering and tamper-evidence, which are the parts that were already tractable with a hash and a signature. Adopting it as the core would import a network dependency, a cost model and an operational surface into a system whose central promise is that it runs offline on one file, and would buy none of the guarantees anybody actually wanted.

There is a narrower version of the request that is reasonable: *prove this bundle existed before that date.* That is a timestamping need, it is real, and the answer is that a `.wiab` digest is an ordinary hash — any timestamping authority, notary, ledger or witness an organization already trusts can attest to it, without the core knowing or caring which. The seam is deliberate. Attestation is somebody else's business and should be replaceable in an afternoon.

If an organization wants external timestamping or anchoring of bundle digests, that is optional infrastructure they can layer on top. It is not in the core, it is not required for any constitutional guarantee, and it will not be described anywhere in this project as verification. Tamper-evidence answers *was this changed*. This project answers *is this supported*, and those are not the same question — a perfectly preserved record of an unsupported claim is still an unsupported claim.

### No public transparency log by default

**Opt-in only.**

v5 does not publish document digests, signer identities, decision records or bundle metadata to any shared or public log unless a project explicitly turns it on.

**Why it is load-bearing.** A digest looks like it reveals nothing and frequently reveals a great deal. Publishing the hash of a document proves possession of that exact document at that time — useful when you want it, disclosive when you do not. Timing alone leaks: a stream of decision records shows when an organization was working on something, how fast, how many revisions, and when it stopped. Signer identities map a team. For a sealed bid, an unannounced filing, an investigation with a confidential source, or privileged work, that metadata is the sensitive part and the content was never the exposure.

Transparency logs solve a real problem — third-party auditability of what was claimed when — and organizations that need it should have it. It has to be a decision someone makes, with the exposure explained, not a default they discover.

### No autonomous source approval

**A discovered source is `candidate`, never `approved`, until a human approves it under project policy.**

Retrieval, crawling, import and adapter ingestion all produce candidates. Approval is a decision record under Law J with a `human`, `team_member` or `authorized_editor` actor attached.

**Why it is load-bearing.** Source selection is the highest-leverage editorial act in the entire pipeline and it is upstream of every guarantee the system makes. Everything below it — anchors, checks, bundles, proofs — verifies *support within the approved set*. Get the set wrong and the machinery faithfully proves a document against bad material, with full cryptographic rigor and a clean bundle. That is the failure mode where the system's strength becomes the danger.

An automated approver would also be an unbounded prompt-injection surface: a hostile document that can get itself approved has defeated Law F by walking through the front door. `automated_policy` may filter, rank, deduplicate and reject. It may not approve.

### No automatic legal or medical adjudication

**v5 does not decide whether something is legally compliant, defamatory, admissible, medically correct, safe, or fit for a clinical purpose.**

It can extract obligations, track definitions, flag unsupported claims, detect changes in legal force under Law H, escalate to `regulated` mode, and require every proceed-anyway to be recorded. Those are inputs to a professional's judgment. They are not the judgment.

**Why it is load-bearing.** These domains attach liability to a licensed human, and the licensing exists because the judgments are contested, jurisdiction-specific, fact-dependent and consequential in ways no document graph can see. A tool that produced a compliance verdict would be doing two harmful things at once: telling a professional something it cannot know, and giving a non-professional a reason not to consult one. The second is the one that hurts people.

The `regulated` evidence mode makes the system *more* conservative in these domains, not more decisive. That direction is deliberate and it does not reverse.

### No claim of invention over prior art

**v5 combines existing ideas. The ideas have names and owners, and they are named here.**

Prior art this project builds on, honestly listed:

| Prior art | What it contributes |
|---|---|
| Provenance graphs (W3C PROV and its lineage) | Entities, activities, agents, and derivation |
| Claim–evidence graphs and argumentation models | Claims bound to supporting evidence |
| Content-addressed storage | Immutable object identity by digest |
| Merkle trees and Merkle lineage | Efficient tamper-evident structure over history |
| Software artifact signing and supply-chain attestation | Signed, verifiable release metadata |
| Content credentials and media provenance standards | Asset-level provenance and edit history |
| Semantic diff, as a general concept | Difference classified by meaning rather than by character |
| Knowledge graphs and ontologies | Entities and relations with stable identity |
| Story bibles and continuity systems | Canon as a maintained, queryable body of fact |
| CI/CD and policy gates | Automated, blocking checks in a pipeline |
| Source control and review workflow | Diff, proposal, review, merge, history |

**What is distinctive about v5** is the combination, stated precisely and without inflation: a local-first authorship compiler in which atomic semantic units, multimodal evidence anchors, author decisions, proof state, canon state and rendered outputs are nodes in *one* dependency graph — so that a semantic edit invalidates only the affected proof closure, and a release carries a machine-verifiable record of source state, human decisions, checks and render lineage.

That is a real claim about architecture and it is worth making. It is not a claim that any component is new.

**Why the refusal is load-bearing.** Overclaiming invention is the same failure this entire project exists to prevent, pointed at itself — an assertion made without checking, in a register that discourages checking. It is also strategically foolish: a claim of novelty over well-documented prior art is trivially rebutted and takes the credible parts down with it.

Stated plainly, without hedging: **the distinctiveness described above is a design claim, not a legal conclusion. It requires real prior-art review by qualified counsel before any patent claim is drafted.** Nothing in this repository constitutes that review, and no sentence here should be quoted as if it were.

---

---

## How to decline without being useless

**Status: specified.**

A refusal that stops at "no" has moved the problem to the author without moving it forward. Every non-goal in this document has a legitimate need behind it, and the need is usually serviceable by something adjacent. The pattern is three moves, in order:

1. **Name the line and why it exists**, in one sentence, without a lecture.
2. **Do the part that is legitimate**, without being asked twice.
3. **Say what would actually solve their problem**, including when the answer is a person rather than a tool.

| Request | What is declined | What is delivered instead |
|---|---|---|
| "Make this pass an AI detector." | The evasion framing | The full craft pass, which is what they wanted; a plain statement that evasion is not the goal |
| "Add a citation for this — anything plausible." | Constructing the reference | `needs_source` on the claim, the exact wording that would need support, and — where search exists — an offer to look |
| "Is this true?" | A truth verdict | What the supplied sources do and do not support, and a clear statement that source quality is a human judgment |
| "Give me one score I can put on the slide." | A blended composite | The counts with their denominators, and the sentence that makes them mean something |
| "Just approve these sources automatically." | Autonomous approval | A ranked, deduplicated `candidate` set ready for one human pass, and the injection scan on all of it |
| "Does this comply?" | Adjudication | Extracted obligations, changes in legal force, unsupported claims, `regulated` mode, and a recommendation to route it to counsel |

**Why the pattern is load-bearing.** A refusal delivered badly gets routed around. The author goes to a tool with no refusals at all, and the line held in this repository protects nobody. The objective is not purity; it is that the person leaves with the legitimate part of their need met and an accurate picture of what nothing can do for them.

---

## What a non-goal is not

A non-goal is not a technical limitation, and the two must never be reported in the same words. A limitation says *not yet*. A refusal says *not ever*, and gives the reason.

| | Limitation | Non-goal |
|---|---|---|
| Example | Paraphrase support is not checked — the judgment tier is unimplemented | Citations will never be constructed |
| Changes with | Time, work, a release | Nothing |
| Correct phrasing | "Not run — no judgment tier on this surface" | "This system does not do that, because —" |
| Where it lives | [`../../ROADMAP.md`](../../ROADMAP.md) and the disclosure block | This document |

Conflating them corrodes both. A limitation described as a refusal is an excuse. A refusal described as a limitation is a promise to cross the line later, and everyone who reads it will plan on that.

---

These are refusals, not unbuilt features. They do not move.

---

Read next:

- [`CONSTITUTION.md`](CONSTITUTION.md) — the laws these refusals protect
- [`RELIABILITY_TYPES.md`](RELIABILITY_TYPES.md) — why a similarity score cannot become a proof score
- [`SURFACES.md`](SURFACES.md) — what each surface may and may not imply
- [`../v4/NON_GOALS.md`](../v4/NON_GOALS.md) — the v4 originals
- [`../../README.md`](../../README.md) — the project
