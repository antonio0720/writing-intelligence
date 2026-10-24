# Adversarial and operational boundaries

**Threats**: prompt injection in wiki content; scope laundering of a local cultural claim; fabricated kanji pronunciation; version-stale train/festival facts; alias collision; untrusted creative seed entering canon; rights-encumbered reference excerpt; guardian privilege spoof; unrelated AI model rewrite; private chapter leak; cross-world magic rule bleed; copied third-party character design; rival changes in parallel; stale decision; edited archive masquerading as verified result.

**Implemented refusals (limited):** no network modules; `network_policy=offline` contract; no publisher API; source cards with rights flags; source text always treated as data; nonce-style local proposal IDs; CAS on manuscript revisions; immutable content-addressed objects checked on read; permissions on private POSIX files; no implicit archive publisher; no canonical ID migration writes; no canonical graph status; nonmatching source scope detected; no nationwide factual conclusion without explicit basis reference; Ki-Thread logic only when world opts into it.

**Not proven or delivered:** production tenant isolation; signed identities; role delegation/revocation; encryption at rest; adversarial hostile-filesystem race protection; policy-grade content safety; true network sandbox of an LLM, native Japanese language competence, source authenticity, rights review, RAG security, multi-device sync or public runtime integration. Avoid calling the local vault a 'secure SaaS'.

### Failure matrix

| Failure | Signal | Required next action |
|---|---|---|
| `JP_SOURCE_REQUIRED` | cultural assertion has no linked source | research, cite exact site/period; retain uncertainty |
| `JP_UNIVERSAL_SCOPE_UNSUPPORTED` | one source promoted to all Japan | narrow scope or seek genuinely broad evidence |
| `JP_VARIANTS_PRESERVED` | multiple attested forms | keep both with variant provenance, no forced synthesis |
| `JP_READING_UNKNOWN` | ambiguous kanji | ask author or identify qualified reference, no guess |
| `JP_TIMETABLE_NEEDS_CURRENT_SOURCE` | last-train claim lacks source | check operator and event date at publication time |
| `JP_FESTIVAL_SCOPE_MISSING` | event lacks organizer/year | find organizer and current local calendar |
| `JP_SEED_ADOPTION_FORBIDDEN` | seed marked adopted without author decision | revert to proposed until explicitly approved |
| `JP_RESOURCE_OVERSPENT` | fictional resource ledger goes negative | repair event budget or explicitly add a canonical replenishment |
| `JP_ADAPTATION_NOT_CANON` | derivative tries to update source | separate fork and obtain author decision; upstream simulate |
| `ContractError` | incomplete/malicious input | refuse; correct source schema; never silently coerce |

Test oracle: deterministic checks establish *declared structural consistency*. Human source review establishes factual credibility at its chosen time/place. Author authority establishes fictional canon choices. Representative human readers can report what they felt. No one type of evidence substitutes for another.
