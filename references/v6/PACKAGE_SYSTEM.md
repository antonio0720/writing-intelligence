# The package system — `.wipack`

**Status: specified.** No pack format, no lockfile, no resolver and no installer ships in v6.0.0. Genre packs, voiceprints and pattern libraries exist in this repository today as loose Markdown under `references/`, copied into every distribution. Section 8 is a measured fact about that arrangement and is marked accordingly.

A check is parameterized. `wi verify` does not decide on its own what counts as a hedge, which claims a jurisdiction requires a disclaimer for, or whether a sentence sounds like the author. Those decisions live in content — a genre pack, a voiceprint, a jurisdiction rule set — and the engine applies them.

That content is capability. It changes what passes and what blocks. Which means every property the system claims about a release depends on it, and none of those properties survive if the content is unversioned, unpinned or silently replaced. A house style pack revised in March and a release attested in January are two different definitions of *passed*, and a system that cannot tell them apart has an attestation that means whatever the current directory contents happen to mean.

A pack is that content, made into an object: named, versioned, content-addressed, capability-declared, pinned by a lockfile, and recorded in the proof closure of any release produced under it.

Read this with [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) for the closure a pack digest enters, [`CAPABILITY_SECURITY.md`](CAPABILITY_SECURITY.md) for the plugin host a pack may carry a check for, and [`FEDERATION.md`](FEDERATION.md) §9.4 for pack substitution as an attack.

**Contents:** [1 Capability copied, not installed](#1-capability-copied-not-installed) · [2 Pack contents and manifest](#2-pack-contents-and-manifest) · [3 The five pack kinds](#3-the-five-pack-kinds) · [4 The lockfile](#4-the-lockfile) · [5 Packs in the release closure](#5-why-pack-digests-belong-in-the-release-closure) · [6 Pack capability declaration](#6-pack-capability-declaration) · [7 Resolution and refusal](#7-resolution-and-refusal) · [8 The distribution consequence](#8-the-distribution-consequence) · [9 Executable and specified](#9-what-is-executable-and-what-is-specified)

---

## 1. Capability copied, not installed

**Status: specified.**

The current arrangement is that every piece of parameterizing content is a file in the repository, and every distribution contains all of them. It has three failures, and they compound.

**Everybody gets everything.** A user writing regulatory filings ships with twenty-seven genre packs covering fiction, screenwriting and technical documentation. None of it is loaded, all of it is transferred, and the ones that are irrelevant are not merely wasted — they are indistinguishable, from outside, from the ones that matter. There is no statement anywhere of which content this workspace actually depends on.

**A revision is invisible.** A style rule is edited. Nothing records that a change occurred, which releases were produced before it and which after. The rule is not versioned because it is a file, and files in a repository have a history that belongs to the repository rather than to the rule.

**A release cannot be reproduced.** Given an attestation from January, reproducing the gate outcome requires the exact content in force in January. Reconstructing that from repository history is possible for somebody who knows to try and impossible for a recipient who holds only the attestation. The gate said `PASS`; nothing says what it was applying.

The failure the third one produces is specific and worth stating without hedging:

> **A style rule changing six months later cannot retroactively change what `passed` meant for an older release.**

If it can, an attestation is not a record of a check. It is a record that *a* check ran, with the parameters resolved at reading time rather than at running time, which means the same attestation yields different answers on different days. That is the failure this project exists to catch, arriving through configuration rather than through prose.

---

## 2. Pack contents and manifest

**Status: specified.**

A pack is a deterministic archive with a manifest at its root. The archive digest is the pack's identity; the version string is a label for humans and is never the thing anything resolves against.

```
house-style-density6-2.4.0.wipack
├── pack.json              Manifest. Identity, version, capability, contents.
├── rules/                 Declarative rule content the engine interprets.
│   ├── hedging.json
│   ├── attribution.json
│   └── quantities.json
├── lexicon/               Term bindings, banned constructions, preferred forms.
│   └── terms.json
├── fixtures/              Cases the pack must pass, including negatives.
│   ├── pass/
│   └── fail/
├── checks/                Optional. WASM modules, one per declared check.
│   └── quantity_denominator.wasm
└── LICENSE
```

```json
{
  "format": "wipack/1",
  "id": "density6/house-style",
  "version": "2.4.0",
  "kind": "organization",
  "publisher": {
    "name": "Density6 LLC",
    "key_id": "d6-pack-signing-01"
  },
  "engine": {
    "requires_wi": ">=6.0.0,<7.0.0",
    "requires_schema": "wi-node/6"
  },
  "capabilities": {
    "network": false,
    "graph_write": false,
    "sign": false,
    "filesystem": false,
    "wall_clock": false,
    "randomness": false
  },
  "provides": {
    "rules": 41,
    "lexicon_entries": 380,
    "checks": ["quantity_denominator"],
    "renderers": []
  },
  "policy_effect": "tighten_only",
  "fixtures": {
    "pass": 62,
    "fail": 24,
    "must_all_pass": true
  },
  "content_digest": "sha256:3d81f04b7ae296c5108bd3f7a24e6905...",
  "signature": {"present": false}
}
```

**`content_digest` covers everything except itself and the signature block.** Two packs with identical content have identical digests regardless of who built them, when, or what they called the version. Two packs with the same version string and different content have different digests, and the lockfile resolves on the digest, so the second one does not silently replace the first.

**`fixtures.fail` is mandatory and `must_all_pass` applies to both directories.** A pack whose fixtures only demonstrate acceptance has not shown that its rules can refuse anything. Every rule content library eventually acquires a rule that matches nothing — a pattern with a typo, a condition that can never hold — and the only evidence that a rule is live is a case it rejects. This is the same discipline the adversarial suite in [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md) applies to the test suites: a check that has never failed has not been shown to work.

**`policy_effect: tighten_only` is the only permitted value in v6.** A pack may add a requirement, narrow an acceptable range, or forbid a construction. A pack may not remove a requirement, widen a range, or permit something a hard invariant forbids. The field exists so the constraint is declared and machine-checkable rather than implied — and so that a future value has to be added deliberately, by somebody who has to explain what a loosening pack would mean for an attestation produced under it.

### 2.1 What a rule looks like

Rule content is declarative. The engine interprets it; the pack does not carry executable logic unless it ships a WASM check under section 6.

```json
{
  "rule_id": "d6.quantity.denominator_required",
  "applies_to": {
    "node_family": "meaning.claim_atom",
    "realm": ["external_fact", "author_observation"],
    "when": {"has_dimension": "quantity", "quantity_form": "proportion"}
  },
  "requires": {
    "dimension_present": "population_scope",
    "reason": "A proportion without a stated population is not a measurement."
  },
  "on_violation": {
    "result": "BLOCK",
    "reliability_effect": "cannot_emit_measured",
    "message": "This states a proportion with no population it is a proportion of."
  },
  "fixtures": {
    "fail": ["fixtures/fail/proportion-no-population.json"],
    "pass": ["fixtures/pass/proportion-with-population.json"]
  }
}
```

**`reliability_effect` is the part a rule format usually omits.** A blocked check is a gate outcome; what a violated rule does to the *reliability type* of the state it touched is a separate question, and leaving it implicit is how a claim ends up rendered `measured` after the check establishing the denominator refused to run. `cannot_emit_measured` says that whatever else happens, this state does not carry that word.

**Every rule names its own fixtures.** A rule with no fixture is a rule the install-time check cannot exercise, and the resolver refuses a pack containing one — section 7. It is not enough for a pack to have fixtures somewhere; each rule has to be reachable by at least one that fails.

---

## 3. The five pack kinds

**Status: specified.**

| Kind | Parameterizes | Typical publisher | Example |
|---|---|---|---|
| `genre` | Structural expectations, register, permitted constructions | Community, publisher | Long-form investigative journalism |
| `voiceprint` | Whether a passage sounds like a specific author | The author, always | An individual's consented voiceprint |
| `jurisdiction` | Which claims require which disclosures, and in what proximity | Counsel, trade body | US securities marketing disclosure |
| `organization` | House style, terminology bindings, prohibited constructions | The organization | The manifest above |
| `storyworld` | Canonical facts inside a constructed world | The rights holder | A series bible |

**A voiceprint pack is not like the others and the difference is not cosmetic.** It encodes a real person's writing patterns, and [`../v4/VOICE_CONSENT.md`](../v4/VOICE_CONSENT.md) governs it: consent is recorded, scoped and revocable. A pack format that treated a voiceprint as ordinary content would make revocation a matter of persuading everybody who installed it to uninstall. The pack manifest therefore carries the consent record inside it, a voiceprint pack is refused at install if the consent record is absent or expired, and revocation is a publisher action that a resolver honors at resolution time rather than a request.

**A storyworld pack parameterizes `fictional_canon`, and only that realm.** A canon fact inside a constructed world is not an external fact, and a pack that could bind `external_fact` claims would let a series bible assert things about the world. The realm separation in [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) is enforced at the pack boundary: a `storyworld` pack that emits bindings outside `fictional_canon` is refused at load.

**A jurisdiction pack is the one most likely to be wrong in a way nobody notices.** It encodes somebody's reading of a rule, and that reading has a date. The manifest carries `as_of` and the resolver refuses to apply a jurisdiction pack whose `as_of` precedes a release's content dates by more than a configured window — not because the pack is necessarily wrong, but because a silently stale legal reading is the failure mode that produces a confident `PASS` on a filing that is no longer compliant.

---

## 4. The lockfile

**Status: specified.**

The workspace declares packs by name and range. The lockfile records what those resolved to.

```json
{
  "format": "wilock/1",
  "resolved_at": "2026-09-14T10:58:03Z",
  "wi_version": "6.0.0",
  "packs": [
    {
      "id": "density6/house-style",
      "requested": "^2.4",
      "resolved_version": "2.4.0",
      "content_digest": "sha256:3d81f04b7ae296c5108bd3f7a24e6905...",
      "kind": "organization",
      "policy_effect": "tighten_only",
      "signature_verified": false
    },
    {
      "id": "sec/marketing-disclosure-us",
      "requested": "=1.9.2",
      "resolved_version": "1.9.2",
      "content_digest": "sha256:aa41c7d8e05b2936f4c81a0d76e3b8f2...",
      "kind": "jurisdiction",
      "as_of": "2026-06-30",
      "policy_effect": "tighten_only",
      "signature_verified": false
    }
  ],
  "lock_digest": "sha256:5c2e88f31a7d40b96e0c7fa2358d1b47..."
}
```

**Resolution happens on the digest, never on the version string.** A publisher who re-publishes `2.4.0` with different content produces a different digest, the lockfile does not match, and the resolver refuses. Versions are for humans deciding what to request; digests are what anything resolves against.

**`lock_digest` is a single value covering the whole resolution.** It is what a release attestation records, so that a release names one digest rather than a list that a later reader has to compare element by element. A change to any pack changes the lock digest.

**The lockfile is committed, and updating it is a decision.** `wi pack update` produces a proposal showing which digests moved, which rules changed, and — the part that matters — which currently-passing states would fail under the new resolution. It is a proposal, under [Law A](../v5/CONSTITUTION.md), because updating a pack is a change to what the workspace considers acceptable, and a change to what the workspace considers acceptable is not a thing that should happen because somebody ran an install command.

### 4.1 A worked update proposal

```
wi pack update density6/house-style

PROPOSAL — pack resolution change
  density6/house-style   2.4.0 -> 2.5.0
    sha256:3d81f04b...  ->  sha256:c7e2a9b4...

  Rules added        3
  Rules removed      0
  Rules tightened    2
    d6.hedging.attribution_required
      before  attribution required on claims with causal_force >= contribution
      after   attribution required on claims with causal_force >= correlation
    d6.quantity.denominator_required
      before  applies to quantity_form = proportion
      after   applies to quantity_form in {proportion, rate}

  Effect on current workspace state:
    would newly BLOCK      14 claim atoms
    would newly WARN        6 claim atoms
    would change reliability 9 claim atoms  measured -> needs_source

  Releases already attested under 2.4.0:  3
    Those attestations are unaffected. They record the digest they were
    produced under, and verify against it. See PACKAGE_SYSTEM.md section 5.

Nothing has been changed. Accept with:  wi decide --accept <proposal-id>
```

**The three-line effect block is the reason the command exists.** A resolver that reported only which digests moved would be reporting a fact nobody can act on. The question somebody is actually asking before accepting a pack update is *how much work does this create*, and the answer is a count of states that stop passing — which requires evaluating the new rules against the current graph before adopting them, exactly as [`COUNTERFACTUAL_SIMULATION.md`](COUNTERFACTUAL_SIMULATION.md) evaluates a proposed change before committing it.

**The `measured -> needs_source` row is separate from the block count on purpose.** A state that stops passing is visible. A state that keeps passing while its reliability type weakens is not, and it is the one that changes what a document says without changing whether it builds.

**The note about already-attested releases is printed every time**, because the fear it addresses — that updating a pack will invalidate historical releases — is the reasonable assumption, and the answer is section 5.

---

## 5. Why pack digests belong in the release closure

**Status: specified.**

Layer 9 of the proof closure in [`../v5/AUTHORSHIP_GRAPH.md`](../v5/AUTHORSHIP_GRAPH.md) §5 is "the policy state in force at build time". A pack is policy state. Its digest belongs in the closure, and its absence is a hole in an otherwise complete chain.

Without pack digests in the closure:

1. A release attests that its claims passed the gate.
2. The gate's behavior was determined by packs.
3. The attestation does not name the packs.
4. Therefore the attestation names checks whose definitions cannot be recovered.

Step 4 is not a theoretical weakness. It is the mechanism by which an organization revises a house rule, re-runs verification on a two-year-old release out of curiosity, gets a different answer, and has no way to determine whether the document changed or the rule did.

**With pack digests in the closure, `wi verify-release` distinguishes three outcomes** that a naive re-run collapses into one:

| Outcome | Meaning |
|---|---|
| `VALID` | Every closure state matches, packs included. The check that passed is the check that would pass now. |
| `INVALID — content drift` | A node state, source version or anchor moved. The document's evidence changed. |
| `INVALID — policy drift` | Every content state matches; a pack digest does not. The document did not change; the definition of passing did. |

The third is the one that does not exist without pack pinning, and it is the one that answers the question a reviewer actually asks. `INVALID` alone sends somebody looking for an edit that never happened.

**This is also the control for pack substitution as an attack.** [`FEDERATION.md`](FEDERATION.md) §9.4 describes an attacker who replaces a pack rather than touching a node: every claim verifies, every digest matches, and the meaning of `PASS` has changed underneath. A closure that names pack digests catches it, because verification recomputes against the digests recorded at build time rather than against whatever is installed at verification time.

---

## 6. Pack capability declaration

**Status: specified.**

Every capability defaults to `false` and must be declared to be requested. The three that matter most are `network`, `graph_write` and `sign`, and all three have exactly one permitted value in v6.

| Capability | Permitted values | Why |
|---|---|---|
| `network` | `false` | A pack that can fetch makes gate behavior depend on a server's availability and current contents. Two runs of the same release would differ for reasons nothing records. |
| `graph_write` | `false` | A pack parameterizes checks. A pack that could write is an unauthenticated actor mutating authoritative state, outside the decision model of [Law O](CONSTITUTION.md). |
| `sign` | `false` | Signing is a person's assent (see [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) §8). Installed content cannot assent. |
| `filesystem` | `false` | A pack's content is its archive. Reading outside it makes the archive digest an incomplete description of the pack. |
| `wall_clock` | `false` for deterministic checks | A check that reads the clock can pass in the morning and fail in the afternoon over identical state, which ends reproducibility. |
| `randomness` | `false` for deterministic checks | Same reason, arriving faster. |

**The three pinned values are written out rather than omitted.** An absent field invites a permissive default from whoever implements the resolver; a field that is present, documented and constrained states that the question was asked and answered. This mirrors `auto_merge` in [`FEDERATION.md`](FEDERATION.md) §3 and the `denied` list in [`AUTONOMOUS_EXECUTION.md`](AUTONOMOUS_EXECUTION.md) §6.

**A pack that carries a check carries a WASM module, and the module runs under the plugin host in [`CAPABILITY_SECURITY.md`](CAPABILITY_SECURITY.md) §7.** It gets no ambient authority from the fact that it arrived in a pack rather than by itself, and the pack's declared capabilities are an upper bound on what the host grants — never a grant in themselves. A pack declaring a capability the host does not offer is refused at load rather than silently downgraded.

---

## 7. Resolution and refusal

**Status: specified.**

Resolution is offline. A pack is a file that was obtained, checked and stored; there is no registry call in the resolution path, and the reason is section 6 row one applied to the resolver itself. A resolver that fetched during resolution would make a build's outcome depend on network state.

Refusals, and what each one prevents:

| Refusal | Prevents |
|---|---|
| Digest does not match the lockfile | Silent substitution |
| `requires_wi` excludes the running version | A pack interpreted by an engine whose rule semantics differ from the one it was written against |
| `requires_schema` excludes the workspace schema | Rules referencing fields that do not exist, evaluated as vacuously true |
| Declared capability not offered by the host | A pack running with less isolation than it declared, or with more |
| `policy_effect` is not `tighten_only` | A pack that loosens an invariant |
| Fixtures do not all pass at install | A pack whose rules do not do what its own examples say |
| Voiceprint consent absent, expired or revoked | Use of a person's voice model without live consent |
| Jurisdiction `as_of` outside the configured window | A stale legal reading producing a confident pass |
| Two packs bind the same term to different definitions | A term whose meaning depends on load order |

**The last one refuses rather than resolving by precedence.** A precedence rule — later pack wins, more specific pack wins — makes the meaning of a term a function of installation order, and installation order is not recorded anywhere a reviewer would look. The conflict is surfaced as a conflict, and a human decides which binding governs. It is the same reasoning that forbids splitting the difference on a semantic merge in [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) §5: an automatic resolution of a genuine disagreement produces a state neither party asserted.

**Fixtures run at install, not at publish.** A publisher's fixtures passing on the publisher's engine says nothing about this engine, this schema version, and this combination of other installed packs. Running them locally is what turns a pack's claims about itself into a local observation.

### 7.1 A worked refusal

```
wi pack add ./sec-marketing-disclosure-us-2.0.0.wipack

REFUSED — 2 conditions

  jurisdiction.as_of_outside_window
    pack as_of      2024-11-01
    workspace holds content dated through 2026-09-12
    configured window  540 days      exceeded by 141 days
    A jurisdiction pack encodes somebody's reading of a rule on a date.
    This one predates the material it would be applied to.

  term_binding_conflict
    term            "material"
    density6/house-style 2.4.0   binds to  d6.term.material_significance
    this pack               binds to  sec.term.material_reasonable_investor
    Two live bindings for one term. Load order would decide which governs,
    and load order is recorded nowhere a reviewer would look.
    Resolve by choosing a binding:  wi decide --bind-term material <id>

Nothing was installed. The lockfile is unchanged.
```

**Both refusals name what to do next.** A refusal that states a condition and stops produces a workaround; the workaround for a term conflict is uninstalling the pack that raised it, which leaves the conflict in place and removes the thing that found it.

---

## 8. The distribution consequence

**Status: measured, this repository, at the time of writing.** The observation below is a fact about the current build, not a specified mechanism.

`scripts/build-skill.sh` enforces `MAX_FILES=200` with `WARN_FILES=185`. The limit is not a preference of that script. Commit `fd90653` records what happens above it:

> the skill bundle exceeded the 200-file upload limit — At 211 files the bundle was rejected on upload outright — it does not degrade, it will not load — which made every install instruction in README.md and docs/INSTALL.md false.

The distinction in that line is the whole point. A bundle that is too large does not load more slowly, or partially, or with some content missing. It is refused, and the repository continues to document an installation procedure that cannot succeed.

The current staged payload is **208 files** — over the ceiling by eight, with the build correctly refusing. The composition:

| Directory | Files | Character |
|---|---|---|
| `references/genre_packs/` | 27 | Content packs |
| `references/v5/` | 21 | Doctrine |
| `references/compiler/` | 19 | Engine reference |
| `references/v6/` | 16 | Doctrine, growing |
| `schemas/v5/` + `schemas/v6/` | 26 | Contract |
| `agents/` | 14 | Surface definitions |
| `references/voiceprints/` | 10 | Content packs |
| `docs/` | 10 | Documentation |
| `references/v4/` | 8 | Doctrine |
| `references/anti_patterns/` + `positive_patterns/` + `diagnostics/` + `academic/` | 21 | Content packs |
| `governance/`, `tests/`, `scripts/wi.py`, top-level | 36 | Governance, tests, engine |

Fifty-eight of those files are content that parameterizes checks — genre packs, voiceprints, pattern libraries, diagnostics. They are in the bundle because there is nowhere else for them to be, and every user receives all of them regardless of what they write.

Removing them takes the payload to 150, which is well inside the ceiling and leaves room for doctrine to grow. That is the arithmetic behind the design consequence, stated without euphemism:

> **The skill bundle is not the product payload.**

The v6 distribution splits into four artifacts with separate lifecycles:

| Artifact | Contents | Versioned with |
|---|---|---|
| The `wi` binary | Engine, canonicalization, graph, gate, capsule | The engine |
| A minimal audit-only verifier | Digest and closure verification, no authoring | The proof format |
| A thin activation skill | Surface definitions, entry documentation, and a pointer | The surfaces |
| Packs | Genre, voiceprint, jurisdiction, organization, storyworld content | Each pack, independently |

**Every one of these already needed a separate lifecycle for reasons that have nothing to do with a file count.** A jurisdiction pack updates when the law changes. A voiceprint updates when an author's consent changes. The proof format is intended to stay verifiable for years after the engine that produced it has moved on — which is the argument for a minimal verifier that never needs to change, and which cannot be true of an artifact that ships bundled with everything else.

The file ceiling is what makes the necessity impossible to defer. It is not the reason.

---

## 9. What is executable and what is specified

| Mechanism | State at v6.0.0 |
|---|---|
| The 208-file measurement, `MAX_FILES=200`, the `fd90653` refusal | Measured fact about this repository |
| `.wipack` archive format and `wipack/1` manifest | Specified |
| `wilock/1` lockfile, digest resolution, `lock_digest` | Specified |
| Pack digests in the release proof closure | Specified. The closure itself is executable; layer 9 records policy state and does not yet record pack digests, because packs do not exist |
| `policy_effect: tighten_only` | Specified |
| Pack capability declaration and the pinned `false` values | Specified |
| Install-time fixture execution, including negative fixtures | Specified |
| Voiceprint consent enforcement at resolution | Specified. The consent model it builds on is described in [`../v4/VOICE_CONSENT.md`](../v4/VOICE_CONSENT.md) |
| `wi pack add \| update \| verify \| list` | Specified. No pack command exists |
| Pack signing and publisher key verification | Specified. No signing of any kind ships — see [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) §8 |
| The four-artifact distribution split | Specified |

---

## Related documents

- [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) — the closure a pack digest enters, and the signing model packs inherit
- [`CAPABILITY_SECURITY.md`](CAPABILITY_SECURITY.md) — the plugin host a pack's checks run under
- [`FEDERATION.md`](FEDERATION.md) — pack substitution as an attack, and why a delta package cannot install one
- [`MERGE_PROTOCOL.md`](MERGE_PROTOCOL.md) — the reasoning behind refusing a term-binding conflict rather than resolving it
- [`../v5/AUTHORSHIP_GRAPH.md`](../v5/AUTHORSHIP_GRAPH.md) — the ten closure layers, layer 9 in particular
- [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md) — the adversarial suite discipline the fixture rule follows
- [`../v4/VOICE_CONSENT.md`](../v4/VOICE_CONSENT.md) — consent scope and revocation for voiceprints

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
