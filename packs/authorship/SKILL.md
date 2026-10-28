---
name: writing-intelligence-authorship
description: Writing Intelligence v9 preview (not released) — authorship, sources, meaning and venue rules for writing under a person's name. Ties every consequential claim to an exact span of the writer's own sources and checks first-person claims against their private firsthand vault; lists every change a revision makes to what they meant (numbers, dates, plans called done, reversed opinions) for them to accept or reject under their own grant; measures their own voice from their own samples; asks editorial questions about phrases and shape; refuses AI prose for human-only venues; reads release authority from the v6 grant store. Load alongside writing-intelligence when a piece goes out under a person's name, a venue restricts AI help, or first-person experience must be sourced. It never certifies who wrote anything, never targets an AI-detector score, and never sends. Trigger when unnamed — 'can I send this pitch', 'did the edit change what I said', 'check my sources'.
---

# Writing Intelligence — Authorship (v9 preview)

**Project owner:** Antonio T. Smith Jr. — Density6 LLC. **Status:** proposed on PR #8, not released; 8.0.0 is the release. Wave states: `references/v9/WAVES.yaml`.

This bundle carries the v9 preview tools. It ships separately for the reason the story bundle does: a skill bundle may hold at most 200 files and the runtime had six files of headroom. Every tool runs on the writer's own material on their own machine; the bundle carries no voice samples, notes or model. Install it alongside `writing-intelligence`, `writing-intelligence-craft` and `writing-intelligence-story`.

## What it is for

A person's name is about to go on writing: a pitch, an expert comment, an essay, an application, a letter. Before it goes, the questions that matter are not "does it sound human" but: did this person supply what the draft claims they did; does every factual claim rest on a source span; is this the exact text that was reviewed; does the venue allow the help that was used; and did a person with authority decide to send it.

## The rules

1. **Source before style.** Use the author's own notes, transcripts and drafts. Never write an "I did / I saw" scene the author did not supply. A hypothetical stays labeled hypothetical; a roadmap is not a completed build.
2. **Venue contract first.** Read the venue's written rule before drafting. For a **human-only** venue, produce a research brief and interview prompts only — never an AI-written or AI-rewritten pitch, reply or essay for submission. Unknown policy means HOLD.
3. **Evidence by anchor.** Run `python3 scripts/wi-authorship.py audit --input dossier.json`. `REVIEW` (exit 0) means the limited checks passed and is **not** permission to send; `HOLD` (exit 3) names what is missing. Every consequential claim the v4 classifier finds must overlap an anchored span.
4. **Release is a person's decision.** `python3 scripts/wi-authorship.py release --input dossier.json --authority-store STORE` returns `RELEASE_ELIGIBLE` only when a person's decision is bound to the exact draft digest and the v6 grant store (`python3 scripts/wi.py authority`) shows that person holds `release.approve` for this venue, at decision time and now. It sends nothing.
5. **First-person material comes from the writer's vault.** `wi authorship vault check --root <their vault> --claims claims.json` holds any first-person claim with no anchored item, a plan written up as done, a model-written anecdote, or an edited transcript used as a quote. Never fill the gap yourself; ask the writer.
6. **Meaning stays theirs.** After any revision run `wi authorship meaning diff --original <theirs> --candidate <revised>` and put every delta in front of the writer. `meaning review` reaches REVIEW only when they accepted each one in their ledger under a grant that covers it.
7. **Phrase and shape findings are questions.** `wi authorship scan` and `wi authorship structure` flag editorial questions; the writer decides each one in their grant-bound ledger (`wi authorship ledger`, `phrase-review`). A match is never proof of AI authorship and never triggers a rewrite.
8. **Their voice, their samples.** `wi authorship voice`, `voice-review` and `voice-compare` work only on the writer's own samples in their own folder. Matching a baseline proves nothing about who wrote a text.
9. **A model only after the gates.** `wi authorship compose` reaches the writer's own model program only after venue and evidence checks; the best result is a draft for their review, `ai_generated`, never release.
10. **Detector humility.** Never optimize toward an AI-detector score, quote one as an authorship fraction, or promise one.

Every report says `declaration_status: self_reported`. Nothing here can authenticate a writer.

## Files

| Path | What |
|---|---|
| `scripts/wi-authorship.py` | `audit` and `release` |
| `scripts/wi.py` | the canonical v8 runtime; supplies the v4 claim classifier and the v6 grant store |
| `schemas/v9/authorship-dossier.schema.json` | the dossier contract (`wi9-authorship-2`) |
| `prototypes/wi9/` | firsthand vault, meaning diff, grant-bound review ledger, voice measures, structure checks, chunked phrase scanner (334 rules), composition contract and model connector, benchmark aggregator |
| `references/v9/` | README, defects, waves, editorial protocol, quality benchmark, engineering handoff |
| `examples/v9/` | synthetic worked examples with real command output |
| `tests/v9/`, `scripts/test-v9.sh` | the v9 regression; run `bash scripts/test-v9.sh` |

## What it does not do

Authenticate a writer · prove a source true or that a paraphrase is entailed · understand meaning (the diff is lexical) · measure writing quality (the 60-case editorial benchmark, WI9-07, has not run) · ship or use anybody else's voice samples · run on non-POSIX systems (it refuses with `PLATFORM_UNSUPPORTED`) · send, submit or publish.
