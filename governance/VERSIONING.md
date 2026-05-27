# Versioning — Writing Intelligence

Writing Intelligence follows [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH).

## MAJOR

Bump MAJOR when a release breaks backwards compatibility:

- Kernel changes that invalidate prior intake contracts
- Schema changes that break existing artifact consumers
- Removal of public-facing APIs, rewrite operators, or output modes
- Changes to the v3.0 Law or Irreversibility laws
- License changes

A MAJOR bump requires:

- A formal migration guide (e.g., `docs/MIGRATION_v3_to_v4.md`)
- An RFC explaining the break and its necessity
- Maintainer (Antonio T. Smith Jr.) sign-off

## MINOR

Bump MINOR when a release adds capability backwards-compatibly:

- New genre packs
- New voiceprints
- New rewrite operators
- New scoring rubrics
- New agents
- New output modes
- New domain pack categories

A MINOR bump requires:

- Benchmark cases for the new capability
- Documentation updates
- No breaking changes to existing schemas

## PATCH

Bump PATCH when a release fixes bugs or polish without adding capability:

- Documentation fixes
- Typo corrections
- Anti-pattern library updates
- Benchmark case additions inside existing categories
- Performance improvements
- Internal refactors with no API change

## Pre-Release

Use suffixes for pre-release versions:

- `3.1.0-alpha.1` — alpha, expect breakage
- `3.1.0-beta.1` — beta, mostly stable
- `3.1.0-rc.1` — release candidate

## Skill Bundle Version Alignment

`writing-intelligence.skill` is versioned alongside the repository:

- `writing-intelligence-3.0.0.skill`
- `writing-intelligence-3.0.1.skill`
- etc.

The bundle's internal `SKILL.md` carries the same version stamp.

## Schema Versioning

Every schema declares `version: "3.x.y"`. Schema consumers MUST check version compatibility:

- Same MAJOR.MINOR → fully compatible
- Same MAJOR, different MINOR → backwards-compatible; consumer may need to ignore unknown fields
- Different MAJOR → incompatible; consumer must update or use a migration adapter

## Release Cadence

There is no fixed cadence. Releases ship when:

1. A meaningful capability is ready
2. The release passes every gate in `governance/RELEASE_CHECKLIST.md`
3. The maintainer signs off

Targets in `ROADMAP.md` are aspirational, not contractual.

## Deprecation Policy

Capabilities marked deprecated in MINOR releases must be preserved for at least one full MINOR cycle before removal in the next MAJOR. Deprecation notices appear in `CHANGELOG.md` and in the relevant doctrine files.
