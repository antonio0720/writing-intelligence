---
name: writing-intelligence-story
description: Story Intelligence for Writing Intelligence v8 — four offline fiction engines carrying 340 numbered requirements. Fiction and thriller audit (tension, rule integrity, power limits and cost, promise debt). Arc, want/need and ending intelligence (two-clock character state, the sweet, semi-sweet, bittersweet and bitter ending algebra, arc kept separate from ending). The craft of openings, fights, opposition, suspense and sequences. A Japan Story OS for culturally careful worlds, folklore variants, names and a private author vault. Each engine is stdlib Python, read-only and deterministic, and never certifies a good novel; publication gates HOLD until an editor and real readers have spoken. Load alongside writing-intelligence for novels, thrillers, mysteries, fantasy, manga, screenplays and series. Trigger when unnamed — 'does my ending land', 'is the villain too smart', 'why is this scene flat', 'does this magic cost enough', 'is this accurate to Japan'.
---

# Writing Intelligence v8 — Story Intelligence

**Author:** Antonio T. Smith Jr. — Founder & CEO, Density6 LLC
**License:** MIT
**Version:** 8.0.0
**Companion to:** `writing-intelligence` (the Sovereign Meaning Runtime) and `writing-intelligence-craft` (the craft library)

---

## What this is

v8 brings the fiction half of Writing Intelligence up to the standard v4–v7 built for evidence. Four engines, each built and tested on its own, folded into one release:

| Engine | Requirements | Run it | Read first |
|---|---|---|---|
| **Fiction & Thriller Intelligence** | FI-01–FI-60 (B001–B060) | `python3 scripts/wi-fiction.py` | `references/v8/FICTION_INTELLIGENCE_CONSTITUTION.md` |
| **Arc, Want/Need & Ending Intelligence** | N061–N120 | `python3 scripts/wi-arc.py` | `references/v8/ARC_ENDING_CONSTITUTION.md`, `ENDING_ALGEBRA.md` |
| **The Craft** — openings, action, opposition, suspense, sequences | C121–C180 | `python3 extensions/wi8/craft03/scripts/wi-craft.py` | `extensions/wi8/craft03/references/v8/CRAFT03_CONSTITUTION.md` |
| **Japan Story OS** | JP-181–JP-340 | `python3 extensions/wi8/japan04/cli/wi8_japan.py` | `extensions/wi8/japan04/README.md` |

340 numbered requirements. Each has a stable ID, a canonical owner, an acceptance condition and an honest implementation state — many are editorial judgments that no code may claim to settle, and the registers say which.

## The v8 rule

**A structural pass is not a good novel.** Four states are kept apart and never coerced into one another:

1. **Mechanical consistency** — typed references resolve, events do not cause themselves, a power is used inside its stated limits and pays its stated cost, a fight's resources add up. Code can prove this.
2. **Interpretive signal** — a claimed change with no witnessed choice, a clue nobody could have found, a promise with no payoff. Code can *raise* this; a person decides.
3. **Editorial judgment** — whether the scene works. A human editor decides, and the decision is recorded as theirs.
4. **Reader reception** — whether readers were satisfied, frightened, moved. Only an independent reader study answers it.

So every publication gate here holds by design: **HOLD (exit 3)** for fiction, arc and craft; the Japan Story OS preflight refuses with exit 2, because a preflight is never an authorization. A need is an interpretation attributed to a named person, never a model's access to a character's inner truth. A cultural fact needs a source scoped by place, period and institution; a fictional canon needs the author's adoption; missing information stays missing.

## Quick start

From this bundle's root (Python 3.8+, no dependencies, no network):

```bash
bash scripts/test-v8.sh                                     # all four suites + cross-engine twins
python3 scripts/wi-fiction.py audit --input story.json      # fiction & thriller audit
python3 scripts/wi-fiction.py text-signals --text chapter.txt
python3 scripts/wi-fiction.py explain-rule FI-25
python3 scripts/wi-arc.py classify --want attained --need unfulfilled   # bittersweet
python3 scripts/wi-arc.py evaluate --input arc.json
python3 scripts/wi-arc.py as-of --input arc.json --event ev-2 --known-at 2026-10-24T13:00:00-05:00
python3 extensions/wi8/craft03/scripts/wi-craft.py evaluate --input scene.json
python3 extensions/wi8/japan04/cli/wi8_japan.py check project.json
python3 extensions/wi8/japan04/cli/wi8_japan.py studio questions-only draft.txt
```

Exit codes, all four engines: `0` analysis ran or mechanical-only pass · `2` malformed input or structural block · `3` editorial or publication hold. Output is deterministic JSON; input is never overwritten; inputs are capped at 8 MiB.

## How to use it in a conversation

- **Ask before you prescribe.** The author owns the story. Diagnose with questions and named findings; propose, never silently replace (Law A).
- **Project, then evaluate.** These engines read a typed JSON projection of the story (characters, events, wants and needs, powers, scenes), not raw prose. Build the projection with the author, mark its `origin` honestly (`draft_projection` for author annotations), and never present a fixture or a guess as canon.
- **Report the state, not a score.** Say *mechanical defect*, *signal for review*, *needs the author's call* or *needs readers* — never "this novel is good".
- **Respect the genre.** A flat protagonist, an open ending, a quiet climax and a story with no Japanese folklore at all are valid inputs, not failures.
- **For Japan-set work**, separate `external_fact` (needs a scoped source), `fictional_canon` (needs the author's adoption) and `interpretation` (cannot be machine-certified). Do not infer a unique reading of a name from its kanji. Ainu, Ryukyuan and living religious traditions need the right kind of source before publication.

## What does not run

Extraction of every scene from a full manuscript, canonical `wi.py` and v6 graph integration, model-based literary judgment, reader recruitment, cultural authenticity adjudication, Japanese morphological parsing, EPUB or print proofs, publishing. These are specified and planned — waves FI8-03–06 and WI8-00–WI8-43 in the runtime's `plans/v8.manifest.yaml` — and are never presented as working.

## Map

```
scripts/wi-fiction.py, scripts/fiction_v8/      Fiction & Thriller engine
scripts/wi-arc.py, scripts/arc_v8/              Arc, Want/Need & Ending engine
scripts/test-v8.sh                              v8 integration check
references/v8/                                  Constitutions, ending algebra, arc state machine, editorial judgment, crosswalk
rules/                                          FI and N requirement registers
schemas/v8/                                     JSON Schema 2020-12 for projections, findings, gates, reports
policies/fiction_profiles.json                  Genre and stage profiles
extensions/wi8/craft03/                         The Craft — C121–C180
extensions/wi8/japan04/                         Japan Story OS — JP-181–JP-340
tests/v8, tests/v8_arc                          Suites with negative controls
```
