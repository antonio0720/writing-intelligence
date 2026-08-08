# Proof capsules — selective disclosure over a Merkleized closure

**Status: `wi capsule create | inspect | verify` executable in `scripts/wi.py`, including Merkle closure construction and inclusion proof generation and checking. External signing, signing-key isolation and the challenge-response profile are specified and do not ship.**

A release attestation in v5 says: these claims were checked, against these sources, under this policy, by these actors, and here are the digests of every state involved. Verifying it requires the workspace. That is correct inside an organization and useless at its edge, because the party who most needs to check the attestation is the party you cannot hand the workspace to — counsel, a funder, a regulator, a partner, a customer's compliance officer.

The obvious answers are both wrong. Ship the whole workspace and you have disclosed every source, every draft, every internal decision and every rejected proposal to somebody entitled to see one figure. Ship a summary and you have shipped a claim about verification with nothing behind it, which is the failure this project exists to catch.

A proof capsule is the third answer: a self-contained file that lets a recipient verify that a specific disclosed claim belonged to a specific release closure, without receiving the closure. The mechanism is a Merkle commitment over the closure's states, computed at release time, with inclusion proofs for the leaves the producer chose to disclose. What the recipient gains and what they do not gain are both precise, and section 6 is entirely about not overstating the first.

Read this with [`../v5/PROOF_CARRYING_RELEASE.md`](../v5/PROOF_CARRYING_RELEASE.md) for the `.wiab` bundle a capsule is derived from, [`../v5/AUTHORSHIP_GRAPH.md`](../v5/AUTHORSHIP_GRAPH.md) §5 for the ten closure layers, [`../v5/CANONICAL_HASHING.md`](../v5/CANONICAL_HASHING.md) for the digest rules the leaves obey, and [`FEDERATION.md`](FEDERATION.md) for what happens when a capsule crosses an organizational boundary.

**Contents:** [1 The disclosure problem](#1-the-disclosure-problem) · [2 The `.wic` format](#2-the-wic-format) · [3 The five profiles](#3-the-five-profiles) · [4 Merkleized closure](#4-the-merkleized-proof-closure) · [5 Not a blockchain](#5-this-is-not-a-blockchain) · [6 The redaction contract](#6-the-redaction-contract) · [7 Salted commitments](#7-salted-commitments-for-low-entropy-fields) · [8 Signing and key isolation](#8-external-signatures-and-key-isolation) · [9 The command surface](#9-the-command-surface) · [10 Executable and specified](#10-what-is-executable-and-what-is-specified)

---

## 1. The disclosure problem

**Status: specified.** This section is framing; the mechanisms it motivates are marked individually below.

An organization publishes a report containing forty-one verified figures. A regulator asks about three of them. The organization's proof closure for that release contains 2,300 states across the ten layers — every claim atom, every anchor, every source version, every decision, every waiver, every judgment record, the policy state, the renderer identity. Of those, the three figures under question touch perhaps sixty.

Four things are true simultaneously, and no format that ignores any of them is honest:

1. The regulator must be able to verify that the three figures were part of what was attested, and not assembled afterwards.
2. The organization must not be compelled to disclose the other 2,240 states, several of which are under licence terms that prohibit redistribution and several of which are privileged.
3. A digest of a withheld state is not evidence about its content. It proves that *something* with that digest was in the closure. It does not tell the regulator what it was.
4. The organization must not be able to construct a capsule that appears to prove more than it does — and the constraint has to be structural, because the organization writes the capsule.

The fourth is the hard one, and it is why the redaction contract in section 6 is written as a prohibition on rendering rather than a guideline about honesty. A producer who wants to overstate does not have to lie about a digest. They only have to display a withheld source's digest in a column headed *evidence*, and a reader will do the rest.

---

## 2. The `.wic` format

**Status: executable in `scripts/wi.py`.**

A capsule is a deterministic archive. Same closure, same disclosure set, same salt file, same bytes — which matters because two parties comparing capsules should be comparing content and not compression artifacts.

```
report-q3-2026.wic
├── capsule.json               Manifest. Profile, root, producer, disclosure set.
├── closure/
│   ├── root.json              Merkle root, leaf count, ordering rule, algorithm.
│   └── proofs/                One inclusion proof per disclosed leaf.
│       ├── L2-01H8X4...json
│       └── L5-01H8X9...json
├── disclosed/
│   ├── claims/                Full claim atom states, canonically serialized.
│   ├── anchors/               Anchor descriptors for disclosed claims.
│   ├── sources/               Source bytes — present only in `full` and `selective`.
│   └── decisions/             Decision records covering the disclosed states.
├── attestation/
│   ├── release.json           The v5 release attestation, verbatim.
│   └── release.sig            Detached signature. Absent unless signed.
└── verifier/
    └── VERIFY.md              How to check this capsule with no network.
```

The manifest:

```json
{
  "format": "wic/1",
  "capsule_id": "01HQ7K4F9TZ2M8V3XW6RJ0PBNC",
  "profile": "selective",
  "produced_at": "2026-09-14T11:03:22Z",
  "producer": {
    "organization": "Density6 LLC",
    "workspace_root": "sha256:9f14ac6e0b7d5382c1ae44b9d0f7e2a3...",
    "wi_version": "6.0.0",
    "core": "python"
  },
  "release": {
    "attestation_digest": "sha256:44d0b9e17c3a8f52ee1b6c09d7a4f381...",
    "target": "narrative.pdf",
    "target_digest": "sha256:1c9e77a4b0d3f6821ea55b8c4f2079d6..."
  },
  "closure": {
    "algorithm": "sha256",
    "leaf_count": 2300,
    "root": "sha256:7ab3f0c85d19e4762b0fa3c8e15d97b4...",
    "ordering": "layer,logical_id,state_digest",
    "domain": "wi-closure-v6"
  },
  "disclosure": {
    "disclosed_leaf_count": 61,
    "withheld_leaf_count": 2239,
    "withheld_reason_summary": {
      "licence_prohibits_redistribution": 812,
      "not_relevant_to_this_disclosure": 1401,
      "privileged": 26
    },
    "source_bytes_included": true,
    "source_bytes_included_for": 4,
    "source_bytes_withheld_for": 19
  },
  "signature": {"present": false, "reason": "no signing key configured"}
}
```

**`withheld_leaf_count` is mandatory and is not a courtesy.** A capsule that discloses sixty-one leaves out of 2,300 and a capsule that discloses sixty-one out of sixty-one are radically different documents, and a manifest that omits the denominator lets the first be read as the second. This is the same rule that forbids a percentage without a denominator in [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md), applied to disclosure coverage.

**`source_bytes_withheld_for` is separate from `withheld_leaf_count`** because they answer different questions. A source version state can be disclosed — its digest, its retrieval metadata, its byte length — while its bytes are withheld. The recipient then holds a claim, its anchor, and the identity of the document the anchor points into, and cannot open the document. That is a legitimate and common state. It is also the state most likely to be misread, which section 6 addresses directly.

**`core: "python"` records which implementation produced the capsule.** During the dual-core window described in [`MIGRATION_V5_TO_V6.md`](MIGRATION_V5_TO_V6.md), two implementations compute these digests, and a capsule that does not say which one built it cannot participate in a parity investigation.

---

## 3. The five profiles

**Status: `full`, `hash-only`, `redacted` and `selective` executable in `scripts/wi.py`. `challenge-response` specified.**

| Profile | Discloses | Merkle proofs | Intended reader |
|---|---|---|---|
| `full` | Every closure state and every source byte | Not required; the whole closure is present | Internal audit, archival, a successor team |
| `redacted` | Approved excerpts and approved regions only, each carrying its approval record | For disclosed leaves | Counsel, funder, publisher under limited disclosure |
| `hash-only` | Every state's digest; no source bytes at all | For all leaves | A reviewer confirming chain of custody who already holds the sources, or who does not need them |
| `selective` | A producer-chosen subset of leaves, with bytes for a further subset | For disclosed leaves; withheld leaves are commitments only | A regulator asking about three figures out of forty-one |
| `challenge-response` | Nothing in advance. The verifier names leaves; the producer answers with proofs | Generated per challenge | An adversarial verifier who does not trust the producer's choice of what to disclose |

The first three carry forward from the v5 bundle profiles unchanged, and their limits are unchanged with them. `selective` is what the Merkle commitment makes possible: before it, disclosing a subset meant shipping a subset, and a subset of a closure is not verifiable as a subset *of that closure* — it is just a smaller closure, which the producer could have assembled from anything.

**`challenge-response` exists because `selective` has a real weakness and it should be named rather than glossed.** In `selective`, the producer chooses which leaves to disclose. A producer with something to hide discloses the sixty-one leaves that look best. Every inclusion proof verifies; the root is correct; nothing is forged. The verifier has learned that sixty-one particular states were in the closure and nothing about the 2,239 that were not offered.

Challenge-response inverts the choice. The verifier receives the root and the leaf count, then names leaves by index or by predicate, and the producer must answer with inclusion proofs and content. A producer who cannot answer for a leaf they committed to has failed a check they could not have anticipated. It does not ship, it requires an interactive session between two parties, and the reason it is specified rather than built is that it requires a protocol between two live endpoints, which is exactly what v6.0.0 does not have. Naming it here is a statement about what `selective` does not do.

---

## 4. The Merkleized proof closure

**Status: executable in `scripts/wi.py`.**

### 4.1 The leaf

One leaf per closure state. The leaf commits to *which layer* a state occupied, not only to the state — because the same state digest appearing in layer 5 and in layer 8 means different things, and a commitment that could not tell them apart would let a producer present a source version as though it were a verification result.

```rust
/// One state in the proof closure, as committed.
pub struct ClosureLeaf {
    pub layer: u8,                 // 1..=10, per AUTHORSHIP_GRAPH.md §5
    pub logical_id: LogicalId,     // stable identity, never changes
    pub state_digest: Digest,      // SHA-256 over canonical serialization
    pub node_family: NodeFamily,   // source.* | meaning.* | verification.* | ...
}

impl ClosureLeaf {
    /// Domain-separated leaf hash. The 0x00 prefix distinguishes a leaf from
    /// an internal node — see 4.3 for why that separation is required and not
    /// stylistic.
    pub fn hash(&self) -> Digest {
        let mut h = Sha256::new();
        h.update(&[0x00u8]);
        h.update(b"wi-closure-v6\0");
        h.update(&[self.layer]);
        h.update(b"\0");
        h.update(self.logical_id.as_bytes());
        h.update(b"\0");
        h.update(self.state_digest.as_bytes());
        h.update(b"\0");
        h.update(self.node_family.wire_name().as_bytes());
        Digest(h.finalize().into())
    }
}
```

The `\0` separators and the domain string follow the preimage discipline in [`../v5/CANONICAL_HASHING.md`](../v5/CANONICAL_HASHING.md). Without separators, a logical id ending in digits and a layer byte can be reassembled into a different valid preimage, and two distinct leaves collide.

### 4.2 Canonical leaf ordering

Leaves are sorted by `(layer, logical_id, state_digest)`, comparing each field as raw bytes.

**Why the ordering is part of the format.** The root is a function of the leaf sequence. Two implementations that sort differently compute different roots from identical closures, and every capsule one produces fails verification by the other — a failure indistinguishable from tampering. The ordering is declared in `closure.root.json` and repeated in the manifest so that a verifier can check it was the one used rather than assuming.

**Byte comparison, not locale collation.** A locale-aware sort produces different orders on different systems for identifiers containing non-ASCII characters, which is a reproducibility failure that appears only for some users, only for some data, and is close to impossible to diagnose from a root mismatch.

### 4.3 Tree construction

Binary, bottom-up, with two rules that exist to close known attacks.

**Rule one: leaves and internal nodes are prefixed differently.** A leaf preimage begins `0x00`; an internal node preimage begins `0x01`, followed by the left child hash and the right child hash. Without the distinction, an attacker who controls leaf content can submit a leaf whose bytes are the concatenation of two other hashes, and a verifier cannot tell whether a given hash was produced from a leaf or from an internal node. The attack lets a producer present an internal node as a leaf, which is a second-preimage on the tree structure rather than on SHA-256.

**Rule two: an odd node at any level is promoted, never duplicated.** The naive construction duplicates the last node when a level has an odd count. Duplication makes two different leaf sequences produce the same root — the sequence `[A, B, C]` and the sequence `[A, B, C, C]` build identical trees — so a producer can claim a different leaf count for the same root. Promotion carries the odd node up one level unchanged and pairs it at the next.

```rust
fn build(mut level: Vec<Digest>) -> Digest {
    assert!(!level.is_empty(), "a closure with no leaves has no root");
    while level.len() > 1 {
        let mut next = Vec::with_capacity(level.len().div_ceil(2));
        let mut i = 0;
        while i + 1 < level.len() {
            next.push(internal(&level[i], &level[i + 1]));
            i += 2;
        }
        if i < level.len() {
            // Promote. Duplicating here would make [A,B,C] and [A,B,C,C]
            // share a root, and leaf_count would stop being a commitment.
            next.push(level[i]);
        }
        level = next;
    }
    level[0]
}

fn internal(left: &Digest, right: &Digest) -> Digest {
    let mut h = Sha256::new();
    h.update(&[0x01u8]);
    h.update(left.as_bytes());
    h.update(right.as_bytes());
    Digest(h.finalize().into())
}
```

**An empty closure has no root and does not get one.** A tree over zero leaves would have to be either an error or a fixed sentinel, and a sentinel root is a root that verifies — a capsule committing to nothing would present a valid-looking commitment. The construction refuses.

### 4.4 The inclusion proof

```json
{
  "format": "wiproof/1",
  "leaf": {
    "layer": 2,
    "logical_id": "01H8X4KDPQ7R2N6VYB3ZM9TFAC",
    "state_digest": "sha256:e3b0c44298fc1c149afbf4c8996fb924...",
    "node_family": "meaning.claim_atom"
  },
  "leaf_index": 417,
  "leaf_count": 2300,
  "path": [
    {"side": "right", "hash": "sha256:2a7f91c0b48d6e35..."},
    {"side": "left",  "hash": "sha256:cd0e83b5194a7f26..."},
    {"side": "right", "hash": "sha256:6b1d4f8e0c93a572..."},
    {"side": "right", "hash": "sha256:f04a72c9e18b5d3e..."}
  ],
  "root": "sha256:7ab3f0c85d19e4762b0fa3c8e15d97b4..."
}
```

Verification recomputes the leaf hash from the leaf fields, folds the path, and compares against the root in `closure/root.json` — which is compared in turn against the root recorded in the release attestation. Three digests must agree; two agreeing is not enough, because a producer who wrote both the proof and the root file has proved a relationship between two things they control.

**`leaf_index` and `leaf_count` are both carried and both checked.** The path length must equal the number of levels implied by `leaf_count`, and the sides must match the binary expansion of `leaf_index` with promotion accounted for. Omitting them would let a producer supply a shorter path that happens to fold to the root — which, with promotion, is achievable for leaves that were promoted.

### 4.5 What a verifier learns, and what it does not

| The verifier can establish | The verifier cannot establish |
|---|---|
| This leaf was in the closure committed at release time | What the withheld leaves contained |
| The closure had exactly `leaf_count` leaves | That the producer disclosed the relevant ones (see `challenge-response`) |
| The root matches the one in the release attestation | That the sources are true — closure integrity is not source truth |
| A disclosed claim's state digest matches its disclosed content | That an undisclosed source says what an anchor claims about it |

The third row is the boundary v4 set and neither v5 nor v6 relaxes: the closure proves that the checks that were run still apply to the states they were run against. It does not prove that a source told the truth.

---

## 5. This is not a blockchain

**Status: specified.** This section is a statement about what the mechanism is, not a mechanism.

The Merkle tree invites a category error, and the error is worth refusing plainly because a reader who makes it will either dismiss the design or oversell it.

**There is no consensus network.** No nodes, no validators, no agreement protocol, nothing to join. A capsule is a file.

**There is no token, no chain and no global ledger.** Roots are not linked to one another. There is no ordering between the capsules of two organizations, and no global state anybody queries.

**There is no distributed timestamp.** `produced_at` is what the producer's clock said. A capsule proves that a closure had a particular shape; it does not prove *when* it had that shape. Anchoring a root in an external transparency log would provide that, and it is not built — the hook is described in [`../v5/PROOF_CARRYING_RELEASE.md`](../v5/PROOF_CARRYING_RELEASE.md) as opt-in and specified, and remains so.

**There is no immutability guarantee against the producer.** The producer can build a different closure tomorrow and commit to that. What they cannot do is produce two different disclosure sets that both verify against one root, which is the property required and the whole of what is claimed.

What this is: **a local cryptographic commitment to a finite dependency set.** One party computes a root over states they hold, and can later prove membership of individual states without revealing the rest. The technique predates blockchains by fifteen years and does not need one.

The reason to be exact is [Law E](../v5/CONSTITUTION.md). Describing a Merkle commitment as a blockchain claims a trust property — distributed consensus about time and order — that the mechanism does not deliver, in a document whose entire purpose is to make claims checkable.

---

## 6. The redaction contract

**Status: executable in `scripts/wi.py` — the reliability rendering rules below are enforced by `wi capsule inspect` and `wi capsule verify`.**

> A capsule may prove: **a source object with this digest was part of the producer's closure.**
>
> A capsule may not claim, and its rendering may not imply: **you have independently verified the underlying source content** — unless that content is disclosed in the capsule.

**Why this is load-bearing.** It is the exact seam where a careful system becomes a misleading one, and it does not require anybody to lie. A capsule contains a claim atom, an anchor with a `quote_digest`, and a source version state with a digest and a title. Everything present is true and verifiable. Rendered in a table with columns *Claim*, *Source*, *Verified*, it reads to a reviewer as though the source was checked. The reviewer holds no source bytes and could not have checked anything.

The four reliability types in [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) do not survive a capsule boundary unchanged, and the transformation is mechanical:

| In the workspace | With source bytes disclosed | With source bytes withheld |
|---|---|---|
| `verified` | `verified` — the recipient can re-run the comparison | `verified_by_producer` — the recipient verified the chain, not the evidence |
| `measured` | `measured`, denominator disclosed | `measured_by_producer`, denominator disclosed or the measure is withheld entirely |
| `judged` | `judged` | `judged` — unchanged; a judgment was never independently checkable |
| `human-declared` | `human-declared` | `human-declared` |

`verified_by_producer` is a distinct wire value and not a presentation variant. A recipient's tooling must be able to filter on it, count it, and refuse a document where it exceeds a threshold. Rendering it as `verified` with a footnote is the failure this table exists to prevent — footnotes are not read, and the word in the column is what gets quoted.

**`wi capsule verify` states the limitation in its own output**, following the pattern the v5 `hash-only` verifier already uses:

```
Profile: selective
Root:    sha256:7ab3f0c8...  (matches attestation)

  61 of 2300 closure leaves are disclosed. 2239 are committed to but not
  disclosed; their digests prove membership and say nothing about content.

  Source bytes are present for 4 of 23 referenced source versions. For the
  other 19, this capsule establishes that a source with the stated digest
  was in the producer's closure. It does not let you read that source or
  confirm it says what the anchor claims.

  38 claims are marked verified_by_producer. You have verified the chain
  of custody for those claims. You have not verified the evidence at the
  end of it.

VALID — as a commitment. Coverage is partial by construction.
```

The last line separates two questions a single word would merge. *Valid* answers whether the cryptography holds. *Coverage is partial* answers whether it establishes what a reader wants. A verifier that printed only `VALID` would be technically correct and would be read as an endorsement of the content.

**Redaction is a decision, not a filter.** Carried forward from v5 without change: every excerpt in a `redacted` or `selective` capsule carries the identity of the human who approved that disclosure and the state it was approved against. An automatic redactor deciding what is safe to disclose would be making a legal judgment with a pattern match.

---

## 7. Salted commitments for low-entropy fields

**Status: executable in `scripts/wi.py` for commitment construction and revelation checking.**

A withheld leaf commits to a state digest. When the state's canonical serialization has low entropy, the commitment leaks: a recipient who suspects a withheld field is `"approved"` or `"denied"` hashes both and compares. Two guesses recover the value. Boolean fields, small enumerations, dates within a known window and monetary amounts in a known band are all in this category.

The commitment is therefore salted:

```
commitment = sha256(domain || "\0" || salt || "\0" || canonical_value)
```

with `domain` naming the field's role (`wi-commit-v6/decision.outcome`), `salt` at least 32 bytes from a cryptographic source, generated per field per capsule and never reused. Salts live in a separate `salts.json` that is not part of the capsule and is retained by the producer.

Revelation discloses the value and its salt. The recipient recomputes the commitment and compares against the committed leaf. A producer cannot reveal a different value later, because they would have to find a second salt producing the same commitment.

**Per-field salts, never one capsule salt.** With a shared salt, revealing any one field discloses the salt, and every other low-entropy field in the capsule becomes guessable again — one revelation unwinding the protection on all the rest.

> **This is a commitment scheme with selective revelation. It must not be described, marketed or documented as a zero-knowledge proof.**

**Why the prohibition is explicit.** A commitment reveals nothing about a value until the value is revealed, and then reveals the value exactly. A zero-knowledge proof establishes a *predicate* over a hidden value — that a withheld amount is under a threshold, that a withheld date precedes another — while keeping the value hidden. This design does neither of those things and cannot be extended to by adding salt. Calling it zero-knowledge would claim a property that determines whether a disclosure is legally adequate, and a counterparty relying on that description would be relying on something false.

What a recipient can do with a salted commitment is exactly two things: verify a revealed value, and observe that a commitment exists. There is no third capability, and any presentation implying one is a defect.

---

## 8. External signatures and key isolation

**Status: specified.** No signing, no key handling and no signature verification ships in v6.0.0. A capsule verifies on digests alone; `signature.present` is `false` and the reason is stated.

**The signature covers the canonical release attestation digest, not a filename.**

```
signed_payload = attestation_digest            // 32 bytes, nothing else
```

**Why.** A capsule renamed from `report-q3-2026.wic` to `2026-Q3-final.wic` in an email thread is the same capsule and must still verify. A capsule whose bytes were altered is not, and must not. A signature over a filename or over a transport envelope gets both cases backwards: it breaks on the harmless operation and holds through the harmful one, and users respond to a signature that breaks during normal handling by ignoring signature failures. Signing the digest of the attested content is the only binding that fails exactly when something is wrong.

**The signer runs outside the worker runtime, and receives four values.**

```rust
/// Everything a signing service is given. It receives no graph handle, no
/// workspace path, no source bytes and no judgment output.
pub struct SigningRequest {
    pub attestation_digest: Digest,   // what is being signed
    pub actor: ActorRef,              // who is authorizing this signature
    pub release_target: ReleaseRef,   // what release this attestation covers
    pub authorization: DecisionRef,   // the local decision that permits it
}
```

**Why isolation matters more here than anywhere else in the system.** A signature is the one output that carries weight outside the workspace. Everything else the system produces can be recomputed and checked by anybody holding the inputs; a signature is a claim that a specific key-holder assented, and it cannot be re-derived. A worker runtime that could reach the key could produce that assent as a side effect of a build, and no downstream verifier could tell the difference between a signature a person authorized and one a process emitted.

The capability token in [`AUTONOMOUS_EXECUTION.md`](AUTONOMOUS_EXECUTION.md) §6 denies `release.sign` and `decision.sign` unconditionally, and the denials are written out rather than omitted. This section is the other half of the same rule: the worker cannot ask, and the signer would not have anything to sign if it did, because the signer takes a digest and not a workspace.

**Signature verification is optional and is never load-bearing for closure verification.** A recipient with no key material verifies the Merkle root, every inclusion proof and every disclosed state digest, and reaches `VALID — as a commitment`. The signature adds the assertion that a named key-holder assented. A design in which verification required a key would make every offline recipient dependent on key distribution to check arithmetic they can do themselves.

---

## 9. The command surface

**Status: executable in `scripts/wi.py`.**

```
wi capsule create --release <target> --profile <profile> [--disclose <selector>...] --out <path>
wi capsule inspect <path>
wi capsule verify  <path> [--attestation <path>]
```

`create` builds the closure, sorts leaves, constructs the tree, generates an inclusion proof per disclosed leaf, copies disclosed content, and writes the manifest. It refuses when a requested disclosure has no approval record under a profile that requires one, and it refuses when the disclosure set is empty — an empty capsule commits to a root and discloses nothing, and there is no reader for whom that is the intended artifact rather than a mistake.

`inspect` prints the manifest, the profile, the disclosure counts with their denominators, and the reliability breakdown including the `*_by_producer` counts. It performs no cryptographic verification and says so, because an inspection that looked like a verification is the same category error as a `VALID` line with no coverage statement.

`verify` recomputes every leaf hash from disclosed content, folds every inclusion proof, compares the root against `closure/root.json` and against the release attestation, and prints the section 6 output. It exits non-zero on any mismatch. It requires no network, no key material and no workspace.

**`verify` runs against a capsule alone.** A verifier that needed the producer's workspace to check a capsule would defeat the purpose of the format at the first step.

### 9.1 A tampered capsule

Two words changed inside a disclosed claim atom. The archive is otherwise untouched, the manifest is unmodified, every inclusion proof is byte-identical to the one the producer generated.

```
Profile: selective
Root:    sha256:7ab3f0c8...  (matches attestation)

  Leaf L2-01H8X4KDPQ7R2N6VYB3ZM9TFAC
    disclosed content digest  sha256:b19d70e4f2c8a635...
    committed state digest    sha256:e3b0c44298fc1c14...
    MISMATCH

  1 of 61 disclosed leaves does not match its commitment. The inclusion
  proof for this leaf is internally valid — it folds to the stated root —
  which means the commitment is intact and the disclosed content is not
  the content that was committed.

INVALID — disclosed content does not match the closure it claims to be from.
```

**The distinction in the middle paragraph is the useful part.** A reader who sees `INVALID` will ask which half failed, and the two halves have different meanings. A folding failure says the proof is malformed or the root is wrong. A content mismatch with a well-formed proof says the commitment is sound and somebody edited what was disclosed against it — which localizes the alteration to one leaf and rules out a corrupted archive.

### 9.2 A capsule whose closure has moved

A capsule is a commitment to a closure as it stood at release time. It does not track the workspace afterwards, and it must not: a capsule that could change after being handed to a regulator would be worthless as evidence.

The consequence is that a valid capsule and a current release are different assertions. A source acquires a new version, the anchors into the old version go stale, and `wi verify-release` in the producer's workspace reports `INVALID` for that release — exactly as [`../v5/AUTHORSHIP_GRAPH.md`](../v5/AUTHORSHIP_GRAPH.md) §5 describes. The capsule in the regulator's hands still verifies, and still should: it is an accurate record of what was committed on the day it was produced.

**Nothing in the capsule reports this, because nothing in the capsule can.** A capsule is a file with no network access and no knowledge of the workspace it came from. Producing a capsule therefore obliges the producer to a live release, not to a snapshot of one, and a `superseded_by` field naming a later capsule is the mechanism — specified, not built. What is built is the honest boundary: `wi capsule verify` answers whether the capsule is internally sound, and never claims the release it describes is still current.

---

## 10. What is executable and what is specified

| Mechanism | State at v6.0.0 |
|---|---|
| `.wic` archive layout and `wic/1` manifest | Executable in `scripts/wi.py` |
| Closure leaf construction, domain separation, canonical ordering | Executable in `scripts/wi.py` |
| Merkle tree with leaf/internal prefixes and odd-node promotion | Executable in `scripts/wi.py` |
| Inclusion proof generation and verification | Executable in `scripts/wi.py` |
| `wi capsule create \| inspect \| verify` | Executable in `scripts/wi.py` |
| Profiles `full`, `hash-only`, `redacted`, `selective` | Executable in `scripts/wi.py` |
| Redaction contract, `*_by_producer` reliability values, coverage output | Executable in `scripts/wi.py` |
| Salted commitments and revelation checking | Executable in `scripts/wi.py` |
| Profile `challenge-response` | Specified. Requires an interactive session between two endpoints |
| External signing, key isolation, `SigningRequest` | Specified. No key handling of any kind ships |
| Signature verification | Specified |
| Transparency log anchoring for a trusted timestamp | Specified, opt-in by design, carried forward from v5 |

---

## Related documents

- [`../v5/PROOF_CARRYING_RELEASE.md`](../v5/PROOF_CARRYING_RELEASE.md) — the `.wiab` bundle, the release attestation and the ten verify stages
- [`../v5/AUTHORSHIP_GRAPH.md`](../v5/AUTHORSHIP_GRAPH.md) — the ten closure layers a capsule commits over
- [`../v5/CANONICAL_HASHING.md`](../v5/CANONICAL_HASHING.md) — the digest and preimage rules the leaves obey
- [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) — the four reliability types the redaction contract transforms
- [`FEDERATION.md`](FEDERATION.md) — what a capsule means when it crosses an organizational boundary
- [`PACKAGE_SYSTEM.md`](PACKAGE_SYSTEM.md) — why pack digests belong in the closure a capsule commits to
- [`AUTONOMOUS_EXECUTION.md`](AUTONOMOUS_EXECUTION.md) — the capability token that denies `release.sign`
- [`../v4/PROOF_PROTOCOL.md`](../v4/PROOF_PROTOCOL.md) — the boundary between closure integrity and source truth

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
