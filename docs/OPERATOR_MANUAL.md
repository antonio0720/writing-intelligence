# Writing Intelligence v3.0 — Operator Manual

For the user who has moved past basic prompts and is running the system on real work, repeatedly, at quality scale.

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
