# Install

Writing Intelligence v5 runs on eight surfaces. They share one doctrine and differ in what they can physically do — whether a filesystem exists, whether a workspace can persist, whether a proof can be recomputed.

Pick your surface, install once, then read [the capability matrix](#the-capability-matrix) so you know which half of the system you are getting. **Free. Open source. MIT. Forever.**

---

## The capability matrix

Doctrine is identical everywhere. Capability is not. Read down a column to see what a surface must never imply.

| | Chat | Claude Code / terminal | Cowork | CLI only | CI | REST service | MCP | Air-gapped review |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **Craft passes** (11-pass kernel) | yes | yes | yes | **no** | **no** | yes (v3) | specified | **no** |
| **Proposal discipline** (Law A) | yes | yes | yes | **no** | **no** | partial | specified | **no** |
| **Deterministic checks** (Laws D, F) | **no** | yes | yes | yes | yes | **no** — must call the core | specified | from the bundle |
| **Workspace + graph** | **no** | yes | yes | yes | yes | specified | specified | not required |
| **Staleness** (`impact`, Law I) | **no** | yes | yes | yes | yes | specified | specified | **no** |
| **Bundles** (`bundle` / `verify-release`) | **no** | yes | yes | yes | yes | specified | specified | **verify only** |
| **Offline** | n/a | yes | yes | yes | yes | server has network | adapter-dependent | **always** |

Three cells deserve their own sentences.

**Chat cannot run a deterministic check.** `scripts/wi.py` does not exist there. What happens instead is careful reading, which is real work and catches real errors, and which is *not* verification. A chat surface that prints a checkmark, the word `verified` or a file path is broken. See [`../references/v5/SURFACES.md`](../references/v5/SURFACES.md) §2.

**CI cannot approve anything.** It can determine that every factual claim carries a resolvable anchor and that the checks passed. It cannot produce a `human-declared` record and cannot accept a proposal, because those need a human actor and no pipeline has one. A green build means the deterministic tier found nothing blocking. It does not mean anybody read it.

**The REST service does not implement checks.** `services/api/` is the **v3 craft runtime** — compile, score, voice, benchmark, repackage. It does not expose the v5 verification tier and it must not, because two implementations of `verified` disagree on the fifth edge case in the document that mattered. That is Law K.

"specified" means designed and normatively described in this repository, and **not executable anywhere**. It is not a roadmap tease; it is the honest label on a contract that binds a future implementation.

---

## What is inside the `.skill` bundle

A skill bundle may contain **at most 200 files**. Over that, the upload is
rejected outright — it does not degrade, it simply will not load. So the bundle
ships the operating set and `scripts/build-skill.sh` fails the build if the
count is ever exceeded.

**Ships in the bundle (182 files):** `SKILL.md`, the twenty `references/v5/`
doctrine documents, the eight `references/v4/` accountability documents, the
craft corpus (`compiler`, `genre_packs`, `voiceprints`, `anti_patterns`,
`diagnostics`, `positive_patterns`, `academic`), all 26 schemas, the twelve
agents, `docs/`, `governance/`, `scripts/wi.py`, and the `tests/v4` and
`tests/v5` fixtures so the verifier can be proven from the extracted bundle.

**Repository only:** `benchmarks/`, `certification/`, `examples/`, `release/`,
the regression corpora at the top of `tests/`, and `services/api/`. Nothing in
the shipped set links to any of them, and a `git clone` is one command away.

If you want everything, clone the repository instead of uploading the bundle —
see [Claude Code — as a skill](#claude-code--as-a-skill) above.

## 1. Claude Code and other terminal agents *(fullest surface)*

Filesystem, shell, version control, CI wiring, long-running work, and the deterministic core all available.

```bash
git clone https://github.com/antonio0720/writing-intelligence \
  ~/.claude/skills/writing-intelligence
```

Restart, then confirm it loaded:

```bash
ls ~/.claude/skills/writing-intelligence/SKILL.md
```

**Project-scoped instead of user-scoped** — commit the skill into one repository so every collaborator gets it:

```bash
git clone https://github.com/antonio0720/writing-intelligence \
  .claude/skills/writing-intelligence
```

**Updating:** `cd ~/.claude/skills/writing-intelligence && git pull`

The skill triggers on any writing, editing, auditing, fact-checking or verification request — including unnamed ones: *"clean this up"*, *"is this accurate"*, *"will this hold up?"*

---

## 2. Cowork and Claude.ai — the uploaded bundle

1. Download **`writing-intelligence.skill`**:

   ```bash
   curl -LO https://raw.githubusercontent.com/antonio0720/writing-intelligence/main/writing-intelligence.skill
   ```

   This tracks `main`, so it always matches these instructions. CI rebuilds the bundle on every push and fails if it does not byte-match the committed one, so this file cannot quietly go stale.

   Want a pinned version? Take it from [Releases](https://github.com/antonio0720/writing-intelligence/releases), where each bundle ships with a `.sha256` beside it. Note that `releases/latest` resolves to the newest **published release** — if a version has landed on `main` and has not been released yet, `latest` is behind it.

2. In Claude: **Settings → Capabilities → Skills → Upload skill** (labelled **Settings → Skills** in some versions).
3. Select the downloaded `.skill` file.

**Verify what you downloaded** before uploading:

```bash
unzip -l writing-intelligence.skill | head
shasum -a 256 writing-intelligence.skill
```

The bundle is a zip carrying the full doctrine payload — `SKILL.md`, `README.md`, `USER_GUIDE.md`, `CHEATSHEET.md`, all `references/` (including `references/v5/`), `schemas/`, `agents/`, `docs/`, `tests/` and `scripts/wi.py`. It excludes the REST service and repository scaffolding, which are not useful inside a chat surface and more than double the download.

**Cowork gets the whole deterministic core**, because Cowork has a filesystem and a shell. Claude.ai without a filesystem does not — see §4.

---

## 3. Claude Projects

Upload to project knowledge:

- `SKILL.md` *(required)*
- `references/` *(required for depth — the v5 laws live in `references/v5/`)*
- `schemas/` *(if you want structured output)*
- `agents/` *(if you want the multi-agent board)*

Projects have no filesystem, so the deterministic core cannot run. There is no workspace, no graph, no staleness, no bundle. Claim checking becomes careful reading rather than string comparison, and the skill is written to say so rather than implying otherwise.

---

## 4. Any other LLM

Put the contents of `SKILL.md` in the system prompt. That single file carries the laws, the evidence modes, the workflow and the pass structure. Reference files load on demand when the model can read them; when it cannot, the skill degrades honestly — it states which checks it could not run instead of performing them silently.

For a smaller context budget, [`../CHEATSHEET.md`](../CHEATSHEET.md) is the compressed form.

---

## 5. CLI only — no model required

`scripts/wi.py` is the deterministic tier and the canonical core. **Stdlib-only Python 3.8+.** No pip install, no dependencies, no network calls, no model.

```bash
curl -O https://raw.githubusercontent.com/antonio0720/writing-intelligence/main/scripts/wi.py
python3 wi.py --version
```

This is the half of the system that does not require trusting anything. It compares bytes, numbers and dates. Command table: [`../CHEATSHEET.md`](../CHEATSHEET.md). Worked walkthrough: [`../USER_GUIDE.md`](../USER_GUIDE.md).

---

## 6. CI

Nothing to install beyond Python. Commit the workspace (see [The `.wi/` workspace](#the-wi-workspace)) and wire the gate:

```yaml
- name: Writing gate
  run: |
    python3 scripts/wi.py ingest sources/
    python3 scripts/wi.py atomize drafts/narrative.md
    python3 scripts/wi.py anchor .wi/graph/ledger-*.json sources/
    python3 scripts/wi.py test
    python3 scripts/wi.py gate .wi/graph/ledger-*.json --mode strict --exit-code
```

`gate --exit-code` returns **0** RELEASE · **1** HOLD · **2** BLOCK. `test` returns **1** on any failure. Drop `--exit-code` if you want holds to warn rather than fail the job.

---

## 7. REST service — v3 craft runtime only

```bash
cd services/api
npm install
npm test
npm run dev
```

Or:

```bash
docker build -t writing-intelligence-api services/api
docker run -p 8080:8080 writing-intelligence-api
```

**Scope, stated plainly:** this service implements the **v3 craft kernel** — the eleven passes, scoring, voice metrics and repackaging. It does **not** expose the v4 accountability tier or the v5 verification tier. Those have exactly one implementation, `scripts/wi.py`, and it stays that way on purpose: two implementations of a verification rule drift, and the one that drifts is invisible because both look correct.

v5 REST endpoints are **specified, not implemented**. See [`../services/api/README.md`](../services/api/README.md) and [`api/API_SPEC.md`](api/API_SPEC.md).

---

## 8. MCP — specified, not implemented

[`mcp/MCP_SPEC.md`](mcp/MCP_SPEC.md) describes the interface and [`../references/v5/SURFACES.md`](../references/v5/SURFACES.md) §9 lists the ten conformance rules an adapter must satisfy. **No MCP server ships in this repository.** There is nothing to install. The rules were written before any implementation because every one of them is cheap at design time and expensive to retrofit.

---

## 9. Air-gapped review

One file and a Python interpreter. Nothing else, by design.

```bash
# on a machine that has never seen this project, with no network
python3 wi.py --offline verify-release release.wiab
```

This is the surface the whole v5 design is aimed at: the reviewer who was not in the room, does not trust the author's toolchain, and cannot install anything. Detail in [Air-gapped and offline](#air-gapped-and-offline).

---

<a id="verify-your-install"></a>
## Verify your install

Four checks. Run all four; each catches a different failure.

### 1. The core loads

```bash
python3 scripts/wi.py --version
```

```
wi 5.0.0
```

### 2. The v4 adversarial suite

```bash
bash tests/v4/test_wi.sh
```

```
PASS injection detected
PASS gate BLOCK
PASS statuses
```

Three passes means the deterministic tier catches a prompt injection, a fabricated citation, an inflated figure and a reshaped quotation on the shipped adversarial fixture. Anything less and the verifier is not doing its job — do not trust its verdicts until it does.

### 3. The v5 suite

```bash
bash tests/v5/test_wi5.sh
```

```
PASS workspace created
PASS sources ingested
PASS source digest is stable
PASS claim ledger written
PASS compound sentence split into atoms
PASS evidence anchors bound
PASS unrun checks are named
PASS clean draft releases at strict
PASS may -> reduces classified
PASS 11,800 -> 12,400 classified
PASS proof impact reported
PASS unchanged sentences left alone
PASS writing tests run
PASS coverage reports a denominator
PASS release bundle built
PASS bundle build is reproducible
PASS intact bundle verifies offline
PASS tampered bundle is rejected
PASS tamper rejected for the right reason
PASS exactly one claim atom invalidated
PASS unaffected anchors reported as unaffected
PASS repair path named
PASS stale source holds the gate
PASS doctor states what is unavailable
PASS unimplemented anchors declared missing

v5 regression complete
```

Every assertion in that file has a negative twin. A suite that can only pass tells you nothing, so it checks that the good case is accepted **and** that the tampered, stale and contradicted cases are rejected *for the correct reason*. `PASS tamper rejected for the right reason` is the one to look for: it asserts that a single-figure swap inside a sealed bundle produces `FAIL release.artifact_digest` and exit 2, not merely a non-zero exit.

### 4. The capability report

```bash
python3 scripts/wi.py doctor
```

```
Writing Intelligence 5.0.0 — capability report

python            3.11.15
schema            5.0.0
canonicalization  wi-json-v1
workspace         /tmp/w5
network           disabled

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

Your `python` line and your `workspace` line will differ; outside a workspace the latter reads `workspace         none found`. Everything else should match exactly. If your build reports a capability that is not on that list, or omits the "Not available here" section, you are not running this core.

`doctor --json` gives the machine form for a capability negotiation block.

---

<a id="the-wi-workspace"></a>
## The `.wi/` workspace

`wi init` creates one directory and one project file.

```
my-project/
├── wi.project.yaml          project identity, inputs, sources, evidence mode, concepts, tests
├── .wi/
│   ├── workspace.db         SQLite index: nodes, states, edges, invalidations
│   ├── objects/sha256/      content-addressed blobs, sharded by digest prefix
│   ├── graph/               claim-atom ledgers, JSON
│   ├── snapshots/           Law B originals
│   ├── decisions/           proposal, decision and waiver records
│   ├── judgments/           judgment records
│   ├── builds/              build manifests
│   ├── reports/             gate and impact reports
│   ├── attestations/        statements about produced artifacts
│   └── cache/               derived indexes and closures — deletable at any time
├── sources/                 what you supplied, untouched
├── drafts/                  what you are writing
└── outputs/                 what gets sent
```

**Which of those are populated in this build.** `workspace.db`, `objects/sha256/` and `graph/` are written and read by every command. `snapshots/`, `decisions/`, `judgments/`, `builds/`, `reports/`, `attestations/` and `cache/` are created empty; the mechanisms that fill them — hashed decision records, judgment records, build manifests, attestations — are **specified and not executable in this build**. The directories exist so that a workspace has one shape everywhere, not because something is quietly writing to them.

`wi.lock`, the pinned-versions lockfile described in [`../references/v5/WORKSPACE.md`](../references/v5/WORKSPACE.md), is likewise **specified and is not written by this build**.

### What to commit and what to ignore

```gitignore
# Writing Intelligence workspace — derived state
.wi/objects/
.wi/cache/
```

| Path | Git | Why |
|---|---|---|
| `wi.project.yaml` | **commit** | Identity, inputs, evidence mode, concepts and tests. It is the policy your reviewers can read |
| `.wi/workspace.db` | **commit** | The graph. Without it a colleague has no staleness and no dependency edges |
| `.wi/graph/` | **commit** | Claim-atom ledgers; small, diffable, greppable |
| `sources/`, `drafts/` | **commit** | Your inputs and your text |
| `.wi/objects/` | **ignore** | Reconstructable from `sources/` by re-running `wi ingest`, and it duplicates every byte you already committed |
| `.wi/cache/` | **ignore** | Pure derivation. Deleting it costs time and nothing else |
| `outputs/`, `*.wiab` | your call | Build artifacts. Commit them only if you want the release history in git |

`.wi/cache/` is the only directory whose absence can never change a verdict. That is a design constraint, not an observation: a cache whose absence changes a verdict is a correctness surface pretending to be an optimization.

### Handing a workspace to a colleague

The whole system is a directory. There is no server and no account.

```bash
git clone <your repo> && cd <your repo>
python3 scripts/wi.py ingest sources/     # rebuilds .wi/objects/ from the committed sources
python3 scripts/wi.py graph               # same node and edge counts you saw
python3 scripts/wi.py gate .wi/graph/ledger-*.json --mode strict
```

If `.wi/objects/` was ignored, the single `ingest` restores it — the digests are deterministic, so the same bytes rebuild the same object store. If they skip that step, a command that needs a blob fails loudly with `WI_GRAPH_INTEGRITY` rather than silently reporting less.

No git? Copy the project directory including `.wi/`. `workspace.db` is one SQLite file — mailable, printable in `sqlite3`, openable in ten years with tools that ship on every operating system. The portability *is* the accountability argument: a reviewer who must first be issued database credentials cannot check your work.

---

<a id="air-gapped-and-offline"></a>
## Air-gapped and offline

Everything in the deterministic core is offline by default. `privacy.network_default: deny` is written into every new project file, and **this build never opens a network connection at all** — `--offline` asserts that fact rather than switching something off.

To review a release on a machine that has never seen the project:

```bash
# carry two files in: wi.py and the .wiab
python3 wi.py --offline verify-release release.wiab
```

You get the verification block shown in [`../USER_GUIDE.md`](../USER_GUIDE.md) §9: archive integrity, bundle completeness, manifest format, object digests, artifact digest, graph reference integrity, proof dependencies, stale closure, manifest counts, core version — plus `SKIP release.signature — unsigned bundle`, plus the producer's own list of checks that were not run.

Three limits, stated because a printed page has to carry them:

1. **Digest-sealed, not signed.** A digest proves integrity and detects tampering by anyone who does not also control the digest. It does not prove identity. External signing is specified and not executable in this build.
2. **Internal consistency, not truth.** `verify-release` confirms the record is intact. It says nothing about whether the sources are correct.
3. **`hash-only` bundles carry digests, not sources.** A reviewer who does not already hold the sources cannot inspect them from a `hash-only` bundle, and the manifest says so on its face. Use `--profile full` when the reviewer is entitled to the evidence.

Format details: [`../references/v5/PROOF_CARRYING_RELEASE.md`](../references/v5/PROOF_CARRYING_RELEASE.md).

---

## Uninstall and downgrade

**Remove the skill:**

```bash
rm -rf ~/.claude/skills/writing-intelligence      # Claude Code
rm -rf .claude/skills/writing-intelligence        # project-scoped
```

Claude.ai / Cowork: **Settings → Capabilities → Skills →** remove the skill.

**Drop back to v4 behavior.** The v4 commands are still in the same file and unchanged. Delete the workspace and use them:

```bash
rm -rf .wi wi.project.yaml
python3 scripts/wi.py extract-claims draft.md --out claims.json
python3 scripts/wi.py verify claims.json sources/
python3 scripts/wi.py gate claims.json --mode strict --exit-code
```

Nothing outside the project directory is touched. `preserve` writes a sibling `.original-<timestamp>` file; `extract-claims`, `verify` and `gate` write only to paths you pass; the v5 commands write only inside `.wi/` and wherever you point `bundle`.

Deleting `.wi/` loses the graph, the source versions and the staleness history. It does not touch `sources/`, `drafts/` or anything you have already shipped, and a later `wi init` + `ingest` + `atomize` + `anchor` rebuilds an equivalent workspace from the same inputs.

Migration guides: [`MIGRATION_v4_to_v5.md`](MIGRATION_v4_to_v5.md) · [`MIGRATION_v3_to_v4.md`](MIGRATION_v3_to_v4.md).

---

## Requirements

| | |
|---|---|
| **Python** | 3.8 or newer |
| **Dependencies** | None. Standard library only — no pip, no virtualenv, no lockfile |
| **Network** | Never used. The core opens no connection |
| **Size** | One file, `scripts/wi.py`, about 3,300 lines |
| **Disk** | The workspace is one SQLite file plus a copy of each source, addressed by digest |
| **Tested on** | Linux (Python 3.8, 3.11, 3.13) and macOS (3.12) in CI, on every push |
| **Windows** | Supported by construction — stdlib only, no shell dependencies, `pathlib` throughout — and **not covered by CI today**. Run `bash tests/v4/test_wi.sh` under Git Bash or WSL to confirm your environment |

CI also checks that every relative link in this repository resolves (`python3 scripts/check-links.py`) and that the committed `.skill` bundle byte-matches a fresh build, so a stale bundle cannot ship silently.

---

## Troubleshooting

**The skill does not trigger in Claude Code.** Confirm `~/.claude/skills/writing-intelligence/SKILL.md` exists and its YAML frontmatter is intact — the `name` and `description` fields are what the loader reads. Restart after installing.

**`python3: command not found`.** The core needs Python 3.8 or newer. On macOS it ships with the system; on Debian/Ubuntu, `apt install python3`. There are no other dependencies.

**`WI_INPUT_INVALID: no Writing Intelligence workspace found`.** You are outside a project. Run `wi init`, or pass `--root /path/to/project`. The error prints `searched_from:` so you can see where it looked.

**`gate` returns HOLD on a document I believe is correct.** Usually right, and worth reading before overriding. Common causes: a figure that appears in your source in a different form (`11,800` vs `11800` is handled, `11.8k` is not), a well-paraphrased claim with no verbatim span, or a source you did not ingest. Try `wi anchor ... --tolerance 0.01` for rounded figures.

**`gate` returns BLOCK on a citation I know is real.** Citations resolve against *supplied sources only*. Ingest the cited source, or state plainly that it is external and unverified.

**A PDF is not being verified against.** Correct. It is reported as `not plain text; extract before verifying` and counted in the `need extraction first` total. PDF region anchors are specified and not executable in this build. Extract the text yourself and ingest that.

**`verify-release` fails on a bundle I just built.** Check that the bundle was not modified in transit — some mail systems rewrite zip archives. Rebuild and compare the printed `sha256`. If they differ before and after transport, the transport is the problem.

---

## Getting help

- **Bugs and detector benchmarks:** [Issues](https://github.com/antonio0720/writing-intelligence/issues) — templates exist for bug reports, new genre packs, new voiceprints, new anti-patterns and detector benchmarks.
- **Proposing changes to doctrine:** [`../governance/RFC_PROCESS.md`](../governance/RFC_PROCESS.md). Changing what `verified`, `stale`, `BLOCK`, `permitted` or `source quarantine` *promises* requires an RFC and a benchmark case that fails before the change and passes after it.
- **Contributing:** [`../CONTRIBUTING.md`](../CONTRIBUTING.md)

---

**Antonio T. Smith Jr. / Density6 LLC** · MIT · v5.0.0
