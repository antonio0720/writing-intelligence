# Versioning — Writing Intelligence

Writing Intelligence follows [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH).

The version number is a promise about what still works. Since v6 the system also
publishes **digests** — a state digest, a graph root, a capsule closure root — and a
digest is a promise of a different kind: it says *this exact object*. A version number
that moves without warning breaks a build. A digest that moves without warning breaks
every proof that ever named it, on machines this project has no access to, in a way
that looks like tampering rather than an upgrade.

So this document has two halves. The first is the ordinary semver contract. The second
is [digest stability](#digest-stability-is-a-compatibility-surface), which is the harder
one and the one a well-meant cleanup breaks.

---

## MAJOR

Bump MAJOR when a release breaks backwards compatibility.

**Inherited from v3–v5, unchanged:**

- Kernel changes that invalidate prior intake contracts
- Schema changes that break existing artifact consumers
- Removal of public-facing APIs, rewrite operators, or output modes
- Changes to the v3.0 Law or the Irreversibility laws
- Changes to canonical serialization — NFC normalization, key ordering, decimal
  representation, escaping, or the contents of any digest preimage
- Changes to the meaning of `verified`, `stale`, `BLOCK`, `permitted` or
  `source quarantine`
- License changes

**Added by v6:**

| Change | Why it is MAJOR |
|---|---|
| The v6 state digest computation, or the domain separation between v5 and v6 | Every digest in every workspace moves. See [digest stability](#digest-stability-is-a-compatibility-surface) |
| The graph root computation in `ObjectStore.put_root` | A branch head is a root digest. Every commit, decision binding and simulation comparison is stated in terms of one |
| The capsule closure root or its Merkle construction | A `.wic` that verified yesterday fails today, and the failure is indistinguishable from a tampered capsule |
| Any of the eighteen laws A–R | The laws are what the system is. `references/v6/CONSTITUTION.md` is the text |
| A schema change in `schemas/v6/` that invalidates existing graph roots | The schema id and version are bound *into* the digest preimage. Changing either moves every digest of that schema, whether or not the payload changed |
| Removing or renaming a member of the closed capability vocabulary | `wi authority issue` refuses a capability outside `V6_CAPABILITIES`. Renaming one turns every grant naming it into a grant nothing recognises |
| Removing or renaming a member of the closed delta-class vocabulary | Delta class decides required authority. A rename silently changes who may accept a change |
| A change to merge conflict typing — which comparisons produce a conflict, or which kind a conflict is given | Conflict kind is what a resolver reads before deciding. Reclassifying quietly changes who is asked and what they think they are answering |
| Anything that permits a merge to resolve a semantic conflict automatically | Law Q. It is a refusal, not a default — see [`RFC_PROCESS.md`](RFC_PROCESS.md) |

A MAJOR bump requires:

- A migration guide (`references/v6/MIGRATION_V5_TO_V6.md` is the current example)
- An RFC explaining the break and its necessity
- A statement of what happens to artifacts already in circulation — bundles, capsules,
  workspaces — including the ones already sent to people who will never read this file
- Maintainer (Antonio T. Smith Jr.) sign-off

---

## MINOR

Bump MINOR when a release adds capability backwards-compatibly.

- New genre packs
- New voiceprints
- New rewrite operators
- New scoring rubrics
- New agents
- New output modes
- New domain pack categories
- New deterministic checks
- New graph constraints
- **New members of a closed vocabulary** — a capability, a delta class, a conflict kind,
  an actor kind or a scope kind — *provided* existing members keep their names and their
  meanings, and no existing digest moves

A MINOR bump requires:

- Benchmark cases for the new capability
- Documentation updates, with every new capability marked *executable in
  `scripts/wi.py`* or *specified*
- A **negative fixture** for every new deterministic check or refusal, shown failing with
  the implementation disabled. A guard that has only ever passed has not been shown to
  work, and its green line is indistinguishable from a broken one
- No breaking changes to existing schemas
- No digest movement

**A new obligation is a MINOR that every prior release reports as unmet.** That is the
correct behaviour and it is worth stating so nobody treats it as a regression: obligations
are derived from typed state, so adding one means every historical node now owes something
it was never checked against. Reporting that honestly is the point of a derived set rather
than a hidden checklist.

---

## PATCH

Bump PATCH when a release fixes bugs or polish without adding capability:

- Documentation fixes
- Typo corrections
- Anti-pattern library updates
- Benchmark case additions inside existing categories
- Performance improvements
- Internal refactors with no API change **and no digest change**

The last clause is the one that catches people. A refactor that changes how an object is
built — reordering a dict literal that feeds a canonicalizer, changing a default that
lands in a payload — is not a PATCH, whatever the diff looks like. Run `wi canon` on the
fixture world before and after and compare.

---

## Digest stability is a compatibility surface

**A released digest is a public identifier.** It is quoted in a capsule, in a decision
record, in a release manifest, in a proposal binding, and in whatever a reader wrote down
when they verified something. Some of those live outside this repository, on machines this
project cannot reach, in filings that cannot be reissued.

**Moving a digest silently is the worst break this project can ship.** Not because the
consequence is large — a broken build is also large — but because of what the failure
*looks like*. A capsule whose state digest no longer matches reports `VERDICT TAMPERED`.
A release bundle whose artifact digest no longer matches reports `WI_RELEASE_TAMPERED`.
Those are the correct words for the check that ran and the wrong words for what happened,
and the reader has no way to tell the difference. A verifier that cries tampering after
an upgrade is a verifier nobody believes the next time, which is precisely the time it
matters.

So:

1. **Any change to a digest preimage is MAJOR.** The v6 preimage binds, in order: the
   domain tag `wi-state-v6`, the schema id and `V6_SCHEMA_VERSION`, the normalization
   version, the canonical payload length, and the canonical payload. The v5 preimage binds
   the domain tag `wi-state-v5`, the schema id and `SCHEMA_VERSION`, the normalization
   version, and the payload. Every field in both is load-bearing. Adding, removing or
   reordering one is a break.

2. **A digest change is announced in `CHANGELOG.md` before it is discovered.** A release
   that moves a digest says which digests move, for which object kinds, and what happens
   to artifacts already produced. A reader who verifies a capsule the week after an upgrade
   must be able to find the sentence explaining the failure faster than they can conclude
   they were attacked.

3. **A digest change requires a migration path stated as a refusal.** Not *the old digests
   are wrong now* — a statement of what a holder of an old artifact should do, and what
   this release cannot do for them. Re-anchoring an old capsule to a new digest is not
   available and will not be built: it would mean the producer can restate what was
   attested, which is the property the capsule exists to remove.

4. **The stability test is `wi canon` on the fixture world, run before and after.** Key
   order and Unicode form must not move a digest; a changed value must. Both directions
   are asserted in `tests/v6/test_wi6.sh`, because a digest that never moves and a digest
   that always moves are equally useless and only one of them looks broken.

5. **Three digest surfaces move independently and must be checked independently.**

   | Surface | Produced by | Moves when |
   |---|---|---|
   | v6 state digest | `wi canon`, every semantic node | The preimage, the canonicalizer, the schema id or `V6_SCHEMA_VERSION` changes |
   | Graph root | `wi commit`, `wi simulate`, `wi branch` | Any node state moves, or the root object's own shape changes |
   | Capsule closure root | `wi capsule create` | Any leaf moves, or the Merkle construction or its domain tags change |

   A root is pure state — no timestamp, no author, no counter — which is what makes
   *unchanged* an equality test on 32 bytes rather than a walk. That property is a
   compatibility surface too: adding a field to the root object breaks it.

**The one exception, and it is not an exception to the rule above.** The v5 digest and the
v6 digest of a byte-identical payload differ, deliberately, by domain separation. That is
not drift and it is not a break; it is the guarantee described next.

---

## The v5/v6 domain-separation rule

**A byte-identical payload must never be ambiguously readable as both a v5 and a v6
object.** The two layers make different promises about what a payload means, and a single
identity spanning both would let a claim about one be presented as a claim about the other.

Stated as a versioning constraint:

- Every digest domain carries a distinct tag in its preimage. Today those are
  `wi-state-v5`, `wi-state-v6`, and the capsule tags `wi-closure-node-v6` and
  `wi-closure-empty-v6`.
- **A new layer takes a new tag.** Reusing an existing tag for a new object kind is a
  MAJOR change even when no byte of any existing payload moves, because it makes two
  different things collide in one identity space.
- **Removing domain separation is not available at any version.** It would not appear in a
  diff as a security change. It would appear as a simplification.
- A future core — compiled, WASM, or another language — must reproduce every domain tag
  byte for byte. `references/v6/BUILD_MANIFEST.md` §9 makes this a parity gate: two cores
  that canonicalize identically and separate domains differently produce different
  identities for the same object, and nothing detects it until a verification fails on the
  wrong machine.

---

## Pre-Release

Use suffixes for pre-release versions:

- `6.1.0-alpha.1` — alpha, expect breakage
- `6.1.0-beta.1` — beta, mostly stable
- `6.1.0-rc.1` — release candidate

A pre-release may move a digest. It must say so, in the same words a stable release would
use, because a pre-release artifact is still an artifact somebody may verify a year later.

---

## Skill Bundle Version Alignment

The payload ships as two bundles, and both are versioned with the repository:

- `writing-intelligence.skill` — the runtime
- `writing-intelligence-craft.skill` — the craft library

`SKILL.md` carries the version stamp, and `scripts/build-skill.sh` refuses to build unless
the CLI version, the `SKILL.md` stamp and the `CHANGELOG.md` heading are one number.

**The 200-file ceiling is a versioning constraint, not a packaging note.** A bundle over
the limit does not degrade — it does not load, which turns every install instruction in
the repository into a false claim on the surface where a reader can least check it.
`build-skill.sh` enforces it and prints the arithmetic. Raising `MAX_FILES` is not a fix.

---

## Schema Versioning

Three schema families ship, each under its own namespace:

| Family | Location | Count | Version constant |
|---|---|---|---|
| v3 craft | `schemas/` | 11 | declared per schema |
| v5 state | `schemas/v5/` | 15 | `SCHEMA_VERSION = 5.0.0` |
| v6 runtime | `schemas/v6/` | 20 | `V6_SCHEMA_VERSION = 6.0` |

Schema consumers MUST check version compatibility:

- Same MAJOR.MINOR → fully compatible
- Same MAJOR, different MINOR → backwards-compatible; consumer may need to ignore unknown
  fields
- Different MAJOR → incompatible; consumer must update or use a migration adapter

**The v6 family carries an extra constraint the others do not.** `V6_SCHEMA_VERSION` is
bound into the state digest preimage. Bumping it moves every v6 digest in every workspace,
for every object of every schema, whether or not one field changed. It is therefore a
MAJOR act on its own, and it is not the mechanism for adding an optional field.

---

## Release Cadence

There is no fixed cadence. Releases ship when:

1. A meaningful capability is ready
2. The release passes every gate in [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md)
3. The maintainer signs off

Targets in `ROADMAP.md` and wave statuses in `plans/v6.manifest.yaml` are the plan, not a
contract. `scripts/check-manifest.py` enforces the one thing that is a contract: a wave
marked `shipped` must name commands that appear in `wi --help`, and artifacts that exist.

---

## Deprecation Policy

Capabilities marked deprecated in MINOR releases must be preserved for at least one full
MINOR cycle before removal in the next MAJOR. Deprecation notices appear in `CHANGELOG.md`
and in the relevant doctrine files.

**Nothing that verifies an already-published artifact is ever deprecated.** A `.wiab`
carries the promise that a reader with the file and a Python interpreter can verify it,
offline, with no model and no prior knowledge of the project. That promise has no expiry
date in it, so no release may introduce one. `references/v6/BUILD_MANIFEST.md` §8 states
the same rule as release-candidate requirement J.
