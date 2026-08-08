# Release Checklist — Writing Intelligence

Releases are published by [`.github/workflows/release.yml`](../.github/workflows/release.yml),
never by hand.

This checklist is split by **who enforces each item**, because a checklist that mixes
automated gates with human ones teaches people to skim both. An item marked **automated**
cannot be skipped — the job stops. An item marked **manual** can be skipped by anybody in a
hurry, and several of them protect things nothing else protects.

| Marker | Means |
|---|---|
| **[release]** | Enforced by `release.yml`. The publish does not happen |
| **[ci]** | Enforced by `ci.yml` on every push. Confirm the commit is green before tagging — `release.yml` does not re-run these |
| **[build]** | Enforced by `scripts/build-skill.sh`, which `release.yml` calls |
| **[manual]** | Enforced by a person. Nothing checks it |

---

## 1. What the release workflow actually enforces

Two ways in, and they are not the same trust level: pushing a `v*` tag, or
*Actions → Release → Run workflow* with `tag` and `ref`. The dispatch path creates the tag
itself, and it is not a looser path — the tag is created **after** the gates, so a commit
that fails its own release gate never gets stamped with a version number.

In order, the job:

1. Checks out the ref, on **Python 3.12 only**. There is no matrix here.
2. **[release]** `bash tests/v4/test_wi.sh` — the adversarial floor.
3. **[release]** `bash tests/v5/test_wi5.sh` — workspace, staleness, bundles, drift.
4. **[release]** `bash tests/v6/test_wi6.sh` — authority, decisions, merge, capsules.
5. **[release]** `python3 scripts/check-manifest.py` — `plans/v6.manifest.yaml` is acyclic,
   every wave declares an exit condition, and every wave marked `shipped` names commands
   that appear in `wi --help` and artifacts that exist.
6. **[release]** `python3 scripts/check-links.py` — every relative link resolves, and every
   absolute link pointing back into this repository resolves.
7. **[release]** `bash scripts/build-skill.sh --no-root` — see section 2.
8. **[release]** Version consistency: the tag minus `v` equals `python3 scripts/wi.py --version`,
   and `CHANGELOG.md` contains a `## [<version>]` heading.
9. **[release]** Tag safety: if the tag already exists on the remote it must point at the
   commit that was built, or the job stops. Publishing assets under a tag naming a different
   commit is the one failure here nobody can see afterwards, because the release page looks
   entirely normal.
10. Release notes: uses `release/RELEASE_NOTES_<tag>.md` if it exists. **If it does not, the
    job emits a warning and falls back to `--generate-notes`.** This is not a gate.
11. **[release]** Publishes four assets — `writing-intelligence.skill`,
    `writing-intelligence-craft.skill` and a `.sha256` for each — with `--verify-tag`.

### What `release.yml` does **not** gate

Read this list before tagging. Every item here is real and is enforced somewhere else, or
nowhere.

- **PASS counts.** `release.yml` relies on exit codes. An exit code cannot tell you a script
  stopped early and skipped checks it never ran. `ci.yml` asserts 3, 32 and 70 separately.
- **The two mutation checks.** `ci.yml` disables the artifact-digest comparison and requires
  the v5 suite to go red, then disables conflict preservation and requires the v6 suite to go
  red. Neither runs at release time.
- **Reproducible build.** `ci.yml` builds twice and compares bytes. Without it a published
  checksum is a number with no meaning attached.
- **Committed bundles match the tree.** `ci.yml` checks this, and **skips it on pushes to
  `main`** because `bundle.yml` rebuilds there. `release.yml` builds fresh and publishes the
  fresh build, so a stale committed bundle at the repo root would not fail the release — it
  would only mislead everyone downloading from `main`.
- **Schema parse and self-description.** `ci.yml`.
- **Documented subcommands exist.** `ci.yml`.
- **Gate exit codes.** `ci.yml` asserts `gate --exit-code` returns 2 for BLOCK.
- **Python 3.8, 3.11, 3.13 and macOS.** `ci.yml` only. The 3.8 floor claim is backed by CI,
  not by the release job.
- **`services/api` typecheck and tests.** `ci.yml` only.
- **Release notes existence.** Warns, does not fail.
- **Everything in section 4.** Nothing checks those.

---

## 2. What `build-skill.sh` enforces

`release.yml` calls it, so these are release gates by inheritance. Worth knowing separately
because they fail with different messages.

- **[build]** Every payload path exists.
- **[build]** Frontmatter fields are inside the loader's hard limits.
- **[build]** At least 20 schemas in `schemas/v6/`.
- **[build]** `writing-intelligence-craft.skill`'s own `SKILL.md` is present.
- **[build]** One version number across three files: `wi.py --version`, the
  `**Version:**` line in `SKILL.md`, and a `## [<version>]` heading in `CHANGELOG.md`.
- **[build]** All three regression suites pass. A bundle that ships a broken verifier is
  worse than no bundle, because it looks installed.
- **[build]** **Both bundles are at or under 200 files.** Not a style preference — a bundle
  over the ceiling does not load, which turns every install instruction in this repository
  into a false claim. Raising `MAX_FILES` is not a fix.

---

## 3. Pre-tag checklist

### Version and documentation

- [ ] **[manual]** `CHANGELOG.md` updated with everything since the last release
- [ ] **[release]** `CHANGELOG.md` has a `## [<version>]` heading matching the tag
- [ ] **[build]** `SKILL.md` declares the same version
- [ ] **[release]** `python3 scripts/wi.py --version` prints the same version
- [ ] **[manual]** `README.md` version metadata current
- [ ] **[manual]** `ROADMAP.md` reconciled — nothing shown as future that has shipped, and
      nothing shown as shipped that has not
- [ ] **[manual]** [`VERSIONING.md`](VERSIONING.md) followed — the MAJOR/MINOR/PATCH decision
      is defensible, and a digest move is a MAJOR
- [ ] **[release]** `python3 scripts/check-links.py` passes
- [ ] **[manual]** `USER_GUIDE.md` and `CHEATSHEET.md` cover every new command, mode, status
      and error code
- [ ] **[manual]** Every new capability in any document is marked *executable in
      `scripts/wi.py`* or *specified*. "Specified" means designed and normatively described
      here and **not executable anywhere**

### The suites

- [ ] **[release]** `bash tests/v4/test_wi.sh` passes
- [ ] **[release]** `bash tests/v5/test_wi5.sh` passes
- [ ] **[release]** `bash tests/v6/test_wi6.sh` passes
- [ ] **[ci]** The PASS counts are 3, 32 and 70 — confirm the commit's CI run is green
- [ ] **[ci]** Both mutation checks caught their control
- [ ] **[manual]** Every new check or refusal in this release ships a **negative fixture,
      shown failing with the implementation disabled**. A guard that has only ever passed has
      not been shown to work

### v6 state and digests

These are the items this release cycle added, and four of the five are enforced by nobody.

- [ ] **[manual]** **`wi canon` digests are unchanged for the fixture world** — unless this
      release intends to move them, in which case `CHANGELOG.md` says so explicitly, names
      the object kinds affected, and states what happens to artifacts already in circulation.
      A released digest is a public identifier. Moving one silently produces `VERDICT
      TAMPERED` and `WI_RELEASE_TAMPERED` on machines this project cannot reach, which are
      the correct words for the check that ran and the wrong words for what happened.
- [ ] **[manual]** **The candidate root a simulation prints equals the root the commit
      produces.** Run `wi propose` → `wi simulate` → `wi decide` → `wi commit` in a scratch
      workspace and compare `candidate root` to `next root`. A simulation that produces a
      different root than the commit is not a preview, it is a guess with formatting.
      Nothing in any suite asserts this today.
- [ ] **[ci]** `wi canon` digest stability and domain separation hold — `tests/v6/test_wi6.sh`
      asserts that key order and NFC normalization do not move a digest, that a changed
      payload does, and that the v5 and v6 digests of identical bytes differ
- [ ] **[ci]** **The merge still proves no fabricated middle value appears.**
      `tests/v6/test_wi6.sh` asserts both sides are shown verbatim and that the strings
      `12100` and `12000` are absent from the output. `ci.yml` additionally deletes the
      conflict-preservation branch and requires the suite to go red
- [ ] **[ci]** Every authority refusal fires with its own code — `WI_AUTHORITY_DENIED`,
      `WI_AUTHORITY_EXPIRED`, `WI_AUTHORITY_REVOKED`, `WI_GRANT_SCOPE_EXCEEDED`,
      `WI_DECISION_STALE`
- [ ] **[manual]** `python3 scripts/wi.py constraints` on the fixture world reports what it
      should. Five constraints report `--` rather than `ok` in a workspace with no v6 release
      closure, no render source maps and no declared protected spans; `--` is not `ok` and
      folding them into a pass is the failure this project exists to catch
- [ ] **[manual]** `tests/v5/EXPECTED_TRANSCRIPT.txt` matches the tool. A transcript that no
      longer matches is a document that lies about the tool. Nothing checks this

### Schemas and the manifest

- [ ] **[ci]** Every schema parses and carries `$schema`, `$id`, `title`, `description`
- [ ] **[ci]** / **[build]** At least 15 v5 schemas and 20 v6 schemas present
- [ ] **[manual]** Schema version stamps current, and no schema id or version bound into a
      digest preimage moved without a MAJOR bump
- [ ] **[release]** `python3 scripts/check-manifest.py` passes — no wave claims a command the
      CLI does not have

### Benchmarks

- [ ] **[manual]** Benchmark gate assessed against `benchmarks/benchmark_manifest.yaml`

  **This is a judgment gate, not an automated one.** There is no benchmark runner in
  `scripts/`, `wi benchmark` is not a CLI subcommand, and no workflow executes the suite.
  `benchmarks/runbook.md` describes a procedure a model or an operator performs by hand, and
  `benchmarks/cases/` currently holds **2 of the 12 Class A category files** the manifest
  declares — `ai_slop_rewrite.md` and `grant_narrative.md`. The other two files in that
  directory, `conflict_preservation.md` and `simulation_fidelity.md`, are Class B runtime
  gates and are not manifest categories; they are pass/fail and are never scored, so counting
  them toward the twelve would inflate the coverage number with results that cannot be
  averaged. `_template.md` is a template. The declared Class A gates — ≥ 5 points on ≥ 70% of
  cases, no drop over 3 points without a documented reason, 100% fabrication-trap recall,
  ≥ 80% voice-drift-direction recall, a valid delivery bundle per case — are the standard to
  assess against, and the assessment is a person's. Write the assessment down where a reader
  will find it; **`benchmarks/reports/` does not exist yet** and creating an empty one would
  imply a suite that has run.

### The bundles

- [ ] **[release]** / **[build]** `bash scripts/build-skill.sh` succeeds
- [ ] **[ci]** The build is byte-reproducible across two runs
- [ ] **[ci]** / **[build]** Both bundles are at or under 200 files
- [ ] **[ci]** The committed bundles at the repo root match the tree. `README.md` and
      `docs/INSTALL.md` tell people to download from `main`, and that instruction is only
      safe while the committed bundle is the tree it claims to be
- [ ] **[manual]** Runtime bundle installs in Claude.ai
- [ ] **[manual]** Runtime bundle installs in Claude Code
- [ ] **[manual]** Craft bundle installs alongside it

### Release notes

- [ ] **[manual]** **`release/RELEASE_NOTES_<tag>.md` exists.** The workflow warns and
      generates notes from commits if it is missing, and commit-generated notes on the most
      widely read page in the project is a poor substitute for a document somebody wrote
- [ ] **[manual]** **Every link in it is absolute**, pinned into this repository. A release
      body is not rendered from its own directory, so a relative `../docs/INSTALL.md`
      resolves to nothing on the page most people will ever read. `check-links.py` verifies
      absolute links that point back into this repository, so the resolution is checked; the
      *choice* to write them absolute is not
- [ ] **[manual]** Every transcript quoted in it was produced by running the tool
- [ ] **[manual]** Anything specified-and-not-executable is labelled as such

---

## 4. Tag and publish

- [ ] **[manual]** Choose the path: push the tag, or run the workflow with `tag` and `ref`
- [ ] **[release]** Tag, `wi.py --version` and the `CHANGELOG.md` heading agree
- [ ] **[release]** If the tag already exists, it points at the commit being built
- [ ] **[release]** Four assets published with `--verify-tag`

  If a release for the tag already exists, the workflow **uploads assets with `--clobber`
  and does not update the title or the notes.** A re-run to fix an asset will not fix a
  release body. Editing that is manual.

- [ ] **[manual]** Tag signed, if the maintainer has a signing key. The workflow creates an
      annotated tag on the dispatch path and does not sign it

---

## 5. Public verification (Chrome MCP gate)

None of this is automated.

- [ ] **[manual]** Repo About description and topics current
- [ ] **[manual]** `README.md` renders correctly on GitHub.com
- [ ] **[manual]** The release page renders correctly
- [ ] **[manual]** All four asset downloads work end to end
- [ ] **[manual]** `shasum -a 256 -c` verifies both downloaded bundles against their
      published `.sha256`
- [ ] **[manual]** Console clean, no errors
- [ ] **[manual]** Screenshots saved to `verification-screenshots/wave-NN/`

**The one worth doing on a second machine:** download `scripts/wi.py` and a `.wiab`, and run
`python3 wi.py verify-release <bundle>` with the network off. That is the promise the
project makes to a reader who has no reason to trust it, and it is the only item on this
list that tests the promise rather than the process.

---

## 6. Post-release

- [ ] **[manual]** Announcement posted
- [ ] **[manual]** `ROADMAP.md` and `plans/v6.manifest.yaml` updated for the next release
- [ ] **[manual]** Open RFCs tagged with disposition — deferred, in-flight, merged
- [ ] **[manual]** Benchmark assessment written down and linked from the release notes. The
      intended home is `benchmarks/reports/`, which **does not exist yet** — the first
      assessment creates it. Nothing checks this box for you.

---

## Author sign-off

**Antonio T. Smith Jr.** — final release authorization holder.
