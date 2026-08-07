# Contributing to Writing Intelligence v5

Welcome. Writing Intelligence is free and open under MIT. Contributions are how it stays alive and how it gets better than its author alone could make it.

**The v3 Law**: *If a rule cannot be applied, audited, scored, tested, or explained — it is not a rule yet.*

**The v4 Law**: *If a claim cannot be pointed at, it has not been verified — and fluent prose must never be allowed to look like checked prose.*

**The v5 Law**: *A reader can point at any sentence and ask why it is here, what supports it, what depends on it, and what breaks if it changes — and another machine can independently verify the answer.*

Every contribution must satisfy all three.

---

## Where things live

| Path | What it holds |
|---|---|
| `scripts/wi.py` | **The canonical deterministic core.** One stdlib-only file. Every surface calls it; nothing reimplements it |
| `references/v4/` | The six accountability laws A–F. Still normative, unchanged by v5 |
| `references/v5/` | The 20 v5 doctrine documents — constitution, graph, anchors, hashing, staleness, semantic diff, release, policy, workspace, security, non-goals |
| `schemas/v5/` | The 15 v5 state schemas. `schemas/v3/` is unchanged and still valid under its own namespace |
| `tests/v4/` | The adversarial fixture and the 3-check regression suite |
| `tests/v5/` | The worked world fixture, the 32-check regression suite, and `EXPECTED_TRANSCRIPT.txt` |
| `governance/` | RFC process, ADR template, versioning rules, release checklist |

`tests/v5/EXPECTED_TRANSCRIPT.txt` is a real recorded session. If your change moves any output that appears in it, the transcript is part of your diff — a transcript that no longer matches the tool is a document that lies about the tool, which is this project's own failure mode.

---

## Before you open a PR

```bash
bash tests/v4/test_wi.sh          # v4 regression — must print 3 × PASS
bash tests/v5/test_wi5.sh         # v5 regression — 32 checks, ends "v5 regression complete"
python3 scripts/wi.py doctor      # capability report loads
python3 scripts/check-links.py    # every relative link must resolve
bash scripts/build-skill.sh --check
cd services/api && npm ci && npm run typecheck && npm test
```

Both suites exit non-zero on failure and both must pass before a PR is opened.

CI runs the v4 regression, the link check, the bundle build and the API tests on every push, across Python 3.8–3.13 on Linux and macOS, and on Node 20 and 22. It asserts the **PASS count** separately from the exit code, because an exit code cannot tell you the script stopped early and skipped checks it never ran. **`tests/v5/test_wi5.sh` is not yet wired into `.github/workflows/ci.yml`** — run it locally, every time. Wiring it in, with the same PASS-count assertion, is a welcome patch.

`scripts/wi.py` must keep running on Python 3.8 with **no dependencies installed**. That is tested, so the claim is backed.

---

## Cutting a release

Releases are published by `.github/workflows/release.yml`, never by hand. There are two ways in:

**Push a tag** — `git tag -a v4.1.0 -m … && git push origin v4.1.0`.

**Or run the workflow** — *Actions → Release → Run workflow*, `tag: v4.1.0`, `ref: main`. This path creates the tag itself, which is the one to use when tag pushing is unavailable (a sandboxed runner, a machine without permission for `refs/tags`, a fork).

Either way the job refuses to publish unless, in this order:

1. `tests/v4/test_wi.sh` passes — a release whose verifier is broken installs cleanly and quietly certifies nothing, which is the worst artifact this project could ship. `tests/v5/test_wi5.sh` is **not** a workflow gate today; adding it to `release.yml` is the right patch, and until it lands it is a manual step to run by hand before tagging;
2. every link resolves;
3. the bundle builds;
4. the tag, `wi.py --version` and the `CHANGELOG.md` heading all agree.

Only then is the tag created — a commit that fails its own release gate never gets stamped with a version number. And if the tag already exists it must point at the commit that was built, or the job stops: publishing assets under a tag naming a different commit is the one failure here nobody can see afterwards, because the release page looks entirely normal.

Before tagging, write `release/RELEASE_NOTES_<tag>.md`; the workflow uses it as the release body. **Links in that file must be absolute**, pinned to the tag. A release body is not rendered from its own directory, so a relative `../docs/INSTALL.md` resolves to nothing on the page most people will ever read. `check-links.py` verifies absolute links that point back into this repository, so this is checked rather than trusted.

---

## Contributing to the accountability and proof layers

This is the part of the project where a well-meant change does the most damage, so it carries extra rules. They apply to the v4 accountability tier and the v5 proof tier alike.

**A check must be able to fail — and you must ship the fixture that trips it.** Every new deterministic check needs a **negative fixture that fails if the implementation were disabled**, in the same PR, wired into the suite. A guard that has only ever passed has not been shown to work; its green line is indistinguishable from a broken one. `tests/v4/test_wi.sh` is proven able to fail — disable citation resolution in `wi.py` and it turns the gate from BLOCK to HOLD and says so. `tests/v5/test_wi5.sh` is built entirely on negative twins: the tampered bundle must be rejected *and* rejected for the right reason; the concept registry must accept the governing figure *and* fail on the forbidden alias; the changed sentence must be classified *and* the unchanged sentences left alone. Follow that pattern.

**Under-claim, always.** Wrongly `supported` is a catastrophe; wrongly `needs_source` is a nuisance. Any change that moves a claim toward `supported` needs a stronger argument than one that moves it away.

**`scripts/wi.py` stays stdlib-only.** No pip installs, no network, no model calls. It must run air-gapped on Python 3.8. The whole value of the deterministic tier is that it requires trusting nothing — a single dependency ends that.

**Never make the system able to invent a source.** This is not a tunable. See `references/v4/NON_GOALS.md` and `references/v5/NON_GOALS.md`.

**Do not add a second implementation of a verification rule.** If a check exists in `wi.py`, the REST service does not reimplement it — it shells out or does without. Two implementations drift and the drifting one is invisible. This is Law K, and it binds every future surface: CLI, MCP, REST, Workbench, CI, browser and skill wrappers. Adapters translate. They do not decide.

**Report what was not done.** If a check could not run, the output says so, and it distinguishes *could not* from *chose not to* from *ran and was later invalidated by an edit*. Silence that reads as success is the failure mode this project exists to remove.

**Documentation must label anything not executable.** Every section of every `references/v5/` document carries one of exactly two markers on its first line: **executable in `scripts/wi.py`** or **specified**. New doctrine follows the same rule, and so does any prose anywhere in the repository that describes a capability. "Specified" means designed and normatively described here and **not executable anywhere** — it is not a roadmap tease and it must never be written in a register that lets a reader assume it ships. If a PR describes something as working, a reviewer must be able to run it. See `references/v5/NON_GOALS.md` for why a limitation and a refusal must never be reported in the same words.

**Changing canonical serialization is a major-version act.** Canonical JSON, NFC normalization, key ordering, domain separation and the contents of the digest preimage are defined in `references/v5/CANONICAL_HASHING.md`. **Change any of them and every digest in every workspace and every already-shipped bundle moves.** Bundles that verified yesterday fail today, for a reason that looks like tampering and is not. That is not a patch, not a minor, and not a cleanup — it is a MAJOR release with a migration path, an RFC, and a statement of what happens to existing artifacts.

**The five protocol words go through the RFC process.** Any change to the meaning of `verified`, `stale`, `BLOCK`, `permitted` or `source quarantine` requires an accepted RFC per `governance/RFC_PROCESS.md` **and** a benchmark case that fails before the change and passes after it. Not a pull request. Not a documentation clarification. These words are the interface between this system and every reader who never opens it, and they are load-bearing in other people's compliance processes, CI pipelines and contracts. Quietly widening `verified` to cover one more thing is a silent breaking change to every artifact ever produced, retroactively, including the ones already sent — and in a diff it does not look like a breaking change. It looks like an improvement to a sentence. Loosening happens by accretion, never by decision; the RFC requirement exists to make each widening cost something and leave a record of who paid.

---

## The Three Contribution Tiers

| Tier | Effort | Process |
|---|---|---|
| **Patch** | Small fixes | Open a PR with a clear description |
| **Minor** | New capability | RFC → PR → benchmark gate |
| **Major** | Structural change | Maintainer-led; community discussion required |

See `governance/RFC_PROCESS.md` for the full RFC lifecycle and `governance/VERSIONING.md` for what counts as which tier.

---

## Patch Contributions

Open a PR directly. Examples:

- Typo fixes
- Doc clarifications
- Anti-pattern library additions (must include detection rule + before/after)
- Benchmark cases added inside an existing category
- Bug fixes in schema files
- Reference example additions

**PR checklist**:

- [ ] Description explains the change and why
- [ ] Existing tests / benchmarks still pass
- [ ] No breaking changes to schemas
- [ ] Documentation reflects the change

---

## Minor Contributions (Require RFC)

Open an RFC first. Use the template in `governance/RFC_PROCESS.md`. Examples:

- **New genre pack**: must follow the 15-section Domain Pack Schema (`docs/DOMAIN_PACK_GUIDE.md`). Must include at least 5 benchmark cases.
- **New voiceprint**: must include the measurable fingerprint per `docs/VOICEPRINT_GUIDE.md` — NOT only a descriptive sketch.
- **New rewrite operator**: must declare its effect, its before/after examples, and its placement in the v3.0 operator table.
- **New scoring rubric**: must declare its dimensions, weighting, and how it interacts with v3.0 Composite.
- **New agent**: must follow the agent spec format. Must declare job, artifact, schema, dependencies, conflict resolution.
- **New domain pack category**: must include at least 5 benchmark cases and update the genre collision matrix.
- **New deterministic check**: must declare what it compares, what it cannot see, which reliability type it emits, and how it appears in `wi doctor`. Must ship a **negative fixture that trips it if the implementation were disabled**.
- **New evidence anchor kind**: must supply the adapter contract per `references/v5/EVIDENCE_ANCHORS.md` — locator format, raw-bytes rule, extractor identity, sandbox posture and declared limits — and must report `unavailable` rather than degrading into a text-span anchor when it cannot resolve.
- **New writing test or concept contract**: must state its denominator and ship both the passing and the failing fixture.

**RFC + PR checklist**:

- [ ] RFC accepted before PR opens
- [ ] PR linked to the accepted RFC
- [ ] Benchmark cases authored
- [ ] Benchmark suite passes for the change
- [ ] Negative fixture added for every new deterministic check, and shown failing with the check disabled
- [ ] Genre collision matrix updated (if new pack)
- [ ] Documentation updated (USER_GUIDE, CHEATSHEET, applicable docs/), with every new capability marked *executable* or *specified*
- [ ] `tests/v5/EXPECTED_TRANSCRIPT.txt` updated if any quoted output moved
- [ ] No breaking changes to existing schemas
- [ ] No change to canonical serialization or to the meaning of `verified` / `stale` / `BLOCK` / `permitted` / `source quarantine` (those are not minor contributions)

---

## Major Contributions

Major contributions change the kernel, the laws, or the public API. These are maintainer-led. Open an issue describing the change you want to see; expect deep discussion. Major contributions ship in MAJOR-version releases only.

Three things are always major, no matter how small the diff: **canonical serialization** (it moves every digest ever produced), **the meaning of a protocol word** (`verified`, `stale`, `BLOCK`, `permitted`, `source quarantine`), and **anything that lets a model produce a record typed `verified`**.

---

## Quality Requirements for All Contributions

Every contributed rule, pack, voiceprint, operator, schema, agent, or doctrine file must be:

1. **Applicable** — a writer or operator can use it on a real task
2. **Auditable** — its effect can be observed in the output
3. **Scored** — its presence or absence shifts a measurable score
4. **Testable** — there's at least one benchmark case demonstrating its effect
5. **Explainable** — its rationale can be stated in plain language

Contributions that satisfy fewer than 3 of these criteria will be returned for revision.

---

## What We Will Not Merge

- Anti-patterns that are stylistic preferences without measurable effect
- Voiceprints that are mood boards without metrics
- "Tips" that read like motivational content
- Genre packs without benchmark cases
- Schemas without backwards compatibility consideration
- Changes that reduce evidence discipline in high-stakes domains
- Anything that makes a fabrication risk easier

Five of these are not negotiable and will be closed rather than revised:

- **Detector evasion.** Any feature whose purpose is to make writing pass as human rather than *be* better constructed. A system built to produce a machine-checkable account of how a document came to exist cannot also be a system for concealing how it came to exist. Those are opposite products, and building one would require the release bundle to lie — a bundle that lies once is worth nothing forever.
- **Citation generation.** Any path that constructs, completes, guesses or plausibly reconstructs a reference. If support does not exist in the supplied material, the answer is `needs_source`. A fabricated citation is self-concealing: it looks exactly like a real one, survives casual review, and is usually found by the one reader who was going to decide something.
- **Blended quality scores.** Any single number that averages across the reliability types. `verified`, `measured`, `judged` and `human-declared` do not average — that is their entire job. A composite that hides the mix is authority theater, and a percentage without a denominator is not a measurement.
- **Any code path where a model can write a verification record.** A judgment provider may emit `judged`. It may never emit `verified`, may never sign a decision record, and may never be the actor on an acceptance. `verified` names *how a result was produced*, not how sure anybody is, and there is no confidence threshold that promotes one into the other.
- **Similarity as support.** No record typed `verified` may cite a retrieval or embedding score as its basis, and no similarity value may render as a confidence, a coverage figure or a support strength. Retrieval proposes candidates; deterministic comparison decides.

---

## Communication

- Open an issue before opening a PR for anything beyond a typo
- Use the issue labels: `bug`, `docs`, `genre`, `voiceprint`, `schema`, `agent`, `benchmark`, `governance`, `certification`, `rfc`
- Keep discussions in the issue or PR thread; the maintainer reads everything

## Code of Conduct

- Be precise. Be kind. Be honest.
- Disagree with arguments, not people.
- Surface evidence; cite sources.
- Treat the doctrine like a living thing — it can change, but only for cause.

---

## Recognition

Every accepted contribution is acknowledged in `CHANGELOG.md`. Operators who contribute multiple accepted minor or major changes can apply for Architect tier (see `certification/operator_levels.md`).

---

## License

By submitting a contribution, you agree to license it under MIT (the same license as the project) and confirm you own the work or have the right to submit it.

---

## Author

Antonio T. Smith Jr. / Density6 LLC

[densitysix.com](https://densitysix.com) · [github.com/antonio0720/writing-intelligence](https://github.com/antonio0720/writing-intelligence)
