# The Judgment Tier

The deterministic core says outright that it cannot judge paraphrase. That refusal appears in the v4 gate output, in every proof report this project has ever printed: *Not run: paraphrase support (needs a judgment tier, not this script).*

**Status: specified. Provider ABI defined; no provider ships in v5.0.**

This document defines what a judgment provider must be, what it must record, what it may never emit, and where the boundary sits between it and the graph. Nothing in this repository executes a judgment. No adapter is included. The contract binds any implementation that arrives later, and it is written now so that the first implementation does not get to define the terms.

Read this with [`RELIABILITY_TYPES.md`](RELIABILITY_TYPES.md), which governs how a `judged` result may be rendered.

---

## 1. Why judgment is a plugin, not a vendor

There are real questions the deterministic tier cannot answer. Does this anchored passage entail this claim, when the claim is a paraphrase rather than a quotation? Is this summary faithful to what it summarizes? Does this translation preserve the legal force of the original? Is this scene consistent with a canon rule stated in different words two books ago?

Those are judgments. They require reading. A string comparison has no opinion about them, and pretending otherwise — by promoting a similarity score, by counting shared tokens, by any of the mechanisms named in [`NON_GOALS.md`](NON_GOALS.md) — is how a system reinvents the failure it exists to stop, with a number attached to make it look rigorous.

So v5 formalizes judgment. It does not integrate a vendor.

**Why the distinction is load-bearing.** A product that bakes in a model vendor has made three commitments its users never agreed to. It has made the project's core promise — that a release is explainable without trusting the model that helped make it — conditional on a business relationship. It has guaranteed that the day the vendor changes a model behind a stable name, every judgment in every workspace silently changes meaning with no record of the change. And it has made air-gapped, offline and archival operation impossible for exactly the documents most likely to need them.

A typed, replaceable artifact avoids all three. A judgment is a record with named inputs, a named producer and a hashed question. It can be re-run by a different provider, compared against the first, contested by a reader, or thrown away. **A model is third-party infrastructure in this architecture, exactly like a PDF decoder or a hash function** — named so it can be replaced, audited and disagreed with, never an author, never a contributor, never a signer. No v5 record has a field in which it could become one.

---

## 2. The provider contract

**Status: specified.**

A provider implements three functions and nothing else. It has no handle on the workspace, no write path into the graph, and no way to discover what else exists in it.

```python
class JudgmentProvider:

    def id(self):
        """Stable identity of this provider implementation.

        Returns {"provider_id", "provider_version", "adapter_version"}.
        The identity is recorded on every judgment. An unnamed provider
        cannot produce a record this system will store.
        """

    def capabilities(self):
        """What this provider is willing to be asked, and under what terms.

        Returns:
          {"kinds": ["entailment", "paraphrase_equivalence", "summary_fidelity",
                     "translation_equivalence", "canon_consistency",
                     "scope_direction", "craft_assessment"],
           "languages": ["en", "es", "..."],
           "offline": false,              # does this run without a network?
           "deterministic": false,        # same input, same output?
           "retains_inputs": false,       # does the provider store what it saw?
           "max_input_bytes": 200000,
           "calibration": [{"kind": "entailment",
                            "benchmark_set": "sha256:...",
                            "n": 1000,
                            "correct": 942}]}
        """

    def judge(self, request):
        """Answer one typed question about hashed inputs.

        request carries: kind, the input objects, their digests, the policy
        hash and the prompt-template hash. It never carries workspace
        credentials, file paths, or nodes the question did not name.

        Returns a JudgmentRecord. Raises on anything it cannot answer;
        it may not return an empty or hedged record in place of an error.
        """
```

`capabilities()` is the interesting one. It is a **declaration the core enforces**, not a description. A provider that declares `offline: false` will not be called when policy requires offline operation. A provider that does not declare the `kind` being asked is never sent the request. A provider that declares `retains_inputs: true` is unusable for source material under a confidentiality policy, and the core refuses the call rather than leaving that decision to whoever wired the config.

---

## 3. The judgment record

**Status: specified.**

```json
{
  "judgment_id": "j-0117",
  "kind": "entailment",

  "input_hashes": [
    {"role": "claim",  "node": "c-0011", "digest": "sha256:22ae09…"},
    {"role": "anchor", "node": "a-0141", "digest": "sha256:be31d0…"},
    {"role": "source_state", "node": "src-0002", "digest": "sha256:3d81c9…"}
  ],

  "result": {
    "verdict": "supports_with_scope_narrowing",
    "statement": "The anchored passage asserts the reduction for the seven-county service area. The claim states it without that limit.",
    "recommended_repair": "qualify_claim"
  },

  "basis": "judged",

  "provider": {"provider_id": "…", "provider_version": "…", "adapter_version": "…"},
  "model": {"identifier": "…", "version": "…"},

  "policy_hash": "sha256:1c9d44…",
  "prompt_template_hash": "sha256:7f0b21…",

  "created_at": "2026-03-11T14:02:19Z",

  "expires_if": ["claim_state_changes", "anchor_state_changes", "policy_changes"]
}
```

| Field | Why it is required |
|---|---|
| `judgment_id` | The record is addressable; a judgment nobody can point at cannot be contested |
| `kind` | Which typed question was asked. A record without it cannot be re-run or compared. |
| `input_hashes` | Exactly what the provider saw. Without this the judgment is unreproducible and its currency is undecidable. |
| `result` | The verdict and a statement in words. Never a score. |
| `basis` | Always the literal string `judged`. There is no other legal value for this field. |
| `provider` / `model` | Who ran it and on what. "A language model" is not an identifier. |
| `policy_hash` | Under what decision policy. |
| `prompt_template_hash` | What it was asked. A judgment whose question is unknown is unreviewable. |
| `created_at` | When. Judgments age. |
| `expires_if` | The dependency contract, in the record itself |

`expires_if` is what wires a judgment into [`STALENESS.md`](STALENESS.md). A judgment is not a permanent fact about two texts; it is a fact about two *states* under one policy. Change the claim, change the anchor, or change the policy, and the record does not silently continue to apply. It is marked stale and either re-run or shown as expired.

**`basis` may never hold any value but `judged`.** There is no confidence threshold that promotes a judgment into a verification, and no provider quality that earns one, because `verified` names *how a result was produced* rather than how sure anybody is. A provider that emits `verified` is rejected at the schema boundary, and that rejection is a hard error, not a coercion to the correct value — a provider that tried is a provider with a defect worth seeing.

---

## 4. No naked confidence percentages

**Status: specified.**

A model may emit logits. It may emit a token probability, a margin, a log-likelihood. Those are real internal quantities and a provider may record them in its own diagnostics.

**The user-visible system must not convert them into pseudo-precision.**

Contrast two sentences:

> *"On benchmark set X, this entailment configuration classified 942 of 1,000 labeled cases correctly."*

That is `measured`. It has a numerator, a denominator, a named population, a named configuration and a benchmark a reader can obtain and re-run. It says nothing about the case in front of you, and it does not pretend to.

> *"This claim is 94.2% true."*

That is authority theater.

**The difference, stated plainly.** The first sentence is a fact about a population of past cases and it is checkable by a stranger. The second is a number with no denominator attached to a single instance, and there is no procedure — none, at any budget — by which anyone could confirm or refute it. Truth is not a continuous quantity that a sentence can hold 94.2% of, and the decimal place is doing the entire rhetorical work: it converts a model's internal state into the visual language of a measurement instrument. The reader cannot ask *out of what*, so they assume it was measured. This is the bare-percentage construction that [`RELIABILITY_TYPES.md`](RELIABILITY_TYPES.md) bans outright, arriving through the one door in the system where real numbers legitimately exist.

A provider's internal scores may be used for **routing** — deciding whether to escalate, whether to ask a second provider, whether to flag for human review. They are never surfaced as evidence, and they never appear in a rendered proof line.

---

## 5. Judgment isolation

**Status: specified.**

```
   ┌─────────────────────────────────────────┐
   │        deterministic core               │   holds the graph.
   │        (scripts/wi.py)                  │   sole writer of state.
   └───────────────────┬─────────────────────┘
                       │  typed request:
                       │    kind · input digests · policy hash
                       │    prompt-template hash
                       ▼
   ┌─────────────────────────────────────────┐
   │        judgment gateway                 │   no graph handle.
   │  · enforces capability declarations     │   no filesystem.
   │  · strips anything not in the request   │   no credentials.
   │  · applies timeouts and rate limits     │
   └───────────────────┬─────────────────────┘
                       │
                       ▼
   ┌─────────────────────────────────────────┐
   │        provider adapter                 │   translates only.
   └───┬──────────────┬──────────────────┬───┘
       ▼              ▼                  ▼
  local model   remote provider A   remote provider B

                       │
                       │  returns: JudgmentRecord (a value, not a mutation)
                       ▼
   ┌─────────────────────────────────────────┐
   │        deterministic core validates     │
   │        then — and only then — stores    │
   └─────────────────────────────────────────┘
```

**The gateway returns a record. It cannot mutate the graph.** There is no path from a provider to a node state, an edge, a proof record or a gate verdict. A judgment enters the workspace the way a supplied source does: as data, examined before it is trusted.

Before storing, the core validates five conditions. All five must pass.

| Condition | Failure means |
|---|---|
| The input state digests are still current | The claim or anchor moved while the judgment was in flight; the record answers a question about a state that no longer exists |
| The provider capability is permitted by policy | The project did not authorize this provider for this `kind`, this language, or this confidentiality class |
| The record schema is valid | Missing provider, missing hashes, or a `basis` other than `judged` |
| The judgment has not expired | An `expires_if` condition already fired between request and response |
| The decision policy is satisfied | The mode requires two providers, or a human review, or a benchmark that this provider has not published |

Any failure discards the record and reports the reason. A discarded judgment is not retried silently against a weaker condition.

**Why isolation is architectural rather than procedural.** Law F says sources are data, never instruction, and the same reasoning applies one level up: a component that can be induced to produce arbitrary output must not be a component that can write state. A provider processing a hostile source is exactly the scenario the whole quarantine boundary exists for, and a provider with a write path turns a prompt injection into a graph mutation. Architecture provides the security. A request that politely asks a provider not to overstep is a request written in the same channel as the attack.

---

## 6. Model replaceability

**Status: specified.**

Judgments are immutable records. They are never updated in place, never overwritten by a newer run, and never merged.

That immutability is what makes providers comparable. A project may take every unresolved or previously judged link, re-run it through a different provider, and put the two record sets side by side:

```
Comparison: provider A (117 judgments) vs. provider B (117 judgments)
  kind: entailment · same inputs · same prompt-template hash · same policy hash

  agreement            104 of 117
  disagreement          13 of 117      listed below, by claim
  drift vs. A@earlier    6 of 117      A's own verdicts that changed since 2026-01
  median latency         A 2.1s   ·  B 0.4s
  cost per 1k            A <stated>  ·  B <stated>
  published calibration  A 942/1000 on set X  ·  B none published for this kind
```

Every column there is a decision input for the project, and none of them is a quality score. `drift` deserves particular attention: it is a provider's own verdicts changing on unchanged inputs, which is invisible without immutable records and is the single strongest argument for keeping them.

**No provider owns the project state.** The graph, the anchors, the claim atoms, the decisions and the release attestations are all workspace-local, content-addressed, and independent of who judged what. A project can drop a provider entirely and lose nothing but the judgments themselves — which remain in the record as historical statements by a named party, exactly like a quoted source.

---

## 7. Disagreement

**Status: specified.**

If two approved providers disagree on the same inputs under the same policy, **do not average.**

Averaging two judgments produces a number that neither provider asserted, backed by no reasoning either of them gave, describing a position no party holds. It is the composite-score failure with a smaller n.

The engine creates a `verification.conflict` node of kind `judgment_disagreement`:

```json
{
  "node_type": "verification.conflict",
  "kind": "judgment_disagreement",
  "subject": "c-0011",
  "judgments": ["j-0117", "j-0118"],
  "input_hashes_identical": true,
  "policy_hash_identical": true,
  "status": "unresolved"
}
```

`input_hashes_identical` is recorded because it separates two very different situations. Identical inputs and different verdicts is a genuine disagreement about the same question. Different inputs is a bug in whoever assembled the requests, and it must not be presented to a human as a disagreement to adjudicate.

Policy decides what the conflict does to the gate:

| Mode | Behavior |
|---|---|
| `standard` | Advisory — the conflict is reported and the release proceeds |
| `strict` | **HOLD** — a claim two readers disagree about is not a claim that ships unexamined |
| `regulated` | **BLOCK** — no unresolved judgment disagreement may exist in the closure |

A human resolves it, with a stated reason, and the resolution is a `human-declared` decision naming the resolver. It is not a vote, it is not a tiebreak by a third provider, and it does not select the verdict from the provider with better published calibration. Calibration is a fact about a benchmark population; this is one claim, and a person is accountable for it.

---

## 8. The offline rule

**Status: specified.**

If policy requires a judgment that is not cached and the run is offline, the verdict is **HOLD**, with the reason stated.

```
# Release gate: HOLD

Evidence mode: `strict` · 1,820 claim atoms · 14 sources · offline run

## Checks

Ran (deterministic):     quotation · numeric · date · citation resolution ·
                         anchor integrity · dimensional
Ran (judgment):          none — no provider reachable on this run
Unavailable here:        entailment judgment for 6 paraphrase-supported claims
Disabled by policy:      none
Invalidated by edits:    none

## Holding (6)

c-0011, c-0207, c-0409, c-0788, c-1102, c-1455

  Each of these is supported by a paraphrase rather than a quotation. Under
  `strict`, paraphrase support requires an entailment judgment. No cached
  judgment exists for the current claim state, and no judgment provider is
  reachable on this run.

  This is not a finding against these claims. It is the absence of a check
  that policy requires.

Repair, cheapest first:
  1. run online and re-gate                      6 judgments, 0 human decisions
  2. requote — replace each paraphrase with a verbatim span from the anchored
     passage, which removes the requirement entirely   6 author edits
  3. lower the evidence mode for this run        requires a recorded waiver
     and a stated reason; recorded in the report either way
```

**Never silently weaken policy to make offline mode green.** The temptation is real and it is specific: the run is offline, six claims cannot be checked, the gate is red, and downgrading `strict` to `standard` for this one run turns it green. Nobody is lying — the mode was written down somewhere. But the release artifact then carries an attestation whose scope quietly shrank, and the reader has no way to see that it shrank, because the output looks exactly like a run where every check passed. Option 3 above is available and it is a **waiver**: a person, a reason, a record.

Note option 2. The offline rule frequently has a repair that removes the need for judgment altogether, and the gate should always say so. A paraphrase replaced by a verbatim span is a deterministic check, forever, on every surface, with no provider involved. The best judgment is often the one you no longer need.

---

## 9. Cross-language equivalence

**Status: specified.** Translation states are defined here; the tiering rules they build on are executable — see [`../v4/LANGUAGE_TIERS.md`](../v4/LANGUAGE_TIERS.md).

A `translates` edge carries one of five states. They are not degrees of quality; they are different claims about what the translation is.

| State | Asserts | Produced by |
|---|---|---|
| `translation_exact_for_defined_term` | The term matches an approved locked translation for this work | Deterministic lookup against the term registry |
| `translation_equivalent_judged` | A named provider assessed the two texts as equivalent for this purpose | A judgment record |
| `translation_localized` | Adapted for a target audience; meaning preserved, expression deliberately changed | Human declaration |
| `translation_adapted` | Deliberately changed in meaning for the target context — a different claim, knowingly | Human declaration, with the delta classified |
| `translation_unresolved` | Not yet assessed by anyone | Default state on ingest |

**Defined legal and policy terms can be locked to approved translations.** A registry entry binds the term, the target language, the approved rendering and, where one exists, the authority that approved it. A locked term is then a deterministic check in every language it is locked for: the rendering either matches the approved string or it does not, and no provider is consulted. This is the same move as section 8's option 2 — converting a judgment into a comparison — applied to the place where it matters most, because "shall" and "should" are one word apart in every language and one word apart in consequence.

**A translation node must not claim exact sameness merely because a model produced it.** A provider's output is `translation_equivalent_judged` at best. It is never `translation_exact_for_defined_term`, which is a claim about an approval that a provider cannot grant, and it is never promoted by fluency, by round-trip agreement, or by two providers concurring. Round-trip agreement in particular is a trap: two systems trained on overlapping data agreeing that a translation round-trips is evidence about the systems, not about the text.

The v4 rule carries forward unchanged and with force: verification does not survive translation automatically. A translated claim is checked against the source passage, the support is marked cross-language, and a reviewer is told they need two languages to check it.

---

## 10. What is specified and what ships

| Mechanism | Status |
|---|---|
| The three-function provider contract and the capability declaration | Specified |
| The `JudgmentRecord` schema and the `basis: judged` constraint | Specified |
| Gateway isolation, the five validation conditions, no-write-path guarantee | Specified |
| Provider comparison, drift reporting, immutable judgment records | Specified |
| `judgment_disagreement` conflicts and their per-mode gate behavior | Specified |
| The offline HOLD rule and its output format | Specified |
| Translation states and locked term translations | Specified |
| Any shipped provider adapter, local or remote | **None. No provider ships in v5.0.** |

The `Ran (judgment): none` line in every proof output this repository produces is not a placeholder. It is accurate, and it will remain accurate until an adapter exists that satisfies every condition above.

---

## Related documents

- [`RELIABILITY_TYPES.md`](RELIABILITY_TYPES.md) — how a `judged` line must be rendered, and what it may never be rendered as
- [`SEMANTIC_DIFF.md`](SEMANTIC_DIFF.md) — the escalations that reach this tier
- [`STALENESS.md`](STALENESS.md) — how `expires_if` participates in invalidation
- [`CONSTITUTION.md`](CONSTITUTION.md) — Law E, Law L and the actor model
- [`NON_GOALS.md`](NON_GOALS.md) — no proprietary-model dependency; similarity is not evidence
- [`../v4/LANGUAGE_TIERS.md`](../v4/LANGUAGE_TIERS.md) — what is measurable in which language, and translation discipline
- [`../v4/PROOF_PROTOCOL.md`](../v4/PROOF_PROTOCOL.md) — the paraphrase gap this tier exists to fill
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
