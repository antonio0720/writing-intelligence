# Writing Intelligence v3.0 — RFC Process

The Request for Comments (RFC) process governs substantive additions to Writing Intelligence. The goal is to keep contribution velocity high while protecting the doctrine from drift.

## When You Need an RFC

You need an RFC for:

- New genre packs
- New voiceprints
- New schemas or schema-breaking changes
- New rewrite operators
- New scoring systems or scoring-rubric changes
- New agents
- Changes to the 11-pass kernel
- Changes to the Irreversibility laws or the v3.0 Law

You do **not** need an RFC for:

- Bug fixes
- Typo fixes
- Doc clarifications
- Additional benchmark cases inside existing categories
- Additional examples inside existing folders

## RFC Lifecycle

1. **Draft**: Open a GitHub issue with the `rfc` label and the title `RFC: <one-line summary>`.
2. **Specification**: Use the template below. Be specific.
3. **Comment Period**: Minimum 7 days. Maintainers and community discuss.
4. **Resolution**: Maintainer marks the issue `accepted`, `rejected`, or `needs-revision`.
5. **Implementation**: An accepted RFC becomes a PR. The PR must link the RFC.
6. **Merge Gates**: PR must pass benchmark thresholds (see `governance/RELEASE_CHECKLIST.md`).

## RFC Template

```markdown
# RFC: <title>

**Author**: <github handle>
**Date**: YYYY-MM-DD
**Status**: draft | discussion | accepted | rejected | needs-revision
**Tracking issue**: #

## Summary

One paragraph describing what is being proposed.

## Motivation

Why does this need to exist? Who is asking for it? What problem does it solve?

## Detailed Design

What changes. Where. Why this design rather than alternatives.

If proposing a new genre pack: follow the Domain Pack Schema (15 sections) in `docs/DOMAIN_PACK_GUIDE.md`.

If proposing a new voiceprint: follow the Voiceprint Schema in `docs/VOICEPRINT_GUIDE.md`. Must include measurable fingerprint, not only description.

If proposing a new schema or schema change: provide the JSON Schema and a migration note.

If proposing a new agent: declare the agent's job, artifact, schema, dependencies, conflict-resolution rules.

If proposing a kernel change: explain why the existing kernel cannot handle this.

## Alternatives Considered

What other designs were rejected and why.

## Drawbacks

What could go wrong. What this costs.

## Backwards Compatibility

Does this break anything? If yes, what's the migration path?

## Benchmark Requirement

Every RFC must propose at least one benchmark case demonstrating that the addition improves measurable outcomes. The PR cannot merge until the benchmark case passes.

## Documentation Requirement

What docs need to change. List them.

## Open Questions

Things the author isn't sure about and wants community input on.
```

## Decision Rights

- Maintainer (currently Antonio T. Smith Jr.) holds final decision on:
  - Kernel changes
  - The v3.0 Law
  - The Irreversibility laws
  - License terms
  - Public positioning

- Community + maintainer jointly decide:
  - New genre packs
  - New voiceprints
  - New schemas
  - New agents
  - Benchmark cases

## The Spirit

Open source grows by attracting talented contributors. v3.0's governance exists to make contribution welcome and high-quality, not to gatekeep. If you're unsure whether your change needs an RFC, ask in an issue first.

The doctrine that matters most: every contribution must be **applicable, auditable, scored, testable, or explainable**. That is the v3.0 Law. The RFC process exists to keep that law alive.
