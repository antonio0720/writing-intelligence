# Writing Intelligence v3.0 — Operator Manual

For the user who has moved past basic prompts and is running the system on real work, repeatedly, at quality scale.

## v8 — operating on story work

The disciplines below still hold. For fiction, v8 adds four engines (see [`../references/v8/README.md`](../references/v8/README.md)) and three operator rules:

1. **Project before you diagnose.** Build the typed story projection with the author, mark it `draft_projection`, and run `validate` before `audit` or `evaluate`. A refused projection (exit 2) is information, not an obstacle.
2. **Report the state, never a score.** Every finding is a mechanical defect, a signal for review, the author's call, or a question for readers. Never summarise a run as "the book is good" — every publication gate holds (exit 3), by design.
3. **Run `bash scripts/test-v8.sh` after any change to the story engines or their registers.** It must read 19 passed, 0 failed, and 340 requirements.

Pattern: *author brief → projection → validate → audit / evaluate / classify → editorial conversation → revised projection → as-of / impact → gate (HOLD) → human editor → reader study.*

## v9 preview — operating `audit`, `release`, the per-writer tools and the review ledger

v9 is a **preview on PR #8**, not a release; v8.0.0 is the published version. These are the operating rules for the v9 tools you can run today, all reachable as `wi authorship <tool>`. Reference: [`../references/v9/README.md`](../references/v9/README.md).

1. **Gather the sources first, then the draft.** A dossier names the draft (with a pinned `expected_sha256`), the evidence spans that support it, the contribution log (who or what wrote which part), the declared origin and the venue contract. Source before style: nothing here helps you invent an experience the sources do not contain.
2. **Run `audit`; read the whole report.** `REVIEW` (exit 0) means the limited checks passed and a person still has to decide. `HOLD` (exit 3) means stop. `audit` never authorizes release and every report carries `declaration_status: self_reported`.
3. **Read the HOLD code, then fix the cause, never the check.** The codes you will meet most:

| Reading | What it means | What to do |
|---|---|---|
| Unanchored consequential claim (claim coverage) | The v4 classifier found a claim in the draft that no anchored evidence span overlaps | Add the source span, soften the claim, or cut it. One anchor does not carry three claims |
| `ORIGIN_CONTRADICTS_LOG` | Declared `human_authored`, but the contribution log shows AI prose | Correct the declaration or the log to what happened |
| Planned or hypothetical `experience_state` backing a firsthand claim | A firsthand "I did" rests on something that was only planned or imagined | Keep it labeled hypothetical, or replace it with a confirmed experience |
| `needs_source` or `conflicted` support | A reviewer recorded the evidence does not support the claim | Resolve it; a submission holds until you do |
| Draft digest mismatch / ambiguous anchor | The draft changed after it was pinned, or an excerpt appears twice and needs `start` | Re-pin the digest after review; add `start` |
| Human-only venue with unlisted assistance | The venue contract does not list the help recorded in the log | Remove the AI-written or AI-rewritten package; research briefs may be prepared separately |

4. **Treat a resolved anchor as presence, not truth.** `ANCHOR_RESOLVED` means the exact excerpt exists at that place. Whether it supports the claim is `support_status`, recorded by a reviewer.
5. **Run `release` only after a person has decided.** It needs a REVIEW audit, a `review_decision` bound to the exact draft sha256, a v6 grant (`wi.py authority issue --capability release.approve --scope release_target --scope-value "<venue>"`) held by that person and active both when they decided and now, a venue contract listing `submit`, and an unpassed deadline. A grant written only into the dossier holds with `AUTHORITY_UNBOUND`. You — the operator, not the dossier — name the store: `--authority-store <dir>`, a v6 workspace outside the dossier folder. A store inside the dossier folder holds (`AUTHORITY_STORE_UNTRUSTED`), because whoever wrote the dossier could have written a grant to themselves into it; a dossier that tries to choose the store holds (`AUTHORITY_STORE_FROM_DOSSIER`); the store is opened read-only and never created. `RELEASE_ELIGIBLE` transmits nothing; you still send it, by hand.
6. **Use the phrase scan as an editor's question list.** `wi9_hotphrases.py scan` reports where a pattern appears (code-point offsets, line and column, document and rule digests). A match asks "does this sentence carry the author's thought?" It is never proof that anyone or anything wrote the passage, and never an automatic rewrite.
7. **Record each decision in the review ledger, under the reviewer's own grant.** `wi authorship ledger record --ledger <their folder> --authority-store <store> --actor <them> --kind phrase|meaning ...` writes a decision only after the v6 store shows that person holds the capability as a human: issue `claim.accept.wording_only` for phrase decisions, `claim.accept` for meaning decisions, and `claim.accept.quantity_change` (or `claim.accept`, which covers it) where numbers change. The ledger is append-only; a change of mind is a new entry with `--supersedes`. `wi authorship phrase-review --ledger ... --authority-store ...` then binds each disposition to the exact document and rule digests. A typed reviewer name without a ledger entry holds `REVIEWER_UNBOUND`. A valid review means *reviewed*, never publication-approved; a grant shows who was authorized, not who typed.
8. **Every writer keeps their own material.** The vault (`wi authorship vault`), voice samples and ledger live in folders the writer chooses, outside any repository; the tools refuse to create or open them inside a git working tree, and nothing ships a corpus. As an operator you never collect another person's notes or samples into a shared folder or a commit.
9. **Run `meaning diff` after every revision and hand the deltas to the writer.** Each delta is a question only the writer can answer. Do not accept deltas on their behalf; `meaning review` reaches REVIEW only on their grant-bound decisions, and a new first-person sentence also needs an anchored claim in their vault.
10. **A model is the writer's choice and comes after the gates.** `wi authorship compose --provider-cmd <their program> --key-env <NAME> --consent-to-send` never reaches a model for a human-only or unknown venue or unconsented evidence. Keys are named, never typed into arguments or files. The draft is `ai_generated` and needs the writer's review.
11. **Never optimize to a detector.** Do not insert typos, shuffle sentence lengths or paraphrase to move a vendor score. If a detector result bothers you, ask the editorial question it points at and answer it from your sources and your thinking. The rhythm operator is `repair_rhythm`, applied because the thought changes shape.

What v9 cannot do, so you do not ask it to: it cannot prove a person wrote a manuscript; it cannot decide a claim is true; it does not understand meaning (the diff is lexical); it has not been benchmarked against editors (WI9-07 has not run); no real writer has yet run the voice tools on their own samples; and on Windows it refuses rather than runs.

## The Operator's Discipline

1. **Always declare the intake contract.** Don't trust auto-detection on important work.
2. **Always run the corpus audit when sources matter.** Don't let memory contaminate fresh drafts.
3. **Always emit the epistemic ledger in high-stakes work.** Even if it's "just an internal memo," your future self deserves the receipts.
4. **Always preserve voice fingerprint across arenas.** Cross-arena repackaging is where voice dies.
5. **Always update memory at the end of a session.** Pass 11 isn't optional for longform projects.
6. **Always check the regression matrix when revising.** Quality drift happens between sessions.

## Daily Operating Patterns

### Pattern A — Single-Piece Compilation

```
1. Paste source draft + describe task
2. Skill emits intake contract — verify
3. Skill runs Passes 1-11 — review at Pass 5 (ledger) and Pass 9 (stress battery)
4. Receive delivery bundle
5. Surface any soft-flagged decisions for your review
6. Approve or iterate
```

### Pattern B — Voice Build + Drift Tracking

```
1. Submit 3+ writing samples
2. Skill builds VoiceFingerprintV3 baseline
3. Save the baseline ID
4. On every subsequent piece, reference the baseline
5. After Pass 7, review drift report
6. If drift is unintentional, run voice restoration; if intentional, update baseline
```

### Pattern C — Cross-Arena Distribution

```
1. Approve a single source piece (clean, scored, ledgered)
2. Run Pass 8 with multi-arena directive
3. Skill emits delivery bundle per arena
4. Verify channel constraints
5. Distribute
```

### Pattern D — Series / Longform

```
1. Initialize storyworld memory on chapter 1
2. Every subsequent chapter: load memory at Pass 2, update at Pass 11
3. Quarterly: run series continuity audit
4. Surface any drift / orphaned plants / dead motifs
```

### Pattern E — Team Voice Enforcement

```
1. Build a team voice fingerprint from senior writers' work
2. Every contributor's output runs against the team fingerprint
3. Editorial review uses the drift report as starting point
4. Operator-tier writers can approve voice variance with justification
```

## Operator Anti-Patterns

- **Skipping Pass 0 because "I know what I want."** You think you do. Make it explicit; you'll be surprised.
- **Skipping Pass 5 because "it's not high-stakes."** You may be right. But the ledger costs little and prevents the fabrication you didn't notice you were making.
- **Approving Pass 6 output without reading the rewrite log.** That log is the receipt. Voice damage hides in the log.
- **Running Pass 8 before Pass 5 is clean.** Arena packaging cannot save fabricated content.
- **Ignoring drift reports.** Drift is the slow death of voice.

## High-Stakes Operating Rules

When the work is high-stakes (academic, medical, legal, government, grant, financial, public release):

1. Set `high_stakes: true` explicitly. Don't trust auto-detection.
2. Run the corpus audit even if no external sources were attached.
3. Read the epistemic ledger end-to-end.
4. Resolve every `claim_softened` / `claim_qualified` decision yourself; don't approve in bulk.
5. Run the steel-man check (Pass 9 question 11) and address the strongest counter-argument explicitly.
6. Pass 10 should produce `delivery_decision: release`. If `hold_for_review`, do not ship until you've reviewed.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Output sounds flat | Voice drift in Pass 6 | Re-run Pass 7 with stronger voice anchor |
| Output sounds like a memo when you wanted a sermon | Wrong arena in intake contract | Re-issue contract with arena: `sermon` |
| Stripped a claim you wanted to keep | `preserve_user_claims: false` (default true) | Re-issue with `preserve_user_claims: true` |
| Delivery blocked | Unsafe source or fabrication risk | Read epistemic ledger; address each block |
| Score capped at 65 | Auto-fail condition triggered | Read which condition; address |
| Multi-arena bundle voice drifted | Pass 7 baseline missing | Provide fingerprint baseline before Pass 8 |
| Architecture graph shows orphan claim | Pass 4 detected unsupported claim | Add evidence or remove |
| Plant audit shows orphaned plant | Pass 4 detected setup without payoff | Add payoff or remove plant |

## Productivity Tips

- Cache fingerprints. Build once, reference forever.
- Build a personal genre stack profile for recurring work patterns.
- Use benchmarks to validate big rewrites against your prior baselines.
- Run multi-arena bundles in advance of campaigns to test voice stability.
- Run pre-deadline benchmark suites against drafts to surface regression hazards.

## Operator Certification

If you've shipped 5+ deliverables at v3.0 quality across multiple arenas, consider applying for Operator tier (`certification/operator_levels.md`). The bar is shipping work scored ≥ 85 prose + ≥ 85 epistemic integrity across 5 pieces in 3 arenas.

## Author

Antonio T. Smith Jr. / Density6 LLC
