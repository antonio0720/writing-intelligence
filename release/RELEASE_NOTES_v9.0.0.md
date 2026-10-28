# Writing Intelligence v9.0.0 — Authentic Voice & Authorship Provenance

**Every tool in this field makes prose sound better. v9 keeps it yours: your experience, your numbers, your positions and your voice survive every edit, and nothing goes out under your name that you did not stand behind.**

Free. Open source. MIT. Forever. Offline, standard-library Python, no account, no model required.

---

## Install

Download all four bundles from this release and install them together; they are one system in four files.

| Bundle | Files | What |
|---|---|---|
| `writing-intelligence.skill` | 197 | The runtime: the skill, the v4–v9 doctrine, schemas, agents and `scripts/wi.py` (`wi --version` → `wi 9.0.0`) |
| `writing-intelligence-craft.skill` | 86 | The craft library: 27 genre packs, voiceprints, anti-slop, the compiler references |
| `writing-intelligence-story.skill` | 184 | The four v8 story engines, unchanged |
| `writing-intelligence-authorship.skill` | 70 | **New in v9.** The authorship, vault, meaning, review, voice, phrase and structure tools, and their tests |

Each bundle has a `.sha256` beside it. From a clone, every tool runs as `python3 scripts/wi.py authorship <tool>`. Step-by-step: [`USER_GUIDE.md`](https://github.com/antonio0720/writing-intelligence/blob/v9.0.0/USER_GUIDE.md#authorship-and-venue-checks-v9) · one page: [`CHEATSHEET.md`](https://github.com/antonio0720/writing-intelligence/blob/v9.0.0/CHEATSHEET.md).

## What v9 adds

Every tool works on the writer's own material, on their own machine. v9 ships no voice samples, no notes and no model, and its private stores refuse to live inside a git repository.

| `wi authorship …` | What it does for you |
|---|---|
| `vault` | Your firsthand material — notes, transcripts, dated drafts, interviews — each labelled (`observed`, `said_by_author`, `measured`, `sourced`, `inferred`, `hypothetical`, `planned`) with consent. Redact or withdraw any time; the bytes are deleted. `check` holds a first-person claim with no source, a plan written up as done, a model-written anecdote, an edited transcript used as a quote. |
| `meaning` | Lists every change a revision makes to what you meant — a changed number or date, a plan described as done, an estimate turned exact, a reversed opinion, a moved or invented cause or outcome, a dropped hedge or concession, an altered quotation, a new first-person sentence — for you to accept or reject. |
| `ledger`, `phrase-review` | Your review decisions, recorded only under your own v6 grant, never overwritten; a typed name alone is not authority. |
| `voice`, `voice-review`, `voice-compare` | Your voice from at least three of your own 500-word samples, including how you argue; a held-out check per measure; drift shown measure by measure. Matching proves nothing about who wrote a text. |
| `audit`, `release` | Declared origin, consent and contributions checked against the venue; every consequential claim anchored to an exact source span; release bound to a person's decision and grant. Sends nothing. |
| `scan`, `structure` | 334 phrase rules and five shape checks, as editorial questions with exact spans; long manuscripts scanned in chunks. |
| `compose` | Your own model, reached only after the venue and evidence checks; the result is a draft for your review, marked `ai_generated`, never a release. |

Also: the craft doctrine no longer asks for sentence-length quotas or detector-oriented edits (`repair_rhythm`); every refusal has a negative-control test and CI disables each guard to prove the suite notices; CI runs on Linux (Python 3.8–3.13), macOS and Windows, where the file-safe tools refuse by name (`PLATFORM_UNSUPPORTED`).

## What 9.0.0 does not claim

- **No benchmark result.** The 60-case blinded editorial benchmark (WI9-07) has not run. No quality score exists.
- **No independent review yet.** WI9-09's review by someone who did not build v9 is open.
- **No real writer's run yet.** The voice tools, vault and meaning diff have been tested on synthetic material only.
- **No authentication.** Nothing here can prove who wrote a passage; declarations stay declarations, and a grant shows who was authorized, not who typed.
- **Lexical, not semantic.** The meaning diff finds where meaning most often moves; it does not understand meaning.
- **Not on Windows.** The private stores and checker refuse there rather than run unsafely.
- **The vault is not encrypted at rest.**
- **AI-detector scores are never a target, a gate or a claim.**

Wave states and receipts: [`plans/v9.manifest.yaml`](https://github.com/antonio0720/writing-intelligence/blob/v9.0.0/plans/v9.manifest.yaml) · [`references/v9/WAVES.yaml`](https://github.com/antonio0720/writing-intelligence/blob/v9.0.0/references/v9/WAVES.yaml) · defects: [`references/v9/defects.md`](https://github.com/antonio0720/writing-intelligence/blob/v9.0.0/references/v9/defects.md).

## Upgrading from v8

Nothing you run changes: every v4–v8 command, exit code and digest is the same, and the story engines ship unchanged. One behaviour to know: a phrase review whose decisions carry only a typed reviewer name now holds `REVIEWER_UNBOUND`; record decisions with `wi authorship ledger record`. Detail: [`UPGRADE_README.md`](https://github.com/antonio0720/writing-intelligence/blob/v9.0.0/UPGRADE_README.md).

— Antonio T. Smith Jr., Density6 LLC
