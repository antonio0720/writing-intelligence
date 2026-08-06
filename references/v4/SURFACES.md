# Surfaces

The doctrine is identical everywhere. What changes is what you can actually do — whether there is a filesystem, whether scripts can run, whether work persists. Match the output to the surface or the author gets a response shaped for a machine they are not using.

Detect the surface from the tools available, not by asking.

---

## Chat (claude.ai, mobile, no filesystem)

**Available:** conversation only. Text in, text out. Files may be attached but not written.

**Behavior:**

- Do the whole protocol; deliver it inline and compressed. No file paths, no "I've saved it to."
- Keep the original recoverable by keeping it quotable — do not paraphrase the author's input when reflecting it back.
- Deterministic checks are done by reading carefully rather than by script. Say which you did.
- Long documents: work in sections and say which section you are on. Do not silently truncate a 40-page analysis to the first ten claims — say "claims 1–12 of an estimated 40; continue?"
- Default to inline response. Reach for an artifact only when the deliverable is a standalone document the author will take elsewhere.

**Compression discipline:** the full proof table for a 60-claim document does not belong in a chat message. Lead with the verdict and the blocking items; offer the full table on request.

---

## Cowork (filesystem, agentic, multi-step)

**Available:** files, scripts, multi-step work, persistence across a session.

**Behavior:**

- **Preserve the original before touching anything.** `cp draft.md draft.original.md`, or `scripts/wi.py preserve draft.md`. This is Law B and it is not optional; on a filesystem there is no excuse for a lost original.
- **Never edit the author's file in place** unless they explicitly asked for in-place editing. Write proposals to a separate file. Let them apply.
- Run `scripts/wi.py` for the deterministic checks rather than eyeballing them. It does not get tired on page 40 and its output is reproducible next week.
- Produce the artifact set:
  ```
  draft.original.md          untouched input
  draft.proposals.md         redline: before/after/why/effect/basis
  draft.claims.json          claim ledger with statuses and spans
  draft.gate.md              verdict, reasons, repairs
  ```
- For long documents, checkpoint. Write partial results as you go rather than holding a 40-page analysis in flight and losing it to a timeout.

---

## Claude Code (repository, git, execution)

**Available:** everything Cowork has, plus version control and CI.

**Behavior:**

- **Git is the immutability mechanism.** Commit the original before editing — that satisfies Law B better than a `.original` copy, and the author already trusts it. Check `git status` first; if the working tree is dirty, say so before adding to the mess.
- Run the scripts. In a repo, prefer wiring them into the workflow over running them ad hoc:
  ```bash
  python scripts/wi.py scan-sources sources/           # injection + hidden text
  python scripts/wi.py extract-claims draft.md         # claim ledger
  python scripts/wi.py verify draft.claims.json sources/   # span lock + numeric + date
  python scripts/wi.py gate draft.claims.json --mode strict
  ```
- **Offer the pre-commit hook** when the repository contains consequential prose — grant narratives, policy documents, compliance text, published documentation. Blocking a commit that contains a fabricated citation is worth more than any amount of doctrine:
  ```bash
  python scripts/wi.py gate draft.claims.json --mode strict --exit-code
  ```
  Exits non-zero on BLOCK. Wire into `.git/hooks/pre-commit` or CI.
- For docs-as-code repositories, the natural home is a CI job on changed `.md` files. Suggest it once; do not build it unasked.
- Follow the repository's existing conventions over the templates here. A repo with an established changelog or review format wins.

---

## Shared across all three

**Say which mode you are in** when it affects the output. "Running strict evidence mode — every factual claim needs a verbatim span" sets expectations before the author is surprised by a HOLD.

**Never claim a check ran where it could not.** In chat, `scripts/wi.py` does not exist. Do not reference it, do not imply it ran, and do not present chat-side careful reading as mechanical verification. That is Law C, and it is easiest to violate by habit — by carrying a Claude Code output shape into a chat response.
