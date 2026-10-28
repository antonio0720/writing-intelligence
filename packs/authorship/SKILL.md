---
name: writing-intelligence-authorship
description: Writing Intelligence v9 preview (not released) — authorship, sources and venue rules for writing under a person's name. An authorship-claim declaration checker (wi-authorship.py audit and release) ties every consequential claim in a draft to an exact span of the author's own sources, pins the reviewed bytes, refuses submission-ready AI prose for human-only venues, and reads release authority from the v6 grant store. Also a 334-rule editorial phrase scanner whose matches are questions for the author, and a review ledger bound to exact digests. Load alongside writing-intelligence when a piece will be submitted, pitched or published under a person's name, when a venue restricts AI help, or when first-person experience must be sourced. It never certifies who wrote anything, never targets an AI-detector score, and never sends. Trigger when unnamed — 'can I send this pitch', 'is AI help allowed here', 'check my sources'.
---

# Writing Intelligence — Authorship (v9 preview)

**Project owner:** Antonio T. Smith Jr. — Density6 LLC. **Status:** proposed on PR #8, not released; 8.0.0 is the release. Wave states: `references/v9/WAVES.yaml`.

This bundle carries the v9 preview tools. It ships separately for the reason the story bundle does: a skill bundle may hold at most 200 files, the runtime had six files of headroom, and these tools are about twenty. Install it alongside `writing-intelligence`, `writing-intelligence-craft` and `writing-intelligence-story`.

## What it is for

A person's name is about to go on writing: a pitch, an expert comment, an essay, an application, a letter. Before it goes, the questions that matter are not "does it sound human" but: did this person supply what the draft claims they did; does every factual claim rest on a source span; is this the exact text that was reviewed; does the venue allow the help that was used; and did a person with authority decide to send it.

## The rules

1. **Source before style.** Use the author's own notes, transcripts and drafts. Never write an "I did / I saw" scene the author did not supply. A hypothetical stays labeled hypothetical; a roadmap is not a completed build.
2. **Venue contract first.** Read the venue's written rule before drafting. For a **human-only** venue, produce a research brief and interview prompts only — never an AI-written or AI-rewritten pitch, reply or essay for submission. Unknown policy means HOLD.
3. **Evidence by anchor.** Run `python3 scripts/wi-authorship.py audit --input dossier.json`. `REVIEW` (exit 0) means the limited checks passed and is **not** permission to send; `HOLD` (exit 3) names what is missing. Every consequential claim the v4 classifier finds must overlap an anchored span.
4. **Release is a person's decision.** `python3 scripts/wi-authorship.py release --input dossier.json --authority-store STORE` returns `RELEASE_ELIGIBLE` only when a person's decision is bound to the exact draft digest and the v6 grant store (`python3 scripts/wi.py authority`) shows that person holds `release.approve` for this venue, at decision time and now. It sends nothing.
5. **Phrase findings are questions.** `python3 prototypes/wi9/wi9_hotphrases.py scan --input FILE --format text` flags editorial questions; the author decides each one in the review ledger (`prototypes/wi9/wi9_phrase_review.py`). A match is never proof of AI authorship and never triggers a rewrite.
6. **Detector humility.** Never optimize toward an AI-detector score, quote one as an authorship fraction, or promise one.

Every report says `declaration_status: self_reported`. Nothing here can authenticate a writer.

## Files

| Path | What |
|---|---|
| `scripts/wi-authorship.py` | `audit` and `release` |
| `scripts/wi.py` | the canonical v8 runtime; supplies the v4 claim classifier and the v6 grant store |
| `schemas/v9/authorship-dossier.schema.json` | the dossier contract (`wi9-authorship-2`) |
| `prototypes/wi9/` | reference kernel: phrase scanner and 334 rules, review ledger, composition contract, voice and benchmark tools |
| `references/v9/` | README, defects, waves, editorial protocol, quality benchmark, engineering handoff |
| `examples/v9/` | synthetic worked examples with real command output |
| `tests/v9/`, `scripts/test-v9.sh` | the v9 regression; run `bash scripts/test-v9.sh` |

## What it does not do

Authenticate a writer · prove a source true or that a paraphrase is entailed · measure writing quality (the 60-case editorial benchmark, WI9-07, has not run) · build a voiceprint without consented samples · run on non-POSIX systems · send, submit or publish.
