# Proof-Carrying Release

**Status: executable — `wi bundle` / `wi verify-release`.**

This is the point where Writing Intelligence stops being a writing assistant and becomes authorship infrastructure.

Every layer below this one produces something a reader has to take on faith: a graph they cannot see, a check they were not present for, a decision recorded in a workspace they do not have. A proof-carrying release removes that requirement. The proof travels with the artifact, in a form a stranger can open on a machine that has never seen the workspace, with no network, no model, and no reason to trust the author.

Read this with [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) for the proof closure it verifies, [`CANONICAL_HASHING.md`](CANONICAL_HASHING.md) for how every digest here is computed, and [`POLICY_AS_CODE.md`](POLICY_AS_CODE.md) for the policy object the manifest binds.

---

## Table of contents

1. The thesis
2. The `.wiab` bundle
3. The release manifest
4. What `wi verify-release` checks
5. The three privacy profiles
6. Signing
7. Reviewer mode
8. External provenance compatibility
9. Supply-chain security for the tool itself
10. What is executable and what is specified

---

## 1. The thesis

**Status: executable — `wi bundle` / `wi verify-release`.**

A v4 release was a document and a verdict. The verdict was true when it was printed, and after that it was a sentence in a chat log.

A v5 release is not only `book.pdf`. It ships with a machine-verifiable record of:

| The record states | Because a reader will ask |
|---|---|
| What source artifacts were used, and their exact byte digests | *What is this built on, and is it the version you say it is?* |
| What claims exist in the artifact | *What is this document actually asserting?* |
| What evidence anchors support those claims | *Where, exactly, can I go look?* |
| What checks ran | *What was actually done?* |
| **What checks did not run** | *And what was not done?* |
| What model judgments, if any, were used | *Where does an opinion sit inside this, and whose?* |
| What proposals changed meaning | *Did an edit move the assertion, or only the sentence?* |
| Which human accepted those changes | *Who approved this line?* |
| What waivers exist | *What did you proceed on anyway, and why?* |
| Which version of the tool built the artifact | *Under what rules was this checked?* |
| Whether the final output still matches the verified state | *Is the file in my hands the file that was checked?* |

The fifth row is the one that distinguishes this from a compliance artifact. **A record of what did not run is worth more than a record of what did**, because the first is the only thing that tells a reader where to spend their own scrutiny. A bundle that lists twenty passing checks and stays silent about the paraphrase support it never attempted is Law C violated at release scale — the report's structure implies coverage the run never had.

The bundle answers those eleven questions or it does not ship. There is no partial mode in which the answers are implied by the format.

---

## 2. The `.wiab` bundle

**Status: executable — `wi bundle`.**

`.wiab` is the **W**riting **I**ntelligence **A**uthorship **B**undle. It is a deterministic zip archive — stored entry order, normalized entry metadata, no timestamps that vary between runs of the same state — produced by `zipfile` from the Python standard library. Two `wi bundle` runs over the same workspace state produce byte-identical archives, which is what makes the bundle itself hashable and therefore attestable.

```
release-2026-03-19.wiab
│
├── manifest.json                  the release manifest — §3
│
├── artifact/
│   ├── narrative.pdf              the released bytes, exactly as distributed
│   ├── narrative.md               source rendering, when the target declares one
│   └── deck.md
│
├── graph/
│   ├── nodes.jsonl                every node state in the proof closure
│   └── edges.jsonl                every edge in the closure, with invalidation policy
│
├── proof/
│   ├── checks.jsonl               every check: what ran, what did not, and why
│   └── judgments.jsonl            every judgment record, with provider and inputs
│
├── decisions/
│   ├── proposals.jsonl            every proposal that touched a closure node
│   ├── decisions.jsonl            accept / reject / defer, bound to target states
│   └── waivers.jsonl              every proceed-anyway, bound to a claim state
│
├── sources/
│   ├── sources.lock               source identities, versions, raw-byte digests
│   ├── anchor-index.json          every anchor, its locator, its quote digest
│   └── blobs/                     raw source bytes — full profile only
│
├── policy/
│   └── wi.policy.yaml             the policy in force, verbatim
│
├── build/
│   ├── environment.json           core version, platform, canonicalization version
│   └── renderers.json             renderer identities and digests, per target
│
├── attestations/
│   ├── release.json               the attestation over each target artifact
│   └── signature.bundle           detached signatures — present only when signed
│
└── checksums.sha256               digest of every other entry in the archive
```

Each directory answers one of the eleven questions and nothing else. The separation is not filing convenience: `proof/` can be read by an auditor who does not care who approved anything, `decisions/` can be read by counsel who does not care which trigram retriever found a candidate, and `sources/` can be stripped entirely under a privacy profile without any other directory becoming unreadable.

`checksums.sha256` is last on purpose. It covers every other entry, so archive integrity is checkable with `sha256sum -c` and no Writing Intelligence installation at all.

---

## 3. The release manifest

**Status: executable — `wi bundle`.**

```json
{
  "format": "wiab/1",
  "version": "5.0.0",

  "release_id": "rel-2026-03-19-0001",
  "project_id": "0192f3a1-7c40-7b2e-9000-0d4a1b6c3e77",

  "project_state_digest": "sha256:c9f4a1e7...b0d3",
  "policy_digest": "sha256:41ba7c02...9e18",

  "core": {
    "version": "5.0.0",
    "artifact_digest": "sha256:7d20e5b8...4c61"
  },

  "targets": [
    {
      "target": "book",
      "path": "artifact/narrative.pdf",
      "digest": "sha256:e11c0a94...77f2",
      "proof_closure_digest": "sha256:b8032dfe...15a9"
    },
    {
      "target": "web",
      "path": "artifact/deck.md",
      "digest": "sha256:5aa9013c...c0e4",
      "proof_closure_digest": "sha256:2f77b1a0...8d36"
    }
  ],

  "gate": {
    "verdict": "HOLD",
    "reasons": ["stale_claim:c-0002", "waiver_required:c-0006"]
  },

  "counts": {
    "claim_atoms_required": 41,
    "claim_atoms_permitted": 39,
    "waivers": 1,
    "stale_nodes": 2
  },

  "privacy_profile": "hash-only",

  "attestations": [
    {"target": "book", "path": "attestations/release.json", "signed": false},
    {"target": "web",  "path": "attestations/release.json", "signed": false}
  ]
}
```

Field by field:

| Field | Holds |
|---|---|
| `format` | The bundle format identity, versioned independently of the tool |
| `version` | The Writing Intelligence release line the bundle was produced under |
| `release_id` | The identity of this release, stable across re-verification |
| `project_id` | The workspace's logical identity, stable across releases |
| `project_state_digest` | The digest over the workspace state this release was cut from |
| `policy_digest` | The digest of the exact policy document in `policy/` |
| `core` | The core version and the digest of the executable that produced the bundle |
| `targets[]` | One entry per released output: name, path inside the archive, byte digest, and the digest of its proof closure |
| `gate` | The verdict at build time and the machine-readable reasons behind it |
| `counts` | Summary counts, defined below |
| `privacy_profile` | Which of the three profiles in §5 governed what is inside |
| `attestations[]` | Where the attestation for each target lives, and whether it carries a signature |

**`gate.verdict` is recorded, not suppressed.** A bundle may be built at `HOLD`. The manifest says so, `reasons` names what is outstanding, and `wi verify-release` will confirm that the bundle honestly reports its own unresolved state. A tool that could only bundle a green release would teach its users to stop bundling.

**Counts are summaries. The members are queryable.** `claim_atoms_required: 41` is a fact about a number; it is not evidence about any particular claim. Every count in the manifest resolves to a membership query against `graph/`, `proof/` and `decisions/`:

```
$ python3 scripts/wi.py bundle --show waivers release-2026-03-19.wiab

waivers  1 of 1

  w-0004  c-0006  evidence_reviewer:a.smith  2026-03-18T21:04:11Z
          state: sha256:9c02...41ff
          reason: "Figure confirmed by phone with the county administrator;
                   written confirmation expected before the April filing."
          status: active — bound state unchanged since the waiver was recorded
```

**A number without membership is a dashboard, not a proof.** "39 of 41 claims permitted" tells a reviewer how much work there is; it tells them nothing about whether the two that failed are typographical or fatal. Any count in this manifest that cannot be expanded into the exact set of nodes it counts is a defect in the bundle, not a display preference.

---

## 4. What `wi verify-release` checks

**Status: executable — `wi verify-release`.**

In order, each stage gating the next:

1. **Archive integrity.** Every entry named in `checksums.sha256` is present, and its bytes hash to the recorded digest. Extra entries not named in the checksum file are reported, not ignored.
2. **Object hashes.** Every object referenced from `graph/`, `proof/`, `decisions/` and `sources/` resolves to a payload whose canonical digest matches the reference, under the canonicalization version named in `build/environment.json`.
3. **Graph references.** Every edge endpoint in `edges.jsonl` names a node state present in `nodes.jsonl`. No dangling references, no orphaned states, no supersession chain with a missing link.
4. **Final artifact digest.** The bytes at each `targets[].path` hash to `targets[].digest`. This is the check that answers *is the file in my hands the file that was checked?*
5. **Proof dependencies.** Each target's proof closure is recomputed from `graph/` and compared to `targets[].proof_closure_digest`. A closure that recomputes to a different digest means the bundle's contents do not support the claim its manifest makes about them.
6. **Decision references.** Every decision in `decisions.jsonl` names a proposal present in `proposals.jsonl` and a target state present in `nodes.jsonl`. Every waiver names a claim state that exists. A decision bound to nothing is a signature on a blank page.
7. **Policy hash.** The digest of `policy/wi.policy.yaml` matches `policy_digest`. The gate verdict in the manifest was produced under the policy in the archive, not under one that has since been edited.
8. **Core version.** `core.version` and `core.artifact_digest` are recorded and reported. A mismatch against the verifying installation is stated, never silently accommodated — the verifier says which version produced the bundle and which version is reading it.
9. **Stale-state closure.** Every state in every closure is checked against the invalidations recorded in the bundle. A closure containing an invalidated state is reported with the state, the cause, and the reason code.
10. **Signature.** Optional. If `attestations/signature.bundle` is present, each signature is verified against the attestation it covers. If it is absent, the verifier says the bundle is unsigned — it does not treat absence as a pass.

A passing bundle:

```
$ python3 scripts/wi.py verify-release release-2026-03-19.wiab

release-2026-03-19.wiab  ·  wiab/1  ·  built by wi 5.0.0

  1  archive integrity           OK    28 entries, all checksums match
  2  object hashes               OK    1,204 objects, canonicalization wi-json-v1
  3  graph references            OK    892 nodes, 2,140 edges, no dangling endpoints
  4  final artifact digest       OK    book  sha256:e11c0a94...77f2
                                       web   sha256:5aa9013c...c0e4
  5  proof dependencies          OK    2 closures recomputed and matched
  6  decision references         OK    31 proposals, 31 decisions, 1 waiver
  7  policy hash                 OK    sha256:41ba7c02...9e18
  8  core version                OK    bundle 5.0.0 · verifier 5.0.0
  9  stale-state closure         OK    2 stale nodes, both declared in the manifest
 10  signature                   —     unsigned bundle

VERDICT: VERIFIED — the bundle is internally consistent and the artifacts
         match the state that was checked.

Gate at build time: HOLD (stale_claim:c-0002, waiver_required:c-0006)
This bundle honestly reports an unresolved release. It does not claim RELEASE.

Checks run: archive integrity · object hashes · graph references · artifact
digest · closure recomputation · decision binding · policy hash · core version ·
stale-state closure.
Not run: signature verification (bundle is unsigned) · source byte inspection
(privacy profile: hash-only, source bytes not included).
```

A tampered bundle — the same archive with two words changed inside `narrative.pdf`:

```
$ python3 scripts/wi.py verify-release release-2026-03-19.wiab

release-2026-03-19.wiab  ·  wiab/1  ·  built by wi 5.0.0

  1  archive integrity           FAIL  1 of 28 entries does not match
  2  object hashes               —     not run: archive integrity failed
  3  graph references            —     not run: archive integrity failed
  4  final artifact digest       FAIL  artifact/narrative.pdf
                                       manifest  sha256:e11c0a94...77f2
                                       observed  sha256:0b7f39ac...1d55
  5  proof dependencies          —     not run: artifact digest failed
  6  decision references         —     not run
  7  policy hash                 —     not run
  8  core version                —     not run
  9  stale-state closure         —     not run
 10  signature                   —     not run

VERDICT: WI_RELEASE_TAMPERED

  The bytes of artifact/narrative.pdf do not match the digest its attestation
  names. The attestation describes a document that is not the one in this
  archive. Nothing downstream of this check was evaluated, and no statement
  about the claims in this document is available from this bundle.

$ echo $?
2
```

Two properties of that output are deliberate. The verifier stops rather than continuing to green-tick stages that no longer mean anything, and it says so per stage — `not run: archive integrity failed` — instead of leaving them blank. And it draws the correct conclusion: not *the document is false*, but *no statement about this document is available from this bundle*.

**No model is required to verify any of this.** Every stage is a hash comparison, a set membership test or a graph walk. `wi verify-release` runs offline, on stdlib-only Python 3.8+, on a machine that has never seen the workspace, in an air-gapped review room, with no account, no license check and no telemetry. That property is the entire product. A proof that requires the prover's infrastructure to check is not a proof; it is a promise with better formatting.

---

## 5. The three privacy profiles

**Status: executable — `wi bundle --profile`.**

A bundle that always contained source bytes would be unusable for most of the work it is built for. Licensed research, confidential partner documents, patient material, unredacted personnel files and pre-publication manuscripts cannot be redistributed to a reviewer because a provenance tool would find it convenient.

So the bundle has three profiles, and the manifest states which one was used.

| Profile | Contains | Use when | Cannot do |
|---|---|---|---|
| `full` | Everything, including raw source bytes in `sources/blobs/` | Internal audit, archival, regulated handoff where redistribution is permitted | Nothing — this is the complete record. It is also the one you must not email casually. |
| `hash-only` | Source metadata, raw-byte digests, anchor descriptors and quote digests. **No source bytes.** | Licensing or confidentiality prevents redistributing the sources | An external reviewer who does not already possess the source **cannot inspect it**. They can confirm that an anchor is internally consistent; they cannot confirm the source says what the anchor claims. |
| `redacted` | Approved evidence excerpts and approved regions only, each carrying its approval record | External review under limited disclosure — counsel, funder, publisher, partner | Show anything a human did not approve for disclosure. Coverage is therefore partial by construction, and the manifest names which anchors were withheld. |

The `hash-only` limitation is stated in the verifier's own output, not only here, because it is the profile most likely to be mistaken for something stronger than it is:

```
Profile: hash-only

  Source bytes are not present in this bundle. Anchors are verified for
  internal consistency — locator well-formed, quote digest matches the
  recorded quote, source version current at build time.

  This bundle CANNOT demonstrate that needs_assessment.txt@v3 contains the
  quoted text. To check that, obtain the source and run:

      wi verify-release --with-sources /path/to/sources release-2026-03-19.wiab
```

That is Law E applied to distribution. A reviewer holding a `hash-only` bundle has verified the chain of custody and not the evidence at the end of it, and telling them otherwise would convert a careful design into a misleading one at the last step.

**Redaction is a decision, not a filter.** Every excerpt in a `redacted` bundle carries the identity of the human who approved that disclosure and the state it was approved against. An automatic redactor that decided what was safe would be making a legal judgment with a regular expression.

---

## 6. Signing

**Status: local digest verification executable; external signing specified.**

The default is unsigned, or locally signed with a key the author controls. That default is not a gap. Everything in §4 works without a signature, because every guarantee in the bundle reduces to a hash comparison a stranger can recompute. Signatures answer a different question — *who produced this bundle* — and that question does not always have a useful answer.

Optional paths, none of which is required:

| Path | What it adds | Status |
|---|---|---|
| Sigstore / Cosign blob signing | Keyless signing bound to an OIDC identity, with an optional transparency log entry | Specified |
| Enterprise PKI | Signatures chaining to an organization's existing certificate authority | Specified |
| Hardware-backed keys | Private key material that never leaves a token or secure enclave | Specified |
| C2PA Content Credentials | An interoperable signed manifest attached to compatible media at the release boundary | Specified |

**The bundle must remain independently hash-verifiable without any of them.** A signing path that becomes load-bearing has moved the root of trust from arithmetic anyone can redo to a certificate authority the reviewer must accept. If Sigstore is unreachable, if the enterprise CA has rotated, if the hardware token is in a drawer in another city, `wi verify-release` still verifies everything except the signature and says exactly that.

**Public transparency logs are opt-in.** Logging a signature publicly publishes a document digest and a signer identity, and both can be sensitive: a hash of an unreleased manuscript, a timestamp that reveals when counsel reviewed something, an identity that reveals who is working on what. Those are real disclosures. They are worth making deliberately and never by default.

---

## 7. Reviewer mode

**Status: specified.**

```
$ wi review release-2026-03-19.wiab
```

Read-only, no editing capability, no workspace required. The reviewer sees:

| Panel | Shows |
|---|---|
| Artifact | The final document as released |
| Proof margin | Per claim: status, anchors, checks run, checks not run |
| Source anchors | The quoted evidence, when the profile includes it |
| Waivers | Every proceed-anyway, with actor, timestamp and reason |
| Decision provenance | For any sentence: which proposals touched it, who accepted them, against which state |
| Unresolved items | Everything the gate held or blocked on, in full |
| Manifest verification | The §4 stage list, live, against the bundle in hand |

Who this is for, named plainly: **counsel** reviewing a filing, **auditors** checking a compliance narrative, **publishers** confirming a manuscript's factual apparatus, **grant review** panels evaluating an application, **board review** of material a director will be asked to approve.

None of them need to edit anything. All of them need to answer the same question — *what can I rely on here, and what should I ask about?* Building a reviewer surface with editing capability would create a second class of author who never agreed to be one, and would put an untracked edit path into a system whose entire value is that edits are tracked.

---

## 8. External provenance compatibility

**Status: specified.**

These are adjacent infrastructure patterns with real communities behind them. **v5 claims no invention over any of them.** The design position is compatibility at the boundary and independence in the core: a v5 workspace must be exportable to each, and must never require any of them to function.

### 8.1 W3C PROV

PROV is the standard vocabulary for provenance interchange. The export mapping:

| PROV term | v5 node |
|---|---|
| `prov:Entity` | `source.version`, `meaning.claim_atom`, `release.artifact` |
| `prov:Activity` | `release.build`, ingest run, atomization run, check execution |
| `prov:Agent` | `authorship.actor`, including `judgment_provider` as a software agent |
| `prov:wasDerivedFrom` | `derived_from`, `built_from` |
| `prov:wasAttributedTo` | `accepted_by` resolved to its deciding actor |
| `prov:wasGeneratedBy` | The activity that produced a node state |

The mapping runs outward only. **PROV does not constrain the internal model.** PROV has no notion of a proof closure, a semantic delta class, a stale anchor or a reliability type, and expressing v5 state in PROV's vocabulary loses all four. An export is a view for interchange; it is not the record.

### 8.2 C2PA

C2PA Content Credentials sit at the **media release boundary** as an interoperable envelope: a signed manifest attached to an image, audio file or video that downstream platforms can read without knowing anything about Writing Intelligence.

Two limits, stated because collapsing them is the obvious mistake:

- **C2PA is not the internal graph database.** Its manifest is a flat assertion set attached to one asset. The authorship graph is a versioned, queryable state store spanning every asset, source, claim and decision in a project. One is an envelope; the other is the correspondence.
- **Proof state must never depend on C2PA availability.** If a platform strips credentials on upload — and platforms do — the bundle's guarantees are unchanged, because they never rested on the envelope surviving transit.

### 8.3 Sigstore

Sigstore provides keyless signing bound to an identity, with an optional transparency log. It is the least burdensome credible signing path for open work, which is exactly why it is listed as an option rather than a requirement: see §6.

### 8.4 The in-toto pattern

in-toto's contribution is a shape worth borrowing directly: **each stage of a build emits immutable, attributable metadata about what it consumed and what it produced**, and the chain of those attestations is what gets verified.

The authorship build has eight stages, and each emits a link:

```
ingest → normalize → analyze → propose → decide → verify → render → attest
```

| Stage | Emits |
|---|---|
| `ingest` | Source identities, raw-byte digests, quarantine findings |
| `normalize` | Derived objects, extractor identity and version |
| `analyze` | Claim atoms, anchors, candidate retrievals |
| `propose` | Proposal objects with semantic deltas |
| `decide` | Decision records bound to target states |
| `verify` | Check results, judgment records, gate evaluation |
| `render` | Artifacts, renderer identities and digests |
| `attest` | The attestation over each artifact and its closure |

Software supply chains verify that a binary came from the source it claims. This is the same verification applied to a sentence. The analogy is the point, and the credit for the shape belongs upstream.

---

## 9. Supply-chain security for the tool itself

**Status: reproducible skill bundle executable; SBOM and signed build attestations specified.**

A tool that sells provenance holds itself to a high provenance standard, or it is asking for a trust it will not extend.

| The project publishes | For |
|---|---|
| Source commit for every release | Anyone reconstructing what shipped |
| Toolchain versions | Anyone reproducing a build |
| Dependency lockfiles | Auditing what code is in the artifact |
| Build provenance | Confirming the artifact came from the named commit |
| Artifact checksums | Verifying a download without trusting the transport |
| Signed build attestations *(specified)* | Binding the build to a signer |
| SBOM for compiled binaries *(specified, and only where compiled binaries exist)* | Vulnerability tracking against components |
| Reproducible-build status per target | Knowing which targets reproduce byte-for-byte and which do not |

Two of those rows are honest today rather than aspirational, and they are worth naming:

**`scripts/build-skill.sh` already produces a byte-reproducible bundle**, and **CI already fails if two builds of the same tree disagree.** That is a small guarantee with a specific meaning: the distributed skill bundle is a deterministic function of the repository tree, so anyone can rebuild it and compare digests. It is not a claim about compiled binaries, because there are none.

**There is no compiled core, no Rust core and no daemon in this repository.** The canonical deterministic core of v5.0 is `scripts/wi.py`, a stdlib-only Python file. A compiled core is roadmap. The SBOM row above describes what would be published *if and when* compiled binaries exist; it does not describe an artifact that ships today. Stating it the other way — listing an SBOM among the project's current guarantees — would be the exact failure this document exists to make checkable, committed in the section about holding ourselves to the standard.

---

## 10. What is executable and what is specified

| Mechanism | Status |
|---|---|
| `.wiab` deterministic archive construction, `wi bundle` | Executable in `scripts/wi.py` |
| Release manifest with targets, closures, gate, counts | Executable in `scripts/wi.py` |
| The ten `wi verify-release` stages, excluding signatures | Executable in `scripts/wi.py` |
| `WI_RELEASE_TAMPERED` detection and non-zero exit | Executable in `scripts/wi.py` |
| Count expansion to membership via `wi bundle --show` | Executable in `scripts/wi.py` |
| Privacy profiles `full`, `hash-only`, `redacted` | Executable in `scripts/wi.py` |
| Local digest verification without any signature | Executable in `scripts/wi.py` |
| Sigstore, enterprise PKI, hardware-backed keys, C2PA | Specified |
| Transparency log submission | Specified, opt-in by design |
| Reviewer mode `wi review` | Specified |
| W3C PROV export, in-toto link emission | Specified |
| Byte-reproducible skill bundle and CI reproducibility gate | Executable in `scripts/build-skill.sh` and CI |
| SBOM and signed build attestations for compiled binaries | Specified — no compiled binary exists to describe |

---

## Related documents

- [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) — the proof closure this bundle carries and re-verifies
- [`CANONICAL_HASHING.md`](CANONICAL_HASHING.md) — how every digest in the manifest is computed
- [`POLICY_AS_CODE.md`](POLICY_AS_CODE.md) — the policy object bound by `policy_digest`
- [`WORKSPACE.md`](WORKSPACE.md) — the workspace a bundle is cut from, and the lockfile it inherits
- [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md) — what `sources/anchor-index.json` contains
- [`CONSTITUTION.md`](CONSTITUTION.md) — Law L, which this document implements
- [`../v4/ACCOUNTABILITY_LAYER.md`](../v4/ACCOUNTABILITY_LAYER.md) — Law C, which the "checks not run" record enforces
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
