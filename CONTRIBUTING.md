# Contributing to Writing Intelligence v3.0

Welcome. Writing Intelligence is free and open under MIT. Contributions are how it stays alive and how it gets better than its author alone could make it.

This document is the v3.0 contribution standard. It is stricter than v2.0 because v3.0 is infrastructure now, not only a skill.

**The v3.0 Law**: *If a rule cannot be applied, audited, scored, tested, or explained — it is not a v3.0 rule yet.*

Every contribution must satisfy this law.

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

**RFC + PR checklist**:

- [ ] RFC accepted before PR opens
- [ ] PR linked to the accepted RFC
- [ ] Benchmark cases authored
- [ ] Benchmark suite passes for the change
- [ ] Genre collision matrix updated (if new pack)
- [ ] Documentation updated (USER_GUIDE, CHEATSHEET, applicable docs/)
- [ ] No breaking changes to existing schemas

---

## Major Contributions

Major contributions change the kernel, the laws, or the public API. These are maintainer-led. Open an issue describing the change you want to see; expect deep discussion. Major contributions ship in MAJOR-version releases only.

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
