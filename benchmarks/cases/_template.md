# Benchmark Category Template

Use this template to add cases to any new category. Existing categories (ai_slop_rewrite.md, grant_narrative.md) demonstrate the format.

## CASE-NN — Title

**Input**: [Either the prompt or the source draft.]

**Task Contract**:

```yaml
mode: rewrite
intent: persuade
audience: ...
voice: ...
genre_stack: [...]
high_stakes: true|false
arena: ...
success_condition: "..."
```

**Expected Detections**: list of anti-patterns / failure modes the system should catch.

**Expected Range**: min-max. **v2 baseline**: NN. **v3 target**: NN.

---

## Scoring Rubrics Applied

- Prose Quality (100)
- Genre-specific scoring (100 each as applicable)
- Epistemic Integrity (100) if high_stakes
- Arena Fit (100)

## Regression Hazards

- [Specific risks for this category]

---

## Categories Not Yet Detailed

The following categories carry placeholder structure pending v3.0.1 case authoring (every case must be authored by a domain expert, not generated). The structure above applies; cases will fill in via PR:

- `business_strategy_memo.md`
- `founder_manifesto.md`
- `investor_update.md`
- `sales_email.md`
- `sermon_excerpt.md`
- `academic_paragraph.md`
- `government_brief.md`
- `fiction_scene.md`
- `dialogue_scene.md`
- `longform_continuity_audit.md`

Each will follow the same 5-case structure shown in `ai_slop_rewrite.md` and `grant_narrative.md`. Until populated, the manifest reserves 50 case slots; v3.0.0 ships with 10 fully-authored cases (AI Slop + Grant) and reserved slots for the rest, to be filled via community contribution per `governance/RFC_PROCESS.md`.
