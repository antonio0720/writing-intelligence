# Writing Intelligence v5

[![Release](https://img.shields.io/github/v/release/antonio0720/writing-intelligence?label=release&color=0b7285)](https://github.com/antonio0720/writing-intelligence/releases/latest)
[![License: MIT](https://img.shields.io/badge/license-MIT-0b7285)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-none-0b7285)](scripts/wi.py)

**The Proof-Carrying Authorship OS.**

Every writing tool on the market makes prose *sound* better. None of them can tell you whether the sentence you are about to send is one you can defend.

This one can — and it can prove it to someone who does not trust you, offline, with no model running.

**Free. Open source. MIT. No account, no server, no API key, no telemetry. Forever.**

Created by **[Antonio T. Smith Jr.](https://densitysix.com)** — Founder & CEO, [Density6 LLC](https://densitysix.com)

[**See it work**](#see-it-work) · [**Quickstart**](#quickstart-two-minutes) · [**Install**](#install) · [**The twelve laws**](#the-twelve-laws) · [**What it refuses to do**](#what-it-refuses-to-do) · [**What is not built yet**](#what-is-specified-and-not-yet-executable)

---

## See it work

A grant narrative cites a program's outcomes report. Six months later the agency reissues the report and one number moves.

Every writer knows what happens next: search the manuscript, hope you found every instance, hope somebody updated the board deck, hope the website is not still quoting the old figure, hope the footnote still points at the right page.

Here is what happens instead.

```
$ wi impact sources/outcomes_report.txt --apply

Source changed: outcomes_report.txt
  was  66f7d08b
  now  6faba17a  sha256:a8a1aaedb4b4
  1 changed byte range(s)

Affected:
     1  claim atom
     1  evidence anchor
     1  paragraph
     1  document
     1  verification record

Unaffected:
     4  evidence anchor(s) provably outside the change
     5  claim atom(s) still verified

Cheapest safe repair (cost 4):
  1. re-anchor 1 claim(s) to the current source version
  2. re-run deterministic checks on 1 claim atom(s)

Marked 5 node(s) stale. `wi gate` will hold until they are repaired.
```

Read the second block again. **Unaffected.** Not "reverify everything." Five claims are provably untouched, because their evidence anchors sit outside the bytes that moved, and the system can show its work on that. A tool that panics about the whole document on every edit gets ignored inside a week. This one tells you the truth and hands you the shortest safe path back to green.

That is not a demo. It is `tests/v5/EXPECTED_TRANSCRIPT.txt`, reproduced by a regression suite that runs in CI, and you can run it yourself in about ninety seconds.

---

### Ask a sentence why it exists

```
$ wi explain drafts/report.md:5

a0001  sourced_fact
  "Between 2019 and 2022, the Delta Regional Capacity Program served 11,800 households across seven counties"
  status   supported
  realm    external_fact
  quantity 11800 households
  when     2019 to 2022
  modality is
  anchors:
    outcomes_report.txt  bytes 66-171  sha256:347be3eca9f7
      > Between 2019 and 2022, the Delta Regional Capacity Program served 11,800 households across seven counties
  checks:
    anchor.integrity       pass       verified
    numeric.value          pass       verified
    date.range             pass       verified
    entity.presence        pass       verified
  used by  1 structure.paragraph, 1 verification.result
```

Not "the source agrees." **Bytes 66 to 171 of this exact version of this exact file, with this digest, and here is the text.** Point at it in a meeting. Hand it to counsel. It does not require anyone to believe anything.

---

### Know what an edit did to your meaning

```
$ wi diff drafts/report.md drafts/report-v2.md --semantic

6 changed · 0 added · 0 removed · 2 change(s) invalidate existing proof

BEFORE  Sustained case management may reduce median intake wait time by 38 percent...
AFTER   Sustained case management reduces median intake wait time by 38 percent...
EFFECT  certainty_strengthened
PROOF   existing support does not carry forward (certainty_strengthened)
```

One word moved. The claim changed. The proof that covered the hedged version does not cover the confident one, and the system says so before you send it — rather than after a reviewer does.

---

### Let a stranger verify your release

```
$ wi verify-release delta.wiab

PASS  archive.integrity
PASS  object.digests
PASS  release.artifact_digest
PASS  graph.reference_integrity
PASS  proof.dependencies
PASS  release.stale_closure
PASS  manifest.counts

Checks the producer states were NOT run:
  - paraphrase entailment (judgment tier; no provider configured)

RELEASE MANIFEST VALID
```

On a different machine. With no network. With no model. The bundle carries the source hashes, the claim graph, every check that ran, **every check that did not**, and the digest of the artifact that was approved. Swap one figure inside the sealed file and it fails with `WI_RELEASE_TAMPERED` — not eventually, immediately, and for the correct reason.

This is the line that matters: **your work stops depending on whether people trust you, and starts depending on whether the digests match.**

---

## Why this exists

Language models are fluent before they are correct, and fluency reads as diligence. A confident paragraph with a fabricated citation looks exactly like a confident paragraph with a real one. The reader cannot tell. Increasingly, neither can the author.

Four versions of this project have been circling one idea and finally arrived at it:

> *If a claim cannot be pointed at, it has not been verified. And once it has been pointed at, everything that depends on it has to know when it moves.*

**v3** made writing governable. **v4** made claims accountable. **v5** makes authorship *inspectable across time, evidence, people and media* — because a claim you verified in March and a source that changed in August are the same problem, and nothing else in this market treats them that way.

---

## Quickstart (two minutes)

`scripts/wi.py` is one stdlib-only Python 3.8+ file. No install, no dependencies, no network, no account. Copy it anywhere Python exists, including an air-gapped review machine.

```bash
git clone https://github.com/antonio0720/writing-intelligence
cd writing-intelligence
alias wi="python3 $PWD/scripts/wi.py"

# Copy the shipped fixture project — real sources, a real draft
cp -r tests/v5/world ~/wi-demo && cd ~/wi-demo

wi init --mode strict            # .wi workspace: index + object store
wi ingest sources/               # content-addressed, immutable versions
wi atomize drafts/report.md      # sentences become claim atoms
wi anchor .wi/graph/ledger-*.json sources/
wi gate .wi/graph/ledger-*.json  # RELEASE
```

Now break it on purpose. Change `11,800` to any other figure in `sources/outcomes_report.txt`, then:

```bash
wi impact sources/outcomes_report.txt --apply   # the block at the top of this page
wi gate .wi/graph/ledger-*.json                 # HOLD, naming the one claim
wi explain drafts/report.md:5                   # and why
```

Full walkthrough: [**`USER_GUIDE.md`**](USER_GUIDE.md) · one-page reference: [**`CHEATSHEET.md`**](CHEATSHEET.md)

---

## The unit changed

v4 verified sentences. v5 verifies **claim atoms**, and this is the difference you feel first.

> Between 2019 and 2022, the program served 11,800 households across seven counties, and median wait time fell from 42 days to 26 days.

One sentence. Four independently checkable assertions. As a sentence it is supported or it is not, and one bad figure poisons three good ones. As atoms, three stay green and only the fourth gets marked, repaired and reverified.

| Status | What it means |
|---|---|
| `supported` | Appears verbatim in a supplied source |
| `quote_verified` | The quoted text appears verbatim |
| `span_supported` | Every checkable component — figures, dates, entities — found **co-located inside one span of one source** |
| `candidate_support` | Components found, but scattered across the corpus rather than co-located |
| `author_asserted` | The author's own observation; they are the source |
| `inference` | Reasoning from premises, not a sourced fact |
| `needs_source` | Nothing locates it, or a figure contradicts every source |
| `conflicted` | A quotation was reshaped, or sources disagree |
| `unsafe` | A citation resolves to nothing supplied — **blocks, always** |

`span_supported` is the honest middle v4 threw away. "These numbers exist somewhere in my sources" and "these numbers, dates and entities all appear together in this one sentence of this one source" are not the same claim, and the second is a real deterministic result. It is never rendered as `supported`, and neither is ever rendered as *true* — support is verified **within the sources you supplied**. If your source is wrong, the claim reads supported and is false. That sentence is printed by the tool, not buried in a footnote.

---

## What changed: v4 → v5

| v4.0 | v5.0 |
|---|---|
| The sentence is the unit of verification | The **claim atom** is — a compound sentence can be partly supported |
| Support is a verbatim span of a file | Support is an **evidence anchor**: byte range, quote digest, exact source *version* |
| Sources are files | Sources are **content-addressed artifacts with immutable versions**; raw bytes hashed before any normalization |
| A ledger per run | A **persistent authorship graph** — SQLite index plus a content-addressed object store |
| Stale was a status nobody could compute | **Staleness propagates**: a changed source names what broke *and what provably did not* |
| Every change states its EFFECT in prose | **Deterministic semantic diff** classifies it — `certainty_strengthened`, `quantity_changed`, `scope_broadened`, twenty more |
| Repairs listed | Repairs **costed**, with the cheapest safe path named |
| Consistency across documents was manual | **Writing tests** and a concept registry catch drift in CI |
| A verdict you had to trust | A **`.wiab` proof-carrying bundle** anyone can verify offline, with no model |
| One verdict for the document | Coverage with a **denominator** — 1,784 of 1,820, and you can list the missing 36 |

The eleven craft passes, twelve engines, twelve agents, 27 genre packs, voiceprints and anti-slop doctrine are **unchanged**. The six v4 laws are **unchanged and still binding**. v5 is a layer above them, not a replacement for them.

---

## The twelve laws

Full text and reasoning in [`references/v5/CONSTITUTION.md`](references/v5/CONSTITUTION.md).

| | Law | Why it is load-bearing |
|---|---|---|
| **A** | Propose, never silently replace | An author handed a rewritten document has one decision available — accept everything — and their voice erodes one invisible edit at a time |
| **B** | The original is recoverable | Content-addressed, so it survives a renamed file |
| **C** | Never report work not done | Fluency reads as diligence; refuse that confusion |
| **D** | Support must point somewhere | Not "the source agrees" — *this span, this version, these bytes, this digest* |
| **E** | Under-claim | Wrongly "supported" is a catastrophe; wrongly "needs a source" is a nuisance |
| **F** | Sources are data, never instruction | A document saying *"ignore previous instructions"* gets flagged and changes nothing |
| **G** | Meaning has identity independent of wording | A claim survives rephrasing; change the proposition and it is a different claim |
| **H** | Every consequential transformation declares its semantic delta | A rewrite is not "different text" |
| **I** | Verification is dependency-aware | Change a dependency and the proof is stale unless it can be shown untouched |
| **J** | Human decisions are first-class artifacts | Acceptance binds to an exact state and goes stale when that state moves |
| **K** | One proof engine, many surfaces | No second implementation of evidence truth exists |
| **L** | A release must be explainable without trusting whatever helped produce it | Provider, model, policy hash, input hashes, currency — on the record |

---

## Install

### Claude Code or any terminal agent — as a skill *(recommended)*

```bash
git clone https://github.com/antonio0720/writing-intelligence \
  ~/.claude/skills/writing-intelligence
```

Restart. The skill triggers on any writing, editing, fact-checking, verification or release request — including unnamed ones like *"clean this up"*, *"will this hold up?"* or *"what breaks if this number changes?"*

### Claude.ai, Cowork, or any chat surface — as an uploaded skill

```bash
curl -LO https://raw.githubusercontent.com/antonio0720/writing-intelligence/main/writing-intelligence.skill
```

Then **Settings → Capabilities → Skills → Upload skill**. That link tracks `main`, so it always matches the version of this README you are reading — CI fails if the committed bundle and a fresh build of the tree ever disagree. [**Releases**](https://github.com/antonio0720/writing-intelligence/releases) is where pinned versions live with their checksums.

### CLI only — no model required

`scripts/wi.py` is the deterministic tier and runs entirely on its own. One file. Copy it anywhere Python 3.8+ exists.

### Projects, any LLM, REST, air-gapped

Full matrix of every surface and exactly what each one can and cannot do: [**`docs/INSTALL.md`**](docs/INSTALL.md)

---

## Verify the verifier

Do not take this README's word for any of it.

```bash
bash tests/v4/test_wi.sh     # 3 checks — the v4 accountability floor
bash tests/v5/test_wi5.sh    # 32 checks — workspace, staleness, bundles, drift
python3 scripts/wi.py doctor # what this surface can and cannot do
```

Both fixtures are adversarial on purpose: an inflated figure, a reshaped quotation, a fabricated citation, a prompt injection buried in a partner document, a tampered release bundle, a source that moves under a verified claim, and a governing figure that drifts between two drafts.

**Every assertion in the v5 suite has a negative twin.** It checks that a tampered bundle is *rejected*, that a stale source *holds* the gate, that concept drift *fails* — not merely that the happy path prints something. CI goes further and runs a mutation check: it disables the artifact-digest comparison and requires the suite to go red. A test suite that cannot fail is decoration, and this project does not ship decoration.

---

## What it refuses to do

The refusals are load-bearing. Full reasoning in [`references/v5/NON_GOALS.md`](references/v5/NON_GOALS.md).

- **Detector evasion.** Anti-slop is a craft objective — prose that does not pattern-match to machine writing because it is genuinely better built. It is not a laundering service.
- **Source generation.** It will never construct a citation. If a claim needs support and none exists, the output is `needs_source`. Inventing a plausible reference is the single most damaging thing this system could do, and the anchor model exists so it cannot happen quietly.
- **Truth verification.** It verifies support within the sources you supplied. It cannot tell you the source is right, and it says so the first time it says anything.
- **Absolute quality scores.** There is no universal writing number, and presenting one is the fake-authority pattern the doctrine already names.
- **Similarity as evidence.** Retrieval finds candidates. Comparison produces proof. High cosine similarity is not support, and no amount of embedding will make it support.
- **A hosted account, a proprietary model, a vector database, or a blockchain.** None of them answer whether the source supports the claim, whether the meaning changed, or whether the anchor points at the right region.

---

## What is specified and not yet executable

This section is a feature of the release, not an apology. Law C applies to the project's own claims about itself.

| Not executable in v5.0 | Status |
|---|---|
| Paraphrase entailment | Provider ABI defined in [`references/v5/JUDGMENT_TIER.md`](references/v5/JUDGMENT_TIER.md); **no provider ships** |
| PDF, DOCX, XLSX, image, audio, video anchors | Contracts defined in [`references/v5/EVIDENCE_ANCHORS.md`](references/v5/EVIDENCE_ANCHORS.md); only `text_span` executes |
| Proposals and decisions as stored records | Laws A and J are conduct today, not persisted objects |
| External signing — Sigstore, C2PA, PROV export | Specified; bundles are hash-verifiable without any of them |
| Workbench, MCP server, REST v5 | Specified in [`references/v5/ARCHITECTURE.md`](references/v5/ARCHITECTURE.md) |
| Compiled Rust/WASM core | Roadmap. Nothing in this release requires it |

A binary file you hand it today is **reported as needing extraction**, never silently skipped. `wi doctor` prints this list on demand, on any surface, so the tool can never look more capable than it is.

---

## The craft core (unchanged from v3)

<details>
<summary><strong>The 11-pass kernel</strong></summary>

| Pass | Name | Artifact |
|---|---|---|
| 0 | Intake Contract | `IntakeContractV3` |
| 1 | Mission Lock | `MissionLockV3` |
| 2 | Corpus & Context Ingestion | `CorpusMapV3` |
| 3 | Diagnostic Scan | `DiagnosticReportV3` |
| 4 | Architecture Compile | `ArchitecturePlanV3` |
| 5 | Evidence & Epistemic Ledger | `EpistemicLedgerV3` |
| 6 | Sentence Surgery | `SentenceSurgeryLogV3` |
| 7 | Voice Restoration | `VoiceMatchReportV3` |
| 8 | Genre & Arena Alignment | `ArenaAlignmentV3` |
| 9 | Adversarial Stress Battery | `StressBatteryV3` |
| 10 | Score & Delivery Packaging | `DeliveryBundleV3` |
| 11 | Memory & Benchmark Update | `MemoryBenchmarkUpdateV3` |

</details>

<details>
<summary><strong>12 engines · 12 specialist agents</strong></summary>

**Engines:** Intake Contract · Corpus Governance · Voice Fingerprint · Genre Stack · Architecture Graph · Epistemic Ledger · Prose Compiler · Narrative Intelligence · Arena Delivery · Benchmark & Regression · Agent Orchestration · Certification & Governance

**Agents:** Intake Architect · Corpus Auditor · Voice Fingerprinter · Genre Marshal · Structure Engineer · Evidence Prosecutor · Sentence Surgeon · Dialogue Commander · Narrative Architect · Stress Tester · Scorekeeper · Delivery Packager

Runs as one skill or as a coordinated multi-agent board — see [`agents/agent_manifest.yaml`](agents/agent_manifest.yaml).

</details>

<details>
<summary><strong>27 genre packs</strong></summary>

academic · church_leadership · cinematic_narration · dialogue · email · fiction · government_brief · grant_nofo · journalism · legal_positioning · loan_officer · medical_writing · newsletter · patent_claims · pitch_deck · real_estate · resume_cover_letter · sales · sermon · small_business_operator · social_media · speech · strategy · technical_documentation · thriller_scene_architecture · transmedia_character · youtube_script

Every pack shares one structure: purpose → when to use → when not → audience model → required evidence → forbidden claims → voice weighting → structure templates → scoring adjustments → failure modes → before/after → stress tests → delivery formats → schema hooks → benchmark cases.

</details>

<details>
<summary><strong>Schemas</strong></summary>

11 v3 craft schemas (`schemas/`) plus 15 v5 state schemas (`schemas/v5/`): workspace · source artifact · source version · evidence anchor · claim atom · graph node · graph edge · verification record · judgment record · proposal · decision · invalidation · policy · concept registry · release manifest.

Schemas are what turn a skill into infrastructure: CLI execution, CI writing checks, automated scoring, reproducible output, and a bundle a stranger can parse.

</details>

---

## Repository map

```
SKILL.md                  The skill. Start here if you are a model.
scripts/wi.py             The canonical deterministic core. One file, stdlib only, offline.

references/v5/            The proof-carrying layer (20 documents)
  CONSTITUTION              The twelve laws, reliability types, realms, actors
  AUTHORSHIP_GRAPH          Nodes, edges, identity, proof closure, storage
  SEMANTIC_IR               Claim atoms, meaning dimensions, renderers
  EVIDENCE_ANCHORS          Seven anchor types; text spans execute today
  SEMANTIC_DIFF             The delta taxonomy and what each does to proof
  STALENESS                 Invalidation, minimum repair frontier, repair costs
  CONCEPT_REGISTRY          The semantic ABI and writing tests
  PROOF_CARRYING_RELEASE    .wiab bundles, profiles, offline verification
  POLICY_AS_CODE            wi.policy.yaml, evidence modes, authority
  JUDGMENT_TIER             Provider ABI, isolation, disagreement, calibration
  MULTIMODAL                Audio, video, images, charts, script-shot binding
  STORYWORLD_OS             Canon graph, character state, transmedia invalidation
  WORKSPACE                 .wi layout, lockfile, reproducibility classes
  CANONICAL_HASHING         Serialization contract and the WI_ error taxonomy
  SECURITY_MODEL            Threat model, sandbox, injection, tamper
  RIGHTS_AND_CONSENT        Licence, likeness, voice, deletion, redaction
  RELIABILITY_TYPES         verified / measured / judged / human-declared
  SURFACES                  What each surface may honestly claim
  NON_GOALS                 What this refuses to do, and why
  ARCHITECTURE              Diagnosis, milestones, CI matrix, contributor map

references/v4/            The accountability layer (8 documents, still binding)
references/compiler/      19 craft engines
references/genre_packs/   27 domain packs
references/voiceprints/   8 voiceprints + fingerprint engine + builder
references/anti_patterns/ 7 slop taxonomies
references/diagnostics/   6 diagnostic systems

schemas/                  11 v3 craft schemas
schemas/v5/               15 v5 state schemas
agents/                   12 specialist agents + manifest
tests/v4/                 Adversarial fixture: injection, misquote, fake citation
tests/v5/                 Fixture world + 32-check regression + expected transcript
benchmarks/               Benchmark harness and cases
docs/                     Install, operator manual, builder guide, migration
governance/               RFC, ADR, versioning, release checklist
services/api/             REST reference runtime for the v3 craft kernel
```

---

## Documentation

| Document | For |
|---|---|
| [`USER_GUIDE.md`](USER_GUIDE.md) | Working with the system day to day |
| [`CHEATSHEET.md`](CHEATSHEET.md) | One page, every command, mode and status |
| [`docs/INSTALL.md`](docs/INSTALL.md) | Every surface and what each can actually do |
| [`docs/MIGRATION_v4_to_v5.md`](docs/MIGRATION_v4_to_v5.md) | Upgrading from v4 |
| [`references/v5/README.md`](references/v5/README.md) | Index of the v5 doctrine |
| [`schemas/v5/README.md`](schemas/v5/README.md) | Building on the state model |
| [`docs/OPERATOR_MANUAL.md`](docs/OPERATOR_MANUAL.md) | Running it as an operator |
| [`docs/VOICEPRINT_GUIDE.md`](docs/VOICEPRINT_GUIDE.md) | Building a voiceprint |
| [`docs/DOMAIN_PACK_GUIDE.md`](docs/DOMAIN_PACK_GUIDE.md) | Writing a new genre pack |
| [`docs/BUILDER_GUIDE.md`](docs/BUILDER_GUIDE.md) | Building on the schemas |
| [`ROADMAP.md`](ROADMAP.md) | Where it goes next |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Contributing |

---

## Why it is free

Because the thing that has to spread is the standard, not the software.

An author who can prove what they wrote is only safe if the people reading them know what that proof looks like. A verification format nobody else can read protects nobody. So the format is open, the verifier is one file with no dependencies, the bundle can be checked by a stranger on a machine that has never heard of this project, and none of it costs anything or phones anywhere.

Take it. Fork it. Put it in your newsroom, your grants office, your law firm, your classroom, your publishing house, your government agency. Ship it inside your own product if you want to — the licence permits it.

[MIT](LICENSE). Credit appreciated: **Antonio T. Smith Jr. / Density6 LLC**.

---

## Author

**Antonio T. Smith Jr.** is the Founder and CEO of [Density6 LLC](https://densitysix.com) and the inventor of Operational Machine Consciousness (OMC) and Existential Recursive Intelligence (ERI).

**[densitysix.com](https://densitysix.com)** · **[@theatsjr](https://instagram.com/theatsjr)**

---

*v1.0 proved AI-sounding prose can be defeated by compilation instead of cosmetic cleanup. v2.0 proved fiction can be engineered as a living architecture. v3.0 proved authorship can be governed without being flattened. v4.0 proved it can be held accountable. **v5.0 proves it can be inspected — across time, evidence, people and media — by someone who has no reason to trust you.***
