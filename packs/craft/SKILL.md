---
name: writing-intelligence-craft
description: The craft library for Writing Intelligence — 27 genre packs (grant and NOFO, policy brief, journalism, medical, legal, investor memo, technical doc, book, resume, sermon, speech, newsletter, social, fiction, screenplay and more), the measurable voiceprint system, the anti-slop diagnostic set, the positive-pattern corpus, the diagnostic scan library, the full 11-pass compiler reference and v8's novel-architecture, rule-integrity, reader-experience and arc-ending references. Load this alongside writing-intelligence whenever the task is to write, rewrite, edit, ghostwrite, redline or restructure prose in a specific genre or a specific person's voice, or whenever a draft needs diagnosing for machine-writing patterns, hedging, abstraction drift, cadence flatness or structural collapse. Trigger when unnamed — 'make this sound like me', 'this reads like AI wrote it', 'tighten this up', 'what genre conventions am I breaking', 'why is this boring'.
---

# Writing Intelligence — The Craft Library

**Author:** Antonio T. Smith Jr. — Founder & CEO, Density6 LLC
**License:** MIT
**Version:** 8.0.0
**Companion to:** `writing-intelligence` — the Sovereign Meaning Runtime

---

## What this is, and why it ships separately

This bundle is the craft corpus of Writing Intelligence — the reference material the eleven passes consult while the writing is actually being built. Genre conventions. Measured voiceprints. The anti-pattern diagnostics that flag templated, empty or generic prose for an editor's judgment — a phrase match never proves who or what wrote a passage. The positive-pattern corpus that shows what good looks like instead of only naming what bad looks like. The diagnostic scan library. The compiler references for every pass.

It ships as its own installable bundle for one reason, and the reason is arithmetic rather than taste: **a skill bundle may contain at most 200 files.** A bundle that exceeds the ceiling does not degrade and does not warn — it simply does not load, which would turn every install instruction in the repository into a false claim. The runtime and the library together are 229 files. Split, they are 150 and 79, and both have room to grow.

Install all three — `writing-intelligence` (the runtime), this library, and `writing-intelligence-story` (the v8 story engines). They are one system in three artifacts.

---

## How to use it

The governing skill is `writing-intelligence`. It holds the eighteen laws, the eleven passes, the twelve engines, the workflow and the deterministic verifier. **Read it first.** This bundle is what that skill reaches into.

| When you are | Read |
|---|---|
| Writing in a specific genre | `references/genre_packs/` — pick the pack, honor its arena, its objection set and its structural contract |
| Writing in someone's voice | `references/voiceprints/` — a voiceprint is measured from real text, never guessed from adjectives |
| Diagnosing a flat or machine-sounding draft | `references/anti_patterns/` then `references/positive_patterns/` |
| Running Pass 3 — the diagnostic scan | `references/diagnostics/` |
| Executing or extending any of the eleven passes | `references/compiler/` |
| Grounding a claim about writing research | `references/academic/` |
| Building a novel, thriller, series or ending (v8) | `references/compiler/novel_architecture.md`, `fiction_rule_integrity.md`, `reader_experience.md`, `arc_ending_projection.md`, then the engines in `writing-intelligence-story` |

---

## The rules that travel with this library

These are the craft rules. They are not softened by being in the smaller bundle.

1. **A voiceprint is measured, not described.** Feed it real text by the person — consented, human-authored samples (v9: 3+ samples of 500+ words each, per genre, reviewed by the author). Adjectives like "warm but authoritative" are a starting brief, never a voiceprint. Measured features, author-declared preferences and model-judged resemblance are three different things and must never be blended into one score.
2. **Anti-slop is a craft objective, not a laundering service.** The goal is prose that does not pattern-match to machine writing *because it is genuinely better built*. This library will never be used to help a document evade a detector. A phrase match is an editorial question, never proof of who or what wrote a passage. (v9 preview: cadence is repaired because the thought changes shape — `repair_rhythm` — never to move a detector number; no length quotas, synonym swaps or planted typos.)
3. **A genre pack is a contract with a reader, not a template.** It names the arena, the reader's likely objection, the structural obligations and the failure modes. Filling in a shape without meeting the obligations produces a document that looks right and does nothing.
4. **A diagnostic reports, it does not rewrite.** Every finding names the span, the pattern and the repair. The author decides. This is Law A, and it applies here exactly as it applies in the runtime.
5. **There is no universal writing number.** Every score in this library is relative to a stated profile, arena and mission, and the profile is always printed beside the number.

---

## v9 preview — authorship and venue rules (proposed, not released)

8.0.0 is the release; v9 is a preview on PR #8 and has not run its benchmark. When a craft task touches who wrote something or what the author lived: use only the author's supplied material for first-person scenes (never invent one; hypotheticals stay labeled); for a **human-only** venue give research briefs and interview prompts, not a ghostwritten submission; treat voice resemblance as style, never as authorship. The checkers (`scripts/wi-authorship.py`, `prototypes/wi9/`) live in the repository's runtime, not in this bundle — see `references/v9/README.md` there. They check declarations and flag editorial questions; they do not authenticate a writer.

---

## What is in here

| Directory | Files | Holds |
|---|---|---|
| `references/genre_packs/` | 29 | One pack per genre — arena, objections, structure, failure modes — plus the two v8 fiction addenda |
| `references/compiler/` | 23 | Pass-by-pass execution references for the 11-pass kernel, plus v8's novel architecture, fiction rule integrity, reader experience and arc-ending projection |
| `references/voiceprints/` | 10 | The measurable voiceprint system and worked profiles |
| `references/anti_patterns/` | 7 | Editorial diagnostics for templated phrasing, hedging and abstraction drift (never an authorship verdict) |
| `references/positive_patterns/` | 6 | What good construction looks like, with worked examples |
| `references/diagnostics/` | 7 | The Pass 3 diagnostic scan library, plus v8's fiction quality separation |
| `references/academic/` | 2 | Grounding literature for claims about writing |

---

## What this bundle does not contain

No verifier. No schemas. No doctrine on evidence, authority, time or proof. None of the eighteen laws in full. Those live in `writing-intelligence`, and this bundle is not a substitute for it — a craft library with no accountability layer is exactly the thing this project was built to replace.

If you have only this half installed, say so rather than improvising the governance.

---

*Writing Intelligence — Antonio T. Smith Jr., Density6 LLC. MIT licensed.*
