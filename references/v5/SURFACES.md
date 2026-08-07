# Surfaces

**Law C as protocol.**

v4 stated the surface rule as a discipline: never claim a check ran where it could not. That worked because there were three surfaces and one script. v5 has a workspace, a graph, a bundle format, an adapter layer and a specified server interface, and a discipline does not survive that. So v5 turns the rule into a protocol: a surface *declares* its capabilities in a machine-readable form, the output is built from the declaration, and a capability that is not declared cannot be implied.

This document supersedes [`../v4/SURFACES.md`](../v4/SURFACES.md). The v4 behavioral guidance for chat, Cowork and Claude Code remains correct and is preserved here with the v5 additions.

The doctrine is identical everywhere. What changes is what can actually be done. **Detect the surface from the tools available, not by asking.**

---

## The matrix

What each surface can actually do. Read down a column to see what a surface must never imply.

| | Chat | Cowork | Terminal agent | CI | REST | MCP | Air-gapped |
|---|---|---|---|---|---|---|---|
| Filesystem | no | yes | yes | yes | server-side | adapter-dependent | yes |
| `.wi/` workspace | no | yes | yes | yes | specified | specified | not required |
| Deterministic checks | **no** | yes | yes | yes | via core only | via core only | from bundle |
| Semantic diff · impact | no | yes | yes | yes | specified | specified | no |
| Bundle build | no | yes | yes | yes | specified | specified | no |
| `verify-release` | no | yes | yes | yes | specified | specified | **yes** |
| Judgment tier | no | no | no | no | no | no | no |
| Human decisions | quotable only | yes | yes | **no** | yes | yes | no |
| Network | no | no | optional | optional | yes | adapter-dependent | **never** |
| Status | executable | executable | executable | executable | v3 craft runtime executable; v5 endpoints specified | specified | executable |

The `judgment` row is uniform because the judgment tier is not implemented anywhere. It is a row rather than a footnote so that no surface reads its own blank as a local gap.

---

## Table of contents

1. Capability negotiation
2. Chat — no filesystem
3. Cowork — filesystem, shell, file delivery
4. Claude Code and any terminal agent — full
5. CI — non-interactive
6. REST service
7. MCP — specified, not implemented
8. Air-gapped review
9. The ten MCP conformance rules
10. Shared across all surfaces

---

## 1. Capability negotiation

**Status: `wi doctor` executable in `scripts/wi.py`; the wire format below is specified.**

Every surface should be able to emit this block, and every output the surface produces should be derivable from it.

```json
{ "core": "5.0.0", "capabilities": { "filesystem": true, "workspace": true, "binary_ingest": ["text"], "judgment": [], "signing": ["local_sha256"], "network": false } }
```

| Field | Means |
|---|---|
| `core` | The version of the canonical deterministic core reachable from here |
| `filesystem` | Files can be read and written |
| `workspace` | A `.wi/` workspace exists or can be created |
| `binary_ingest` | Which source formats have a decoder here. `["text"]` means text only — no PDF, no audio, no images |
| `judgment` | Which judgment providers are configured. `[]` means none, and today it means none anywhere |
| `signing` | Which signing methods are available. `local_sha256` is a digest, not a signature |
| `network` | Whether outbound calls are possible at all |

The two sentences a surface says, built from that block:

**Affirmative:**

> Workspace available on core 5.0.0. Deterministic checks ran against text sources: quotation, numeric, date, citation resolution and anchor resolution. Digests are local SHA-256.

**Honest refusal:**

> No PDF decoder here, so the three PDF-anchored claims were not checked — they are `unavailable_on_surface`, not unsupported. No judgment provider is configured, so paraphrase support was not assessed by anything. Run this in a terminal with the workspace to close both.

**Why negotiation is load-bearing.** A capability block turns Law C from something a writer has to remember into something the output is generated from. It also makes the failure legible to the reader: "unavailable here" tells them their next move is to change surfaces, which "not checked" does not. And it makes the rule testable — a surface that emits a proof record for a capability it did not declare is a bug with a name, not a lapse in judgment.

---

## 2. Chat — no filesystem

**Available:** conversation. Text in, text out. Files may be attached but not written.

```json
{ "core": null, "capabilities": { "filesystem": false, "workspace": false, "binary_ingest": [], "judgment": [], "signing": [], "network": false } }
```

**What it can actually do.** The whole protocol, by reading. Claim extraction, atomization by hand, realm tagging, quotation comparison by eye against pasted text, figure and date matching, injection spotting in pasted sources, proposal-shaped redlines with before/after/why, and a verdict the author can act on. This is real work and it catches real errors. Do it carefully and deliver it inline and compressed.

**What it must never imply.** That anything mechanical happened. There is no core here, `scripts/wi.py` does not exist, no workspace was created, no graph was built, no bundle was produced, and nothing was verified in the sense the word carries in this project. No checkmarks. No `verified`. No file paths. No "I've saved it to."

**What it must say when the capability is missing.** Plainly, once, up front:

> No filesystem on this surface, so no mechanical check ran. I compared the figures and quotations against the text you pasted by reading. Treat that as careful reading, not verification — it does not get the same guarantee, and it will not be the same next week.

**Behavior carried from v4:** keep the original recoverable by keeping it quotable — do not paraphrase the author's input when reflecting it back. On long documents, work in sections and say which section you are on: *"claims 1–12 of an estimated 40; continue?"* Never silently truncate. Lead with the verdict and the blocking items; offer the full table on request. Reach for an artifact only when the deliverable is a standalone document the author will take elsewhere.

**Why this surface is the dangerous one.** It is the surface where the output *shape* of a real verification run is easiest to reproduce and hardest for the reader to distinguish from one. The violation almost never comes from intent; it comes from habit, from carrying a terminal-shaped output into a room with no terminal in it.

---

## 3. Cowork — filesystem, shell, file delivery

**Available:** files, shell, multi-step work, persistence across a session, delivering files to the user.

```json
{ "core": "5.0.0", "capabilities": { "filesystem": true, "workspace": true, "binary_ingest": ["text"], "judgment": [], "signing": ["local_sha256"], "network": false } }
```

**What it can actually do.** Everything the deterministic core does. Workspaces are real here and so are bundles.

```bash
python3 scripts/wi.py init                       # .wi/ workspace: SQLite index + object store
python3 scripts/wi.py ingest sources/            # content-address, with source versions
python3 scripts/wi.py scan-sources sources/      # Law F quarantine scan
python3 scripts/wi.py atomize draft.md           # claim atoms
python3 scripts/wi.py anchor                     # bind atoms to evidence anchors
python3 scripts/wi.py verify                     # deterministic checks
python3 scripts/wi.py graph --export graph.json  # nodes, edges, state digests
python3 scripts/wi.py gate --mode strict         # verdict
python3 scripts/wi.py bundle --out release.wiab  # proof-carrying bundle
```

**Behavior carried from v4:** preserve the original before touching anything — `wi preserve draft.md`. This is Law B and on a filesystem there is no excuse for a lost original. Never edit the author's file in place unless they explicitly asked for in-place editing; write proposals to a separate file and let them apply. Run the script rather than eyeballing the checks — it does not get tired on page 40 and its output is reproducible next week. Checkpoint on long documents rather than holding a 40-page analysis in flight.

**What it must never imply.** That a `.wiab` was checked by anything other than the local core, that binary sources were decoded when `binary_ingest` says `["text"]`, or that `local_sha256` is a signature. A digest proves integrity against accident and detects tampering by anyone who does not also control the digest. It does not prove identity. Say "digest," not "signed."

**What it must say when a capability is missing.** Deliver the bundle as a file and name what it does and does not carry:

> `release.wiab` — verify it anywhere with `python3 wi.py verify-release release.wiab`, offline, no model needed. It carries source digests, anchors, deterministic check results and decision records. It is digest-sealed, not cryptographically signed, and it contains no judgment records because none were produced.

---

## 4. Claude Code and any terminal agent — full

**Available:** everything Cowork has, plus version control, CI wiring and long-running work.

**What it can actually do.** The full v5 loop, including the parts that only pay off across time:

```bash
python3 scripts/wi.py impact --source needs_assessment.txt   # minimum repair frontier
python3 scripts/wi.py diff --semantic draft.v3.md draft.v4.md
python3 scripts/wi.py explain "median wait times fell by 38%"  # atoms, anchors, checks, dependents
python3 scripts/wi.py test                                     # writing tests, concept contracts
python3 scripts/wi.py doctor                                   # capability report
```

**Behavior carried from v4:** git is the immutability mechanism — commit the original before editing, which satisfies Law B better than a `.original` copy and which the author already trusts. Check `git status` first; if the tree is dirty, say so before adding to the mess. Offer the pre-commit hook when the repository holds consequential prose; blocking a commit that contains a fabricated citation is worth more than any amount of doctrine. Follow the repository's existing conventions over the templates here.

**What it must never imply.** That a compiled core is doing the work. It is not. The canonical core is `scripts/wi.py`, a single stdlib-only Python file, and Law K says so out loud precisely so that no surface quietly implies otherwise. Also: the presence of a workspace does not create a judgment tier. `judgment: []` is true in a terminal too.

**What it must say when a capability is missing.** `wi doctor` output belongs in the report when anything is absent, verbatim rather than summarized. A summarized capability report is a capability report the reader cannot check.

---

## 5. CI — non-interactive

**Available:** the deterministic core, no human, no prompts, no interactive repair.

**What it can actually do.**

```bash
python3 scripts/wi.py gate claims.json --mode strict --exit-code   # 0 RELEASE · 1 HOLD · 2 BLOCK
python3 scripts/wi.py test
python3 scripts/wi.py verify-release release.wiab
```

**What it must never imply.** That a gate result is an approval. CI can determine that every factual claim carries a resolvable anchor and that the checks passed. It cannot produce a `human-declared` record, it cannot approve a source, and it cannot accept a proposal — those require a human actor under Laws J and the actor model, and no pipeline has one. A green build means the deterministic tier found nothing blocking. It does not mean anybody read it.

**What it must say when a capability is missing.** CI output is read fast, so it must be structured for the reader who is only going to see the failure line. Print the disclosure block on failure, and name the repair rather than the violation alone. A gate that says "unsupported claim" and stops has moved the problem to the author without moving it forward: attach a source · qualify the claim · cut the claim · proceed with a stated caveat, and say which is cheapest.

---

## 6. REST service

**Status: `services/api/` is the v3 craft runtime, executable. v5 verification endpoints are specified.**

`services/api/` is a containerized reference runtime for the **v3 craft kernel** — compile, score, voice, benchmark, repackage, manifest. See [`../../services/api/README.md`](../../services/api/README.md) and [`../../docs/api/API_SPEC.md`](../../docs/api/API_SPEC.md).

**What it must never do.** Duplicate verification rules. That is Law K, and the REST surface is where the temptation is strongest — a service under latency pressure, with its own language, its own parser and its own normalization, is exactly where a second implementation of `verified` gets written by accident and by well-meaning people. It will not disagree with the core loudly. It will disagree on the fifth edge case, in the document that mattered.

The boundary: the REST layer may handle transport, auth, tenancy, rate limiting, batching, caching and presentation. It may not implement a check, compute a digest by its own rule, resolve an anchor by its own logic, or emit a proof record it did not receive from the canonical core.

**What it must say when a capability is missing.** Serve the capability block at a stable endpoint and refuse to answer verification requests it cannot route to the core. An error is correct here. A best-effort answer is not.

---

## 7. MCP — specified, not implemented

**Status: specified.** [`../../docs/mcp/MCP_SPEC.md`](../../docs/mcp/MCP_SPEC.md) describes the interface. No MCP server ships in this repository.

An MCP adapter is the highest-risk surface in the system, because it is the one that puts tool calls between a model and a proof record, in both directions. It is also the one most likely to be implemented by a third party. So the conformance rules are written before the implementation rather than after it.

---

## 8. Air-gapped review

**Available:** a single file and a Python interpreter. Nothing else, by design.

```json
{ "core": "5.0.0", "capabilities": { "filesystem": true, "workspace": false, "binary_ingest": ["text"], "judgment": [], "signing": ["local_sha256"], "network": false } }
```

**What it can actually do.** Copy `wi.py` onto the machine. Then:

```bash
python3 wi.py --offline verify-release release.wiab
```

The bundle verifies with no network, no model, no workspace and no prior knowledge of the project that produced it. This is the surface the whole v5 design is aimed at — the reviewer who was not in the room, does not trust the author's toolchain, and cannot install anything.

**What it must never imply.** That verification of the bundle is verification of the sources. `verify-release` confirms internal consistency: that the digests match, the anchors resolve into the carried source versions, the recorded checks correspond to the recorded results, and the decision records bind to the states they claim. It says nothing about whether the sources are correct. That refusal is permanent — see [`NON_GOALS.md`](NON_GOALS.md).

**What it must say when a capability is missing.** State the scope of the verification in the output itself, so a printed page carries it:

> Bundle internally consistent. 14 anchors resolved, 11 deterministic checks reproduced, 6 decision records bound to their target states. This confirms the record is intact and untampered. It does not confirm the sources are correct.

---

## 9. The ten MCP conformance rules

**Status: specified.**

Any MCP adapter claiming Writing Intelligence v5 conformance must satisfy all ten. They are numbered so a conformance report can cite them.

| # | Rule |
|---|---|
| 1 | **Deterministic operations call the canonical core.** No adapter re-implements a check, a digest, an anchor resolution or a gate decision. |
| 2 | **State digests match the CLI on the same fixture.** Run the shipped fixture through the adapter and through `scripts/wi.py`; every state digest is identical, byte for byte. A divergence is a conformance failure, not a rounding difference. |
| 3 | **No tool may write a `verified` record except through the core.** An adapter may read, cache, present and forward proof records. It may not author one. |
| 4 | **Source content passes as data.** Ingested source text travels in a typed data field, structurally separated, never concatenated into an instruction channel. Law F is enforced by the message architecture, not by a warning string. |
| 5 | **Proposal decisions bind to an exact target state.** A decision tool call that does not carry the target state digest is rejected. An unbound approval is a signature on a blank page. |
| 6 | **Errors return stable `WI_` codes.** Machine-readable, documented, versioned — `WI_ANCHOR_UNRESOLVED`, `WI_SOURCE_QUARANTINED`, `WI_STATE_STALE`, `WI_CAPABILITY_UNAVAILABLE`. A prose error message is not an interface. |
| 7 | **The adapter advertises unavailable capabilities rather than simulating them.** Missing decoder, missing provider, missing workspace: declare it in the capability block and return `WI_CAPABILITY_UNAVAILABLE`. Never approximate. |
| 8 | **Judgment providers are named in every record.** Provider, model identifier, prompt/policy hash, input hashes, output, calibration basis, currency. Law L, with no field optional. |
| 9 | **Resources expose stable logical IDs.** A claim atom, anchor, proposal or bundle keeps its identifier across reconnects, restarts and sessions. An identifier that changes underneath a client makes every dependency edge unreliable. |
| 10 | **Tests include hostile source payloads.** The conformance suite ships sources carrying injection attempts, invisible characters, encoding tricks and instruction-shaped text. An adapter that has never been tested against a hostile source has not been tested. |

**Why these are written before the implementation.** Every one of them is cheap to satisfy at design time and expensive to retrofit. Rules 1, 2 and 3 are the same rule seen from three angles — Law K — and they are the ones that quietly break first, because re-implementing a small check locally is always the faster path in the moment. Rule 5 is the one that looks like ceremony and is not: an unbound decision is the single easiest way to make a document appear approved by a person who never saw it.

---

## 10. Shared across all surfaces

**Say which mode you are in** when it affects the output. *"Running strict evidence mode — every factual claim needs a resolvable anchor"* sets expectations before the author is surprised by a HOLD.

**Never claim a check ran where it could not.** This is Law C and it is easiest to violate by habit, by carrying an output shape from one surface into another that cannot back it.

**Emit the disclosure block everywhere.** Checks run · checks not run · unavailable on this surface · disabled by policy · invalidated by later edits. Empty sections are stated as empty, never omitted. Format and reasoning: [`RELIABILITY_TYPES.md`](RELIABILITY_TYPES.md).

**Degrade by dropping capability, never by lowering the standard.** A surface with fewer capabilities does less and says so. It does not do the same work to a weaker standard and use the same words for the result. That is the difference between a system that is honest on its worst surface and one that is honest only on its best.

---

Read next:

- [`CONSTITUTION.md`](CONSTITUTION.md) — Law C and Law K in full
- [`RELIABILITY_TYPES.md`](RELIABILITY_TYPES.md) — the disclosure block and per-surface degradation
- [`NON_GOALS.md`](NON_GOALS.md) — the permanent refusals
- [`../v4/SURFACES.md`](../v4/SURFACES.md) — the superseded v4 document
- [`../../docs/INSTALL.md`](../../docs/INSTALL.md) — every install surface and what each can do
