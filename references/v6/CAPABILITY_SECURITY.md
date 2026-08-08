# Capability Security

**Status: specified.** No adapter SDK, plugin host, WASM runtime or non-text anchor executor ships in v6.0.0. Text-span anchoring and source hygiene scanning remain executable in `scripts/wi.py`, unchanged from v5. Everything described below is a contract that binds any implementation that arrives later, written now so that the first implementation does not get to define the terms.

Every system that becomes useful becomes extensible, and every system that becomes extensible acquires the same defect on the same day: the extension inherits the authority of the process that loaded it. A PDF adapter runs with the workspace's filesystem permissions. A style plugin runs with whatever network the host has. Nobody chose that. It is what happens when a capability is a property of the process rather than a property of a grant.

This document specifies extension without ambient authority — adapters and plugins that hold exactly the capabilities they declared, enforced by the runtime rather than by the extension's good behavior — and then applies the same discipline to the one place it is hardest to hold: executing anchors against binary formats, where the extractor's output *is* the evidence.

Read this with [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md) for the ingestion sandbox this extends, [`../v5/EVIDENCE_ANCHORS.md`](../v5/EVIDENCE_ANCHORS.md) for the anchor shapes, and [`AUTONOMOUS_EXECUTION.md`](AUTONOMOUS_EXECUTION.md) for the same capability model applied to workers.

---

**Contents:** ambient authority · the adapter contract · the adapter manifest · out-of-process execution · the derivation record · the plugin host · plugin denials · determinism · anchor execution by evidentiary value · executable and specified.

---

## 1. Ambient authority

**Status: specified.**

Ambient authority is the permission a component has because of *where it runs* rather than because of *what it was given*. A Python module imported into a process can open any file that process can open. A shared library loaded into an address space can read any memory in it. Neither had to ask, neither declared it, and nothing in either case is auditable after the fact — the capability was not a decision, so there is no record of the decision.

The consequences in this system are specific.

| Component | Ambient authority it would inherit | What it turns a bug into |
|---|---|---|
| PDF adapter | The workspace filesystem, the network stack, the process's environment | A parser bug becomes workspace exfiltration |
| Spreadsheet adapter | The same, plus whatever the workbook wants to reach | A formula becomes a request |
| Style plugin | The graph, including target states and decisions | A style rule becomes an unattributed edit |
| Renderer plugin | The network | A layout engine becomes an unrecorded dependency in a release |
| Check plugin | The result writer | A plugin mints `verified` |

The last row is the one that matters most, and it is why this document exists rather than being a section in the security model. Every other guarantee in this project is downstream of `verified` meaning one thing. A plugin that can write a `verification.result` is a second implementation of evidence truth — forbidden by Law K for correctness reasons that turn out to be security reasons, because a second implementation is a second attack surface with fewer tests and no benchmark.

**The replacement rule, stated once and applied everywhere below:**

> **A capability an extension did not declare is a capability the runtime does not provide. There is no fallback, no inherited handle and no default grant. The absence of a declaration is a denial.**

The alternative — extensions hold the host's authority and are trusted to be careful — is not a weaker version of this design. It is a different design in which every extension is a full-trust component and the manifest is documentation.

---

## 2. The adapter contract

**Status: specified.**

An adapter turns supplied bytes into derived objects. It is the only component in the system that reads a format the core does not understand, which makes it the largest attack surface and the one with the worst industry history — every format this project governs has a decoder somewhere with a memory-safety record.

Three functions. No more.

```python
class SourceAdapter:

    def manifest(self):
        """Static declaration of what this adapter is and what it needs.

        Returns an AdapterManifest (§3). Called before the adapter is ever
        handed bytes. The runtime reads it, records it, and enforces every
        limit in it. An adapter whose manifest does not parse does not load;
        an adapter whose manifest declares a capability the host policy
        forbids does not load, and the refusal names the capability.
        """

    def inspect(self, blob):
        """Static, cheap, structural examination. No decoding.

        Returns an InspectionReport: sniffed media type, structural findings,
        declared-vs-observed mismatches, and any static indicator that routes
        the source to quarantine before a decoder ever sees it — the
        /JavaScript, /OpenAction, /Launch and /AA families for PDF, macro
        presence for Office formats, entry counts and nesting depth for
        archives.

        This runs first and it runs cheaply on purpose. A finding here means
        extract() is never called, which is the only defense that works
        against a decoder bug: not invoking the decoder.
        """

    def extract(self, blob, budget):
        """Produce derived objects from the bytes.

        Returns an ExtractionResult carrying source segments, tables, regions,
        intervals or structured values, each with its own content digest, plus
        a DerivationRecord (§6) naming this adapter and version.

        Runs out of process (§5) under the budget the manifest declared and
        the runtime imposes. Receives a read-only blob handle, a scratch
        directory, and nothing else. Has no workspace handle, no graph handle,
        no network, no environment and no path to any other source.
        """
```

**`inspect` is separate from `extract` because the cheap refusal has to come first.** An adapter with one entry point decodes in order to decide whether it should have decoded. Splitting them means a hostile PDF's `/OpenAction` is found by a few hundred bytes of structural reading, and the decoder — the part with the exploitable history — is never invoked at all. The most reliable defense against a parser vulnerability is the path that does not reach the parser.

**`extract` returns a value. It does not write.** The adapter has no handle by which it could write, which is what makes the sentence true rather than aspirational. Its output crosses back to the core as data, is validated against the schema, and is committed by the core or discarded by the core. This is the judgment-gateway shape from [`../v5/JUDGMENT_TIER.md`](../v5/JUDGMENT_TIER.md) §5 applied to a decoder, and for the same reason: a component that can be induced to produce arbitrary output must not be a component that can write state.

---

## 3. The adapter manifest

**Status: specified.**

```json
{
  "format": "wiadapter/1",
  "adapter_id": "wi-xlsx",
  "adapter_version": "6.0.0",
  "adapter_digest": "sha256:4f1a8c3d6b9e2f5a8c1d4e7f0a3b6c9e2f5a8b1d4e7f0a3c6b9d2e5f8a1c4d7f",

  "handles": {
    "media_types": [
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      "application/vnd.ms-excel"
    ],
    "sniff_signatures": ["504b0304"],
    "extension_hints": [".xlsx", ".xlsm", ".xls"]
  },

  "produces": [
    "source.table",
    "source.segment"
  ],

  "anchor_kinds": ["sheet_range"],

  "capabilities_required": [
    "blob.read",
    "scratch.write"
  ],

  "capabilities_refused": [
    "network.any",
    "workspace.read",
    "graph.read",
    "graph.write",
    "process.spawn",
    "env.read",
    "clock.read",
    "random.read"
  ],

  "limits": {
    "max_input_bytes": 268435456,
    "max_wall_ms": 60000,
    "max_cpu_ms": 45000,
    "max_rss_bytes": 1073741824,
    "max_scratch_bytes": 536870912,
    "max_sheets": 512,
    "max_cells": 4000000,
    "max_archive_entries": 4096,
    "max_archive_depth": 4,
    "max_decompression_ratio": 120
  },

  "determinism": {
    "deterministic": true,
    "declared_nondeterminism": []
  },

  "executes_supplied_code": false,
  "evaluates_formulas": false,

  "derivation_basis": "verified",

  "notes": "Formula text and cached values are extracted. Formulas are never evaluated and macros are never executed; see SECURITY_MODEL.md §4."
}
```

Four fields decide whether the adapter can be trusted with anything, and each is enforced rather than displayed.

**`capabilities_required` is a closed grant.** The runtime provides these and nothing else. An adapter that lists `blob.read` and `scratch.write` and then attempts `connect(2)` does not get a degraded network, a proxy, or a helpful error that suggests a retry. The call fails, the process is terminated, and the attempt is recorded as a finding against the *adapter*, not against the source. §5 is why that distinction matters.

**`limits` are imposed by the runtime, not honored by the adapter.** An adapter that declares `max_cells: 4000000` is declaring what it expects to need. The runtime enforces the ceiling from outside the process, where a runaway parser cannot argue with it. An adapter that declares a limit and then exceeds its own declaration is killed at the declared value, and that is the correct behavior — the declaration is the contract, and exceeding it is a defect in the adapter regardless of what the file contained.

**`executes_supplied_code` and `evaluates_formulas` must both be `false`.** The runtime refuses to load an adapter that declares either as `true`. There is no policy setting that admits one, no operator flag, and no consent dialog. Law F is not a text-only law: a workbook is data supplied by somebody else, and running code it carries is obeying it. An adapter that needs to run supplied code to obtain a value is an adapter whose correct output is `WI_CAPABILITY_UNAVAILABLE` with the reason stated.

**`derivation_basis` is the strongest reliability type this adapter's output may carry**, and most adapters may not carry `verified`. An XLSX cell value read from stored bytes is a deterministic reading of a structured format — `verified` is correct. A transcription is not, an OCR pass is not, and a vision description is not; those declare `judged` and the runtime refuses any output from them typed higher. An adapter cannot promote its own output, because the ceiling is in the manifest the runtime read before the adapter ran.

---

## 4. Loading and pinning

**Status: specified.**

An adapter loads only when its bytes hash to `adapter_digest`. The registry records the digest, the manifest and the moment it was registered. An adapter whose bytes changed is a different adapter and needs a different registration — the same discipline the plugin registry carries in [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md) §7, and for the same reason: an extension that can change under a stable identity is an extension whose past outputs cannot be attributed.

The pin appears in three places, and the third is the one that does work.

| Place | What it records |
|---|---|
| The registry | This adapter, at this digest, is permitted in this workspace |
| Every `DerivationRecord` | These derived objects were produced by this adapter at this digest |
| Every `state_digest` of a derived object | The adapter identity is in the digest preimage, per [`../v5/CANONICAL_HASHING.md`](../v5/CANONICAL_HASHING.md) §2 |

The third means an adapter upgrade produces new state digests for the same content, automatically, without anyone deciding to invalidate anything. That is not a side effect to be smoothed over. It is §6.

---

## 5. Out-of-process execution

**Status: specified.**

Every adapter runs in a separate process. It receives four things and no others.

| Given | Shape |
|---|---|
| A read-only blob handle | One file descriptor, opened read-only on the source bytes, at offset zero. Not a path. |
| A scratch directory | Empty, quota-bounded, on a filesystem with no other content, removed on exit |
| The budget | Wall time, CPU time, address space, scratch bytes, and the structural ceilings from the manifest |
| The request | Which extraction was asked for, and over which region if the request is partial |

It does not receive: the workspace path, the object store, the graph, any other source, the environment, a network namespace, a clock it can read, or the ability to spawn.

**A read-only file descriptor rather than a path.** A path is a capability to the *namespace*: an adapter holding a path can walk to its parent, can follow a symlink somebody planted, can reopen with different flags, and can race a replacement between the check and the open. A descriptor is a capability to exactly one already-opened object. There is nothing to traverse and nothing to race.

The three properties this buys, each stated as the failure it prevents:

**An adapter crash leaves the graph intact.** The adapter has no graph handle, so there is no partially-written state to roll back and no transaction to abandon. A segmentation fault in a decoder is a terminated child process and an `WI_SOURCE_EXTRACTION_FAILED` finding against one source. The workspace is in exactly the state it was in before the adapter started, because the adapter was never able to change it.

**A timeout discards partial derived output.** This is the ingestion rule from [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md) §3, restated here because it is the rule most likely to be relaxed under delivery pressure. A parser killed at 60% has produced 60% of a reading. Sixty percent of a reading, committed, is a source whose contents the system is wrong about in a way nothing downstream can detect — and anchors built into it point into a document that does not exist. The output is `WI_SOURCE_LIMIT_EXCEEDED` with the limit named and the observed value stated, and zero derived objects. Not the ones that completed. Zero.

**An attempted network access fails rather than falling back.** The adapter runs in a network namespace with no interfaces. There is no route, no resolver and no proxy. A font reference, a remote image, an external workbook link or a stylesheet URL produces a failed call inside the adapter, which is recorded as an unresolved external reference in the extraction result — a stated gap in the evidence, visible to the author. It does not produce a fetched asset, a cached asset, a substituted default or a silent omission.

The distinction between *failed* and *fell back* is the whole of the paragraph. A fallback produces output. Output produced by a fallback is indistinguishable, in the derived object, from output produced by the real thing — and the reader of the anchor has no way to know that the number they are looking at came from a workbook nobody supplied. An error is legible. A substitution is not.

```rust
pub struct AdapterInvocation {
    /// Read-only, already opened, offset zero. Not a path.
    pub blob: BlobHandle,
    /// Empty, quota-bounded, removed on exit.
    pub scratch: ScratchDir,
    pub budget: Budget,
    pub request: ExtractionRequest,
}

pub enum AdapterOutcome {
    Extracted(ExtractionResult),
    /// Structural finding during inspect(); extract() was never called.
    Quarantined { finding: Finding },
    /// A ceiling was breached. Partial output is dropped, not returned.
    LimitExceeded { limit: LimitKind, observed: u64, declared: u64 },
    /// The adapter attempted an operation its manifest does not declare.
    CapabilityViolation { attempted: Capability },
    /// Terminated abnormally.
    Crashed { signal: Option<i32>, exit: Option<i32> },
}
```

`LimitExceeded` carries no `partial` field. The type has nowhere to put one, which is a stronger guarantee than a rule saying not to use it.

---

## 6. The derivation record

**Status: specified.**

```json
{
  "derivation_id": "der-0119",
  "source_logical_id": "0192f3a1-7c40-7b2e-a077-3e9f1a4b6c28",
  "source_state_digest": "sha256:b7a241d9c0e3f6a9b2c5d8e1f4a7b0c3d6e9f2a5b8c1d4e7f0a3b6c9e2f5a8b1",

  "adapter": {"id": "wi-xlsx", "version": "6.0.0",
              "digest": "sha256:4f1a8c3d6b9e2f5a8c1d4e7f0a3b6c9e2f5a8b1d4e7f0a3c6b9d2e5f8a1c4d7f"},

  "request": {"kind": "full", "region": null},

  "produced": [
    {"node_type": "source.table", "content_digest": "sha256:5e8a0c93…", "count": 3},
    {"node_type": "source.segment", "content_digest": "sha256:1c4d7f0a…", "count": 118}
  ],

  "basis": "verified",

  "limits_observed": {"cells": 41208, "sheets": 4, "wall_ms": 2140},
  "unresolved_external_references": [
    {"kind": "workbook_link", "target": "[Regional2021.xlsx]Summary!$B$7", "resolved": false}
  ],

  "produced_at": "2026-06-02T10:22:41Z"
}
```

**A derivation record makes an extractor upgrade a visible dependency transition, rather than a silent change of what a source says.**

This is the property worth paying for and it is easy to lose. Consider the sequence without it: an extractor is upgraded, reading order in a two-column layout improves, a paragraph that used to be read as belonging to the figure caption is now read as belonging to the body, and the extracted text of page 14 changes. No source changed. Nobody edited anything. The document a claim rests on now says something slightly different, and there is no event anywhere in the system that says so.

With the record, the same sequence produces:

1. The new extraction has a different `adapter.digest`, so the derived objects have different `state_digest` values — the adapter identity is in the preimage.
2. The anchors bound to the old derived state are `WI_ANCHOR_STALE`, by the ordinary staleness rules in [`../v5/STALENESS.md`](../v5/STALENESS.md), with no special case for extractors.
3. `wi impact` prints a repair frontier naming exactly the claims whose evidence moved.
4. The report says *the extractor changed*, not *the source changed*, because the two derivation records differ in the adapter field and agree in `source_state_digest`.

Point four is the one an author needs. "Your source moved" sends them to check whether somebody replaced a file. "The extractor moved and here are the eleven anchors whose extracted text is now different" sends them to look at eleven passages, which is a smaller and more accurate job.

**`unresolved_external_references` is a stated gap, not an omission.** An external workbook link that could not be followed — because the network is denied and the referenced workbook was not supplied — appears here, travels into the anchor, and appears in the proof report. §9.2 is why.

---

## 7. The plugin host

**Status: specified.**

Plugins are compiled to WebAssembly and run in a host that provides an explicit import set. WASM is chosen for one property that matters more than any other: **a WASM module has no ambient authority by construction.** It cannot open a file, resolve a name, allocate outside its own linear memory or issue a syscall unless the host provides a function that does it. The default in every other plugin architecture — a shared library, a script in the host language, a subprocess — is that the plugin inherits the host's powers and the design has to take them away. Here the default is that it has none and the host has to hand them over, one function at a time, in a diff somebody reviewed.

### 7.1 Categories

| Category | Does | May write |
|---|---|---|
| `check` | Evaluates a deterministic condition over declared node states | A finding. Never a `verification.result`. |
| `renderer` | Produces output bytes from a graph state for a declared target | Bytes into a declared output path |
| `policy` | Evaluates a policy predicate and returns a verdict contribution | A verdict contribution the core composes. Never a gate verdict. |
| `import` | Maps an external format into proposal objects | `authorship.proposal` objects only |
| `lint` | Reports craft, style and voice findings over rendered text | Advisory findings |

**A `check` plugin returns a finding; the core decides whether the finding is a result.** The distinction is the entire reason the categories exist. A finding says *this condition did not hold at this node state*. A `verification.result` says *a named check was executed against a named state under a named policy and produced this outcome*, and it is the object a proof closure carries. The core constructs the second from the first, applying the policy, the reliability type and the dependency binding. A plugin that could construct one directly would be minting evidence, and every downstream guarantee about `verified` would then depend on the least-reviewed code in the build.

### 7.2 The capability manifest

```json
{
  "format": "wiplugin/1",
  "plugin_id": "org.example.jurisdiction-lint",
  "plugin_version": "2.1.0",
  "plugin_digest": "sha256:8b1d4e7f0a3c6b9d2e5f8a1c4d7f0a3b6c9e2f5a8b1d4e7f0a3c6b9d2e5f8a1c",
  "category": "lint",

  "abi": "wi-plugin-abi/1",

  "imports_requested": [
    "graph.read_declared",
    "text.read_rendered",
    "finding.emit",
    "pack.read_own"
  ],

  "declares": {
    "reads": ["structure.paragraph", "meaning.claim_atom", "meaning.term"],
    "writes": ["finding"]
  },

  "determinism": {
    "deterministic": true,
    "declared_nondeterminism": []
  },

  "limits": {
    "max_fuel": 200000000,
    "max_memory_pages": 512,
    "max_wall_ms": 10000,
    "max_findings": 5000
  },

  "policy_direction": "tighten_only"
}
```

`policy_direction` may hold `tighten_only` and nothing else. The field exists so the value is stated in the artifact rather than implied by the runtime, and so a plugin that wanted the other value would have to write it down and be refused at load.

### 7.3 The denial list

These are not configurable. There is no import the host will provide for any of them, in any category, under any policy.

| Denied | Because |
|---|---|
| Arbitrary filesystem access | A plugin holding a path holds the namespace; §5 covers the reasoning at the descriptor level |
| Sockets, of any family | A plugin that can connect can exfiltrate a draft, and can turn an injection in a source into an outbound request |
| Signing, of anything | A signature is a statement by a person or a key that person controls. See [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) §8 |
| Direct graph writes | The core is the sole writer of state. Law K, and the reason a `check` returns a finding rather than a result |
| Minting a `verified` result | The type names how a result was produced. A plugin's assertion cannot satisfy the definition, so the host provides no function that accepts one |
| Reading secrets not passed in | A plugin sees what its declaration named. There is no environment, no keyring, no credential store |
| Implicit plugin-to-plugin calls | Composition is a host decision |

**The last row deserves its own paragraph.** Plugin-to-plugin calls look like modularity and are a capability laundering channel: plugin A holds `graph.read_declared`, plugin B holds `finding.emit`, and a call from A to B lets the pair do together what neither was granted alone. Worse, the composite grant is not written down anywhere — it exists only as the transitive closure of who can call whom, which nobody computed and no manifest states. If two plugins should compose, the *host* composes them: it calls A, takes the value, calls B with it, and the data flow is a line of host code somebody can read.

**A plugin may tighten policy. A plugin may never loosen a hard invariant.** Preserved verbatim from [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md) §7. It can add a check, raise a severity, narrow an evidence mode, require an additional anchor kind, forbid a construction. It cannot widen `verified`, downgrade a `block` to a `review`, admit an unanchored claim, remove a required decision, disable the quarantine boundary or grant itself an import. A compromised plugin's maximum achievable outcome is a build stricter than intended — an annoyance, not a breach.

---

## 8. Determinism

**Status: specified.**

A plugin declaring `deterministic: true` receives no wall clock and no random source. The host does not provide `clock.read`, does not provide `random.read`, does not seed the module's memory with entropy, and does not expose any import from which either could be derived. WASI's clock and random interfaces are absent from the import set; a module that imports them fails to instantiate, at load, with the missing import named.

**Why this is not a purity preference.** If a deterministic plugin can read a clock, then identical graph state can produce different proof output on two runs. That single sentence destroys four properties at once:

| Property lost | How |
|---|---|
| Reproducible builds | The artifact digest changes without the content changing, so an attestation cannot be re-derived |
| Closure stability | A recomputed closure differs from the stored one, and `wi verify-release` reports drift that is not real |
| Replay | An autonomous run's `Pure` steps stop replaying to the same output, and §9 of [`AUTONOMOUS_EXECUTION.md`](AUTONOMOUS_EXECUTION.md) stops holding |
| Bisecting a defect | Two runs disagree and there is no way to tell whether the input, the plugin or the clock moved |

The failure is also quiet. A plugin that reads the clock in a rarely-taken branch — a cache key, a nonce, a "generated at" line in a footer — produces stable output for months and then produces one artifact that does not reproduce, on a machine nobody can reach, on a document that mattered.

**A plugin that genuinely needs non-determinism declares it.** `deterministic: false` with `declared_nondeterminism: ["clock"]` is a legal manifest. What it costs is precise and stated at load: the plugin's output cannot enter a proof closure, its findings are advisory, and any artifact it participates in producing is marked as not reproducible in `build/environment.json`. That is a real trade an operator may want to make for a linting pass. It is not a trade anybody should make by accident, which is what a clock in the default import set arranges.

**Fuel, not wall time, bounds a deterministic plugin.** A wall-time ceiling is itself a clock, and a plugin can observe its own termination pressure through it. Fuel — a deterministic instruction budget metered by the runtime — bounds execution without giving the module a quantity that varies between runs. Wall time remains as an outer backstop enforced by the host process, where the plugin cannot observe it.

---

## 9. Anchor execution, in evidentiary-value order

**Status: specified.** No non-text anchor executor ships. The order below is by how much a resolved anchor of each kind actually proves, strongest first, because that is the order in which an author should prefer them and it is not the order in which they are easiest to build.

The governing rule across all five, stated once:

> **What is pinned by a digest is evidence. What is produced by reading is interpretation, and interpretation is `judged` no matter how good the reader is.**

### 9.1 PDF region anchors

The strongest non-text kind, because two independent things are pinned.

| Pinned | By | Basis |
|---|---|---|
| The visual region a human would look at | `region_render_hash` — a digest of the rendered raster of that page region at a declared DPI and colorspace | `verified` |
| The text an extractor read from it | `text_hash` over `extracted_text`, with the extractor identity | `verified` as a reading; the *correspondence* to the region is derived |

**The rendered region digest pins what a human sees. The extracted text is a derived interpretation of it.**

PDF text extraction is an interpretation and not a marginal one. Extractors disagree about reading order in multi-column layouts, about ligatures and about whether a caption belongs to the paragraph above or below. They disagree about text that is drawn and then visually covered, which is a hiding technique, not a curiosity. If the only evidence that page 14 says something is what one extractor reported, then upgrading the extractor changes what a source says with no source having moved — and the derivation record in §6 makes that transition visible precisely because the render hash gives it something to be visible *against*.

A reviewer holding a `full` capsule can regenerate the raster at the declared DPI and colorspace and compare digests. That check requires no trust in the extractor at all.

### 9.2 XLSX range anchors and the formula dependency closure

A spreadsheet is the only source type where a visible value can be *derived*, and the derivation is usually the interesting part.

```json
{
  "anchor_id": "a-0330",
  "anchor_type": "sheet_range",
  "source_state_digest": "sha256:b7a241d9…",

  "sheet": "WaitTimes2022",
  "range": "D14:D14",
  "display_values": ["38%"],
  "raw_values": [0.38],
  "number_formats": ["0%"],
  "cell_values_hash": "sha256:5e8a0c93…",

  "cell_kind": "formula_result",
  "formula_text": "=SUM(A1:A12)/COUNT(A1:A12)",

  "dependency_closure": {
    "complete": false,
    "cells": [
      {"ref": "WaitTimes2022!A1",  "kind": "raw_input", "value_digest": "sha256:0a3b6c9e…"},
      {"ref": "WaitTimes2022!A2",  "kind": "raw_input", "value_digest": "sha256:2f5a8b1d…"},
      {"ref": "WaitTimes2022!A3",  "kind": "formula_result",
       "formula_text": "=[Regional2021.xlsx]Summary!$B$7*1.04"}
    ],
    "external_dependencies": [
      {"target": "[Regional2021.xlsx]Summary!$B$7", "resolved": false,
       "reason": "referenced workbook not supplied"}
    ]
  },

  "evaluated": false,
  "extractor": {"id": "wi-xlsx", "version": "6.0.0"}
}
```

**A number produced by `=SUM(A1:A12)` depends on twelve inputs, and the anchor carries all twelve.** Anchoring only at the output anchors to the surface of the evidence. It is the spreadsheet equivalent of citing a number without citing where the number came from, and it fails in a specific way: an input cell changes, the output cell's formula is untouched, the anchored cell's own digest is unchanged, and a claim that depends on the arithmetic carries forward with a stale value nobody flagged. With the closure recorded, a change to any cell in it moves the claim to `review` — correctly, because the relationship the claim rests on has different inputs than it had when it was checked.

**A number from an external workbook is incomplete evidence until the workbook is supplied or the gap is explicitly waived.** `complete: false` with a named `external_dependencies` entry is the honest state, and it is a reported gap rather than a passed check. The three available resolutions are the three that exist:

| Resolution | Produces |
|---|---|
| Supply the referenced workbook | A complete closure; the anchor resolves fully |
| Requote to a raw input cell that is present | A `raw_input` anchor with a one-cell closure — the strongest form |
| Record a waiver | A proceed-anyway bound to the claim state, naming the actor and the reason, visible in the report and in the closure |

There is no fourth. The adapter does not fetch the workbook, because it has no network. It does not evaluate the formula against assumed inputs, because it evaluates nothing. It does not treat the cached value as sufficient, because a cached value is what the workbook stored the last time somebody opened it, which is a fact about that session rather than about the current inputs. `evaluated` is `false` in every anchor this system produces, and the field is present so its value is stated rather than assumed.

### 9.3 DOCX paragraph-path anchors

```json
{
  "anchor_id": "a-0447",
  "anchor_type": "paragraph_path",
  "source_state_digest": "sha256:c6b9d2e5…",

  "path": "/w:document/w:body/w:sectPr[1]/../w:p[214]",
  "paragraph_index": 214,
  "style": "BodyText",

  "text": "The pilot reduced median wait by 38% across the seven-county area.",
  "text_hash": "sha256:7f0a3b6c…",
  "run_boundaries": [[0, 11], [11, 39], [39, 66]],

  "tracked_changes_present": true,
  "resolved_view": "final",
  "comments_in_range": ["cm-0031"],

  "extractor": {"id": "wi-docx", "version": "6.0.0"}
}
```

Weaker than a PDF region because there is no rendered pin — a paragraph path addresses a position in a document tree, and a document tree can be edited such that position 214 holds different content while the path stays syntactically valid. The `text_hash` is what makes the anchor detect that: the path locates, the hash verifies, and a path that resolves to different text is `WI_ANCHOR_STALE` rather than a silent relocation.

Two fields exist because Word documents routinely contain more than one reading of themselves. `tracked_changes_present` with `resolved_view` states which reading the anchor addresses — the text as it stands with revisions applied, or as it stands with them rejected. An anchor that did not say would be quoting one of two documents without saying which. `comments_in_range` records that a comment overlaps the anchored text, because a passage carrying an unresolved editorial comment is a passage somebody was unsure about, and that is worth surfacing beside a claim that rests on it.

### 9.4 Image region anchors

```json
{
  "anchor_id": "a-0402",
  "anchor_type": "image_region",
  "source_state_digest": "sha256:1f6dcc80…",

  "region": {"x": 0.184, "y": 0.402, "w": 0.311, "h": 0.166, "coords": "normalized"},
  "region_hash": "sha256:a90437bd…",
  "region_render": {"resample": "none", "colorspace": "srgb"},

  "description": {
    "text": "A line chart showing wait times declining from 2019 to 2022.",
    "basis": "judged",
    "produced_by": "vision_capability",
    "supports_claims": false
  }
}
```

**The pixels are deterministic evidence. The description is judgment.** The region hash is a digest over the exact pixels of a normalized region; two parties with the same image compute the same digest, forever, with no model. That is `verified` and it is genuinely useful — it pins that this region of this image has not changed.

What it does not do is tell anyone what the region *means*, and the description that does is produced by reading. `supports_claims: false` is not a default that a policy can flip. An image does not prove an interpretation merely because a model described it, and if the numbers in the chart matter, the numbers need a `sheet_range` or `data_pointer` anchor into the data behind the chart. A description of a picture of a number is three removes from the number, and the anchor's shape is what stops those three removes from collapsing into one citation.

### 9.5 Audio and video segment pinning

The weakest kind, and the one most likely to be over-read.

| Pinned | Basis |
|---|---|
| The audio bytes of the interval, at a declared decode | `verified` |
| Representative frame hashes at declared presentation timestamps | `verified` |
| The transcript of the interval | `judged` |
| OCR of burned-in text in a frame | `judged` |

A transcript is a derived object produced by a fallible process, and its basis is `judged`, never `verified` — regardless of the transcriber's accuracy on any benchmark, because the type names how the output was produced rather than how good it is. A claim quoting a speaker is supported by the transcript only to the strength the policy allows for judged evidence, and the audio segment remains pinned so a human can listen.

**Video adds the frame problem.** A video is not a sequence of addressable images in any stable sense — a re-encode changes every frame's bytes while changing nothing a viewer would notice, and frame *indices* shift with container edits. So the anchor pins representative frames by hash at declared presentation timestamps, and a re-encode invalidates the anchor. That is correct behavior and it is inconvenient: the anchor is telling the truth, which is that the bytes somebody checked are not the bytes in hand.

OCR of burned-in text is the most commonly cited part of a video and the least reliable to read. It is hashed, labelled `judged`, and never promoted.

---

## 10. What is executable and what is specified

| Mechanism | Status |
|---|---|
| Text-span anchoring, quote digests, anchor integrity | Executable in `scripts/wi.py` |
| Source hygiene scanning, injection and invisible-character detection | Executable in `scripts/wi.py` |
| The three-function adapter contract and the adapter manifest | Specified |
| Adapter digest pinning and registry admission | Specified |
| Out-of-process execution, read-only blob handle, scratch quota, ceilings | Specified |
| Partial-output discard on any limit breach | Specified |
| `DerivationRecord` and extractor-upgrade transitions | Specified |
| The WASM plugin host, categories, import set and denial list | Specified |
| Fuel metering and the no-clock, no-random rule | Specified |
| `pdf_region`, `sheet_range`, `paragraph_path`, `image_region`, `audio_time`, `video_time` execution | Specified |
| Formula dependency closure extraction | Specified |
| Any shipped adapter or plugin, of any category | **None ships.** |

The last row is worth reading beside the threat table in [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md) §1. Several of the attacks this document defends against are, today, defended by the absence of the capability: a build with no PDF adapter cannot be attacked through a PDF. That is a real defense and a temporary one, and saying so is Law C.

---

## Related documents

- [`AUTONOMOUS_EXECUTION.md`](AUTONOMOUS_EXECUTION.md) — the same capability model applied to workers and their effect classes
- [`PACKAGE_SYSTEM.md`](PACKAGE_SYSTEM.md) — how a plugin is distributed, pinned and recorded in a release closure
- [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) — why signing is unavailable to every extension point described here
- [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md) — the ingestion sandbox, formula handling and plugin trust this document extends
- [`../v5/EVIDENCE_ANCHORS.md`](../v5/EVIDENCE_ANCHORS.md) — the anchor shapes these executors resolve
- [`../v5/MULTIMODAL.md`](../v5/MULTIMODAL.md) — the media families and the rollout order
- [`../v5/CANONICAL_HASHING.md`](../v5/CANONICAL_HASHING.md) — why an adapter identity belongs in a state digest preimage
- [`../v5/STALENESS.md`](../v5/STALENESS.md) — what an extractor upgrade invalidates, and how the frontier is computed
- [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) — Laws F and K, which bound every extension point here
- [`../v4/SOURCE_HYGIENE.md`](../v4/SOURCE_HYGIENE.md) — the scanner that runs before any decoder
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
