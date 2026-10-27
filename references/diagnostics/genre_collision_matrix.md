# Genre Collision Matrix

**Used by**: Genre Stack Engine (`references/compiler/genre_stack_engine.md`)

This matrix declares what wins when two genre packs disagree on a dimension. The Genre Marshal consults this matrix during stack resolution. Any conflict not covered here surfaces for user resolution.

---

## Evidence Discipline

| Pair | Winner |
|---|---|
| academic + sales | academic |
| grant_nofo + sermon | grant_nofo |
| medical_writing + any | medical_writing |
| legal_positioning + any | legal_positioning |
| government_brief + any non-legal | government_brief |
| journalism + fiction | journalism |
| patent_claims + any | patent_claims |

## Cadence

| Pair | Winner |
|---|---|
| sermon + grant_nofo | grant_nofo for body, sermon for opening/closing |
| dialogue + cinematic_narration | dialogue inside exchanges, cinematic between |
| social_media + newsletter | social_media (platform constraints win) |
| speech + email | speech if oral; email if written |
| sermon + church_leadership | sermon |

## Compression

| Pair | Winner |
|---|---|
| social_media + any | social_media (platform char limit wins) |
| pitch_slide + any | pitch_slide (slide constraint wins) |
| email + newsletter | email (when reply-fast required) |
| sop + procedural | sop |

## Warmth

| Pair | Winner |
|---|---|
| sermon + government_brief | sermon for opening/closing, government_brief mid |
| church_leadership + sales | church_leadership (mission identity over conversion mechanics) |
| journalism + academic | academic (warmer language flagged as bias) |
| small_business_operator + corporate | small_business_operator (kitchen-table register wins) |
| loan_officer + sales | loan_officer (trust over conversion) |

## Persuasion

| Pair | Winner |
|---|---|
| sales + grant_nofo | grant_nofo (compliance over conversion) |
| pitch_deck + investor_precision | investor_precision (over-persuasion damages trust) |
| sermon + sales | sermon (call > close) |
| real_estate + sales | real_estate (specific instance > generic close) |

## Compliance

| Pair | Winner |
|---|---|
| Any + medical_writing | medical_writing |
| Any + legal_positioning | legal_positioning |
| Any + patent_claims | patent_claims |
| Any + government_brief | government_brief |
| Any + grant_nofo | grant_nofo (when funder requirements active) |
| Any + loan_officer | loan_officer (when disclosures active) |

## Formality

| Pair | Winner |
|---|---|
| government_brief + casual_sharp voice | government_brief |
| academic_rigorous + youtube_script | youtube_script (medium overrides) |
| sermon + business_strategy | sermon (per pulpit register) |
| linkedin_post + casual | casual but professionally framed |

## Narrative Distance

| Pair | Winner |
|---|---|
| fiction + journalism | journalism in nut graf, fiction in scene |
| thriller_scene_architecture + cinematic_narration | thriller for confined space, cinematic between |
| chapter + memo | chapter (when narrative is primary) |
| transmedia_character + fiction | transmedia for cross-format, fiction for canonical |

---

## High-Stakes Override

In any conflict, if one pack carries a high-stakes compliance rule (medical, legal, government, grant, financial), that rule wins regardless of the matrix above. The Genre Marshal logs this in `collision_resolutions` with `rationale: "high-stakes compliance override"`.

---

## User Sovereignty Override

The user's explicit instruction always wins. If the user says "write this grant proposal in the warmth of a sermon, not the dryness of a government brief," the matrix yields. The Genre Marshal logs the override.

---

## Extension Rule

New genre packs added to the repository must declare their position on each dimension and propose a row to this matrix when they enter the collision space. PRs that add a pack without updating this matrix will be rejected.

---

## v9: Collisions in Claim Coverage and Venue Contract

Two v9 facts interact with this matrix. Neither changes a row.

**1. The strict-evidence winners also set the claim-coverage burden.** The dossier schema names four strict arenas: `journalism`, `academic`, `legal` and `government`. Where a row above makes `academic`, `journalism`, `legal_positioning` or `government_brief` the evidence-discipline winner, the dossier's `arena` should be declared accordingly. Other evidence winners (`medical_writing`, `patent_claims`, `grant_nofo`) are not named strict arenas in the checker; declare the nearest arena and treat the rest as an editorial obligation. Every consequential claim must overlap an anchored evidence span, and evidence whose `support_status` is `needs_source` or `conflicted` blocks a submission. A collision resolved in favour of a warmer or more persuasive pack (for example `sales` over `academic`) does not relax that burden; the user-sovereignty override changes tone, not the need for a source.

**2. The venue contract outranks the whole matrix for assistance.** Which pack wins is a style question. Whether an AI system may write or rewrite the text at all is decided first by the venue (principle WI9-G). If the venue is human-only, the stack may produce a research brief but not the submission copy, whatever pack won. The matrix is not consulted to override that.

Other notes:

- A collision resolved by "high-stakes compliance override" is logged in `collision_resolutions` with a rationale. That log is the trace for principle WI9-I; it is not a record of authorship.
- The matrix says nothing about voice. Voiceprint similarity (see `references/voiceprints/`) is a diagnostic and never settles a collision.
- Fiction rows (`fiction + journalism`, `thriller_scene_architecture + cinematic_narration`) are unchanged by v9. Fiction quality gates are not touched; see `fiction_quality_separation.md`.
- Nothing here has been run against the unexecuted 60-case editorial benchmark (WI9-07). These rows are craft doctrine, not measured outcomes.
