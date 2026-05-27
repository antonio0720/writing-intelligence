# Release Checklist — Writing Intelligence

Every release follows this checklist. A release that does not complete every checkmark does not ship.

## Pre-Release

- [ ] **CHANGELOG.md** updated with all changes since last release
- [ ] **ROADMAP.md** reconciled (no items shown as future that have shipped; no items shown as shipped that haven't)
- [ ] **README.md** version metadata current
- [ ] **SKILL.md** version current
- [ ] **VERSIONING.md** rules followed (semver: major.minor.patch)

## Benchmark Gate

- [ ] Full benchmark suite run against the prior release
- [ ] Score improvement gate met: **≥ 70% of cases improve by ≥ 5 points**
- [ ] No-regression gate met: **no case drops more than 3 points** without documented reason
- [ ] Evidence safety gate met: **100% fabrication-trap recall**
- [ ] Voice preservation gate met: **≥ 80% drift-direction recall**
- [ ] Output packaging gate met: **every benchmark produces valid delivery bundle**

## Documentation Gate

- [ ] README accurately describes all visible features
- [ ] USER_GUIDE updated with new prompts
- [ ] CHEATSHEET updated with new operators / passes
- [ ] CONTRIBUTING aligned with current RFC process
- [ ] Migration guide present (if breaking changes)
- [ ] API_SPEC and MCP_SPEC current (for v3.1+)

## Schema Gate

- [ ] Every pass produces an artifact validating against its schema
- [ ] Schema version stamps current
- [ ] Backwards compatibility verified (or breaking-change major version bump)

## Skill Bundle

- [ ] `writing-intelligence.skill` regenerated from current source tree
- [ ] Bundle installable in Claude.ai (verified manually)
- [ ] Bundle installable in Claude Code (verified manually)

## Release Artifacts

- [ ] Git tag created (`v3.0.0`, signed if maintainer has signing key)
- [ ] GitHub Release created with:
  - Release title and version
  - Comprehensive release notes (from CHANGELOG + announcement)
  - Downloadable assets:
    - `writing-intelligence-v3.0.0.skill` (skill bundle)
    - `writing-intelligence-v3.0.0-source.zip` (full source)
    - `writing-intelligence-v3.0.0-schemas.zip` (schemas only)
  - Migration notes (if breaking)
- [ ] Release announcement drafted (Adam's Sales Process voice, attribution to Antonio T. Smith Jr.)

## Public Verification (per Antonio's Chrome MCP gate)

- [ ] Repo About description updated
- [ ] Repo topics updated
- [ ] README renders correctly on GitHub.com
- [ ] Release page renders correctly
- [ ] Asset downloads work end-to-end
- [ ] Console clean (no errors)
- [ ] Network requests fire correctly
- [ ] Screenshots saved to `verification-screenshots/wave-NN/`

## Post-Release

- [ ] Announcement posted to relevant channels
- [ ] Roadmap updated for next release
- [ ] Open RFCs tagged with disposition (deferred / in-flight / merged)
- [ ] Benchmark report published to `benchmarks/reports/`

## Author Sign-Off

**Antonio T. Smith Jr.** — final release authorization holder for v3.x.
