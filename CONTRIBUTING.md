# Contributing to Writing Intelligence v6

Welcome. Writing Intelligence is free and open under MIT. Contributions are how it stays alive and how it gets better than its author alone could make it.

**The v3 Law**: *If a rule cannot be applied, audited, scored, tested, or explained — it is not a rule yet.*

**The v4 Law**: *If a claim cannot be pointed at, it has not been verified — and fluent prose must never be allowed to look like checked prose.*

**The v5 Law**: *A reader can point at any sentence and ask why it is here, what supports it, what depends on it, and what breaks if it changes — and another machine can independently verify the answer.*

**The v6 Law**: *No consequential state transition may become authoritative unless the system can identify the exact prior state, the proposed next state, the semantic delta between them, the dependency impact of that delta, the acting authority, the decision basis and the resulting proof closure.*

Every contribution must satisfy all four. The v4 and v5 material below is not deprecated — v6 is a layer beneath those laws, not a replacement for them, and laws A through L are in force unamended.

---

## Where things live

| Path | What it holds |
|---|---|
| `scripts/wi.py` | **The canonical deterministic core.** One stdlib-only file. Every surface calls it; nothing reimplements it |
| `references/v4/` | The 8 accountability documents — laws A–F. Still normative, unchanged by v5 and v6 |
| `references/v5/` | The 20 v5 doctrine documents plus an index — graph, anchors, hashing, staleness, semantic diff, release, policy, workspace, security, non-goals. Still normative |
| `references/v6/` | 24 files — 23 doctrine documents and an index. The constitution, the authority model, semantic version control, the merge protocol, counterfactual simulation, bitemporal state, proof obligations, capsules, autonomous execution, non-goals |
| `schemas/` | 11 v3 craft schemas |
| `schemas/v5/` | 15 v5 state schemas |
| `schemas/v6/` | 20 v6 runtime schemas — actor, argument, authority, claim, common, compile, conflict, constraint, decision, extension, graph_delta, graph_root, meaning, proof, proposal, release, semantic_commit, semantic_node, simulation, time |
| `tests/v4/` | The adversarial fixture and the 3-check regression suite |
| `tests/v5/` | The worked world fixture, the 32-check regression suite, and `EXPECTED_TRANSCRIPT.txt` |
| `tests/v6/` | The 70-check regression suite: canonicalization, authority, decisions, simulation, merge, bitemporal query, obligations, capsules, constraints |
| `plans/v6.manifest.yaml` | The implementation program as an inspectable object. CI validates it; `references/v6/BUILD_MANIFEST.md` is the document it governs, not the other way round |
| `packs/craft/` | The craft bundle's own `SKILL.md` — the entry point for `writing-intelligence-craft.skill` |
| `agents/` | The 12 specialist agents and `agent_manifest.yaml` |
| `services/api/` | The REST reference runtime for the **v3 craft kernel**. It does not expose the v5 or v6 verification tier, and that is Law K rather than an oversight |
| `governance/` | RFC process, ADR template, versioning rules, release checklist |

`tests/v5/EXPECTED_TRANSCRIPT.txt` is a real recorded session. If your change moves any output that appears in it, the transcript is part of your diff — a transcript that no longer matches the tool is a document that lies about the tool, which is this project's own failure mode.

`plans/v6.manifest.yaml` carries the same obligation in a stricter form. A wave marked `shipped` must name commands that exist in `scripts/wi.py --help`, and `scripts/check-manifest.py` enforces it on every push. That rule is Law C compiled: a roadmap cannot claim a capability the CLI does not have.

---

## Before you open a PR

```bash
bash tests/v4/test_wi.sh          # v4 regression  — 3 PASS lines
bash tests/v5/test_wi5.sh         # v5 regression  — 32 PASS, ends "v5 regression complete"
bash tests/v6/test_wi6.sh         # v6 regression  — 70 PASS, ends "v6 regression complete"
python3 scripts/wi.py doctor      # capability report loads
python3 scripts/check-links.py    # every relative link, and every link back into this repo, resolves
python3 scripts/check-manifest.py # no shipped wave names a command that does not answer
bash scripts/build-skill.sh --check
cd services/api && npm ci && npm run typecheck && npm test
```

All three suites exit non-zero on failure and all three must pass before a PR is opened.

CI runs all three on every push and pull request, and asserts the **PASS count** separately from the exit code — 3, 32 and 70 — because an exit code cannot tell you the script stopped early and skipped checks it never ran. The verifier job runs on Python 3.8, 3.11, 3.12 and 3.13, across Linux and macOS, **with no dependencies installed on purpose**. 3.8 is the documented floor and it is tested, so the claim is backed. The API job runs on Node 20 and 22.

CI also runs two mutation checks, and they are the reason the green build means anything. The first disables the artifact-digest comparison in `wi.py` and requires the v5 suite to go red. The second teaches the merge to auto-resolve a semantic conflict and requires the v6 suite to go red. A suite that stays green when you break the control it claims to test was never testing anything, and this project does not ship decoration.

Four more jobs gate a PR: `schemas` parses every schema and requires an `$id`, a title and a description on each; `plan` runs the build-manifest check; `docs` runs the link check and asserts that every subcommand quoted in `README.md`, `CHEATSHEET.md`, `USER_GUIDE.md` and `docs/INSTALL.md` actually exists in `wi.py --help`; `bundle` builds both skill bundles, proves the build is byte-reproducible, verifies the committed bundles match the tree, and enforces the 200-file installer ceiling on each. A bundle over that ceiling does not degrade — it does not load, which would make every install instruction in the repository false.

`scripts/wi.py` must keep running on Python 3.8 with **no dependencies installed**. That is tested, so the claim is backed.

---

## Cutting a release

Releases are published by `.github/workflows/release.yml`, never by hand. There are two ways in:

**Push a tag** — `git tag -a v6.1.0 -m … && git push origin v6.1.0`.

**Or run the workflow** — *Actions → Release → Run workflow*, `tag: v6.1.0`, `ref: main`. This path creates the tag itself, which is the one to use when tag pushing is unavailable (a sandboxed runner, a machine without permission for `refs/tags`, a fork).

Either way the job refuses to publish unless, in this order:

1. `tests/v4/test_wi.sh`, `tests/v5/test_wi5.sh` and `tests/v6/test_wi6.sh` all pass — a release whose verifier is broken installs cleanly and quietly certifies nothing, which is the worst artifact this project could ship;
2. `check-manifest.py` passes, so no shipped wave names a command that does not answer;
3. every link resolves;
4. both bundles build;
5. the tag, `wi.py --version` and the `CHANGELOG.md` heading all agree.

Only then is the tag created — a commit that fails its own release gate never gets stamped with a version number. And if the tag already exists it must point at the commit that was built, or the job stops: publishing assets under a tag naming a different commit is the one failure here nobody can see afterwards, because the release page looks entirely normal.

`scripts/build-skill.sh` runs the same three suites twice — once against the tree, once inside the extracted bundle — and refuses to produce an artifact if either run fails. A verifier that works in the repository and not in the bundle is the one a user actually installs.

Before tagging, write `release/RELEASE_NOTES_<tag>.md`; the workflow uses it as the release body. **Links in that file must be absolute**, pinned to the tag. A release body is not rendered from its own directory, so a relative `../docs/INSTALL.md` resolves to nothing on the page most people will ever read. `check-links.py` verifies absolute links that point back into this repository, so this is checked rather than trusted.

---

## Contributing to the meaning-runtime tiers (v6)

This is where a well-meant change does the most damage, because every control in this layer exists to **refuse** something, and a refusal that has been quietly removed looks exactly like a refusal that was never needed. The v4 and v5 rules in the next section apply here too. These are additional.

**A change to merge behaviour ships a negative fixture proving no third value can be manufactured.** The single most dangerous output this system could produce is a plausible middle number — `approximately 12,000` between an 11,800 and a 12,400 that two authorized actors each committed. It reads as diligence, it is hedged enough to survive review, it is close enough to both inputs that nobody reviewing the diff feels alarmed, and **no source in the workspace supports it**. A wrong number an author chose is a number somebody can be asked about; a number the merge synthesized has no author at all. So `tests/v6/test_wi6.sh` does not merely assert that the merge stops. It asserts that the strings `12100` and `12000` appear **nowhere** in the merge output:

```bash
hasnt "the merge did not invent 12100" "$OUT" "12100"
hasnt "the merge did not invent 12000" "$OUT" "12000"
```

Delete the conflict-preservation logic and those two assertions go red — which is what makes them worth having, and which CI proves on every run with the auto-resolve mutation. A merge change with no such fixture will be returned. The forbidden outputs are enumerated exactly in `references/v6/MERGE_PROTOCOL.md` §5.2: an average, a range, a recency rule, a direction-of-merge rule, and a parenthetical that leaves the graph holding one value while the rendering shows two.

**A new capability string comes with the delta class that requires it.** `V6_CAPABILITIES` in `wi.py` is a closed vocabulary of sixteen, and `V6_DELTA_CAPABILITY` maps each semantic delta class onto the capability an actor must hold to accept it. A delta class absent from that map resolves to `claim.accept` — which means a new class that ought to require `obligation.create` or `canon.modify` would be acceptable by anyone holding general claim authority, silently, with every gate still reporting green. **That is a default-allow and it will be rejected.** The two halves land in the same PR or neither lands. The test for adding a seventeenth capability is in `references/v6/AUTHORITY_MODEL.md` §3 and it is not whether the capability names something real: it is whether any organization would grant one of a pair and withhold the other. If nobody would ever split them, they are one capability.

**No code path may grant ambient authority. Absence of a grant is a refusal, never a default.** Nobody holds authority because of what they are, including the actor who created the workspace. Four refusals exist because each sends a person somewhere different, and a single "permission denied" sends them nowhere: no grant, an expired grant, a grant out of scope, a revoked grant. A PR that collapses them, or that adds a path where a missing grant resolves permissively, removes the only control that makes every other control in the system non-decorative. Delegation is monotonic in capability, scope **and** lifetime, checked at issue time rather than detected at use time — lifetime is the one most often left out, and without it a two-week grant delegates a ten-year one and the expiry that made the parent safe is gone. A judgment provider may never hold a grant at all; that is constitutional rather than configurable, it fails at issue time, and constraint C008 sweeps the whole workspace for violations on every run. An unrecognized scope kind raises. It does not return `True`, which would grant authority the workspace cannot describe, and it does not return `False`, which would silently disable a grant somebody is relying on and produce a refusal nobody can explain.

**Simulation mutates nothing, and the candidate root is the root the commit produces.** `wi simulate` is implemented as an ephemeral branch that is created, walked and dropped; it never advances a named branch, never writes a verification result, never writes a decision, and never records an invalidation against a real state. The suite asserts the branch root is identical before and after — a simulation that mutates the workspace it was asked to reason about has done the one thing it exists not to do, and it will do it quietly, because the report will still look right. The second property is that `candidate root` from `wi simulate` equals `next root` from the commit that follows. A preview that produces a different root than the commit is a guess with formatting. **That equality holds today and is not currently asserted in `tests/v6/test_wi6.sh`** — the suite checks root-immutability, not candidate-equality. Any change touching graph root computation must keep the equality true, and wiring an assertion for it into the suite is a welcome patch.

**A correction supersedes. It never erases.** Valid time is when a claim held in the world; knowledge time is when this workspace believed it. An overwrite answers *what do we now believe was true in 2022* and destroys *what did we know when we filed this in March*. There is no `rebase`, no `squash`, no `amend`, no force push, no history edit and no administrative delete of a committed state, and there is no compaction pass that drops superseded knowledge. A PR that overwrites a state in place is rejected on sight. The legitimate needs behind that request each have an answer that is not rewriting, and they are tabulated in `references/v6/NON_GOALS.md` §13: a messy branch gets a filtered view, a wrong decision gets a new decision recorded after it, an ingested-by-mistake source gets a deletion event where the bytes go and the fact of removal stays.

**Anything automated proposes. It may not bypass the machinery a person uses.** Law A was written for one model helping one author, where the author reads every proposal because there are eleven of them. That premise does not survive scale. The failure mode is not a rogue process — it is an ordinary, well-behaved, useful one that fixes four hundred small things correctly and one thing wrongly, and by the time anybody notices, the wrong one has three hundred commits on top of it. Attribution after the fact is not attribution; it is archaeology. A PR that adds an automated path writing directly to state, skipping proposal, impact or authority, is rejected. The effect classes in `references/v6/AUTONOMOUS_EXECUTION.md` §5 are the mechanism: `ProposalWrite` may write proposals and is forbidden from writing a target state, a decision or a result, and a step declares its effect class **before** it runs, because an effect discovered by observation is an effect discovered on a run that already happened.

**A constraint that could not run is not a constraint that passed.** `wi constraints` reports twenty graph constraints, C001 through C020, with three statuses and no fourth. `--` names the reason it could not be evaluated. Folding those into `ok` is the exact failure this project exists to catch, one level up. There is no percentage and no aggregate score anywhere in that output, and the suite asserts the absence — a constraint engine that emits a score has averaged across kinds of failure that are not commensurable, and the number would be quoted.

**A capsule states what it does not prove, inside the artifact.** A redacted leaf proves it was inside the producer's closure and proves nothing about its content. That limit lives in `does_not_prove`, `declared_omissions` and `not_a_proof_of` rather than in a footnote, because footnotes are not read and the word in the column is what gets quoted. `wi capsule verify` prints the verdict and the scope as two separate lines for the same reason — *valid* answers whether the cryptography holds, *scope* answers whether it establishes what a reader wants, and one word merging them would be technically correct and read as an endorsement. The `*_by_producer` reliability transformation in [`references/v6/PROOF_CAPSULES.md`](references/v6/PROOF_CAPSULES.md) §6 is **specified and does not ship in 6.0.0** — the string appears nowhere in `scripts/wi.py`. Implementing it is a welcome patch and it needs a negative fixture like everything else. A tampered capsule exits 2 and must never print `VERDICT VERIFIED`; the suite tampers with one on every run and asserts that string is absent.

And the two rules that were already here and already work:

**A check must be able to fail — and you must ship the fixture that trips it.** Every new deterministic check needs a **negative fixture that fails if the implementation were disabled**, in the same PR, wired into the suite. A guard that has only ever passed has not been shown to work; its green line is indistinguishable from a broken one. `tests/v6/test_wi6.sh` is built entirely on this: the unauthorized acceptance is denied *and* denied with the right error code; the conflicted merge is refused *and* does not move the root; the wording-only proposal is classified *and* does not demand obligation authority; the tampered capsule is rejected *and* never prints `VERIFIED`. Assert on the exact code string the CLI emits, not a paraphrase of it — the suite is the working list.

**`scripts/wi.py` stays stdlib-only.** No pip installs, no network, no model calls. It must run air-gapped on Python 3.8. The whole value of the deterministic tier is that it requires trusting nothing — a single dependency ends that.

---

## Contributing to the accountability and proof layers (v4 and v5)

These rules are unchanged and still binding.

**Under-claim, always.** Wrongly `supported` is a catastrophe; wrongly `needs_source` is a nuisance. Any change that moves a claim toward `supported` needs a stronger argument than one that moves it away.

**Never make the system able to invent a source.** This is not a tunable. See `references/v4/NON_GOALS.md`, `references/v5/NON_GOALS.md` and `references/v6/NON_GOALS.md`.

**Do not add a second implementation of a verification rule.** If a check exists in `wi.py`, the REST service does not reimplement it — it shells out or does without. Two implementations drift and the drifting one is invisible. This is Law K, and it binds every future surface: CLI, MCP, REST, Workbench, CI, browser and skill wrappers. Adapters translate. They do not decide. A cache keyed by state digest is not a second implementation and is permitted; a cache that computes a verdict is.

**Report what was not done.** If a check could not run, the output says so, and it distinguishes *could not* from *chose not to* from *ran and was later invalidated by an edit*. Silence that reads as success is the failure mode this project exists to remove.

**Documentation must label anything not executable.** Every section of every `references/v5/` and `references/v6/` document carries one of exactly two markers on its first line: **executable in `scripts/wi.py`** or **specified**. New doctrine follows the same rule, and so does any prose anywhere in the repository that describes a capability. "Specified" means designed and normatively described here and **not executable anywhere** — it is not a roadmap tease and it must never be written in a register that lets a reader assume it ships. If a PR describes something as working, a reviewer must be able to run it.

**Changing canonical serialization is a major-version act.** Canonical JSON, NFC normalization, key ordering, domain separation and the contents of the digest preimage are defined in `references/v5/CANONICAL_HASHING.md`. **Change any of them and every digest in every workspace and every already-shipped bundle moves.** Bundles that verified yesterday fail today, for a reason that looks like tampering and is not. That is not a patch, not a minor, and not a cleanup — it is a MAJOR release with a migration path, an RFC, and a statement of what happens to existing artifacts. The v6 state digest is domain-separated from the v5 digest so that a byte-identical payload cannot be ambiguously readable as both; removing that separation is the same class of change.

**The five protocol words go through the RFC process.** Any change to the meaning of `verified`, `stale`, `BLOCK`, `permitted` or `source quarantine` requires an accepted RFC per `governance/RFC_PROCESS.md` **and** a benchmark case that fails before the change and passes after it. Not a pull request. Not a documentation clarification. These words are the interface between this system and every reader who never opens it, and they are load-bearing in other people's compliance processes, CI pipelines and contracts. Quietly widening `verified` to cover one more thing is a silent breaking change to every artifact ever produced, retroactively, including the ones already sent — and in a diff it does not look like a breaking change. It looks like an improvement to a sentence. Loosening happens by accretion, never by decision; the RFC requirement exists to make each widening cost something and leave a record of who paid.

---

## What will get a PR closed

These are not revisions to negotiate. They will be closed.

**A dependency added to `wi.py`.** The deterministic tier's entire value is that it requires trusting nothing and runs on an air-gapped review machine. One import ends that, and it ends it for every reader downstream who was told the file has no dependencies.

**A check with no negative twin.** A guard that has only ever passed certifies nothing while looking like assurance, which is worse than no guard at all.

**A flag that makes merge pick a side.** There is no `--ours`, no `--theirs`, no `--newest`, no averaging option and no strategy that widens automatic resolution beyond disjoint `wording_only` changes. The absence is the feature. In source code an automatic merge is checked downstream by a compiler and a test suite, which object; in meaning there is nothing downstream that objects.

**A stored freshness flag.** Freshness is a property of dependencies, not a badge. A stored flag is a cache that can be wrong about freshness at exactly the moment freshness matters. The answer is the one v5 established and v6 keeps: cache keyed by state digest, because a changed state produces a changed key and a changed key cannot hit the old entry. That is not a discipline anybody maintains; it is a property of the key.

**Softening any of the eighteen laws.** Laws A through F, G through L, and M through R are in force unamended. A PR that reinterprets, qualifies or quietly narrows one of them is a constitutional change and does not arrive as a pull request. `references/v6/CONSTITUTION.md` is the highest authority in the repository; where any other document, schema, adapter, wrapper or surface disagrees with it, that document is the defect.

The five older refusals hold with the same force: **detector evasion**, **citation generation**, **blended quality scores**, **any code path where a model can write a verification record**, and **similarity as support**. Each is explained under *What We Will Not Merge* below.

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
- **New semantic delta class**: must ship its entry in `V6_DELTA_CAPABILITY` in the same PR, must state which capability it requires and why that capability rather than the one below it, and must ship a fixture proving an actor holding only the weaker capability is refused.
- **New graph constraint**: must take the next free `C0NN` identifier, must be able to report `--` with a reason where it cannot be evaluated, and must ship both the passing and the failing fixture.
- **New v6 capability or scope kind**: must be reviewed against the split test in `references/v6/AUTHORITY_MODEL.md` §3, must be checked somewhere, and must not be reachable by any default.
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
- [ ] `plans/v6.manifest.yaml` updated if the change ships or advances a wave, and `check-manifest.py` passes
- [ ] No breaking changes to existing schemas
- [ ] No change to canonical serialization or to the meaning of `verified` / `stale` / `BLOCK` / `permitted` / `source quarantine` (those are not minor contributions)

---

## Major Contributions

Major contributions change the kernel, the laws, or the public API. These are maintainer-led. Open an issue describing the change you want to see; expect deep discussion. Major contributions ship in MAJOR-version releases only.

Four things are always major, no matter how small the diff: **canonical serialization** (it moves every digest ever produced, in every workspace and every already-shipped bundle), **the meaning of a protocol word** (`verified`, `stale`, `BLOCK`, `permitted`, `source quarantine`), **anything that lets a model produce a record typed `verified`**, and **any amendment to laws A through R**.

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
- **Any code path where a model can write a verification record.** A judgment provider may emit `judged`. It may never emit `verified`, may never sign a decision record, may never be the actor on an acceptance, and may never hold a capability grant. `verified` names *how a result was produced*, not how sure anybody is, and there is no confidence threshold that promotes one into the other.
- **Similarity as support.** No record typed `verified` may cite a retrieval or embedding score as its basis, and no similarity value may render as a confidence, a coverage figure or a support strength. Retrieval proposes candidates; deterministic comparison decides. High cosine similarity would happily rank 11,800 as support for 12,400 — the exact fixture this project ships to prove the point.

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

Contributions are accepted under MIT. See `NOTICE` and `PATENTS.md` for trademark and invention-disclosure terms.

---

## Author

Antonio T. Smith Jr. / Density6 LLC

[densitysix.com](https://densitysix.com) · [github.com/antonio0720/writing-intelligence](https://github.com/antonio0720/writing-intelligence)
