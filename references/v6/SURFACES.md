# Surfaces

**One core. Many translations. No second implementation of `verified`.**

v4 stated the surface rule as a discipline: never claim a check ran where it could not. v5 turned it into a protocol: a surface declares its capabilities in a machine-readable form and the output is generated from the declaration. v6 adds the part that only becomes necessary when surfaces can *write* — a rule about who may decide, and a rule about what happens when the same write arrives twice.

This document supersedes [`../v5/SURFACES.md`](../v5/SURFACES.md). Every v5 rule is carried forward unamended; nothing below relaxes one.

The doctrine is identical everywhere. What changes is what can actually be done, and — new in v6 — whether a surface may cause a state to move at all. **Detect the surface from the tools available, not by asking.**

---

## Table of contents

1. The single-facade rule
2. The v6 surface matrix
3. The command families
4. One result object, two renderings
5. Capability negotiation at v6
6. Idempotency on mutation-intent endpoints
7. CLI
8. Library and SDK
9. REST
10. MCP
11. WASM and the browser
12. CI
13. Air-gapped review
14. The Workbench
15. The v6 conformance rules
16. Shared across all surfaces
17. What is executable and what is specified

---

## 1. The single-facade rule

**Status: `scripts/wi.py` executable; `wi-core` as a linkable library specified.**

There is one canonical deterministic core. Today it is `scripts/wi.py` — a single stdlib-only Python file. In the v6 program it becomes `wi-core`, a library with a stable facade that the CLI, the REST service, the MCP adapter, the SDK, the WASM build, the Workbench and CI all call. The transport changes. The core does not.

> **CLI, REST, MCP, Workbench, SDK and WASM bindings never reimplement proof. They translate; the core decides.**

**Why this is the load-bearing sentence in the document.** The moment two implementations of `verified` exist, one of them is wrong and nobody knows which. That is not a rhetorical flourish — it is a description of how the failure presents. The second implementation does not disagree loudly on the first test. It agrees on every fixture anyone thought to write, because it was built by reading the first one. It disagrees on the fifth edge case: a combining character that one normalizes and the other does not, a decimal that one rounds at serialization, a date range whose endpoint one treats as inclusive. And it disagrees in the document that mattered, months later, where the two answers are both defensible and neither can be reproduced from the other's inputs.

A single facade is not an architectural preference. It is the only structure in which the sentence *"this claim is verified"* has one meaning across the system.

### 1.1 What a surface may do

The boundary, stated as a list, so that a code review can cite a line:

| A surface **may** | A surface **may not** |
|---|---|
| Parse arguments, bodies, tool calls and forms | Implement a check |
| Authenticate, authorize its own callers, enforce tenancy | Compute a digest by its own rule |
| Batch, paginate, stream, cache by closure digest | Resolve an anchor by its own logic |
| Render a result object as prose, a table, HTML or a badge | Author a proof record it did not receive from the core |
| Translate a `WI_` code into an interface affordance | Infer a verdict from a partial result |
| Refuse a request it cannot route to the core | Approximate a capability it does not have |

The right-hand column is one rule six times: **L10 does not decide proof.** That is the constitutional row in [`CONSTITUTION.md`](CONSTITUTION.md) §6, and this document is its operational form.

### 1.2 The caching line, drawn precisely

Caching is where the rule gets broken by people who are trying to help. The distinction is exact and worth stating once:

- **Permitted.** A cache keyed by a closure digest. The surface asks the core for a verdict over closure `sha256:9f2ac1…`, stores the answer under that key, and returns it for any later request with the same key. The digest changes when anything in the closure changes, so a stale answer is not reachable.
- **Refused.** A cache keyed by a document path, a claim identifier, a node ID or a timestamp. Every one of those keys can stay the same while the closure underneath it moves, which means the cache is now answering a question the core did not answer. That is a second implementation of `verified` wearing a performance justification.

The test: if the cache can ever return an answer the core would not currently give, it is not a cache — it is an engine.

---

## 2. The v6 surface matrix

What each surface can actually do. Read down a column to see what a surface must never imply. Read the two write rows first — they are new, and they are the ones that decide whether a surface is a viewer or a participant.

| | CLI | Library | REST | MCP | Workbench | WASM · browser | CI | Air-gapped |
|---|---|---|---|---|---|---|---|---|
| Filesystem | yes | host-dependent | server-side | adapter-dependent | via core | **no** | yes | yes |
| Workspace mode | `authoritative` | `authoritative` | `authoritative` | `authoritative` | `authoritative` | `capsule` | `authoritative` | `capsule` |
| Deterministic checks | yes | yes | via core | via core | via core | from capsule | yes | from capsule |
| Semantic diff · impact · simulate | yes | yes | specified | specified | specified | **no** | yes | no |
| **May propose** | yes | yes | specified | specified | specified | **no** | no | no |
| **May decide** | yes, with a grant | yes, with a grant | specified | specified | specified | **never** | **never** | **never** |
| Branch · commit · merge | yes | yes | specified | specified | specified | no | commit only | no |
| Authority issue · delegate | yes | yes | specified | specified | specified | no | **no** | no |
| Capsule create · verify | create and verify | create and verify | specified | specified | specified | **verify only** | verify | verify |
| Judgment tier | no | no | no | no | no | no | no | no |
| Signing | no | no | no | no | no | no | no | no |
| Federation transport | no | no | no | no | no | no | no | no |
| Network | optional | host-dependent | yes | adapter-dependent | yes | page origin only | optional | **never** |

Four rows are uniform, and each is uniform for a reason worth reading rather than skipping. **Judgment** is `no` everywhere because no judgment provider is implemented anywhere; a surface that reads its own blank as a local gap will eventually try to fill it. **Signing** is `no` everywhere because `local_sha256` is a digest and calling it a signature is the misstatement [`SECURITY_MODEL.md`](SECURITY_MODEL.md) §4 exists to prevent. **Federation transport** is `no` everywhere because `wi capsule` produces and verifies a portable closure on a local filesystem and nothing moves one between organizations. **May decide** is `never` in three columns because a decision requires a named human actor holding a live grant, and a browser page, a build runner and a review machine each lack one — see §12 and §13.

---

## 3. The command families

**Status: the v6 and v5 commands below are executable in `scripts/wi.py` at v6.0; every reserved name is specified.**

The CLI is the reference surface. Every other surface's operation set is a subset of this table, expressed in that surface's own idiom. A surface that offers an operation with no row here is offering something the core does not do.

### 3.1 v6 commands

| Command | Family | What it does |
|---|---|---|
| `wi canon` | state | Canonical JSON and a domain-separated state digest for a state document |
| `wi branch` | version control | `create`, `list`, `switch`, `delete` — named movable pointers into the immutable object store |
| `wi commit` | version control | A semantic commit: graph root, delta, actor, optional decision reference |
| `wi log` | version control | Semantic commit history |
| `wi propose` | proposal | A proposal bound to an exact target state digest |
| `wi proposals` | proposal | Proposals and their status |
| `wi simulate` | proposal | A counterfactual report — candidate root, semantic deltas, stale frontier, provably-unaffected count, conflicts, repair plan. Mutates nothing. |
| `wi decide` | decision | An authorized decision; refuses on a stale target binding |
| `wi merge` | merge | Conflict-preserving semantic three-way merge |
| `wi conflicts` | merge | Unresolved semantic conflicts |
| `wi authority` | authority | `issue`, `delegate`, `revoke`, `check` — capability grants |
| `wi obligations` | proof | Proof obligations derived from typed state, release target and policy |
| `wi as-of` | temporal | Bitemporal query by `--valid-at` and `--known-at` |
| `wi constraints` | proof | The graph constraint engine, C001 through C020 |
| `wi capsule` | portability | `create`, `inspect`, `verify` — Merkle closure, selective disclosure, inclusion proofs |
| `wi why` | explanation | Explain a node backward to its basis |

### 3.2 v5 commands, carried forward unchanged

`preserve` · `scan-sources` · `extract-claims` · `verify` · `gate` · `init` · `ingest` · `atomize` · `anchor` · `graph` · `impact` · `diff` · `test` · `explain` · `bundle` · `verify-release` · `doctor`

Their behaviour is unchanged and their governing documents are indexed in [`../v5/README.md`](../v5/README.md).

### 3.3 Reserved names — specified, and not implemented

These names are reserved so that nothing else claims them, and so that a reader who types one gets a refusal rather than a surprise. Every one is a `**Status: specified.**` mechanism elsewhere in this reference set.

| Reserved | Would do | Governed by |
|---|---|---|
| `wi remote` | Add, list and remove federation remotes | [`FEDERATION.md`](FEDERATION.md) |
| `wi fetch` · `wi push` | Move capsules between workspaces | [`FEDERATION.md`](FEDERATION.md) |
| `wi sign` · `wi attest` | Cryptographic signing of a release manifest | [`SECURITY_MODEL.md`](SECURITY_MODEL.md) §4 |
| `wi pack` | Install, pin and audit packs | [`PACKAGE_SYSTEM.md`](PACKAGE_SYSTEM.md) |
| `wi agent` | Run a bounded autonomous objective | [`AUTONOMOUS_EXECUTION.md`](AUTONOMOUS_EXECUTION.md) |
| `wi judge` | Invoke a named judgment provider | [`../v5/JUDGMENT_TIER.md`](../v5/JUDGMENT_TIER.md) |
| `wi build` | Compile a graph root to a target format | [`COMPILER_MODEL.md`](COMPILER_MODEL.md) |
| `wi watch` | Continuous rebuild on source change | [`BUILD_MANIFEST.md`](BUILD_MANIFEST.md) |
| `wi migrate` | v5 to v6 state migration | [`MIGRATION_V5_TO_V6.md`](MIGRATION_V5_TO_V6.md) |

**Why reserving is worth the trouble.** An unreserved name is a name a pack, a wrapper or a well-meaning script will take. When the real implementation arrives it either collides or gets a worse name, and in the meantime a user who runs `wi sign` gets whatever the squatter does — which, for that particular verb, is the worst possible outcome. A reserved name returns `WI_CAPABILITY_UNAVAILABLE` and says where the specification lives.

---

## 4. One result object, two renderings

**Status: `--json` executable on the v5 commands that carry it; universal `--json` specified.**

Every command that prints prose must be able to print the same result as JSON, and **both must be derived from one result object.** Not two code paths that agree. One object, rendered twice.

```
core computes  →  ResultObject  →  render_text()  →  terminal
                              ↘  render_json()  →  stdout, pipe, service, test
```

The shape is uniform across commands:

```json
{
  "wi": "6.0.0",
  "command": "simulate",
  "status": "ok",
  "workspace_mode": "authoritative",
  "state": { "target_digest": "sha256:71b4e8…", "candidate_root": "sha256:c31f07…" },
  "result": { },
  "disclosure": {
    "ran_deterministic": ["quotation", "numeric", "date", "citation.resolution"],
    "ran_judgment": [],
    "unavailable_on_surface": ["anchor.pdf_region"],
    "disabled_by_policy": ["source.fetch"],
    "invalidated_by_edit": ["c0004", "c0009"]
  },
  "codes": []
}
```

**Why one object rather than two renderers that agree.** Two renderers agree until one of them is edited. The prose renderer is edited far more often, because prose is where readability complaints land, and the edit that adds a helpful summary line is the edit that puts a number on the screen which is in no field of the JSON. From that point the terminal and the pipeline disagree, and the disagreement is invisible: nobody diffs a human-readable report against a machine-readable one. Deriving both from one object makes the divergence unrepresentable rather than unlikely.

**Three rules the shape enforces.**

1. **The disclosure block is a field, not a formatting decision.** It is present on every result, with all five states, and empty states are stated as empty rather than omitted. The reasoning is in [`RELIABILITY_RENDERING.md`](RELIABILITY_RENDERING.md) §4 and the vocabulary is fixed by Law C.
2. **`codes` is an array, always present.** A successful result carries `[]`. A surface that omits the array on success and adds it on failure has made the failure path structurally different, which is the path that gets less testing.
3. **`workspace_mode` travels with the result.** A result object read out of context — pasted into a ticket, stored in a build artifact, forwarded by an agent — still says what kind of workspace produced it. A capsule-mode result that later reads as an authoritative one is exactly the confusion §11 exists to prevent.

**The prose rendering is not a summary.** It renders every field the JSON carries, in a different arrangement. If a field is worth omitting from prose it is worth omitting from the result object, and that is a design decision to be argued rather than a formatting one to be made per command.

---

## 5. Capability negotiation at v6

**Status: `wi doctor` executable in `scripts/wi.py`; the v6 wire format below is specified.**

v5 negotiated capability. v6 negotiates capability *and mode*, because a surface can now be fully capable and still forbidden to write.

```json
{
  "core_version": "6.0.0",
  "workspace_mode": "authoritative",
  "capabilities": {
    "filesystem": true,
    "workspace": true,
    "binary_ingest": ["text"],
    "judgment": [],
    "signing": [],
    "network": ["none"],
    "propose": true,
    "decide": true,
    "authority": ["issue", "delegate", "revoke", "check"],
    "merge": true,
    "temporal": ["valid_at", "known_at"],
    "constraints": ["C001-C020"],
    "capsule": ["create", "inspect", "verify"],
    "federation": [],
    "compile_targets": ["markdown", "html"],
    "packs": []
  }
}
```

| Field | Means |
|---|---|
| `core_version` | The version of the canonical deterministic core reachable from here |
| `workspace_mode` | `authoritative` · `read_only` · `capsule` · `none` — see below |
| `binary_ingest` | Which source formats have a decoder here. `["text"]` means text only |
| `judgment` | Which judgment providers are configured. `[]` everywhere today |
| `signing` | Which signing methods are available. `[]` everywhere today; `local_sha256` is a digest, not a signature |
| `network` | Which effects are permitted, from the closed vocabulary in [`SECURITY_MODEL.md`](SECURITY_MODEL.md) §5. `["none"]` is default-deny |
| `propose` · `decide` | Whether the surface can emit a proposal, and whether it can carry a decision to the core |
| `authority` | Which grant operations are reachable |
| `capsule` | Which capsule operations are reachable. Note that `verify` without `create` is a complete and honest profile |
| `federation` | `[]` everywhere today |
| `compile_targets` | Which renderers exist here. `["markdown", "html"]` everywhere today |

### 5.1 The four workspace modes

| Mode | Holds | May commit | Typical surface |
|---|---|---|---|
| `authoritative` | A `.wi/` workspace with an object store and an index | yes, with a grant | CLI, Workbench, REST server, CI |
| `read_only` | A workspace mounted without write access | no | a dashboard, a reviewer's checkout, a read replica |
| `capsule` | A portable proof closure and nothing else | no | air-gapped review, the browser build |
| `none` | No state at all | no | a chat with no filesystem |

**Why mode is separate from capability.** A read-only mount is fully capable of running every deterministic check and completely unable to move a state. Collapsing the two into a single boolean forces a choice between advertising checks it can run and hiding writes it cannot do, and both answers are wrong. Two fields say the true thing: *this surface can compute everything and change nothing.*

### 5.2 The rule that makes negotiation worth doing

> **A missing capability never becomes guessed output.**

Concretely, and these are the three that get violated:

- **If signing is unavailable, do not expose a signing tool.** Not a tool that returns an error, and certainly not one that returns a digest and calls it a signature. The tool is absent from the surface's advertised set, so a caller enumerating capabilities never sees it and never builds a flow around it. `signing: []` is the whole answer.
- **If PDF decoding is unavailable, do not degrade a PDF to remembered text.** The temptation is real: a model has read the PDF, the text is in context, and producing an anchor against that text feels like recovering gracefully. It produces an anchor that resolves against nothing — a byte range into a document the core never opened. The correct output is `unavailable_on_surface` for those claims, and a sentence telling the reader which surface can decode it.
- **If a judgment provider is absent, do not substitute reading.** Careful reading is genuinely valuable and it is not a `judged` record. It has no provider name, no prompt hash, no input digests and nothing to contest. Say what it is.

The pattern joining all three: each degradation makes the output *look complete* while removing the reader's ability to tell that it is not. That is the direction of every failure this project exists to stop, and a capability block is the mechanism that turns "remember not to" into "the output is generated from a declaration that says no."

---

## 6. Idempotency on mutation-intent endpoints

**Status: specified.**

A CLI invocation happens once. A network request may happen twice — a retry after a timeout, a proxy replay, an agent that lost its connection and reconnected, a user who clicked twice. In v5 that was a nuisance. In v6, where a request can commit, decide, merge or issue a grant, a duplicate is a second authoritative state transition that nobody intended.

**Every mutation-intent endpoint requires an idempotency key.**

| Operation | Requires a key | Why |
|---|---|---|
| `propose` | yes | A duplicated proposal splits review attention across two identical items |
| `decide` | yes | A duplicated decision is a second decision record with no second decision behind it |
| `commit` | yes | A duplicated commit produces two roots for one intent, and the log stops meaning what it says |
| `merge` | yes | A duplicated merge can resolve a conflict twice, differently |
| `authority issue` · `delegate` · `revoke` | yes | A duplicated grant is a grant nobody issued once |
| `capsule create` | yes | Cheap to duplicate, and two capsules for one closure invite a substitution |
| `canon` · `simulate` · `log` · `as-of` · `why` · `conflicts` · `proposals` · `constraints` · `obligations` · `capsule inspect` · `capsule verify` | no | Read-only. Mutate nothing, so a repeat is a repeat |

### 6.1 The rule

The key is supplied by the client and is bound to the canonical digest of the request body.

- **Same key, same body digest** → the original result object is returned, unchanged, with `"replayed": true`. The core is not called a second time.
- **Same key, different body digest** → refused with `WI_IDEMPOTENCY_CONFLICT`, and the response names the digest the key is already bound to. This is a surface-layer code: it exists at L10 and the core never sees it, because the core never sees the duplicate.
- **No key on a mutation-intent endpoint** → refused with `WI_INPUT_INVALID`. Not accepted-with-a-warning. A mutation with no key is a mutation that cannot be retried safely, and the caller will retry it anyway.

### 6.2 Why the key binds to the body rather than to the operation

A key bound only to the operation name lets a client reuse a key across genuinely different requests, which turns idempotency into a silent drop: the second, *different* decision returns the first one's result and the caller believes it succeeded. Binding to the body digest makes that case an explicit refusal instead. The client learns that it reused a key; it does not learn later that a decision it made was discarded.

### 6.3 What idempotency does not do

It does not replace the target-state binding. A proposal carries the target state digest, a decision carries it, and a stale binding is refused with `WI_PROPOSAL_STALE` or `WI_DECISION_STALE` regardless of the idempotency key. The two mechanisms answer different questions: the key asks *have I already done this?*, and the binding asks *is this still the thing I was deciding about?* A surface that treats one as covering the other has removed a check nobody will notice is gone until the state it applied to had moved.

---

## 7. CLI

**Status: the command set in §3.1 and §3.2 executable in `scripts/wi.py` at v6.0.**

The reference surface, and the one every other surface is defined against.

```bash
python3 scripts/wi.py branch create review/q3
python3 scripts/wi.py propose --target sha256:71b4e8… --delta delta.json
python3 scripts/wi.py simulate --proposal p0007 --json
python3 scripts/wi.py decide --proposal p0007 --grant g0002 --reason "figures re-checked against the filed return"
python3 scripts/wi.py commit --message "Q3 revision" --decision d0011
python3 scripts/wi.py obligations --target release/regulated
python3 scripts/wi.py capsule create --out review.wicap --profile redacted
```

**What it must never imply.** That a compiled core is doing the work. There is no Rust, no WASM, no daemon and no single-binary distribution; the canonical core is a Python file, and Law K says so out loud precisely so no surface quietly implies otherwise. Also: the presence of a workspace does not create a judgment tier, a signing capability or a federation transport. `judgment: []`, `signing: []` and `federation: []` are true in a terminal too.

**Behaviour carried from v5, unamended.** Preserve the original before touching anything. Never edit the author's file in place unless in-place editing was explicitly asked for. Run the script rather than eyeballing the checks. Check `git status` first and say so if the tree is dirty. Put `wi doctor` output in the report verbatim rather than summarized, because a summarized capability report is one the reader cannot check.

**New in v6: say which branch and which grant.** A CLI session that commits without naming the branch it is on, and decides without naming the grant it used, produces a log entry that is correct and unreadable six months later. Both are in the result object; print them.

---

## 8. Library and SDK

**Status: specified.**

`wi-core` as a linkable library, plus thin language bindings. The bindings are where getting the facade rule right matters most, because a binding that exposes a check function directly is an invitation to call it out of context.

Three binding rules:

1. **Expose operations, not internals.** A binding surfaces `simulate`, `decide`, `commit`. It does not surface `normalize_decimal`, `resolve_span` or `hash_node`. An exposed internal is a partial reimplementation waiting for a caller who needs *almost* that behaviour.
2. **Return the result object, not a boolean.** A binding whose `verify()` returns `true` has thrown away the disclosure block, the codes and the closure digest — everything that makes the answer checkable. The boolean is the one shape guaranteed to be misused.
3. **Errors are `WI_` codes on a structured error type.** Not exceptions with prose messages. A prose error message is not an interface, and every binding that has one eventually grows string matching on it in a caller.

---

## 9. REST

**Status: `services/api/` is the v3 craft runtime, executable. v6 endpoints are specified.**

`services/api/` is a containerized reference runtime for the v3 craft kernel — compile, score, voice, benchmark, repackage, manifest. See [`../../services/api/README.md`](../../services/api/README.md) and [`../../docs/api/API_SPEC.md`](../../docs/api/API_SPEC.md).

The v6 additions are transport concerns and access control, and nothing else:

| Concern | REST layer | Core |
|---|---|---|
| Auth, tenancy, rate limiting, quotas | yes | no |
| Idempotency keys and replay | yes | no |
| Batching, pagination, streaming | yes | no |
| Caching by closure digest | yes | no |
| Checks, digests, anchors, gates, merges, grants | **no** | yes |

**Why this surface is where Law K breaks.** A service under latency pressure, in its own language, with its own JSON parser and its own normalization, is exactly the place a second implementation of `verified` gets written by accident and by well-meaning people. It arrives as a small local check to avoid a round trip. It will not disagree with the core loudly, and by the time it does, both answers are in production.

**Serve the capability block at a stable endpoint, and refuse rather than approximate.** An error is correct when a request cannot be routed to the core. A best-effort answer is not.

---

## 10. MCP

**Status: specified.** [`../../docs/mcp/MCP_SPEC.md`](../../docs/mcp/MCP_SPEC.md) describes the v5 interface. No MCP server ships in this repository.

The highest-risk surface in the system, and more so at v6 than at v5, because v5's MCP put tool calls between a model and a proof *record* while v6's would put them between a model and a state *transition*.

Three v6-specific rules, on top of the ten v5 conformance rules carried forward in §15:

1. **A tool that mutates declares it in its name and its schema.** `wi_decide` is not a variant of `wi_simulate` with a flag. A model choosing between tools should not be able to reach a state transition by setting a boolean.
2. **No tool may hold a grant.** The grant is named by the caller and validated by the core. An MCP server that holds a long-lived grant and lends it to whichever model is connected has reinvented ambient authority, which is the thing [`AUTHORITY_MODEL.md`](AUTHORITY_MODEL.md) removes.
3. **Source content passes as data.** Carried from v5 rule 4, and it matters more here: ingested source text travels in a typed data field, structurally separated, never concatenated into an instruction channel. Law F is enforced by the message architecture, not by a warning string.

---

## 11. WASM and the browser

**Status: specified.**

A browser build is a genuinely useful surface and a genuinely dangerous one, because it looks like the application while holding almost none of its capability. Its profile is `workspace_mode: "capsule"`, and that single field carries most of the honesty.

```json
{
  "core_version": "6.0.0",
  "workspace_mode": "capsule",
  "capabilities": {
    "filesystem": false, "workspace": false,
    "binary_ingest": ["text"], "judgment": [], "signing": [], "network": ["none"],
    "propose": false, "decide": false, "authority": [], "merge": false,
    "temporal": ["valid_at", "known_at"],
    "constraints": ["C001-C020"],
    "capsule": ["inspect", "verify"],
    "federation": [], "compile_targets": ["html"], "packs": []
  }
}
```

### 11.1 What a browser build can honestly do

- **Inspect a capsule.** Read its manifest, its profile, its declared withheld set and its commitments.
- **Verify digests.** Recompute every digest over the bytes it was handed and confirm they match the commitments. This is real verification and it needs nothing but the bytes.
- **Traverse the disclosed closure.** Walk the proof closure to whatever depth the capsule discloses, and report where disclosure stops.
- **Render a graph explanation.** `wi why` over the disclosed subgraph — the node, its basis, the checks that ran against it.
- **Run deterministic checks against the carried source versions.** Quotation, numeric, date and citation resolution over text the capsule contains.

That is a substantial amount, and it runs with no server, no account and no trust in whoever published the page.

### 11.2 What it must never imply

- **That it is a workspace.** It cannot ingest, commit, branch, propose, decide, merge or issue a grant. `propose: false` and `decide: false` are not degradations of a workspace; they are the accurate description of a viewer.
- **That an absent leaf is an absent fact.** A redacted capsule proves less and says so. The browser's job is to render *"withheld under profile `redacted`"* — never to omit the row, and never to render it as a failure. See [`RELIABILITY_RENDERING.md`](RELIABILITY_RENDERING.md) §3.
- **That verifying the capsule verified the sources.** The same refusal as air-gapped review in §13, and it is easier to blur in a browser because the page can be styled to look like an authority.
- **That a check it could not run is a check that failed.** The five disclosure states exist here too, and `unavailable_on_surface` is the honest one for a PDF-region anchor in a page with no decoder.

### 11.3 The one structural rule

The WASM build is the same core compiled to a different target — not a reimplementation in a browser-friendly language. If it ever becomes a separate implementation, §1 applies and the browser is the worst possible place for the second implementation to live, because it is the surface whose output is most often screenshotted and least often reproduced.

---

## 12. CI

**Status: the v5 and v6 CLI commands are executable in CI; gates on v6 state are specified.**

Available: the deterministic core, no human, no prompts, no interactive repair.

```bash
python3 scripts/wi.py constraints --exit-code
python3 scripts/wi.py obligations --target release/standard --json
python3 scripts/wi.py gate claims.json --mode strict --exit-code   # 0 RELEASE · 1 HOLD · 2 BLOCK
python3 scripts/wi.py verify-release release.wiab
```

**CI may commit. CI may never decide.** This is the v6 sharpening of v5's rule that a gate result is not an approval. A pipeline can compute state, run checks, produce a candidate and record a commit under an `automated_policy` actor. It cannot produce a `human-declared` record, approve a source, accept a proposal, resolve a conflict or issue a grant — all of which require a named human actor under Law J and the actor model, and no pipeline has one.

A green build means the deterministic tier found nothing blocking. It does not mean anybody read it, and a CI surface that prints "approved" has said something no runner is able to say.

**Print the disclosure block on failure, and name the repair.** CI output is read fast and usually only at the failure line. A gate that says "unsupported claim" and stops has moved the problem to the author without moving it forward: attach a source · qualify the claim · cut the claim · proceed with a stated caveat, and say which is cheapest.

---

## 13. Air-gapped review

**Status: `verify-release` executable in `scripts/wi.py`; `capsule verify` executable at v6.0.**

Available: one file and a Python interpreter. Nothing else, by design.

```bash
python3 wi.py --offline verify-release release.wiab
python3 wi.py --offline capsule verify review.wicap
```

This is the surface the whole design is aimed at — the reviewer who was not in the room, does not trust the author's toolchain, and cannot install anything.

**What it must never imply.** That verification of the capsule is verification of the sources. `capsule verify` confirms internal consistency: the digests match, the Merkle commitments cover what the capsule carries, the anchors resolve into the carried source versions, the recorded checks correspond to the recorded results, the decision records bind to the states they claim, and the withheld set is declared rather than merely absent. It says nothing about whether the sources are correct. That refusal is permanent — see [`NON_GOALS.md`](NON_GOALS.md).

State the scope in the output itself, so a printed page carries it:

> Capsule internally consistent under profile `redacted`. 14 anchors resolved, 11 deterministic checks reproduced, 6 decision records bound to their target states, 3 leaves withheld and declared. This confirms the record is intact and untampered. It does not confirm the sources are correct.

---

## 14. The Workbench

**Status: specified.** No Workbench ships in this repository.

The Workbench is a **graph instrument**, not an AI editor. That distinction is the whole design and it decides every screen.

An AI editor is organized around a text buffer and a conversation: you type, a model answers, the document changes. A graph instrument is organized around a state and its consequences: you look at what is there, what it depends on, what changed, what that broke, and what you are being asked to decide. The text buffer is one view among twelve, and the conversation is an input method rather than the surface.

**The decision surface is primary and the chat box is secondary.** Not a layout preference — a structural one. A chat box that occupies the centre of the screen makes conversation the default action and decisions an interruption, and a system whose Law J artifacts are interruptions will produce decision records that nobody read carefully. The Proposal Queue and the Decision Room are the centre. The chat box is a way to *draft* a proposal, and a proposal is not a state.

### 14.1 The twelve views

| # | View | Shows | Backed by |
|---|---|---|---|
| 1 | **Source Vault** | Sources, versions, digests, quarantine state, rights and consent | [`../v5/WORKSPACE.md`](../v5/WORKSPACE.md), [`../v5/RIGHTS_AND_CONSENT.md`](../v5/RIGHTS_AND_CONSENT.md) |
| 2 | **Author Canvas** | The text, with the proof margin beside every claim | [`RELIABILITY_RENDERING.md`](RELIABILITY_RENDERING.md) |
| 3 | **Proof Inspector** | One claim: its atoms, anchors, checks, verdicts and closure | [`../v5/EVIDENCE_ANCHORS.md`](../v5/EVIDENCE_ANCHORS.md) |
| 4 | **Meaning Diff** | What a rewrite did to meaning, not to bytes | [`SEMANTIC_IR.md`](SEMANTIC_IR.md), [`../v5/SEMANTIC_DIFF.md`](../v5/SEMANTIC_DIFF.md) |
| 5 | **Impact View** | The stale frontier and the minimum repair set | [`../v5/STALENESS.md`](../v5/STALENESS.md) |
| 6 | **Branch Graph** | Branches, commits, graph roots, deltas | [`SEMANTIC_VERSION_CONTROL.md`](SEMANTIC_VERSION_CONTROL.md) |
| 7 | **Proposal Queue** | Open proposals, each with its simulation report | [`COUNTERFACTUAL_SIMULATION.md`](COUNTERFACTUAL_SIMULATION.md) |
| 8 | **Decision Room** | Conflicts, the two sides preserved, and the decision being made | [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) |
| 9 | **Authority Ledger** | Grants, delegation chains, scope, expiry, revocations | [`AUTHORITY_MODEL.md`](AUTHORITY_MODEL.md) |
| 10 | **Timeline** | Bitemporal reconstruction — what was believed, and when | [`BITEMPORAL_STATE.md`](BITEMPORAL_STATE.md) |
| 11 | **Obligation Board** | Outstanding proof obligations and constraint results C001–C020 | [`PROOF_OBLIGATIONS.md`](PROOF_OBLIGATIONS.md) |
| 12 | **Release Room** | Gate verdict, closure, capsule creation, disclosure profile | [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md), [`../v5/PROOF_CARRYING_RELEASE.md`](../v5/PROOF_CARRYING_RELEASE.md) |

Capsule creation and federation exchange live inside the Release Room rather than as separate views, because both are release acts: a capsule is what a release looks like when it leaves the building, and a remote is where it goes.

### 14.2 Four rules the Workbench inherits rather than invents

- **It computes nothing.** Every number, verdict, digest and diff on every screen came from the core. The Workbench is L10, and L10 does not decide proof.
- **It renders the disclosure block on every view that shows a verdict.** A UI is where the block is most often dropped for space, and it is where a dropped block does the most damage, because a screen reads as complete.
- **No green badge without a denominator.** A count of verified claims is rendered with the count of claims. See [`RELIABILITY_RENDERING.md`](RELIABILITY_RENDERING.md) §2.
- **A decision screen names the grant.** The person deciding sees which authority they are acting under, its scope and its expiry, before the button. An interface that hides the grant produces decisions whose authority nobody checked at the moment it mattered.

---

## 15. The v6 conformance rules

**Status: specified.**

The ten v5 MCP conformance rules in [`../v5/SURFACES.md`](../v5/SURFACES.md) §9 are carried forward and apply to every v6 surface, not only MCP. v6 adds six. They are numbered 11 through 16 so a conformance report can cite the whole set continuously.

| # | Rule |
|---|---|
| 11 | **Mutation-intent operations carry an idempotency key.** A mutation without one is refused, not accepted-with-a-warning. |
| 12 | **A surface declares its `workspace_mode`, and never writes above it.** A `read_only` or `capsule` surface that offers a write path is a conformance failure even if the write would fail downstream. |
| 13 | **No surface holds a grant on a caller's behalf.** Grants are named by the caller and validated by the core. A surface with a long-lived grant it lends out has recreated ambient authority. |
| 14 | **Prose and JSON derive from one result object.** A field in one and not the other is a conformance failure, testable by rendering both from a fixture and comparing coverage. |
| 15 | **Reserved command names return `WI_CAPABILITY_UNAVAILABLE`.** They are not free for a wrapper to define, and a surface that lets a pack claim `wi sign` has failed. |
| 16 | **A capsule-mode surface never renders a withheld leaf as absent.** Withheld and absent are different facts, and only one of them means the evidence does not exist. |

**Why these are written before the implementations.** Every one is cheap at design time and expensive to retrofit. Rules 11 and 14 are structural — they are properties of the request and response shapes, and shapes are the one thing nobody wants to change after clients exist. Rules 12, 13 and 16 are the three ways a v6 surface silently widens beyond what it was meant to do, and each arrives as a convenience: a viewer that grew an edit button, a server that cached a token, a UI that tidied an empty row away.

---

## 16. Shared across all surfaces

**Say which mode you are in** when it affects the output. *"Capsule mode — I can verify this record and cannot change it"* sets expectations before the reader is surprised by a refusal.

**Never claim a check ran where it could not.** Law C, and it is easiest to violate by habit, by carrying an output shape from one surface into another that cannot back it.

**Emit the disclosure block everywhere.** All five states, with empty states stated as empty. Format and reasoning: [`RELIABILITY_RENDERING.md`](RELIABILITY_RENDERING.md).

**Degrade by dropping capability, never by lowering the standard.** A surface with fewer capabilities does less and says so. It does not do the same work to a weaker standard and use the same words for the result. That is the difference between a system that is honest on its worst surface and one that is honest only on its best.

**A refusal is an output.** `WI_CAPABILITY_UNAVAILABLE`, `WI_AUTHORITY_ABSENT` and `WI_PROPOSAL_STALE` are results the surface must render as clearly as a success, with the repair route from [`CONSTITUTION.md`](CONSTITUTION.md) §8 attached. A refusal an operator cannot act on is a refusal they route around.

---

## 17. What is executable and what is specified

**Status: executable in `scripts/wi.py`.**

| Subject | State |
|---|---|
| The v6 command set in §3.1 and the v5 set in §3.2 | Executable in `scripts/wi.py` at v6.0 |
| `wi doctor` capability reporting | Executable |
| `--json` on the v5 commands that carry it | Executable |
| `verify-release` and `capsule verify`, offline | Executable |
| The v6 capability wire format in §5 | Specified |
| Universal `--json` across every command | Specified |
| Idempotency keys and replay semantics | Specified |
| `wi-core` as a linkable library, and the SDK bindings | Specified |
| The v6 REST endpoints | Specified — `services/api/` is the v3 craft runtime |
| The MCP server | Specified — none ships here |
| The WASM build and the browser profile | Specified |
| The Workbench and its twelve views | Specified |
| Every reserved name in §3.3 | Specified |

The honest summary: **v6 has one surface today.** It is a command-line interface over a stdlib-only Python file, and every architectural rule above exists so that the second surface, whenever it arrives, cannot quietly become a second answer.

---

Read next:

- [`CONSTITUTION.md`](CONSTITUTION.md) — Law K, and the twelve-layer table this document operationalizes
- [`RELIABILITY_RENDERING.md`](RELIABILITY_RENDERING.md) — how a result object becomes a line a reader can check
- [`SECURITY_MODEL.md`](SECURITY_MODEL.md) — the effect vocabulary, and why a surface may not fetch
- [`AUTHORITY_MODEL.md`](AUTHORITY_MODEL.md) — grants, and why no surface holds one
- [`NON_GOALS.md`](NON_GOALS.md) — the permanent refusals
- [`../v5/SURFACES.md`](../v5/SURFACES.md) — the superseded v5 document, whose ten conformance rules remain in force
- [`../../docs/INSTALL.md`](../../docs/INSTALL.md) — every install surface and what each can do

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
