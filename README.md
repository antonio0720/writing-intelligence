# Writing Intelligence v6

[![Release](https://img.shields.io/github/v/release/antonio0720/writing-intelligence?label=release&color=0b7285)](https://github.com/antonio0720/writing-intelligence/releases/latest)
[![License: MIT](https://img.shields.io/badge/license-MIT-0b7285)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-none-0b7285)](scripts/wi.py)

**The Sovereign Meaning Runtime.**

Every writing tool on the market makes prose *sound* better. Some can now tell you whether a sentence is supported. None of them can tell you what a change would do before you make it, who was allowed to make it, or what is still true afterward — and none of them will refuse to invent a number when two people disagree.

This one does all four, offline, with no model running, and can prove it to someone who has no reason to trust you.

**Free. Open source. MIT. No account, no server, no API key, no telemetry. Forever.**

Created by **[Antonio T. Smith Jr.](https://densitysix.com)** — Founder & CEO, [Density6 LLC](https://densitysix.com)

[**See it work**](#see-it-work) · [**60-second tour**](#the-60-second-tour) · [**Install**](#install) · [**The eighteen laws**](#the-eighteen-laws) · [**What runs and what does not**](#what-runs-and-what-does-not) · [**What it refuses to do**](#what-it-refuses-to-do)

---

## What v6 is, in one paragraph

v3 governs *how well* the writing is built. v4 governs *what may be claimed about it.* v5 governs *what depends on what.* **v6 governs what may become true, who may make it true, and what it costs.** A document stops being the thing that is edited and becomes a build of governed meaning. A change is proposed against an exact state before it exists, simulated before it is accepted, accepted only by an actor holding a grant that could have been absent, and applied as one transaction. Authority is scoped and expires. Time is two clocks, not one — when a claim held in the world, and when this workspace believed it. And when two branches assert incompatible states, the disagreement is preserved as a typed conflict rather than smoothed into a third claim neither side made.

> **The v6 law:** *No consequential state transition may become authoritative unless the system can identify the exact prior state, the proposed next state, the semantic delta between them, the dependency impact of that delta, the acting authority, the decision basis and the resulting proof closure.*

Seven identifications. Each has a mechanism behind it and a failure code when it is absent.

**Lineage:** v1.0 (7-pass compiler) → v2.0 (Fiction Intelligence Engine) → v3.0 (11-pass governed kernel) → v4.0 (accountability layer) → v5.0 (semantic identity, dependency graph, proof-carrying release) → **v6.0 (executable meaning — branches, authority, simulation, conflict-preserving merge)**

---

## See it work

### Ask what a change would do, before it exists

A grant narrative rests on a figure from an agency outcomes report. The agency reissues the report and the number moves. Every writer knows what happens next: search the manuscript, hope you found every instance, hope somebody updated the board deck, hope the website is not still quoting the old figure.

Here is what happens instead. The change has not been made. Nothing has been written.

```
$ wi simulate --actor antonio

SIMULATION ONLY — main is unchanged

Semantic change
  households
    class   quantity_changed
    proof   invalidates: quantity_changed

Authority required
  households                               claim.accept.quantity_change  [held]

Impact
     1 node(s) directly changed
     0 node(s) become stale
     0 node(s) stale through an invalidated proof

Minimum safe repair frontier
  1. reverify           households
     delta class quantity_changed does not carry a prior proof forward

Provably unaffected
     2 of 3 node(s) on main

candidate root  sha256:7525e75b588c991de4a5bdd344c8d0ca05b62b893f6330ab6b4a457d197e6241
Nothing was written. This root exists only to be compared.
```

Read the last two blocks again. **Provably unaffected: 2 of 3.** Not "reverify everything" — the other two claims are untouched and the system can show its work on that. And **nothing was written**: the candidate root exists so it can be compared to the current one and then discarded. A tool that panics about the whole document on every edit gets switched off inside a week; a tool that will not tell you the cost until you have paid it is worse. This one answers first.

`wi simulate` is the command that changes how the work feels. Use it before every consequential edit.

---

### Refuse to invent a number nobody wrote

Two branches. One says the program served 11,800 households. The audit branch says 12,400. Both were committed by authorized actors against the same base.

Every merge tool you have ever used has an opinion about this. Most take one side by rule. Some take the newer one. A model asked to reconcile them will write *"approximately 12,000 households"* — a figure **neither branch asserted, no source supports, and nobody can be held to** — and it will read like diligence.

```
$ wi merge audit --actor antonio

MERGE audit into main

  base commit  22259e1ba6c4

Conflicts — preserved, not resolved
  Quantity     households
      base    (absent)
      ours    The program served 11800 households in 2022.
      theirs  The program served 12400 households in 2022.
      status  unresolved, requires an authorized decision

The engine did not average, soften or generalize these.
Neither branch asserted a middle value, so there is none.

$ echo $?
2
```

The merge exits 2. **The root does not move.** Both numbers stay visible, typed by what disagrees about them, until a named actor holding a grant decides which one survives and says why:

```
$ wi conflicts --resolve 77a8136e --take theirs --actor antonio

resolved 77a8136e-5ddd-568b-91de-8e8e3c2935de by taking theirs
  actor antonio under grant e322307b-57f3-5158-8108-67c315933eb2 (claim.accept.quantity_change)
```

There is no flag that makes the merge pick a side on its own, and no setting that turns averaging on. The absence is the feature. A test in the regression suite asserts that the strings `12100` and `12000` appear **nowhere** in that output, because the failure this release exists to prevent is a plausible middle number that nobody wrote and everybody believes.

---

### Ask a sentence how it got here

`wi explain` answers *what supports this.* `wi why` answers *how did this get here, and who was allowed.*

```
$ wi why households

WHY

  The program served 11800 households in 2022.

NODE
  logical id  households
  state       sha256:7c6e53ecaae717c762993a8b348d0e9e54c3a083fcfe2b757d47877eaa2aa873
  type        meaning.claim_atom
  realm       external_fact

BASIS
  human_declared
      actor: antonio

TIME
  valid       2022-01-01 -> 2023-01-01
  known from  2026-08-08T00:54:31

INTRODUCED BY
  commit f972af802112  ours: 11800
  actor  antonio at 2026-08-08T00:54:31
  delta  node_created

AUTHORIZED BY
  antonio decided accepted
```

Two clocks, on the record. The claim was **valid** for calendar 2022; this workspace has **known** it since August 2026. *What did we believe in March about what was true in 2019* stops being an act of memory and becomes `wi as-of --valid-at 2019-06-01 --known-at 2026-03-01`.

---

### Ask what must be proved before this ships

```
$ wi obligations --mode strict

PROOF OBLIGATIONS — main, mode strict

  households       [meaning.claim_atom / external_fact / human_declared]
      required   anchor.integrity        an external fact with no anchor is an assertion wearing a citation
      required   numeric.value           every quantity appears in a supporting source
      required   numeric.unit            the unit in the claim matches the unit in the source
      required   scope.temporal          the claim does not widen the source's time scope
      required   modality.no-strengthening   certainty did not increase beyond the source
      required   negation.preservation   polarity survives the rewrite

12 obligation(s) across 1 node(s).
These were derived from typed state, release target and policy —
not from a checklist hard-coded inside a command.
```

That last line is the point. The obligations are **derived** from what kind of node this is, which realm it sits in and what release target you named. A node of a different type derives a different set. Nobody maintains a list.

---

### Hand a regulator one claim without handing them the vault

```
$ wi capsule verify claim.wic

CAPSULE VERIFICATION — claim.wic

  ok   capsule.format         format is 'wic/1'
  ok   leaf.digest            1 disclosed leaf digest(s) recomputed
  ok   state.digest           1 disclosed state(s) hash to the digest the leaf names
  ok   inclusion.proof        1 leaf/leaves proved to belong to closure root sha256:5b2fef742245
  ok   closure.count          1 disclosed + 0 redacted against a declared 1 leaves

VERDICT VERIFIED

  this capsule proves membership in the producer's closure and the integrity
  of what it disclosed; it proves nothing about whether the sources are correct
```

A funder, a regulator or a partner gets a Merkle proof of the one claim they are entitled to see. **A redacted leaf proves it was inside the producer's closure and proves nothing about its content — and the artifact says so itself**, in `declared_omissions`, rather than leaving a reader to assume the more flattering reading.

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

On a different machine. With no network. With no model. The bundle carries the source hashes, the claim graph, every check that ran, **every check that did not**, and the digest of the artifact that was approved. Swap one figure inside the sealed file and it fails with `WI_RELEASE_TAMPERED` — immediately, and for the correct reason.

This is the line that matters: **your work stops depending on whether people trust you, and starts depending on whether the digests match.**

---

## The 60-second tour

`scripts/wi.py` is one stdlib-only Python 3.8+ file. No install, no dependencies, no network, no account. Copy it anywhere Python exists, including an air-gapped review machine.

```bash
git clone https://github.com/antonio0720/writing-intelligence
cd writing-intelligence
alias wi="python3 $PWD/scripts/wi.py"

mkdir ~/wi-demo && cd ~/wi-demo
wi init --title "Delta Regional Capacity" --mode strict

# Authority first. Nobody holds it because of what they are.
wi authority issue --subject antonio --capability claim.accept --scope workspace

# A change is written against an exact state. Nothing has moved.
wi propose --node households --payload figure.json --why "agency reissued the report" --actor antonio

# What would that do? Still nothing has moved. This is the one to reach for.
wi simulate --actor antonio

# An actor with a valid grant accepts. The decision binds to the state they saw.
wi decide PROPOSAL_ID --accept --actor antonio

# Every accepted proposal applies as one transaction.
wi commit -m "raise the served-households figure" --actor antonio
wi log

# Two people, two branches, one number in dispute.
wi branch create audit --switch
wi merge audit --actor antonio        # exits 2 · the conflict is preserved
wi conflicts --resolve ID --take theirs --actor antonio

# Ship it.
wi obligations --mode strict
wi gate .wi/graph/ledger-*.json --mode strict --exit-code
wi capsule create --out claim.wic --select households --profile selective
wi verify-release out/delta.wiab
```

Every command above runs today, offline, with no model. The whole v5 pipeline — `wi ingest`, `wi atomize`, `wi anchor`, `wi impact`, `wi diff`, `wi explain`, `wi bundle` — is unchanged and still there.

Full walkthrough: [**`USER_GUIDE.md`**](USER_GUIDE.md) · one-page reference: [**`CHEATSHEET.md`**](CHEATSHEET.md)

---

## Why this exists

Language models are fluent before they are correct, and fluency reads as diligence. A confident paragraph with a fabricated citation looks exactly like a confident paragraph with a real one. The reader cannot tell. Increasingly, neither can the author.

Five versions have been circling one idea and finally arrived at it:

> *If a claim cannot be pointed at, it has not been verified. Once it has been pointed at, everything that depends on it has to know when it moves. And once more than one person can move it, the system has to know who was allowed to — and refuse to invent an answer when they disagree.*

**v3** made writing governable. **v4** made claims accountable. **v5** made authorship inspectable across time, evidence, people and media. **v6** makes it *governable while several people change it at once* — which is the state every consequential document is actually in, and the state nothing else in this market treats as a first-class problem.

---

## The unit changed twice

v4 checked sentences. v5 checked **claim atoms** — one independently checkable assertion, so a sentence carrying four facts fails on the one that is wrong instead of being marked unsupported as a whole.

v6 changes what an atom *lives in*. An atom is no longer a row in a ledger attached to a document. It is a node in a **versioned semantic graph** that several documents may render at once. Change the node once and the graph names every place it surfaces.

| Status | Means |
|---|---|
| `supported` | An anchor resolves and every deterministic check passed |
| `span_supported` | Every checkable component sits co-located in **one span of one source**; entailment not judged |
| `candidate_support` | Components found, but scattered across the corpus rather than co-located |
| `needs_source` | No supporting span exists in the supplied material. Not a failure — a task |
| `unsupported` | An anchor exists and a check failed. This is a defect |
| `stale` | A dependency moved. The claim was true of a state that no longer holds |
| `judged` | A model or a person assessed it. Never `verified`, whatever the confidence |
| `conflicted` | Two branches assert incompatible states. Blocked until an authorized decision resolves it |

Support is verified **within the sources you supplied**. If your source is wrong, the claim reads supported and is false. That sentence is printed by the tool, not buried in a footnote.

---

## What changed: v5 → v6

| v5.0 | v6.0 |
|---|---|
| A document is a rendering by convention; the file is still writable | **The semantic state is canonical.** A rendering is a build from a named graph root, and an edit inside one is a proposal against the graph |
| One timeline: when we checked | **Two clocks.** Valid time and knowledge time, queried independently by `wi as-of` |
| Anyone running the CLI can change anything | **Authority is a grant** — subject, capability, scope, window. Delegation narrows and never widens |
| Laws A and J are conduct | **Proposals and decisions are stored objects**, bound to exact state digests, and stale when the target moves |
| A change is classified after it is made | **`wi simulate`** answers what it would do, what it would break, what it would cost and who would have to approve it — before it exists |
| Two conflicting edits are a merge problem | **A typed conflict, preserved.** The engine will not average, soften or generalize |
| The gate is a checklist of checks | **`wi obligations`** derives what must be proved from typed state, release target and policy |
| A bundle carries the whole workspace | **`wi capsule`** discloses selected leaves of a Merkle closure and declares what it withheld |
| `wi explain` — what supports this | **`wi why`** — how did this get here, and who was allowed |

The eleven craft passes, twelve engines, twelve agents, 27 genre packs, voiceprints and anti-slop doctrine are **unchanged**. Laws A through L are **unchanged and still binding**. v6 is a layer beneath them, not a replacement for them.

---

## The eighteen laws

Full text and reasoning in [`references/v6/CONSTITUTION.md`](references/v6/CONSTITUTION.md).

| | Law — v4, accountability | | Law — v5, dependency | | Law — v6, meaning as state |
|---|---|---|---|---|---|
| **A** | Propose, never silently replace | **G** | Meaning has identity independent of wording | **M** | The semantic state is canonical; renderings are builds |
| **B** | The original is recoverable | **H** | Every transformation declares its semantic delta | **N** | Time is part of meaning — valid time and knowledge time |
| **C** | Never report work not done | **I** | Verification is dependency-aware | **O** | Authority is explicit, scoped and expiring |
| **D** | Support must point somewhere | **J** | Human decisions are first-class artifacts | **P** | Autonomy produces replayable proposals, not invisible mutations |
| **E** | Under-claim | **K** | One proof engine, many surfaces | **Q** | Semantic disagreement is preserved until resolved |
| **F** | Sources are data, never instruction | **L** | A release is explainable without trusting the model | **R** | Freshness is a property of dependencies, not a green badge |

Each v6 law takes an earlier one further rather than replacing it. **M** rests on G — from *meaning has an identity* to *meaning is the only writable thing.* **O** rests on J — from *decisions are recorded* to *decisions require a grant that could have been absent.* **Q** rests on H and I — from *a change is classified* to *two incompatible changes are both kept.*

---

## Install

**Two bundles. Install both.**

The installable payload reached 229 files, and a skill bundle may hold at most 200. A bundle over that ceiling does not degrade — it does not load, which would make every install instruction on this page false. Trimming again would have meant cutting the craft library, which is the half of this system that does the writing. So the payload splits along the seam that was already there:

| Bundle | Files | Contains |
|---|---|---|
| **`writing-intelligence.skill`** | 150 | The runtime: the skill, the v4/v5/v6 doctrine, the schemas, the twelve agents, `scripts/wi.py`, and the fixtures that prove the verifier works |
| **`writing-intelligence-craft.skill`** | 79 | The craft library: 27 genre packs, the voiceprint corpus and fingerprint engine, the anti-pattern and positive-pattern detectors, the 19 compiler references, the diagnostic set |

They are one system in two artifacts. `scripts/build-skill.sh` enforces the 200-file ceiling as a build gate and prints the arithmetic, so it cannot regress into an upload nobody can install.

If only the runtime is present, the craft doctrine summarized in [`SKILL.md`](SKILL.md) still governs and the genre packs are one `git clone` away — degraded, and honestly degraded, rather than broken.

### Claude Code or any terminal agent — as a skill *(recommended)*

One clone gets you both halves and the CLI.

```bash
git clone https://github.com/antonio0720/writing-intelligence \
  ~/.claude/skills/writing-intelligence
```

Restart. The skill triggers on any writing, editing, fact-checking, verification or release request — including unnamed ones like *"clean this up"*, *"will this hold up?"* or *"what breaks if this number changes?"*

### Claude.ai, Cowork, or any chat surface — as uploaded skills

Download the runtime bundle straight from `main`:

```bash
curl -LO https://raw.githubusercontent.com/antonio0720/writing-intelligence/main/writing-intelligence.skill
```

Then **Settings → Capabilities → Skills → Upload skill**. That link tracks `main`, so it always matches the version of this README you are reading — CI fails if the committed bundle and a fresh build of the tree ever disagree.

Take the craft bundle from [**Releases**](https://github.com/antonio0720/writing-intelligence/releases/latest), where pinned versions of both live with their checksums, and upload it the same way.

### CLI only — no model required

`scripts/wi.py` is the deterministic tier and runs entirely on its own. One file. Copy it anywhere Python 3.8+ exists.

### Projects, any LLM, REST, air-gapped

Full matrix of every surface and exactly what each one can and cannot do: [**`docs/INSTALL.md`**](docs/INSTALL.md)

---

## Verify the verifier

Do not take this README's word for any of it.

```bash
bash tests/v4/test_wi.sh     # 3 checks  — the v4 accountability floor
bash tests/v5/test_wi5.sh    # 32 checks — workspace, staleness, bundles, drift
bash tests/v6/test_wi6.sh    # 70 checks — authority, decisions, merge, capsules
python3 scripts/wi.py doctor # what this surface can and cannot do
```

The fixtures are adversarial on purpose: an inflated figure, a reshaped quotation, a fabricated citation, a prompt injection buried in a partner document, a tampered release bundle, a source that moves under a verified claim, an unauthorized acceptance, a delegation that tries to widen its parent, an approval against a state that has since moved, and two branches asserting numbers that cannot both be right.

**Every assertion has a negative twin.** The v6 layer exists to *refuse* things, so a suite that only walked the happy path would stay green with every refusal deleted — which is worse than no suite, because it certifies nothing while looking like assurance. So it checks that the unauthorized acceptance is **denied** with the right error code, that the conflicted merge **does not move the root**, that a constraint which could not run is **not counted as a pass**, and that no value neither branch asserted appears anywhere in the merge output. CI goes further and runs a mutation check: it disables the artifact-digest comparison and requires the suite to go red. A test suite that cannot fail is decoration, and this project does not ship decoration.

---

## What runs and what does not

Law C — *never report work not done* — applies to this project's claims about itself as strictly as to anything it governs. This section is a feature of the release, not an apology.

**Executable today, offline, with no model:** the whole v4 floor (`preserve` · `scan-sources` · `extract-claims` · `verify` · `gate`); the whole v5 graph (`init` · `ingest` · `atomize` · `anchor` · `graph` · `impact` · `diff` · `test` · `explain` · `bundle` · `verify-release` · `doctor`); and the sixteen v6 commands (`canon` · `branch` · `propose` · `proposals` · `simulate` · `decide` · `commit` · `log` · `merge` · `conflicts` · `authority` · `obligations` · `as-of` · `constraints` · `capsule` · `why`).

**Specified, normatively described, and not executable anywhere:**

| Not executable in v6.0 | Where it is specified |
|---|---|
| The compiled Rust core and its WASM build — there is no Rust, no daemon, no single binary | [`BUILD_MANIFEST.md`](references/v6/BUILD_MANIFEST.md) |
| Compiler backends — DOCX, PDF, EPUB, slides, subtitles — and render source maps | [`COMPILER_MODEL.md`](references/v6/COMPILER_MODEL.md), [`SEMANTIC_SOURCE_MAPS.md`](references/v6/SEMANTIC_SOURCE_MAPS.md) |
| The judgment tier — **no provider ships**; paraphrase entailment is not evaluated | [`references/v5/JUDGMENT_TIER.md`](references/v5/JUDGMENT_TIER.md) |
| Sandboxed ingestion adapters and the WASM plugin host — PDF, XLSX, DOCX, image, audio, video anchors | [`CAPABILITY_SECURITY.md`](references/v6/CAPABILITY_SECURITY.md), [`PACKAGE_SYSTEM.md`](references/v6/PACKAGE_SYSTEM.md) |
| External signing, semantic remotes, signed graph deltas, federation, watch mode | [`FEDERATION.md`](references/v6/FEDERATION.md) |
| The Workbench, REST v6 and MCP v6 | [`SURFACES.md`](references/v6/SURFACES.md) |
| The reverse-proposal round trip from an edited rendering | [`COMPILER_MODEL.md`](references/v6/COMPILER_MODEL.md) |
| Unattended autonomous workers | [`AUTONOMOUS_EXECUTION.md`](references/v6/AUTONOMOUS_EXECUTION.md) |

`text_span` remains the one anchor type that executes; a binary file is **reported as needing extraction**, never silently skipped. `wi doctor` prints the live list on the machine you are standing on, so the tool can never look more capable than it is. A capsule declares its own omissions in `declared_omissions`.

---

## What it refuses to do

The refusals are load-bearing, not decorative. Full reasoning in [`references/v6/NON_GOALS.md`](references/v6/NON_GOALS.md).

- **Detector evasion.** Anti-slop is a craft objective — prose that does not pattern-match to machine writing because it is genuinely better built. It is not a laundering service.
- **Source generation.** It will never construct a citation. If a claim needs support and none exists, the output is `needs_source`. Inventing a plausible reference is the single most damaging thing this system could do, and the anchor model exists so it cannot happen quietly.
- **Truth verification.** It verifies support within the sources you supplied. It cannot tell you the source is right, and it says so the first time it says anything.
- **A universal truth score.** There is no number that stands in for the counts, and no overall health gauge. A dashboard is where a system with four honest reliability types quietly grows a fifth one called *overall*.
- **Similarity as evidence.** Retrieval finds candidates. Comparison produces proof. High cosine similarity would happily rank 11,800 as support for 12,400 — the exact fixture this project ships to prove the point.
- **Hidden auto-merge of consequential state.** If meaning conflicts, the conflict is preserved. There is no averaging flag.
- **Renderer-side facts.** A renderer may change expression. It may not change a quantity, a scope, a modality, a hedge, a negation or a legal force — where it cannot render the meaning completely, it raises a proposal and renders nothing.
- **History rewriting.** A correction supersedes an old state. It does not falsify the record of what was known, and there is no compaction pass that drops superseded knowledge.
- **A hosted account, a proprietary model, a vector database, or a blockchain.** None of them answer whether the source supports the claim, whether the meaning changed, or who was allowed to change it.

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

These ship in the craft bundle.

</details>

<details>
<summary><strong>Schemas</strong></summary>

11 v3 craft schemas (`schemas/`), 15 v5 state schemas (`schemas/v5/`), and 20 v6 runtime schemas (`schemas/v6/`): actor · argument · authority · claim · common · compile · conflict · constraint · decision · extension · graph_delta · graph_root · meaning · proof · proposal · release · semantic_commit · semantic_node · simulation · time.

Schemas are what turn a skill into infrastructure: CLI execution, CI writing checks, automated scoring, reproducible output, and a bundle a stranger can parse.

</details>

---

## Repository map

```
SKILL.md                  The skill. Start here if you are a model.
scripts/wi.py             The canonical deterministic core. One file, stdlib only, offline.

references/v6/            The sovereign meaning runtime (24 documents)
  CONSTITUTION              The eighteen laws, the twelve runtime layers, the failure codes
  EXECUTABLE_MEANING        Why a document became a build artifact
  SEMANTIC_IR               Typed meaning, so two states can be compared without reading a sentence
  BITEMPORAL_STATE          Valid time versus knowledge time
  AUTHORITY_MODEL           Grants, scope, delegation, quorum, expiry
  SEMANTIC_VERSION_CONTROL  Branches, commits, proposals, decisions
  MERGE_PROTOCOL            Why a merge may not split the difference
  COUNTERFACTUAL_SIMULATION What a change would do, before it exists
  PROOF_OBLIGATIONS         What must be proved, derived rather than listed
  ARGUMENT_GRAPH            Reasoning made inspectable without passing as deterministic truth
  PROOF_CAPSULES            Merkle closure and selective disclosure
  RELIABILITY_RENDERING     The closed basis enum, declared omission, denominators
  AUTONOMOUS_EXECUTION      What must be true before an agent works unattended
  COMPILER_MODEL            A document as a build from selected semantic states
  SEMANTIC_SOURCE_MAPS      Every artifact maps its bytes back to the meaning that produced them
  CAPABILITY_SECURITY       Why an extension must not inherit the loader's authority
  PACKAGE_SYSTEM            .wipack — packs and voiceprints as pinned, effect-declaring content
  FEDERATION                Meaning across organizations, where trust is computed and never inherited
  SECURITY_MODEL            The threat matrix and its controls
  SURFACES                  One core facade; capability negotiation; the surface matrix
  MIGRATION_V5_TO_V6        What a migration must do before a core swap
  BUILD_MANIFEST            The twenty-three-wave dependency order and the release-candidate gates
  NON_GOALS                 The twelve v6 refusals, and why they do not move

references/v5/            The proof-carrying layer (20 documents, still binding)
references/v4/            The accountability layer (8 documents, still binding)
references/compiler/      19 craft engines            ─┐
references/genre_packs/   27 domain packs              │  the craft bundle
references/voiceprints/   8 voiceprints + builder      │
references/anti_patterns/ 7 slop taxonomies            │
references/diagnostics/   6 diagnostic systems        ─┘

schemas/                  11 v3 craft schemas
schemas/v5/               15 v5 state schemas
schemas/v6/               20 v6 runtime schemas
agents/                   12 specialist agents + manifest
tests/v4/                 Adversarial fixture: injection, misquote, fake citation
tests/v5/                 Fixture world + 32-check regression + expected transcript
tests/v6/                 70-check regression: authority, decisions, merge, capsules
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
| [`CHEATSHEET.md`](CHEATSHEET.md) | One page, every command, mode, status and error code |
| [`docs/INSTALL.md`](docs/INSTALL.md) | Every surface and what each can actually do |
| [`references/v6/README.md`](references/v6/README.md) | Index of the v6 doctrine, and the order to read it in |
| [`references/v6/MIGRATION_V5_TO_V6.md`](references/v6/MIGRATION_V5_TO_V6.md) | Upgrading from v5 |
| [`docs/MIGRATION_v4_to_v5.md`](docs/MIGRATION_v4_to_v5.md) | Upgrading from v4 |
| [`schemas/v6/README.md`](schemas/v6/README.md) | Building on the runtime schemas |
| [`docs/OPERATOR_MANUAL.md`](docs/OPERATOR_MANUAL.md) | Running it as an operator |
| [`docs/VOICEPRINT_GUIDE.md`](docs/VOICEPRINT_GUIDE.md) | Building a voiceprint |
| [`docs/DOMAIN_PACK_GUIDE.md`](docs/DOMAIN_PACK_GUIDE.md) | Writing a new genre pack |
| [`docs/BUILDER_GUIDE.md`](docs/BUILDER_GUIDE.md) | Building on the schemas |
| [`ROADMAP.md`](ROADMAP.md) | Where it goes next |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Contributing |

---

## Why it is free

Because the thing that has to spread is the standard, not the software.

An author who can prove what they wrote is only safe if the people reading them know what that proof looks like. A verification format nobody else can read protects nobody. So the format is open, the verifier is one file with no dependencies, the capsule can be checked by a stranger on a machine that has never heard of this project, and none of it costs anything or phones anywhere.

Take it. Fork it. Put it in your newsroom, your grants office, your law firm, your classroom, your publishing house, your government agency. Ship it inside your own product if you want to — the licence permits it.

[MIT](LICENSE). Credit appreciated: **Antonio T. Smith Jr. / Density6 LLC**.

---

## Author

**Antonio T. Smith Jr.** is the Founder and CEO of [Density6 LLC](https://densitysix.com) and the inventor of Operational Machine Consciousness (OMC) and Existential Recursive Intelligence (ERI).

**[densitysix.com](https://densitysix.com)** · **[@theatsjr](https://instagram.com/theatsjr)**

---

*v1.0 proved AI-sounding prose can be defeated by compilation instead of cosmetic cleanup. v2.0 proved fiction can be engineered as a living architecture. v3.0 proved authorship can be governed without being flattened. v4.0 proved it can be held accountable. v5.0 proved it can be inspected by someone who has no reason to trust you. **v6.0 proves it can be changed — by several people, across time, under authority — without anybody losing track of what is still true.***
