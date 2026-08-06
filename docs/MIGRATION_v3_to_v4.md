# Migrating v3 → v4

**Short version: nothing breaks.** v4 is additive. The eleven passes, twelve engines, twelve agents, twenty-seven genre packs, voiceprints, schemas and anti-slop doctrine are unchanged. Every v3 workflow still runs and produces the same artifacts.

What changes is what happens *around* the writing — and what the system is now willing to claim about it.

---

## Do this

```bash
cd ~/.claude/skills/writing-intelligence && git pull
bash tests/v4/test_wi.sh          # 3 × PASS
python3 scripts/wi.py --version   # wi 4.0.0
```

That is the whole upgrade. No schema migration, no config, no re-authoring.

---

## What is new

| | New in v4 | Where |
|---|---|---|
| Six operating laws | The layer that can stop the kernel | `references/v4/ACCOUNTABILITY_LAYER.md` |
| Proposal redlines | `before → after → why → effect` instead of a rewritten file | `references/v4/PROPOSAL_PROTOCOL.md` |
| Span lock | Support means a verbatim quote or it is `needs_source` | `references/v4/PROOF_PROTOCOL.md` |
| Source hygiene | Prompt-injection scanning on supplied documents | `references/v4/SOURCE_HYGIENE.md` |
| Language tiers | Unavailable metrics reported unavailable, never faked | `references/v4/LANGUAGE_TIERS.md` |
| Voice consent | A stated basis before modeling a named person | `references/v4/VOICE_CONSENT.md` |
| Surface awareness | Output shaped to what the surface can actually do | `references/v4/SURFACES.md` |
| Stated refusals | What the system will not do, and why | `references/v4/NON_GOALS.md` |
| Deterministic verifier | Offline CLI: span, quote, number, date, citation | `scripts/wi.py` |

---

## What behaves differently

These are deliberate. Each one is a v3 behavior that looked helpful and was quietly costing something.

### 1. Edits come back as proposals, not as a finished document

**v3:** returned the rewritten text.
**v4:** returns each change as `before → after → why → effect`, with the original recoverable.

**Why:** an author handed a rewritten document has exactly one decision available — accept the whole thing — and under that pressure they accept. Their voice then erodes one invisible edit at a time. A set of discrete proposals restores a decision per change, which is the only arrangement in which they are still the author.

**If you want the old behavior:** ask for the clean rewrite explicitly. You will get it, along with the diff. The default changed; the capability did not go away.

### 2. Claims are no longer "supported" because they sound supported

**v3:** the epistemic ledger classified claims and scored integrity.
**v4:** a claim is `supported` only when a verbatim span from a supplied source can be quoted beside it. Everything else is `needs_source`, `inference`, `author_asserted`, `recommendation`, `conflicted` or `unsafe`.

**Expect more `needs_source` than you are used to.** That is Law E working: wrongly "supported" is a catastrophe, wrongly "needs a source" is a nuisance. A well-paraphrased claim with no verbatim span reads `needs_source` — the deterministic tier says outright that it cannot judge paraphrase, so treat that status as *unproven at this tier*, not as *wrong*.

### 3. Documents get a verdict

`RELEASE` · `HOLD` · `BLOCK`, each item carrying its repairs — attach a source · qualify · cut · proceed with a caveat — and which is cheapest.

`BLOCK` is reserved for the two failures a hostile reader can prove: a citation that resolves to nothing, and a source that directly contradicts the claim. Everything else holds at most.

### 4. Supplied sources are scanned before they are read

A document that says *"ignore previous instructions"*, carries zero-width characters, or contains role markers is flagged and quarantined. It still gets read as evidence. It never gets read as instruction.

**This will flag documents you consider trustworthy.** Scraped web content and PDFs assembled from mixed sources trip it regularly. A flag is a finding to look at, not an accusation.

### 5. Percentages stopped appearing on judgments

**v3:** confidence scores.
**v4:** `verified` (checked by comparison) · `measured` (against a stated baseline) · `judged` (reasoned, unchecked). Mixing them is fine; hiding the mix is authority theater.

A percentage with no denominator is gone. If you were parsing confidence numbers out of v3 output, read the verdict word instead.

### 6. Non-English documents report which metrics are legitimate

Word-per-sentence metrics are undefined without a tokenizer in Chinese, Japanese, Thai and Khmer, and a whitespace count returns nonsense. v4 classifies the script and reports structural metrics only where word metrics do not apply, rather than emitting an English-shaped number that looks real.

---

## Compatibility

| | Status |
|---|---|
| 11-pass kernel | Unchanged |
| 11 JSON schemas | Unchanged — no version bump, no field changes |
| 27 genre packs | Unchanged |
| Voiceprints | Unchanged; consent basis added as a gate before *building* a new one from a named person |
| Agents and manifest | Unchanged |
| Benchmark harness and gold outputs | Unchanged |
| `services/api` REST runtime | Unchanged — still implements the v3 craft kernel |
| Existing `.claims.json` from v3 tooling | Not applicable; v4 introduces this format |

**The REST service is deliberately still v3.** The v4 accountability tier has exactly one implementation — `scripts/wi.py` — and it stays that way. Two implementations of a verification rule drift, and the one that drifts is invisible, because both look correct right up until they disagree about something that matters.

---

## Adopting v4 in stages

You do not have to take all of it at once.

**Stage 1 — verify only.** Keep writing exactly as you do now. Run `wi.py` on finished drafts before they go out. Costs nothing, changes no workflow, and catches fabricated citations and inflated figures immediately.

**Stage 2 — scan sources on intake.** Run `scan-sources` on anything supplied by a third party before you build on it. Conflicts between two supplied documents are the highest-value thing you can find, and you want them *before* you write, not after you submit.

**Stage 3 — proposals.** Let redlines come back as proposals. This is the stage that feels slower and is the one that keeps your voice.

**Stage 4 — gate in CI.** Add `gate --exit-code` to a pre-commit hook or pipeline. See [`docs/INSTALL.md`](INSTALL.md).

---

## What did not change, and will not

- **MIT. Free. Forever.**
- No telemetry, no network calls, no account required.
- `scripts/wi.py` is stdlib-only and runs air-gapped.
- The system will never construct a citation.
- The system will not help with AI-detector evasion.

---

## If something regressed

Open an [issue](https://github.com/antonio0720/writing-intelligence/issues) with the input, the output you got, and the output you expected. v3 behavior that stopped working is a bug, not a v4 design decision — the layer is meant to sit above the kernel, not amputate it.
