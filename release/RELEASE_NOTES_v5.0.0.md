# Writing Intelligence v5.0.0 — The Proof-Carrying Authorship OS

**v3 governs how well the writing is built. v4 governs what may be claimed about it. v5 governs what a finished document can prove about itself to a reader who does not trust the author, the tools, or the model that helped.**

Free. Open source. MIT. Forever.

---

## The promise, in one line

> **Point at any sentence and ask why it is here, what supports it, what depends on it, and what breaks if it changes — and let someone who does not trust you verify the answer offline.**

v4 could tell you a claim was supported at the moment it was checked. It could not tell you that the check was still true after you edited the paragraph, or after the source was revised, or after somebody tightened a hedge into an assertion. And it could not hand a reader anything they could check without taking your word for the tooling.

v5 is that gap closed. Every proof is bound to the exact source state, the exact anchor, the exact claim state and the exact chain of accepted changes that produced it. Change any one of them and the proof is stale — unless the engine can *prove* the dependency was unaffected. And the whole account packages into a `.wiab` bundle that verifies on a stranger's laptop with no model, no network, and no reason to trust whoever produced it.

---

## Show, don't tell

Everything below is real output from the shipped fixture — the session recorded in [`tests/v5/EXPECTED_TRANSCRIPT.txt`](https://github.com/antonio0720/writing-intelligence/blob/main/tests/v5/EXPECTED_TRANSCRIPT.txt) and reproduced by [`tests/v5/test_wi5.sh`](https://github.com/antonio0720/writing-intelligence/blob/main/tests/v5/test_wi5.sh). Not an illustration.

### 1. A source changes. What actually broke?

One number moves in one source file — `11,800 households` becomes `11,240 households`. That is the moment every other writing system goes quiet and the author starts re-reading a forty-page document from the top.

```
### the governing source changes: 11,800 -> 11,240
### wi impact sources/outcomes_report.txt --apply
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

Read the **Unaffected** block twice. It is the half that makes the tool usable.

Any system can turn a document red when a source moves. That system gets switched off in a week, because a checker that cries wolf is one somebody disables, and the real rule goes with it. The load-bearing claim here is the negative one: **four anchors are provably outside the changed byte range, and five claim atoms are still verified.** Not "probably fine." Provably outside — the anchor's byte span does not intersect any changed range, and that is a comparison, not a judgment.

The difference between *"417 claims affected"* and *"one claim needs your eyes"* is the difference between a tool that gets used and one that gets uninstalled. And the gate agrees:

```
### wi gate .wi/graph/ledger-*.json
# Release gate: HOLD

Evidence mode: `strict` · 6 claim atom(s) · 2 readable source(s) · 5 stale node(s)

## Holding (1)

You can proceed; you are choosing to, with these outstanding.

**a0001** — verified against an earlier source version

> Between 2019 and 2022, the Delta Regional Capacity Program served 11,800 households across seven counties

- Repairs: attach a source that states this · qualify the claim to match what your sources actually say · cut the claim · proceed with a stated caveat (records a waiver)
```

A green badge over an edited sentence is worse than no badge: it converts the author's caution into false confidence at the exact moment the text stopped being checked. v4 named that failure and asked people not to do it. Asking does not scale past about forty claims, and consequential documents are always larger than that and are always edited after they are checked.

### 2. An edit that looks cosmetic and is not

Someone tightens a sentence. `may reduce` becomes `reduces`. Four characters. It survives every review, because a character diff reports typography and a reviewer reads for rhythm.

```
### wi diff drafts/report.md drafts/report-v2.md --semantic
# Semantic diff

drafts/report.md -> drafts/report-v2.md
6 changed · 0 added · 0 removed · 2 change(s) invalidate existing proof

BEFORE  Between 2019 and 2022, the Delta Regional Capacity Program served 11,800 households across seven counties
AFTER   Between 2019 and 2022, the Delta Regional Capacity Program served 12,400 households across seven counties
EFFECT  quantity_changed
PROOF   existing support does not carry forward (quantity_changed)

BEFORE  median wait time for intake fell from 42 days to 26 days.
AFTER   median wait time for intake fell from 42 days to 26 days.
EFFECT  none detected
PROOF   unaffected

BEFORE  Sustained case management may reduce median intake wait time by 38 percent in programs of this size.
AFTER   Sustained case management reduces median intake wait time by 38 percent in programs of this size.
EFFECT  certainty_strengthened
PROOF   existing support does not carry forward (certainty_strengthened)

deterministic classes only; paraphrase equivalence is a judgment-tier question and was not evaluated
```

`certainty_strengthened` is a named class, not a diff. The sentence stopped being a hedged inference and became an assertion, and its existing support does not carry forward, because the support was never for the stronger statement. And note the last line: the system says what it did **not** evaluate, on every run, without being asked. That is Law C, and it is why the output can be trusted about the things it does claim.

### 3. A release a stranger can verify

```
### wi bundle out/delta.wiab --artifact drafts/report.md
built out/delta.wiab (10787 bytes, profile: hash-only)
  verdict          RELEASE
  claim atoms      5 required, 5 permitted
  graph            31 nodes, 62 edges
  stale nodes      0
  proof closure    sha256:4eda4da4d91aa89e
  sha256           sha256:007ccb9e36ce7534da8bff9a1592c71450647abccc83187d312ea1ee81bc1c0a

This is a hash-only bundle. A reviewer who does not already hold the
sources cannot inspect them from it, and the manifest says so.

Verify anywhere: python3 wi.py verify-release out/delta.wiab
```

Now hand that file to somebody who has never seen your workspace, your sources, your machine or you:

```
### wi verify-release out/delta.wiab
# Release verification: delta.wiab

project   delta-regional-capacity
built by  wi.py 5.0.0
profile   hash-only
verdict   RELEASE

PASS  archive.integrity            
PASS  bundle.completeness          
PASS  manifest.format              wi-release-manifest
PASS  object.digests               
PASS  release.artifact_digest      
PASS  graph.reference_integrity    0 dangling edge(s)
PASS  proof.dependencies           0 check(s) reference a claim not in the graph
PASS  release.stale_closure        0 stale node(s)
PASS  manifest.counts              manifest says 31 nodes / 62 edges; bundle has 31 / 62
PASS  core.version                 5.0.0
SKIP  release.signature            unsigned bundle

Checks the producer states were NOT run:
  - paraphrase entailment (judgment tier; no provider configured)
  - pdf_region / sheet_range / audio_time / video_time / image_region anchors (specified, not executable in this build)

RELEASE MANIFEST VALID

Verified by recomputing digests. No model, no network, no trust in
whoever produced this bundle. It does not mean the sources are correct.
```

Every one of those PASS lines is a recomputation, not a lookup. The verifier does not read a field that says the digests matched; it computes them again and compares.

Now change one number inside the sealed artifact — swap `11,800` for `12,400` in the document and touch nothing else. The regression suite does exactly this, and the verifier reports:

```
FAIL  object.digests               artifact/report.md does not match its recorded digest
FAIL  release.artifact_digest      artifact/report.md is not the artifact that was verified

RELEASE MANIFEST INVALID — WI_RELEASE_TAMPERED
Do not publish or rely on this artifact until the failure is explained.
```

Exit code `2`. A verifier that cannot fail is decoration, so the suite proves it fails, for the correct reason, on every run.

### 4. Why is this sentence here?

```
### wi explain drafts/report.md:5
a0002  sourced_fact
  "median wait time for intake fell from 42 days to 26 days."
  status   span_supported
  realm    external_fact
  quantity 42 days, 26 days
  modality is
  anchors:
    outcomes_report.txt  bytes 173-278  sha256:2cde015f183e
      > Median wait time for intake fell from 42 days to 26 days over the same period, a reduction of 38 percent.
  checks:
    anchor.integrity       pass       verified
    numeric.value          pass       verified
  note     every checkable component appears inside one span of one source; whether that span entails the sentence is a judgment-tier question and was not evaluated
  used by  1 structure.paragraph, 1 verification.result
```

That is the new honest status. **`span_supported`** means every checkable component of the claim was found co-located inside **one span of one source** — not scattered across the corpus, which is `candidate_support`, and not verbatim, which is `supported`. It exists because collapsing it upward overstates and collapsing it downward understates, and both errors are silent. The note is part of the record, not a footnote a renderer may drop.

---

## What's new: v4 → v5

| | v4.0 | v5.0 |
|---|---|---|
| **Unit of verification** | The sentence — one status for a sentence asserting three things | **The claim atom** — verified, invalidated and repaired separately |
| **Support** | A verbatim text span | **A typed evidence anchor** — byte offsets plus a quote digest, into a specific *version* of a source |
| **Source identity** | A file path | **A content digest** — raw bytes hashed before any normalization, with an immutable version per byte state |
| **State** | Stateless run | **A `.wi/` workspace** — SQLite index plus content-addressed object store, plus `wi.lock` |
| **After an edit** | Re-run and re-read everything | **`wi impact`** — the stale set, the provably-unaffected set, and a costed repair plan |
| **Diff** | Character diff, or read it again | **`wi diff --semantic`** — `quantity_changed`, `certainty_strengthened`, and which proofs carry forward |
| **Structure** | A claim ledger | **The authorship graph** — nodes and edges, each with a logical id and an immutable state digest |
| **Status vocabulary** | `supported` · `needs_source` · … | **plus `span_supported` and `candidate_support`** |
| **Project rules** | Evidence modes | **`wi test`** — coverage with a denominator, forbidden terms, concept drift, required sections, orphan citations |
| **Release** | A gate verdict on your screen | **A `.wiab` bundle** verified offline by a stranger, in three privacy profiles |
| **Tamper evidence** | None | **`WI_RELEASE_TAMPERED`**, proven on every test run |
| **Capability honesty** | Stated in output | **`wi doctor`** — the machine-readable list of what this surface cannot do, and why |
| **Doctrine, schemas, tests** | 8 documents, 11 v3 schemas, 3 regression checks | **plus 20 documents** in `references/v5/` with every section marked *executable* or *specified*, **15 schemas** in `schemas/v5/`, and **32 regression checks** each with a negative twin |

The 11-pass kernel, 12 engines, 12 agents, 27 genre packs, voiceprints, anti-slop doctrine and benchmark harness are **unchanged**. So are Laws A through F. v5 adds Laws G through L above them.

---

## Install

Eight surfaces. They share one doctrine and differ in what they can physically do. Full capability matrix: [`docs/INSTALL.md`](https://github.com/antonio0720/writing-intelligence/blob/main/docs/INSTALL.md)

**Claude Code and other terminal agents** — the fullest surface.

```bash
git clone https://github.com/antonio0720/writing-intelligence \
  ~/.claude/skills/writing-intelligence
```

**Cowork and Claude.ai** — download the bundle, then **Settings → Capabilities → Skills → Upload skill**.

```bash
curl -LO https://raw.githubusercontent.com/antonio0720/writing-intelligence/main/writing-intelligence.skill
shasum -a 256 writing-intelligence.skill
```

Cowork has a filesystem and a shell, so it gets the whole deterministic core.

**Claude Projects** — upload `SKILL.md` and `references/`. No filesystem, so no deterministic core, no workspace, no bundle; the skill says so rather than implying otherwise. **Any other LLM** — put [`SKILL.md`](https://github.com/antonio0720/writing-intelligence/blob/main/SKILL.md) in the system prompt, or [`CHEATSHEET.md`](https://github.com/antonio0720/writing-intelligence/blob/main/CHEATSHEET.md) for a smaller context budget.

**CLI only — no model, no dependencies, air-gapped.**

```bash
curl -O https://raw.githubusercontent.com/antonio0720/writing-intelligence/main/scripts/wi.py
python3 wi.py --version        # wi 5.0.0
python3 wi.py doctor
```

**CI** — nothing to install beyond Python. Commit the workspace and wire the gate:

```yaml
- name: Writing gate
  run: |
    python3 scripts/wi.py ingest sources/
    python3 scripts/wi.py atomize drafts/narrative.md
    python3 scripts/wi.py anchor .wi/graph/ledger-*.json sources/
    python3 scripts/wi.py test
    python3 scripts/wi.py gate .wi/graph/ledger-*.json --exit-code
```

`gate --exit-code` returns **0** RELEASE · **1** HOLD · **2** BLOCK.

**REST service** — [`services/api/`](https://github.com/antonio0720/writing-intelligence/blob/main/services/api/) is the **v3 craft runtime** and does not expose the v5 verification tier. That is Law K, not an oversight.

**Air-gapped review** — carry two files into the room, `wi.py` and the `.wiab`, and run `python3 wi.py verify-release delta.wiab`.

---

## Upgrade notes and breaking changes

The upgrade is `git pull`. There is no schema migration, no config file to write, no re-authoring, and every v4 command takes the same arguments and produces the same verdict words. Full path: [`docs/MIGRATION_v4_to_v5.md`](https://github.com/antonio0720/writing-intelligence/blob/main/docs/MIGRATION_v4_to_v5.md)

Five things changed that a careful operator should read before upgrading:

**1. `wi.py` reports `5.0.0`.** Release tooling checks the tag, `wi.py --version` and the `CHANGELOG.md` heading against one another. Anything that pinned the version string needs updating.

**2. `gate` accepts both ledger shapes.** A v4 sentence ledger and a v5 atom ledger are both valid input, and the output adapts — sentences for the former, claim atoms plus a stale-node count for the latter. Existing CI jobs and git hooks keep working with no edit. A v4 `claims.json` stays valid input to `verify` and `gate` forever; there is no converter and none is needed, because moving a document onto the v5 unit is `wi atomize`, which writes a fresh ledger and does not consume, migrate or delete the old file.

**3. `gate --mode` now defaults to the project's `evidence.default_mode`** rather than to `standard`. Where there is no project file the default is still `standard`. **This is a behaviour change**: a workspace initialized with `--mode strict` now gates at `strict` without the flag, which is almost certainly what you wanted and is not what you had. Pass `--mode` explicitly if you need the old behaviour.

**4. The claim status vocabulary gained `span_supported` and `candidate_support`.** Anything parsing status strings must handle both. `span_supported` counts toward evidence coverage; `candidate_support` holds the gate. **5. `preserve` writes into `.wi/snapshots/` when a workspace exists**, instead of beside the file; outside a workspace the v4 behaviour is unchanged.

**What to adopt, in the order it pays off:** `wi init` → `wi ingest` → `wi atomize` + `wi anchor` → `wi impact` the first time a source changes → `wi test` in CI → `wi bundle` when you ship. Step four is the moment v5 stops being ceremony.

---

## What is specified and not yet executable

This section is a feature of the release. A version that ships an architecture and describes it as though the architecture were features has committed the exact failure the project exists to catch, one level up. Every one of these is designed, normatively described in [`references/v5/`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v5/README.md), and **executes nowhere**. `wi doctor` reports the live list on any machine, with a reason per entry.

| Not executable | Status |
|---|---|
| A compiled Rust/WASM core | Roadmap. Nothing in this release is written in Rust. Every `crates/` path in `ARCHITECTURE.md` §4 is a target, not a directory that exists |
| PDF, DOCX, XLSX, image, audio and video anchors | Specified, with adapter contracts. `text_span` is the one anchor kind that runs |
| Any judgment provider — paraphrase entailment | Specified. Nothing in this release evaluates paraphrase. The provider ABI is written to bind an implementation that does not exist |
| Proposal and decision objects as persisted records | Laws A and J are **conduct today, not stored artifacts**. The object formats are specified; the store does not contain them |
| External signing — Sigstore, C2PA, PROV export | Specified. `release.signature` reports `SKIP — unsigned bundle` |
| The Workbench desktop app, the MCP server, REST v5 | Roadmap. `docs/mcp/MCP_SPEC.md` specifies the MCP interface and no implementation ships; `services/api/` remains the v3 craft surface |
| Multi-actor authority policy | The seven actor types are specified; delegated authority is not enforced |
| At-rest encryption of the workspace | Specified |
| `wi migrate` | No schema migration is required for this release, so the command does not exist rather than existing and doing nothing |

**"Specified" means designed and normatively described in this repository, and not executable anywhere.** It is not a roadmap tease. It is the honest label on a contract that binds a future implementation, written in advance so the first implementation does not get to define the terms.

## What it refuses to do

Refusals, not unbuilt features. They do not move. Full reasoning: [`references/v5/NON_GOALS.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v5/NON_GOALS.md)

- **Detector evasion.** A system built to produce a machine-checkable account of how a document came to exist cannot also be a system for concealing it. Those are opposite products.
- **Source generation.** It will never construct a citation. There is no code path in which a well-formed anchor can be produced for a source that was never ingested — a stronger guarantee than asking a generator to behave.
- **Truth verification.** A `.wiab` that verifies offline on a stranger's machine is an extremely convincing artifact. It proves the anchors resolve and nothing drifted. It proves **nothing** about whether your sources are correct, and the output says so every time proof appears.
- **Absolute quality scores.** Counts with visible denominators are legitimate. A number that stands in for the counts is not, and would have to average across the four reliability types — the one operation that destroys the information those types exist to carry.
- **No vector database as the truth layer.** Embeddings are candidate retrieval and never evidence. Negation barely moves a vector, and so does an attribution swap; `11,800` and `12,400` are neighbours in embedding space and are a career-ending difference in a grant narrative.
- **No autonomous source approval.** A discovered source is `candidate` until a human approves it. An automated approver is an unbounded prompt-injection surface: a hostile document that can get itself approved has walked through the front door.
- **No automatic legal or medical adjudication.** `regulated` mode makes the system more conservative in those domains, not more decisive. That direction does not reverse.

## Honest limits

- **Paraphrase is not verified.** Nothing in this release evaluates entailment. A well-paraphrased claim with no verbatim span and no co-located span reads `needs_source` — a limit of the deterministic tier, not a verdict on your writing, and every command that could have used a judgment says so on its own output. Closing this is the whole of v5.1.
- **Six of seven anchor kinds do not run.** A PDF, spreadsheet, image, audio file or video is not anchorable today. `wi doctor` names each one with its reason. And a flattened PDF hides text from extraction entirely: `scan-sources` reads extracted text and cannot see what was rasterized before it arrived.
- **`services/api/` is still the v3 craft kernel.** The verification tier has exactly one implementation and stays that way — two implementations of `verified` disagree on the fifth edge case, in the surface with fewer tests, on the document that mattered.

---

## Verify this release

Do not take any of the above on faith. That is the entire point of the version.

**1. The core loads and reports its version.** `python3 scripts/wi.py --version` prints `wi 5.0.0`.

**2. The v4 adversarial floor still holds.**

```bash
bash tests/v4/test_wi.sh
```

```
PASS injection detected
PASS gate BLOCK
PASS statuses
```

Three passes means the verifier still catches a prompt injection, a fabricated citation, an inflated figure and a reshaped quotation.

**3. The v5 core.** `bash tests/v5/test_wi5.sh` — 32 checks, ending in `v5 regression complete`. **Every one has a negative twin.** A suite that can only pass tells you nothing — if the implementation were disabled, most naive tests would still print PASS because nothing would object. So this file checks that the tampered bundle is rejected *and* that it is rejected for the right reason; that the concept registry accepts the governing figure *and* fails on the forbidden alias; that the changed sentence is classified *and* that the unchanged sentences are left alone; that the bundle is reproducible byte-for-byte across two builds, because otherwise a published checksum is meaningless.

**4. What your machine can and cannot do.**

```bash
python3 scripts/wi.py doctor
```

```
Deterministic checks available (11):
  source.digest
  source.quarantine
  anchor.integrity
  quote.verbatim
  numeric.value
  date.range
  entity.presence
  citation.resolution
  graph.reference_integrity
  release.closure
  release.artifact_digest

Evidence anchor types available: text_span

Not available here — and therefore never reported as done:
  audio_time             adapter specified, not executable in this build
  external_signing       Sigstore and C2PA paths are specified, not executable
  image_region           adapter specified, not executable in this build
  paraphrase_entailment  no judgment provider is configured
  pdf_region             adapter specified, not executable in this build
  sheet_range            adapter specified, not executable in this build
  video_time             adapter specified, not executable in this build

This report is Law C as protocol: a surface states what it cannot do
rather than degrading quietly into looking like it did it.
```

**5. The release asset checksum.** `shasum -a 256 -c writing-intelligence.skill.sha256`

CI runs the v4 suite on Python 3.8, 3.11, 3.12 and 3.13, on Linux and macOS, with **no dependencies installed on purpose**, and asserts the PASS *count* separately from the exit code — an exit code cannot tell you the script stopped early and skipped checks it never ran. The bundle is built reproducibly and CI fails if two builds of the same tree differ, so the checksum above means something. **The v5 suite is not yet wired into the workflow** and is run by hand before tagging; wiring it in is tracked as a contribution people can make, and it is named here rather than left to be assumed.

---

## Full detail

[`CHANGELOG.md`](https://github.com/antonio0720/writing-intelligence/blob/main/CHANGELOG.md) · [`ROADMAP.md`](https://github.com/antonio0720/writing-intelligence/blob/main/ROADMAP.md) · [`docs/INSTALL.md`](https://github.com/antonio0720/writing-intelligence/blob/main/docs/INSTALL.md) · [`docs/MIGRATION_v4_to_v5.md`](https://github.com/antonio0720/writing-intelligence/blob/main/docs/MIGRATION_v4_to_v5.md) · [`USER_GUIDE.md`](https://github.com/antonio0720/writing-intelligence/blob/main/USER_GUIDE.md) · [`CHEATSHEET.md`](https://github.com/antonio0720/writing-intelligence/blob/main/CHEATSHEET.md) · [`CONTRIBUTING.md`](https://github.com/antonio0720/writing-intelligence/blob/main/CONTRIBUTING.md)

The doctrine: [`references/v5/CONSTITUTION.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v5/CONSTITUTION.md) · [`references/v5/AUTHORSHIP_GRAPH.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v5/AUTHORSHIP_GRAPH.md) · [`references/v5/EVIDENCE_ANCHORS.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v5/EVIDENCE_ANCHORS.md) · [`references/v5/STALENESS.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v5/STALENESS.md) · [`references/v5/PROOF_CARRYING_RELEASE.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v5/PROOF_CARRYING_RELEASE.md) · [`references/v5/NON_GOALS.md`](https://github.com/antonio0720/writing-intelligence/blob/main/references/v5/NON_GOALS.md)

---

*v1.0 proved AI-sounding prose can be defeated by compilation instead of cosmetic cleanup. v2.0 proved fiction can be engineered as a living architecture. v3.0 proved authorship can be governed without being flattened. v4.0 proved it can be held accountable. **v5.0 proves the account can be carried, checked and re-checked by someone who was never in the room.***

Free. MIT. Free forever — no account, no server, no key, no telemetry, and nothing that stops working if the author does. **Antonio T. Smith Jr.** — Founder & CEO, [Density6 LLC](https://densitysix.com).
