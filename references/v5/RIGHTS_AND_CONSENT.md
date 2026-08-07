# Rights and Consent

**Status: consent basis fields executable in metadata; enforcement specified.**

v4 asked one rights question and asked it well: when a voiceprint models a real, named person, what is the basis? Five bases, three of them unrestricted, one plain question asked once. That treatment is preserved and is still correct.

v5 raises the stakes, because v5 governs media.

**A text quotation and a person's recorded voice are not the same object with the same permissions.** Quoting a sentence from a supplied report is an ordinary act with a well-understood rule set. Using twelve seconds of someone's recorded speech — as evidence, as an anchor, as an excerpt in a bundle, as a training sample for a style profile — is four different acts with four different permission questions, and the file gives no indication which one you are performing. A photograph containing an identifiable face, a video of a client telling their story, an audio interview with a named source, and a chart exported from a licensed dataset are each governed by something, and in every case the governing thing is invisible in the bytes.

So v5 makes rights state a **field**, not a memory. The point is not that the system knows the law. The point is that when someone asks *do we have the right to publish this*, the answer is a query rather than an archaeology project.

Read this with [`../v4/VOICE_CONSENT.md`](../v4/VOICE_CONSENT.md), which it carries forward and strengthens.

---

**Contents:** the rights block · voice consent · expiry and re-check · deletion · redaction-aware export · attribution and quotation · what this document is not.

---

## 1. The rights block

**Status: fields executable in metadata; gate enforcement specified.**

Every media asset carries a rights block. Not optional, not populated on demand, not inferred.

| Field | Values | Holds |
|---|---|---|
| `rights.basis` | `owned` · `licensed` · `public_domain` · `permission` · `unknown` | On what footing this asset is held |
| `rights.scope` | Free text plus structured facets | What the basis actually permits — internal use, publication, redistribution, derivative works, territory |
| `rights.expires_at` | Date or `null` | When the basis stops being true |
| `identity.contains_identifiable_person` | `true` · `false` · `unknown` | Whether a person is recognizable in it |
| `identity.consent_basis` | `self` · `contract` · `explicit_permission` · `public_figure_context` · `unknown` | On what footing that person appears |

```json
{
  "asset_id": "as-0142",
  "media_type": "audio/wav",
  "source_state_digest": "sha256:6e29...aa41",
  "rights": {
    "basis": "permission",
    "scope": {
      "text": "Recorded interview, permitted for use in the 2026 program report and its public summary.",
      "publication": true,
      "redistribution": false,
      "derivative_works": false,
      "territory": "unrestricted"
    },
    "expires_at": null,
    "declared_by": "act-0007",
    "declared_at": "2026-02-11T15:40:22Z"
  },
  "identity": {
    "contains_identifiable_person": true,
    "consent_basis": "explicit_permission",
    "subject_label": "participant-04",
    "consent_record": "obj:sha256:a1c9...73b0"
  }
}
```

**`unknown` is a legitimate, useful value and must never be silently upgraded.** This is the rule the whole block stands on. A rights field with no honest empty value forces a guess at the moment of ingestion — the moment when the person entering it knows least — and the guess then hardens into a fact that three later readers rely on. `unknown` records the true state: this asset is here, nobody has established its footing, and that is a thing to resolve rather than a thing to assume. It is also the value a policy can act on. A gate can require that no asset with `basis: unknown` appears in a published target, which is a check; it cannot require that nobody guessed wrong, which is a hope.

No inference path exists from `unknown` to any other value. Not from the file's location, not from its metadata, not from the fact that other assets in the same folder are `licensed`, and not from a model's reading of an attached document. A rights basis changes only by a recorded human declaration under Law J, carrying the declaring actor and the time.

---

## 2. Voice consent

**Status: bases executable as recorded metadata; separation enforcement specified.**

The five bases from [`../v4/VOICE_CONSENT.md`](../v4/VOICE_CONSENT.md) are restated in force, unchanged:

| Subject | Basis needed |
|---|---|
| The author themselves | None. Their own writing, their own voice. |
| A fictional character | None. No person exists to have rights. |
| A synthetic voice built from stated traits, not samples | None. |
| A team or house voice, from work the organization owns | The author's statement that the organization owns it. |
| A named third party | An explicit statement that the author is authorized. |

Ask once, plainly, and take the answer. Public figures are not an exception — quoting one is journalism and the proof protocol handles it with verbatim spans; generating new text in their voice is a different act with the same requirement as anyone else. Deceased persons vary by jurisdiction; note the variance once and move on.

**The v5 addition:**

> **A writing-style profile and an acoustic voice profile are separate permissions requiring separate bases. Authorization for one is never authorization for the other.**

They are different objects doing different work. A writing-style profile is a measurement of how a person constructs sentences — length distribution, abstraction tolerance, metaphor density, syntactic preference. It is a set of ranges. An acoustic voice profile is a model of how a person *sounds* — timbre, prosody, pace, the specific physical signature of one throat. It is derived from recordings of their body.

The permission questions diverge completely. A team voiceprint built from work an organization owns is a routine, unremarkable thing; the organization owns the writing. That same organization owning the writing establishes nothing whatsoever about the employee's recorded voice, which is not work product and in much of the world is protected as an attribute of the person rather than as intellectual property. Personality and publicity rights, biometric statutes, and the specific and rapidly moving law on synthetic voice all attach to the acoustic profile and not to the prose measurement. Collapsing them — treating a signed content agreement as covering both — is the most likely way a well-run project acquires a rights problem it did not know it had.

So the graph holds two separate declarations, and the second one has its own gate condition:

```
$ python3 scripts/wi.py gate --target public-summary

BLOCK — 1 rights condition

  vp-0009  acoustic voice profile  ·  subject: A. Reyes (named third party)
    style profile basis:    contract         (declared 2026-01-08, act-0003)
    acoustic profile basis: unknown
    A style-profile authorization does not extend to an acoustic profile.
    Routes: declare_acoustic_basis · remove_asset · restrict_target
```

---

## 3. Expiry and re-check

**Status: specified.**

`rights.expires_at` is a date, and a date in the past is a **gate condition, not a footnote.**

```
$ python3 scripts/wi.py gate --target funder-report --mode strict

HOLD — 2 rights conditions

  as-0088  image/jpeg   licensed   expired 2026-01-31   (37 days ago)
           scope: publication, print, one edition
           used by: structure.section se-0011 (figure 3)
           routes: renew_license · replace_asset · remove_from_target · waive

  as-0119  video/mp4    permission expires 2026-04-02   (in 24 days)
           scope: program report and public summary
           used by: structure.section se-0022, release target public-summary
           routes: renew_before_publication · note_and_proceed

  1 asset re-checked and current: as-0142 (permission, no expiry)
```

**Why an expiry is a gate condition rather than a report line.** A licence that expired last month is not a documentation problem; it is the state of a document that is about to be published without the right to publish part of it. It has all the properties of a stale anchor — it was true, it is not true now, nothing about the artifact changed, and it is invisible to a reader — so it takes the same machinery: a dependency, a staleness computation and a verdict. Under Law I, an expiry date is a dependency on a clock, and a clock is the one dependency guaranteed to change.

The near-expiry line matters for the same reason the "not affected" list matters in an impact report. A rights check that only fires after the fact teaches people to work around it. One that says *this expires in 24 days and here is where it is used* is a check people keep switched on.

---

## 4. Deletion

**Status: specified.**

A subject asks that their raw voice samples be deleted. Or a contract ends, or a retention policy fires, or someone simply changes their mind. The system must be able to honor that without either destroying the work that was legitimately built or pretending the deletion did not happen.

| Retained | Dropped |
|---|---|
| The `media.asset` node's logical identity and its deletion event | The raw bytes in the object store |
| Approved non-identifying aggregate style metrics, **where policy permits** | Any recording, excerpt, waveform or derived acoustic profile |
| The digest of the deleted object, so prior attestations remain checkable as *references* | Transcripts containing identifying content, unless separately permitted |
| Decision and consent records about the asset | Anchors resolving into the deleted bytes — they become `WI_SOURCE_VERSION_MISSING` |
| The rights block, with `basis` set to the post-deletion state | The subject label, where policy requires unlinking |

```
$ python3 scripts/wi.py explain as-0142

media.asset as-0142   ·   status: deleted
  deletion event  del-0003   2026-05-02T10:12:55Z   actor act-0007 (human)
  basis           subject request, recorded at obj:sha256:5f1c...9d40

  Retained:  logical identity · deletion event · consent record · rights block
             aggregate style metrics agg-0021 (approved, non-identifying)
  Dropped:   raw audio object sha256:6e29...aa41
             acoustic profile vp-0009
             2 transcript segments

  3 anchors into this asset now resolve to WI_SOURCE_VERSION_MISSING.
  2 claims lose their support and enter needs_source.
  1 release artifact is affected: dist/summary.pdf — its attestation is now INVALID.

Checks run: object presence · anchor resolution · closure recomputation.
```

Two rules make this honest.

**A deletion is itself a recorded event.** It has an actor, a time, a basis and a digest. A system that deletes by making things vanish cannot answer *why is this missing*, and "we cannot tell whether that ever existed" is a worse answer to a subject than "it existed, here is when it was removed and on whose instruction." The event is the receipt.

**The consequences are computed and reported, not hidden.** Deleting an asset breaks proofs that stood on it, and the closure says so immediately — the artifact's attestation goes `INVALID` rather than quietly continuing to assert a verification whose evidence no longer exists. That is the correct outcome. An attestation that survives the deletion of its evidence is exactly the false confidence this system exists to prevent, arriving from the one direction nobody expects.

---

## 5. Redaction-aware export

**Status: executable — all three bundle profiles (`full`, `hash-only`, `redacted`) build and verify offline.**

A `.wiab` bundle has three profiles, and the difference between them is a rights difference before it is a technical one.

| Profile | Contains | Rights consequence | Verifies offline |
|---|---|---|---|
| **Full** | Every source object's bytes, every anchor, every result, every decision | **Redistributes source bytes** and therefore inherits their licences. Every asset's `rights.scope` must permit redistribution. | Yes, completely — a stranger can re-resolve every anchor |
| **Hash-only** | Digests, anchors, results and decisions; **no source bytes** | Redistributes nothing. Carries no licence obligation from the sources. | Yes, for integrity, structure and closure — a verifier confirms the proof is internally consistent and unaltered, and cannot re-read the evidence |
| **Redacted** | Only approved excerpts, at the anchor granularity policy permits, with everything else digest-only | Redistributes the excerpts and inherits only their permissions. Requires a per-excerpt approval. | Yes, for the approved excerpts and the whole closure |

Who accepts what, plainly:

- **A publisher** will generally accept a **redacted** bundle. They need to see the specific passages behind the specific claims their legal review is worried about, and they do not want — and often may not receive — a full copy of every underlying source.
- **A funder** will generally accept a **hash-only** bundle. Their question is whether the process happened and holds together, and hash-only answers it without moving a single confidential document out of the workspace. It is also the profile most likely to survive an organization's own data policy.
- **A court**, or an adversarial reviewer acting like one, will want a **full** bundle. The point of the exercise is that nothing was curated, and any profile that lets the producing party choose which bytes travel is a profile whose omissions are an argument. This is also the profile with the highest rights cost, and that cost is a real constraint on discovery rather than a technicality.

The rule that makes hash-only honest: **a bundle states its own profile, and `wi verify-release` reports what it could not check.** A hash-only bundle that presented itself as a complete verification would be the security failure in the adversarial suite named "omitted source object in a hash-only bundle." The verifier says which anchors it confirmed by digest and which it confirmed by re-reading, every time, without being asked.

---

## 6. Attribution and quotation

**Status: citation validation executable; citation rendering specified.**

The system's position on citations is two sentences and they do not bend.

**It will format an approved bibliographic record.** Given a source the author supplied, with fields the author or an adapter established, it will render that record into a requested style — consistently, across a whole document, with the same identity behind every rendering so a changed field updates everywhere.

**It will never invent a source record to satisfy formatting.** Not a missing page number, not a guessed publication year, not a plausible volume, not a DOI that has the right shape. If a field is absent, the rendered citation is incomplete and says so, and the gate reports it as an incomplete record rather than emitting a complete-looking one. A well-formed citation is the most convincing artifact in academic and professional writing, and manufacturing one is the single most damaging thing this system could do quietly. Under Law E, a missing field resolves to a stated gap.

Some projects go further, and the system supports them:

> **Policy can disable citation rendering and keep only citation validation.**

Where a project's doctrine requires that even formatting stay human-authored — a scholarly practice, an editorial standard, an institutional rule about what a machine may touch in a manuscript — `citation.render: false` turns off every rendering path while leaving `citation.resolution` fully active. The author writes every citation themselves; the system checks that each one resolves to a supplied source, that the fields match the record, and that nothing points at a document nobody supplied. That is a legitimate configuration and a coherent one: validation is the part that catches errors, and rendering is the part that is merely convenient.

---

## 7. What this document is not

**This is not legal advice.** It is a data model that makes rights state inspectable, so that a lawyer, a rights manager, a publisher or a subject can look at it and reach their own conclusion.

That sentence is the boundary, and stating it does not soften anything above it. The fields are real fields. The gate conditions are real gate conditions. `unknown` really does block a publication target under a policy that requires established rights, and a system that let it through while displaying a rights table would be doing the exact thing Law C exists to forbid — presenting the visual language of diligence over an absence. What the system does not do is decide whether a basis is *sufficient*. It records what the basis is, who declared it, when, and what it covers, and it refuses to let that record be produced by anything other than a person.

---

## 8. What is executable and what is specified

| Mechanism | Status |
|---|---|
| Rights and identity fields recorded as asset metadata, with `unknown` as a first-class value | Executable |
| Voice consent bases recorded per subject | Executable |
| Citation resolution against supplied sources | Executable in `scripts/wi.py` |
| `.wiab` full and hash-only bundle build and offline verification | Executable in `scripts/wi.py` |
| Rights gate conditions — `unknown` basis, expiry, missing acoustic basis | Specified |
| Style-profile / acoustic-profile separation enforcement | Specified |
| Deletion events, retention split, and closure recomputation after deletion | Specified |
| Redacted bundle profile with per-excerpt approval | Specified |
| `citation.render: false` policy | Specified |

---

## Related documents

- [`CONSTITUTION.md`](CONSTITUTION.md) — Law J, the actor model, and why a declaration needs a person behind it
- [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md) — the anchor kinds these assets carry
- [`SECURITY_MODEL.md`](SECURITY_MODEL.md) — privacy defaults, telemetry and webhook redaction
- [`STORYWORLD_OS.md`](STORYWORLD_OS.md) — realm safety, for work that mixes real people with constructed worlds
- [`NON_GOALS.md`](NON_GOALS.md) — why the system will not generate a source
- [`../v4/VOICE_CONSENT.md`](../v4/VOICE_CONSENT.md) — the five bases, carried forward
- [`../v4/PROOF_PROTOCOL.md`](../v4/PROOF_PROTOCOL.md) — citation resolution in its original form
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
