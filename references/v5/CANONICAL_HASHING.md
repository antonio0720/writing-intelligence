# Canonical Hashing

The entire staleness and attestation system depends on one thing being boring and exact:

> **The same state must always hash to the same digest.**

If two runs over identical content produce different digests, every cached proof closure misses, every unchanged claim looks edited, and the system floods an author with staleness that is not real. If two *different* states produce the same digest, verification silently carries across an edit — which is the failure the accountability layer exists to prevent, reintroduced at the bottom of the stack.

Neither failure is exotic. Both arrive through key ordering, whitespace, Unicode composition and float formatting. This document specifies the rules that keep them out.

Read with [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md), which defines what a state digest identifies.

---

## 1. The ten canonical object rules

**Status: executable in `scripts/wi.py`.**

| # | Rule | Reason |
|---|---|---|
| 1 | Encode as UTF-8 | One byte representation per string. Encoding choice must never enter the digest. |
| 2 | Normalize to Unicode NFC, unless the field is declared `verbatim_bytes` | `é` composed and decomposed are the same text and must hash the same — except where the exact bytes are the evidence, which is why the exception exists. |
| 3 | Sort object keys lexicographically | Serializers disagree about insertion order. Sorting removes the disagreement. |
| 4 | Preserve array order where order is semantic | Paragraph order, list order and timeline order carry meaning. Sorting them would destroy the state being hashed. |
| 5 | Sort set-like arrays by the schema's declared canonical key | Anchors, tags and edge sets have no meaningful order; without a declared sort, the same set hashes differently depending on how it was assembled. |
| 6 | Serialize integers as decimal integers | `11800`, `11800.0` and `1.18e4` are the same value and must not be three digests. |
| 7 | Reject NaN and infinities | They are not JSON, they compare unequal to themselves, and a state that cannot be compared cannot be verified. |
| 8 | Serialize decimal quantities as normalized decimal strings where floating-point ambiguity matters | Money and rates must round-trip exactly. Binary floating point does not guarantee that; a normalized decimal string does. |
| 9 | Omit non-semantic runtime fields from state hashes | Cache keys, row ids, elapsed times and file paths are facts about a run, not about the state. Including them makes every re-run look like an edit. |
| 10 | Never include wall-clock timestamps in a semantic state digest, unless time itself is part of the asserted state | A claim does not change because it was serialized twice. A claim *about* a date does contain that date — as content, in a semantic field, not as a header. |

**Recommended encoding: RFC 8785 JSON Canonicalization Scheme.** It already specifies rules 1, 3, 6 and 7 precisely, it is implementable in a few dozen lines of stdlib code, and using a published scheme means an independent reviewer can verify a digest without reading this file first. Where RFC 8785 and these rules could diverge, RFC 8785 governs the JSON encoding and these rules govern what goes into the JSON.

One implementation note stated plainly because it is a real difference: RFC 8785 sorts keys by UTF-16 code units, while a naive sort in most languages orders by code point. For the ASCII field names this schema uses, the two orderings are identical. For any schema that admits non-ASCII keys, they are not, and RFC 8785 is normative.

**Why this is load-bearing.** Every honest claim v5 makes — *this artifact was verified*, *this source has not changed*, *this proof still applies* — reduces to a digest comparison. Ten unglamorous rules are what stand between that claim and a system whose verdicts drift with the serializer version.

---

## 2. Two hashes

**Status: executable in `scripts/wi.py`.**

| Digest | Covers | Answers |
|---|---|---|
| `content_digest` | The canonical payload alone | *Is this the same content?* |
| `state_digest` | The canonical payload plus schema version, policy version, normalization version, and parser identity where extraction produced the object | *Is this the same verified state?* |

They differ because content is not the whole story. The same extracted text produced by extractor 5.0.0 and extractor 5.1.0 has one `content_digest` and two `state_digest` values — correctly, because the second was produced by a different process and its trustworthiness is a different question. The same claim payload under evidence policy `standard` and under `regulated` is the same content and two different verified states.

The `state_digest` preimage is domain-separated:

```
wi-state-v5\0
schema=claim_atom@5.0.0\0
normalization=nfc-1\0
payload=<canonical-json>
```

The four fields are concatenated with a `\0` byte between them. The display above breaks lines for readability; **there are no newline bytes in the preimage.** Where extraction produced the object, a `parser=<id>@<version>\0` field is inserted before `payload=`, and where policy binds the state, `policy=<digest>\0` follows the schema field.

**Domain separation is not decoration.** The same raw digest must never ambiguously represent a source byte stream and a semantic object. Without the prefix, a source file whose bytes happen to equal a canonical claim serialization would produce the identical digest as that claim — and an attestation could then be satisfied by an object of the wrong kind. The prefix makes the *type* of the thing part of what is hashed, so a digest can only mean one thing.

---

## 3. Source bytes are hashed raw

**Status: executable in `scripts/wi.py`.**

Everything in section 1 applies to canonical objects the system constructs. **It does not apply to supplied sources.**

A `source.version` is identified by `sha256(raw bytes)` with no normalization of any kind: no NFC, no whitespace trimming, no line-ending conversion, no re-encoding. Extraction produces derived objects with their own canonical digests, linked back by `derived_from`.

The reasoning is in [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md) §4 and it is short: the author's document is the fixed point of the whole system. Normalizing before hashing would make the fixed point depend on the normalizer.

---

## 4. Hash migration

**Status: specified.**

Canonicalization rules will change. NFC handling gets a correction, a sort rule is tightened, a decimal case is specified more precisely. When that happens:

> **History is not rewritten.**

Every digest in the workspace records how it was produced:

```json
{
  "digest_algorithm": "sha256",
  "canonicalization": "wi-json-v1",
  "digest": "519f1f670e7a1f995e0a249a84dd392b6f0a08feb7f20b3c62747549bbfa174d"
}
```

Under `wi-json-v2`, existing states keep their `wi-json-v1` digests and remain verifiable by anyone who implements v1. New states are written under v2. A state may carry digests under both, computed at migration time, so closures spanning the boundary resolve without a rewrite. Comparison across canonicalization versions is only valid when both sides declare the same version; where they do not, `wi doctor` reports it rather than guessing.

Re-hashing history under new rules would invalidate every attestation ever issued and, worse, would make old attestations *appear* to have been issued under rules that did not exist. An attestation records what was true under the rules in force. Those rules are therefore part of the record.

---

## 5. A worked example

**Status: executable in `scripts/wi.py`.**

A small claim atom payload:

```json
{
  "surface": "Between 2019 and 2022, the program served 11,800 households.",
  "quantity": 11800,
  "unit": "households",
  "temporal_scope": {"start": "2019-01-01", "end": "2022-12-31"},
  "modality": "is",
  "certainty": "asserted",
  "realm": "external_fact"
}
```

Its canonical serialization — keys sorted, no insignificant whitespace, integer as a decimal integer, UTF-8:

```
{"certainty":"asserted","modality":"is","quantity":11800,"realm":"external_fact","surface":"Between 2019 and 2022, the program served 11,800 households.","temporal_scope":{"end":"2022-12-31","start":"2019-01-01"},"unit":"households"}
```

The two digests:

```
content_digest  sha256:0be95f067addfc66d5f20c9da7c2a85edc54471fa6220f9ca4e31f338162bbaf
state_digest    sha256:519f1f670e7a1f995e0a249a84dd392b6f0a08feb7f20b3c62747549bbfa174d
```

`wi graph --json` prints both, so a reviewer never has to take the workspace's word for it:

```
$ python3 scripts/wi.py graph --from c-0002 --json | head -6
{
  "node_type": "meaning.claim_atom",
  "logical_id": "0192f3a1-7c40-7b2e-9f16-2a5c9d0e4b31",
  "content_digest": "sha256:0be95f06...62bbaf",
  "state_digest": "sha256:519f1f67...fa174d",
```

Recompute the `state_digest` from the payload with nothing but Python's standard library:

```bash
python3 -c "import hashlib,json,sys;p=json.dumps(json.load(sys.stdin),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode();print('sha256:'+hashlib.sha256(b'wi-state-v5\0schema=claim_atom@5.0.0\0normalization=nfc-1\0payload='+p).hexdigest())" < atom.json
```

```
sha256:519f1f670e7a1f995e0a249a84dd392b6f0a08feb7f20b3c62747549bbfa174d
```

That one-liner is the whole point of specifying canonicalization publicly. A reviewer with no trust in this project, no installed dependencies and no network can confirm that a claimed digest describes the payload in front of them. **A verification a hostile reader cannot reproduce is not a verification.**

---

## 6. The error taxonomy

**Status: executable in `scripts/wi.py` for the codes reachable from shipped commands; the remainder are specified and reserved.**

Error codes are stable identifiers. They may be added to; an existing code never changes meaning, because operators write CI rules and repair procedures against them.

| Code | Meaning |
|---|---|
| `WI_INPUT_INVALID` | An argument, file or object failed schema or shape validation |
| `WI_SOURCE_UNREADABLE` | The source exists but could not be read — permissions, corruption, truncation |
| `WI_SOURCE_UNSUPPORTED` | The format is recognized and no adapter for it exists in this build |
| `WI_SOURCE_QUARANTINED` | Static inspection or hygiene analysis flagged the source; it is held, not ingested |
| `WI_SOURCE_LIMIT_EXCEEDED` | An ingestion safety limit was hit; the limit and observed value are named |
| `WI_SOURCE_VERSION_MISSING` | A referenced source version is not present in the object store |
| `WI_ANCHOR_INVALID` | The anchor does not resolve, or the resolved content does not match its quote digest |
| `WI_ANCHOR_STALE` | The anchor resolves against a source version that is no longer current |
| `WI_CLAIM_ATOMIZATION_FAILED` | Atomization produced a set that failed reconstruction fidelity or independent checkability |
| `WI_CLAIM_UNSUPPORTED` | No anchor satisfying policy supports this claim |
| `WI_CLAIM_CONFLICTED` | A supplied source states something incompatible with this claim |
| `WI_CITATION_UNRESOLVED` | A citation-shaped reference does not resolve to any supplied source |
| `WI_POLICY_BLOCK` | Policy evaluation produced BLOCK |
| `WI_POLICY_HOLD` | Policy evaluation produced HOLD |
| `WI_PROPOSAL_STALE` | The proposal targets a node state that has since changed |
| `WI_DECISION_STALE` | The decision was made against a state that has since changed |
| `WI_WAIVER_STALE` | The waiver covered a state that has since changed; it does not carry forward |
| `WI_JUDGMENT_UNAVAILABLE` | A judgment is required by policy and no judgment capability is available |
| `WI_JUDGMENT_STALE` | The judgment was recorded against a state that has since changed |
| `WI_GRAPH_INTEGRITY` | The workspace failed an internal consistency check — dangling reference, missing blob, broken supersession chain |
| `WI_BUILD_FAILED` | A renderer or build step did not complete |
| `WI_RELEASE_TAMPERED` | An artifact's bytes do not match the digest its attestation names |
| `WI_SIGNATURE_INVALID` | A signature does not verify against the attestation it covers |
| `WI_CAPABILITY_UNAVAILABLE` | The operation requires a capability this build does not have |

### 6.1 The error envelope

Every error is emitted in one shape:

```json
{
  "code": "WI_ANCHOR_STALE",
  "message": "Anchor a-0114 resolves against needs_assessment.txt@v2; current version is @v3.",
  "basis": {
    "anchor_id": "a-0114",
    "source_logical_id": "0192f3a1-7c40-7b2e-a001-8c4d1e9f0b22",
    "anchored_state": "sha256:3d81...c07f",
    "current_state": "sha256:b7a2...41d9",
    "check": "anchor_integrity.version_currency"
  },
  "repair": [
    {"route": "rebind", "detail": "The quoted text appears in @v3 at bytes 9,004-9,050. Rebind is exact.", "cost": "cheapest"},
    {"route": "requote", "detail": "Quote @v3 directly and re-run numeric and date checks."},
    {"route": "qualify", "detail": "Attribute the figure to the 2026-03-11 version of the assessment in the text."},
    {"route": "waive", "detail": "Proceed with a recorded waiver bound to this exact state."}
  ],
  "details": {
    "affected_claims": ["c-0002", "c-0006"],
    "affected_artifacts": ["dist/narrative.pdf", "dist/deck.md"]
  }
}
```

`basis` says what was checked and what was observed. `repair` is an array of concrete routes forward with the cheapest one named — never a single dead end, and never advice the author cannot act on today. `details` carries the blast radius, because an author deciding between four routes needs to know how much rides on the choice.

**Error language itself follows Law C.** An error never reports work that was not done. `WI_JUDGMENT_UNAVAILABLE` says a judgment was required and no capability was present; it does not say the claim failed. `WI_SOURCE_UNSUPPORTED` says this build has no adapter for the format; it does not say the source is bad. `WI_ANCHOR_STALE` says the anchor points at a superseded version; it does not say the claim is false. Each of those distinctions is the difference between an author fixing the right thing and an author deleting a true sentence because a tool sounded certain.

---

## 7. What is executable and what is specified

| Mechanism | Status |
|---|---|
| The ten canonical object rules and RFC 8785-compatible encoding | Executable in `scripts/wi.py` |
| `content_digest`, `state_digest`, domain-separated preimage | Executable in `scripts/wi.py` |
| Raw-byte source identity | Executable in `scripts/wi.py` |
| `wi graph --json` digest output and independent recomputation | Executable in `scripts/wi.py` |
| Error envelope with `code`, `message`, `basis`, `repair`, `details` | Executable in `scripts/wi.py` |
| Codes reachable only from specified mechanisms — signatures, media adapters, judgment tiers | Specified and reserved |
| Dual-digest hash migration across canonicalization versions | Specified |

---

## Related documents

- [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) — what a state digest identifies and why identity is split
- [`SEMANTIC_IR.md`](SEMANTIC_IR.md) — the objects being hashed
- [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md) — the raw-bytes rule and derived-object digests
- [`../v4/ACCOUNTABILITY_LAYER.md`](../v4/ACCOUNTABILITY_LAYER.md) — Law C, which the error taxonomy implements
- [`../v4/PROOF_PROTOCOL.md`](../v4/PROOF_PROTOCOL.md) — staleness, which these digests make decidable
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
