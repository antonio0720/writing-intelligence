---
name: Bug Report — Output Is Generic, Wrong-Voiced or Lost Meaning
about: The compiler produced generic or templated output, lost meaning, invented a fact, or doesn't match the expected voice
title: "[BUG] "
labels: bug
assignees: ''
---

## What happened?
Describe what you asked the compiler to do and what went wrong.

## Input text (or prompt used)
Paste the text you gave the compiler, or the prompt you used.

## Output received
Paste what the compiler produced.

## What's wrong with the output?
Be specific:
- [ ] Generic or templated prose (describe which part)
- [ ] Added a fact, number, scene or quote no source supplied
- [ ] Wrong voice (expected X, got Y)
- [ ] Lost the argument or meaning during rewrite
- [ ] Hard-ban phrase survived in output
- [ ] Cadence pattern still present
- [ ] Other: ___

## Expected behavior
What should the output have looked like or sounded like?

## v9 only (skip for v4–v8 behavior)
If the problem involves v9 (`scripts/wi-authorship.py` or `prototypes/wi9/`):
- Subcommand and exit code: `audit` / `release` / other — exit 0 or 3?
- HOLD code(s) in `findings[].code` (e.g. `CLAIM_UNANCHORED`, `HUMAN_ONLY_CONFLICT`), or the REVIEW / RELEASE_ELIGIBLE you did not expect:
- Dossier schema version: `wi9-authorship-1` or `wi9-authorship-2`
- Commit or PR head you ran:
- Attach the dossier only if it holds no private material; redact otherwise. Do not paste sources you do not have consent to share.

Reminder: every v9 report is a declaration check (`declaration_status: self_reported`); a bug is the checker disagreeing with its own documented rules, not that it failed to prove who wrote a text.

## Environment
- Platform: Claude.ai / Claude Code / Claude Projects / Other LLM
- Voiceprint used: (if any)
- Genre pack used: (if any)

## Score (if available)
If you scored the output against the editorial rubric, which categories were weakest? Detector scores are not a bug-report criterion.
