# Federation — meaning across organizational boundaries

**Status: specified.** No remote, no transport, no network fetch, no signature verification and no delta package ships in v6.0.0. `wi capsule` produces and verifies a portable proof closure on a local filesystem, and a capsule handed to a partner on a disk is the only cross-organization artifact that exists today. Everything below describes the protocol that would carry one over a wire, and none of it runs.

Two organizations write about the same thing. A regulator and a filer. A publisher and a research institute. A prime contractor and four subcontractors, each maintaining the specification for the part they build. Every one of those pairs has the same problem: they need each other's meaning, and neither of them may hand the other write access to their own record of what is true.

The industry answer is a shared workspace. One tenant, one schema, one policy, one administrator, and a governance conversation about who is allowed to edit what. It works until the two organizations disagree — at which point the shared workspace has to hold two incompatible answers, and it cannot, because it was built on the assumption that agreement is the normal state and conflict is an exception to be resolved.

Federation inverts that. Each organization holds its own authoritative graph. Meaning moves between them as a signed, immutable, content-addressed package that arrives as a *proposal* — inspected, policy-checked, conflict-analyzed and accepted or refused under the receiver's own authority, exactly as if a local editor had proposed it. Disagreement is not an exception. It is the case the protocol is designed around, because [Law Q](CONSTITUTION.md) already says a semantic disagreement is preserved until somebody with authority resolves it, and a disagreement that crosses an organizational boundary is the one nobody can resolve by asking around the office.

Read this with [`CONSTITUTION.md`](CONSTITUTION.md) for Laws O, P and Q, [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) for the conflict vocabulary the receiver runs locally, [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) for the object format that crosses the boundary, and [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md) for the ingestion boundary this reuses without modification.

**Contents:** [1 The two failures](#1-the-two-failures-federation-must-avoid) · [2 Nothing fetched mutates main](#2-the-governing-rule-nothing-fetched-mutates-main) · [3 Semantic remotes](#3-semantic-remotes-over-immutable-object-graphs) · [4 Protocol primitives](#4-the-remote-protocol-primitives) · [5 `SignedDeltaPackage`](#5-signeddeltapackage) · [6 The receiver flow](#6-the-receiver-flow) · [7 Approval is evidence, not authority](#7-a-partners-approval-is-evidence-not-authority) · [8 Concept identity without a global ontology](#8-cross-organization-concept-identity-without-a-global-ontology) · [9 Federation threats](#9-threats-specific-to-federation) · [10 Quarantine and inbound branches](#10-quarantine-and-inbound-branches) · [11 What does not cross](#11-what-does-not-cross-the-boundary) · [12 Executable and specified](#12-what-is-executable-and-what-is-specified)

---

## 1. The two failures federation must avoid

**Status: specified.**

Every federation design fails in one of two directions, and they are opposites, which is why designs oscillate between them.

**The first failure is the shared workspace.** One graph, many organizations, permissions as the only boundary. The failure is not that permissions are weak. It is that a permission model answers *who may write* and never answers *whose meaning this is*. When the regulator and the filer disagree about whether a disclosure obligation applies, the shared workspace holds one value for that node. Somebody wins. The record of the other position exists, if at all, as a comment. Six months later nobody can reconstruct what the filer actually asserted at filing time, because the filer's assertion was overwritten by the resolution of an argument.

**The second failure is the export.** Each organization keeps its own system and they exchange documents. Nothing is shared but prose. The failure here is that all structure is destroyed at the boundary: the claim atoms, the anchors, the verification results, the decisions and the reliability basis go in, and a PDF comes out. The receiver re-derives everything by reading, which means the receiver's structure is a *new interpretation* of the sender's meaning with no cryptographic relationship to it. When the sender later corrects the underlying source, nothing on the receiving side knows.

Federation is the position between the two, and the position is not a compromise. It is a specific claim: **the object graph crosses the boundary intact and the authority does not.**

| | Shared workspace | Document export | Federation |
|---|---|---|---|
| Structure survives the boundary | yes | no | yes |
| Receiver keeps its own authoritative state | no | yes | yes |
| Disagreement can be held by both sides | no | not detectably | yes |
| Sender can invalidate a receiver's proof | yes, silently | no, ever | yes, visibly |
| Receiver can refuse | only by permission | trivially | as a first-class outcome |

The fourth row is the one that decides the design. If the sender corrects a source and the receiver's proof depended on it, the receiver has to learn that its proof is stale. In a shared workspace it happens invisibly and the receiver may never notice. In a document export it cannot happen at all, and the receiver keeps citing a superseded figure indefinitely. Federation makes it an explicit, dated, refusable event.

---

## 2. The governing rule: nothing fetched mutates `main`

**Status: specified.**

> **Nothing that arrives from a remote may mutate the local `main` branch, alter a local authoritative state, invalidate a local proof, or change a local policy as a direct consequence of arriving.** Every inbound object lands on an inbound branch or in quarantine. It becomes part of local authoritative state only through a local authority decision, recorded locally, under the receiver's own policy.

**Why this is load-bearing.** Every remaining property of federation is a consequence of it. If a fetch could write to `main`, then the sender's key is a write credential on the receiver's graph, and the entire authority model of [Law O](CONSTITUTION.md) — scoped, expiring, explicitly granted authority — is bypassed by anybody who is on the remote list. A compromised partner would not need to attack the receiver; it would only need to push.

The rule is stronger than "fetch is read-only", and the distinction matters. Fetch obviously does not write to `main`. The subtle version is *invalidation*: a naive design lets an inbound correction to a shared source object mark the receiver's dependent proofs stale, because the receiver's proofs genuinely do depend on that source and staleness is genuinely correct. That is still a remote-triggered mutation of local state, and it is enough to be an attack: a partner who repeatedly pushes trivial revisions to a source can hold every dependent proof in the receiver's workspace permanently stale, and the receiver's gate will block releases it should have passed.

The resolution is that an inbound source revision produces a **notice**, not an invalidation. The notice is a first-class local object. It says: a remote claims the source you depend on has a newer state, here is its digest, here is the sender, here is the signature. Local proofs remain in whatever state they were in. A local actor with authority decides whether to adopt the new source version, and adopting it is what invalidates the dependent proofs — a local decision with a local decision record, as [Law J](../v5/CONSTITUTION.md) requires.

---

## 3. Semantic remotes over immutable object graphs

**Status: specified.**

A remote is a named endpoint plus a trust configuration. It is not a mirror and it is not a replica: two workspaces federating do not converge on the same graph, and a design goal of convergence would reintroduce failure one from section 1.

```json
{
  "format": "wiremote/1",
  "name": "regulator",
  "endpoint": "https://graph.example-regulator.gov/wi",
  "identity": {
    "organization": "Example Regulatory Authority",
    "key_id": "erka-2026-signing-01",
    "public_key_digest": "sha256:6f2b90c1e4a87d33b5e1cc0a94f7d2e8...",
    "pinned_at": "2026-03-04T09:12:00Z",
    "pinned_by": "actor:human:antonio",
    "rotation_policy": "manual_only"
  },
  "trust": {
    "accepts_inbound": true,
    "inbound_target": "branch:inbound/regulator",
    "auto_merge": false,
    "max_package_bytes": 268435456,
    "accepted_schema_versions": ["wi-node/5", "wi-node/6"],
    "minimum_policy_profile": "standard",
    "accepted_concept_relations": ["exact", "narrower", "broader"]
  },
  "obligations": {
    "verify_signature": "required",
    "verify_base_relationship": "required",
    "run_local_policy": "required",
    "run_local_proof_obligations": "required",
    "require_local_decision": "required"
  }
}
```

`auto_merge` exists in the schema and its only permitted value is `false`. It is written out rather than omitted because a field that is absent invites a future implementer to add it with a permissive default; a field that is present, documented and pinned to one value states that the question was asked and answered. The same reasoning governs the `denied` list in the capability token of [`AUTONOMOUS_EXECUTION.md`](AUTONOMOUS_EXECUTION.md) §6.

**`rotation_policy: manual_only`** means a key rotation announced *by the remote* is not honored automatically. A remote that can rotate its own pinned key by announcing a rotation can be impersonated by anybody who compromises the transport once: the attacker announces a rotation to a key they hold, and every subsequent package verifies. Rotation is a local decision with a local record, taken by a human who confirmed the new key out of band.

**The graph is immutable and content-addressed, which is what makes any of this possible.** A node state is identified by `state_digest` over its canonical serialization ([`../v5/CANONICAL_HASHING.md`](../v5/CANONICAL_HASHING.md)). Two organizations that received the same object from the same origin compute the same digest without coordinating, without a shared database and without trusting each other's implementation. That property is the whole transport: a delta package does not have to say *what changed* in a form the receiver must trust, because the receiver recomputes every digest and finds out.

---

## 4. The remote protocol primitives

**Status: specified.**

Six operations. All of them are reads except `push`, and `push` writes into the *receiver's* inbound area, never into the receiver's authoritative state.

| Operation | Direction | Effect on receiver's `main` | Notes |
|---|---|---|---|
| `advertise` | pull | none | Sender returns branch heads, root digests and schema version. No object bodies. |
| `have` | pull | none | Sender returns which of a digest set it holds. Used to compute a minimal transfer. |
| `fetch-objects` | pull | none | Receiver requests specific digests. Sender returns exactly those bodies. |
| `fetch-closure` | pull | none | Receiver requests the transitive proof closure of one release attestation. |
| `push` | push | none | Sender delivers a `SignedDeltaPackage` to the receiver's inbound area. |
| `notify` | push | none | Sender states that an object the receiver holds has a successor. Produces a notice object. |

**`fetch-objects` takes digests, never names.** The receiver names the exact bytes it wants and verifies on arrival that the bytes hash to the digest it asked for. A sender that returns different content returns an object that fails its own address, and the fetch fails — not because the receiver trusts the sender's honesty, but because a content address is a verifiable claim. Requesting by name (`give me the current definition of "covered entity"`) would make the sender the authority on what that name resolves to, at the moment of the request, with no way for the receiver to detect a substitution.

**`advertise` returns no object bodies**, so discovering that a partner has changed something does not require accepting anything from them. This is what lets a receiver decide, before transferring a byte, that a package is out of policy — a schema version it does not accept, a size beyond its ceiling, a signing key it has not pinned.

**Every operation is subject to the ingestion boundary in [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md).** Bytes arriving over a remote are source bytes. They are quarantined before parse, parsed out of process under the ceilings described in [`CAPABILITY_SECURITY.md`](CAPABILITY_SECURITY.md) §5, and never concatenated into a judgment prompt as instruction. A remote is a network-shaped source, and [Law F](../v5/CONSTITUTION.md) does not weaken because the source arrived over TLS from an organization with a contract.

---

## 5. `SignedDeltaPackage`

**Status: specified.**

The unit that crosses the boundary. It is not a diff in the textual sense; it is a set of immutable object states, the base they were derived from, and a signature over a canonical digest of the whole thing.

```rust
/// A set of object states offered by one organization to another.
/// Immutable. Content-addressed. Signed over `canonical_digest`.
pub struct SignedDeltaPackage {
    pub format: &'static str,          // "widelta/1"
    pub package_id: Uuid,              // UUIDv7-shaped, sender-assigned
    pub sender: RemoteIdentity,

    /// The state the sender believes the receiver already holds. If the
    /// receiver does not hold it, the package cannot be applied without a
    /// rebase the receiver performs and decides on.
    pub base_root: StateDigest,

    /// The root the sender's branch reached after applying these objects.
    pub result_root: StateDigest,

    /// Every object state offered. Each carries its own state digest; the
    /// receiver recomputes all of them and rejects the package on any
    /// mismatch rather than trusting the sender's arithmetic.
    pub objects: Vec<ObjectState>,

    /// Decisions taken on the sending side. Evidence of what the sender
    /// approved. Never authority over the receiver — see section 7.
    pub sender_decisions: Vec<DecisionRecord>,

    /// Concept mappings the sender asserts between its identifiers and the
    /// receiver's. Every one arrives with reliability basis `judged` unless
    /// it names a shared external identifier. See section 8.
    pub concept_mappings: Vec<ConceptMapping>,

    pub schema_version: String,        // "wi-node/6"
    pub policy_profile_at_send: String,// sender's profile, for the record only
    pub created_at: Timestamp,

    /// SHA-256 over the canonical serialization of every field above.
    pub canonical_digest: Digest,
    pub signature: Signature,          // over canonical_digest, not over a filename
}
```

**The signature covers `canonical_digest`, not a filename and not a transport envelope.** A package renamed in transit still verifies; a package whose contents were altered does not. This is the same rule the release attestation follows in [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) §7, and for the same reason: filenames are not part of what was attested to, and treating them as though they were produces a signature that breaks on harmless operations and holds on harmful ones.

**`base_root` is mandatory and is not decoration.** A package that does not state what it was derived from cannot be positioned in the receiver's history, and a receiver that applies it anyway is applying an unordered change to an ordered structure. Section 6 step 2 describes the four base relationships and what each one means.

**`policy_profile_at_send` is recorded and never enforced.** The receiver runs its own policy. The field exists so that a later reviewer can see that the sender committed under `standard` while the receiver requires `regulated` — which is a `policy` conflict in the vocabulary of [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) §4.1, and is exactly the kind of divergence that is arithmetically invisible and consequentially large.

---

## 6. The receiver flow

**Status: specified.**

Eight steps, in this order. The order is not an implementation preference; each step exists to make the next one meaningful, and a reordering produces a specific defect named beneath the table.

| # | Step | Refuses when | On refusal |
|---|---|---|---|
| 1 | Verify signature | Key not pinned, signature invalid, digest mismatch | Package quarantined, nothing materialized |
| 2 | Verify base-root relationship | Base unknown to receiver, or ambiguous | Package held, receiver may request `fetch-objects` for the missing base |
| 3 | Materialize proposal branch | Any object body fails its own digest | Branch discarded whole; no partial materialization |
| 4 | Run local policy | Schema version out of range, size ceiling, capability requirement | Branch retained, marked `policy_refused`, human notified |
| 5 | Run local proof obligations | Obligation cannot be discharged locally | Branch retained, obligations reported unmet |
| 6 | Compute local semantic conflicts | Never refuses; conflicts are output | Conflict set attached to the branch |
| 7 | Require local authority decision | No local actor holds authority over the affected scope | Held indefinitely; a package never times out into acceptance |
| 8 | Merge on local acceptance | — | Merge proceeds under [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) |

**Step 1 before step 3.** Materializing before verifying means unverified object bodies have been written into the receiver's object store. Even on an inbound branch that is a foothold: the receiver now holds addressable content it did not authenticate, and a later reader that resolves a digest cannot tell whether that object arrived verified.

**Step 2 before step 3.** Without the base relationship the receiver cannot tell a fast-forward from a divergent history from a replay of a package it already refused. Four relationships are distinguished:

| Relationship | Meaning | Handling |
|---|---|---|
| `descends_from_local_head` | Sender's base is the receiver's current head | Cleanest case; still requires steps 4 through 8 |
| `descends_from_local_ancestor` | Sender branched from an older local state | Divergent; conflict computation in step 6 does real work |
| `unknown_base` | Receiver has never held `base_root` | Held. Receiver may fetch the base, or refuse the package as unpositionable |
| `already_applied` | `result_root` is already an ancestor of local head | No-op, recorded. Not an error, and not silently discarded |

`already_applied` is separated from the clean case deliberately. A resent package is ordinary — a partner retries after a timeout — and treating it as an error trains people to ignore federation errors. Treating it as a fresh application is worse: it would replay decisions that were already taken and produce duplicate decision records for one act.

**Step 4 before step 5.** Policy determines which obligations apply. Running obligations first and policy second means the receiver has spent effort discharging obligations under the wrong profile, and — the part that matters — may report obligations *met* that the correct profile would not have accepted.

**Step 5 before step 6.** An unmet proof obligation is not a conflict. It is a statement that the inbound material cannot yet be evaluated as a proposal at all. Computing conflicts first produces a conflict report over material that was never admissible, and a human reads a conflict list believing the underlying evidence was sound.

**Step 7 cannot be satisfied by the package.** There is no field in `SignedDeltaPackage` that can grant local authority, and no combination of sender decisions that discharges it. Section 7 is the whole of why.

**Nothing about step 8 is special because the material came from a remote.** By step 8 the inbound branch is an ordinary local branch carrying an ordinary local proposal, and it merges under the ordinary merge protocol, with the ordinary conflict vocabulary and the ordinary prohibition on splitting the difference. That is the intended end state: federation delivers material *to* the local process rather than around it.

---

## 7. A partner's approval is evidence, not authority

**Status: specified.**

> **A partner's approval is evidence that the partner approved it; it is not authority to mutate your workspace.**

`sender_decisions` in a delta package is a list of real `DecisionRecord` objects, correctly formed, correctly hashed, correctly bound to exact state digests, and signed. Every one of them is true. A named actor at the sending organization did approve that exact state at that exact time, and the receiver can verify it. None of that grants anything.

**Why the distinction is not pedantry.** Authority under [Law O](CONSTITUTION.md) is a grant with a scope, an issuer, an expiry and a recorded basis, and it is issued *within* the workspace it applies to. A grant issued elsewhere is a fact about elsewhere. Treating it as effective here would mean that the set of actors who can write to a workspace is the union of every actor at every organization it federates with — a set that grows when a partner hires somebody, that shrinks when a partner fires somebody, and that the local workspace cannot enumerate.

**The failure this prevents is not usually malicious.** The common case is a partner who is genuinely more expert and genuinely correct. Their analyst approved the corrected figure; the receiver's copy is wrong; adopting it automatically saves an obvious round trip. It works for months. Then the partner's analyst approves something under a policy profile the receiver does not accept, or approves a claim whose supporting anchor points into a source the receiver never received, and the receiver's release carries a `verified` result that no local process ever produced. The reliability contract in [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) — that `verified` means a deterministic comparison was actually executed — is broken by a convenience nobody remembers adding.

What the sender's decision *does* do, in the receiver's workspace, is rendered explicitly:

```json
{
  "format": "wiexternal-decision/1",
  "kind": "external_decision_evidence",
  "reliability_basis": "human-declared",
  "asserted_by": {
    "actor_type": "external_import",
    "organization": "Example Regulatory Authority",
    "actor_ref": "actor:human:j.okafor@example-regulator.gov"
  },
  "target_state_digest": "sha256:c81d4f2a90b3e57c...",
  "decision": "approved",
  "decided_at": "2026-05-19T14:02:11Z",
  "signature_verified": true,
  "grants_local_authority": false,
  "note": "Evidence that the sender approved this state. Not a local grant."
}
```

`actor_type` is `external_import` — one of the seven actor types in the v5 constitution — and never `human`. A remote human is not a local human. `grants_local_authority` is present and pinned to `false` for the same reason `auto_merge` is: the field states that the question was asked.

---

## 8. Cross-organization concept identity without a global ontology

**Status: specified.**

[Law G](../v5/CONSTITUTION.md) says meaning has identity independent of wording. Within one workspace that identity is a `logical_id`. Across two workspaces it is not, and cannot be: two organizations that never coordinated assign different identifiers to the same concept, and there is no mechanism by which they would collide correctly.

### 8.1 Why one global ontology makes federation brittle

The tempting fix is a shared registry: everybody binds their concepts to a common vocabulary, and identity across the boundary is identifier equality. It fails in four ways, and the fourth is the one that is fatal.

1. **It requires agreement before exchange.** Two organizations cannot exchange anything until they have negotiated a vocabulary covering everything they might exchange. The negotiation is the project.
2. **It cannot represent partial correspondence.** A regulator's *covered entity* and a filer's *reporting subsidiary* overlap without matching. A registry that must choose forces one of them to be wrong.
3. **It has an owner.** Whoever maintains the registry decides what concepts exist. That is an authority relationship dressed as a data format, and organizations with genuine adversarial interests will not accept it.
4. **It makes disagreement unrepresentable.** If identity is registry membership, then two organizations that disagree about whether two concepts are the same have no way to record the disagreement — one of them must edit the registry, and the edit changes the other's meaning. That is failure one from section 1, arriving through the schema instead of through the permission model.

The fourth is fatal because disagreement about *whether two things are the same thing* is not an edge case in federation. It is the substance of most cross-organizational work.

### 8.2 `ConceptMapping` and `MappingRelation`

Identity across the boundary is an asserted, directional, refusable *relation* between two locally-owned identifiers. It is an object in the graph, subject to every rule that governs other objects, including reliability basis.

```rust
pub enum MappingRelation {
    /// The two concepts are the same concept. The strongest claim, and the
    /// only one under which a proof about one may be reused for the other.
    Exact,
    /// The local concept is strictly contained by the remote concept.
    Narrower,
    /// The local concept strictly contains the remote concept.
    Broader,
    /// The concepts are connected and neither contains the other. Carries no
    /// proof-reuse permission whatsoever.
    Related,
    /// Somebody looked and could not decide. A first-class outcome, and the
    /// default for anything a model proposed and no human accepted.
    Unresolved,
}

pub struct ConceptMapping {
    pub local_concept: LogicalId,
    pub remote_concept: RemoteConceptRef,   // remote name + remote logical id
    pub relation: MappingRelation,

    /// `judged` when proposed by reasoning. `verified` only when established
    /// by a shared external identifier both sides can resolve independently.
    /// A judgment provider may never emit `verified` here or anywhere.
    pub reliability_basis: ReliabilityBasis,

    /// Present only when `reliability_basis` is `verified`.
    pub shared_identifier: Option<SharedIdentifier>,  // e.g. LEI, ISO code, DOI

    /// Present only when a local actor with authority accepted it.
    pub accepted_by: Option<DecisionRef>,

    pub proposed_by: ActorRef,
    pub rationale: String,
    pub asserted_at: Timestamp,
}
```

**A mapping stays `judged` until it is accepted or established.** Two paths lead out of `judged`, and only two:

- **Acceptance.** A local actor with authority over the concept's scope records a decision. The mapping's reliability basis stays `judged` — a human accepting a judgment does not convert it into a deterministic comparison — but `accepted_by` is populated, and the mapping becomes usable under local policy. This is the ordinary path.
- **Establishment.** Both sides name the same external identifier that each can resolve independently — a Legal Entity Identifier, an ISO country code, a DOI. The relation is then `verified`, because a deterministic comparison was actually executed: the two identifier strings were compared and found equal. Nothing weaker qualifies. Two concepts whose *labels* are string-equal are not established; `net revenue` means different things in two organizations more often than it means the same thing.

**A model may propose a mapping and may not establish one.** The proposal is useful — scanning two schemas for plausible correspondences is exactly the kind of work worth automating — and it arrives with `reliability_basis: judged`, `accepted_by: None`, and a rationale. Under [Law E](../v5/CONSTITUTION.md) an uncertain mapping says `Unresolved` rather than guessing `Exact`, and `Unresolved` is a normal, permanent, publishable state rather than a failure to be cleaned up.

### 8.3 What each relation permits

The relation is not a label. It determines what may be reused across the boundary, and the table is the enforcement point.

| Relation | Inbound claim may bind to local concept | Local proof may be reused for remote concept | Quantities may be compared |
|---|---|---|---|
| `Exact` | yes, after acceptance | yes, after acceptance | yes |
| `Narrower` | yes, as a narrower claim | no | only with explicit scope conversion |
| `Broader` | yes, as a broader claim | no | only with explicit scope conversion |
| `Related` | no | no | no |
| `Unresolved` | no | no | no |

**`Narrower` and `Broader` do not permit proof reuse in either direction**, and the asymmetry people expect — that a proof about the broader concept should cover the narrower one — is wrong often enough to be prohibited. A verified figure for *all covered entities* is not a verified figure for *reporting subsidiaries*; it is a figure whose relationship to that population is unstated. Producing it as `verified` for the narrower concept would report a comparison that was never run, which is [Law C](../v5/CONSTITUTION.md).

---

## 9. Threats specific to federation

**Status: specified.**

The threats in [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md) all still apply — a remote is a source, and source-borne instruction, malformed parse targets and hostile media do not become safe by arriving from a partner. Four threats are specific to the fact that a *graph* is crossing the boundary.

| Threat | What the attacker gets | Control |
|---|---|---|
| Remote object poisoning | A node the receiver treats as authoritative, whose content the sender chose | Content addressing plus step 3 whole-branch discard; every body must hash to the digest under which it was offered, and one failure discards the package rather than the object |
| Schema downgrade | Fields the receiver's policy depends on silently absent | `accepted_schema_versions` is an allowlist checked in step 4; an unlisted version is refused rather than best-effort parsed |
| Policy downgrade | Material entering under a weaker profile than the receiver requires | `minimum_policy_profile` in step 4; divergence surfaces as a `policy` conflict in step 6 and cannot be auto-merged |
| Pack substitution | A style, jurisdiction or voiceprint pack replaced by one the attacker wrote | Pack digests are pinned in the lockfile and included in the release closure — see [`PACKAGE_SYSTEM.md`](PACKAGE_SYSTEM.md) |

### 9.1 Remote object poisoning

The naive version is caught immediately: an object whose body does not hash to its digest fails on arrival. The version worth describing is subtler. The attacker sends objects that are all internally valid and hash correctly, but that collectively assert something false — a corrected source version that was never corrected, with a plausible `DerivationRecord` and a real signature from a real key.

Content addressing does not detect this and is not meant to. The controls are elsewhere: the material lands on an inbound branch, the receiver's own proof obligations run against it in step 5, and the receiver's own authority decides in step 7. The receiver does not accept the sender's claim that the source changed; the receiver decides whether to adopt a source state whose digest it can see and whose bytes it holds.

**One object failing discards the whole package.** Applying the valid objects and dropping the invalid one leaves the receiver with a partial branch whose `result_root` cannot be reproduced — a state that exists in no sender's history and no receiver's history, which no future package can be based on. Discarding whole is the only outcome that keeps `base_root` meaningful.

### 9.2 Schema downgrade

The attack is to send `wi-node/4` objects to a `wi-node/6` receiver. Version 4 has no `certainty`, no `causal_force` and no `legal_force`; a permissive parser fills them with defaults, and the defaults are the least constrained values. An obligation that was `shall` becomes unmarked. A `correlation` becomes unspecified and reads as causation to a human.

The control is that missing fields are never defaulted at a version boundary. `accepted_schema_versions` refuses an unlisted version, and where a listed older version genuinely lacks a field, the field is marked `absent_from_source_version` — the same rule the migration in [`MIGRATION_V5_TO_V6.md`](MIGRATION_V5_TO_V6.md) uses, and for the same reason: an absent field and a field whose value is the default are different facts, and collapsing them manufactures assertions nobody made.

### 9.3 Policy downgrade

A partner commits under `draft`, where several gates do not run, and pushes to a receiver operating under `regulated`. Every object is well-formed. Every digest verifies. Nothing in the content is wrong. What is missing is that the material was never held to the receiver's standard, and a merged node carries no record of which standard produced it unless one is kept.

The control has two halves. `minimum_policy_profile` refuses the package outright when the gap is large enough to be categorical. Below that, `policy_profile_at_send` is retained and the divergence appears in step 6 as a `policy` conflict over the affected node set — visible to the human in step 7, listed in `wi conflicts`, and blocking auto-merge, which is already impossible because `auto_merge` is pinned false.

### 9.4 Pack substitution

The receiver's checks are parameterized by installed packs. A house style pack, a jurisdiction pack, a voiceprint. An attacker who can substitute a pack changes what "passed" means without touching a single node.

The control is that packs are content-addressed, pinned in a lockfile, and included in the release proof closure. A release attestation names the exact pack digests in force when it was produced, so a later verifier recomputes the closure against those digests rather than against whatever is installed at verification time. The full mechanism is in [`PACKAGE_SYSTEM.md`](PACKAGE_SYSTEM.md); the federation-specific point is that a delta package cannot install, upgrade or activate a pack. It may *declare* that it was produced under certain packs, which is evidence, and evidence is not installation.

---

## 10. Quarantine and inbound branches

**Status: specified.**

Two holding areas, and the distinction between them is the distinction between *unauthenticated* and *unaccepted*.

**Quarantine** holds bytes that have not passed step 1 or step 3. Nothing in quarantine is addressable from the graph. Nothing in quarantine is parsed by anything other than the out-of-process adapter host described in [`CAPABILITY_SECURITY.md`](CAPABILITY_SECURITY.md) §5. Material leaves quarantine in one of two directions: into an inbound branch, or into a discard record naming why it failed. A quarantined package that fails is not deleted silently — a partner asking why their push had no effect deserves an answer more precise than "it did not work".

**An inbound branch** holds material that is authenticated and positioned but not accepted. It is a real branch: it can be inspected with the ordinary tools, diffed against `main`, simulated against, and reported on. It is named after the remote (`inbound/regulator`), never merged automatically, and never rewritten by a subsequent push — a second package produces a second branch head, so a partner cannot overwrite a proposal the receiver is still reading.

**Neither area affects proof state on `main`.** A proof on `main` that depends on a source object whose successor sits on an inbound branch remains exactly as fresh as it was. Under [Law R](CONSTITUTION.md) freshness is a property of dependencies, and the dependency in question is the state the local workspace adopted, not the newest state anybody anywhere has produced. Adoption is the event that changes freshness, and adoption is step 8.

---

## 11. What does not cross the boundary

**Status: specified.**

A delta package carries object states, decisions, mappings and signatures. It does not carry:

- **Source bytes, unless explicitly included.** A claim can cross with its anchor and its source *version identity* — digest, byte length, retrieval metadata — without the source document itself. The receiver then holds a claim whose support it can name and cannot independently inspect. That is a real and useful state, and it must be rendered as what it is: the reliability distinction in [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) §5 applies unchanged, and a receiver that renders such a claim as though it had checked the source is making a claim about work it did not do.
- **Local authority grants.** Section 7.
- **Policy.** The receiver's policy is the receiver's. A package states the sender's profile as a fact and cannot set the receiver's.
- **Installed capability.** Packs, plugins and adapters do not travel in a delta package. A package that required a plugin the receiver does not have is a package the receiver cannot fully evaluate, and it says so in step 5 rather than acquiring the plugin.
- **Judgment provider configuration.** Which model the sender used is recorded in the sender's judgment records as evidence. It does not configure anything on the receiving side, and a sender cannot cause the receiver to call a provider.

The last two are the same rule stated twice: **inbound material can never cause outbound capability.** A package cannot make the receiver fetch, install, execute or call anything. Everything a package can do is complete when the bytes have been written to an inbound branch.

---

## 12. What is executable and what is specified

**Status: specified.**

| Mechanism | State at v6.0.0 |
|---|---|
| `wi capsule create \| inspect \| verify` — portable proof closure on a local filesystem | **Executable in `scripts/wi.py`.** Described in [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) |
| `wi conflicts`, `wi merge`, `wi decide` — the local half of step 6 through step 8 | **Executable in `scripts/wi.py`.** Described in [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) |
| Remote configuration (`wiremote/1`), key pinning | Specified |
| `advertise`, `have`, `fetch-objects`, `fetch-closure`, `push`, `notify` | Specified. No network transport of any kind ships |
| `SignedDeltaPackage`, signature verification, base-root relationship | Specified. No signing and no signature verification ships |
| Inbound branches and quarantine for remote material | Specified |
| `ConceptMapping`, `MappingRelation`, mapping acceptance | Specified |
| Federation threat controls in section 9 | Specified. The underlying source-ingestion controls they build on are executable and unchanged from v5 |

**Read the two executable rows carefully.** They are executable because they are local: producing a capsule, computing conflicts and recording a decision all happen inside one workspace. Nothing in this document that involves a second organization runs. An organization that wants to move meaning to a partner today writes a capsule to a file and hands it over, and the partner inspects and verifies it locally. That is a genuine and complete workflow with no transport, and it is the only cross-organization workflow v6.0.0 supports.

---

## Related documents

- [`CONSTITUTION.md`](CONSTITUTION.md) — Laws O, P, Q and R
- [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) — the conflict vocabulary the receiver runs in step 6
- [`PROOF_OBLIGATIONS.md`](PROOF_OBLIGATIONS.md) — the obligations discharged in step 5
- [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) — the portable closure format, and the redaction contract for claims whose sources did not cross
- [`PACKAGE_SYSTEM.md`](PACKAGE_SYSTEM.md) — pack pinning, and why pack digests belong in a release closure
- [`CAPABILITY_SECURITY.md`](CAPABILITY_SECURITY.md) — the out-of-process boundary every inbound byte passes through
- [`AUTONOMOUS_EXECUTION.md`](AUTONOMOUS_EXECUTION.md) — the effect classes a fetch step would have to declare
- [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md) — the source ingestion boundary, unchanged
- [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) — Laws A through L, the reliability types and the actor model

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
