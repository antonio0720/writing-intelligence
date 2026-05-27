# Argument Graph — Specialization of Architecture Graph

**Use when**: persuasive, academic, strategic, op-ed, position-paper, pitch, or any prose whose primary job is to move a reader to belief or action.

**Parent**: `references/compiler/architecture_graph.md`

---

## What an Argument Graph Adds

An argument graph specializes the architecture graph for persuasive structure. Where the general graph asks "does this section do its job?", the argument graph asks:

1. Are claims sequenced for maximum cumulative force?
2. Is each premise load-bearing or decorative?
3. What does the argument take for granted (hidden assumptions)?
4. What is the evidence-to-assertion ratio?
5. Does the argument build or plateau?
6. Are two paragraphs making the same point?
7. Does the conclusion do more than summarize?

---

## Argument Topology Audit

The Structure Engineer + Evidence Prosecutor jointly run:

### 1. Claim Sequence Audit

- Are the strongest claims placed at maximum-leverage points (opening hook, mid-arc turn, closing punch)?
- Are weaker claims clustered or hidden behind stronger ones?
- Is there an escalation curve?

### 2. Premise Load-Bearing Audit

For every premise node:
- Remove it mentally. Does the parent claim still stand?
- If yes — premise is decorative, flag for cut.
- If no — premise is load-bearing, must have its own support.

### 3. Hidden Assumption Surface

Walk every claim and ask: what does this take for granted? List every unstated assumption. For each:
- If the audience shares it — OK to leave silent.
- If the audience does not share it — promote to explicit premise, find evidence.
- If the audience would dispute it — surface explicitly and defend.

### 4. Evidence-to-Assertion Ratio

Count claims. Count distinct evidence nodes. Ratio < 0.5 → argument is asserting more than it proves. Ratio > 3 → argument may be over-supporting weak claims (often a sign of low confidence).

### 5. Escalation Curve

Plot stakes per node. Argument should climb. If it plateaus by node N/2, the rest is filler. If it climbs and crashes (long denouement), the closing is wasted.

### 6. Redundancy Collapse

Two paragraphs say the same thing in different words → collapse. Two evidence nodes prove the same sub-claim → keep the stronger one.

### 7. Conclusion Force

The closing must DO something the argument has earned:
- Restate the thesis with new weight
- Make a recommendation
- Pose the next question
- Place a stake (the "what now")

A conclusion that summarizes only is filler.

---

## Argument-Specific Edge Patterns

| Pattern | Diagnosis |
|---|---|
| Claim → Evidence → Claim (chain) | Healthy build |
| Claim → Claim → Claim (no evidence) | Assertion stack — flag |
| Premise → Premise → Premise → Claim | Heavy ramp; consider compression |
| Evidence → Claim → Rebut → Reframe | Steel-man pattern — strong |
| Claim → Evidence (one only) | Single point of failure — risky |
| Many claims → one closing | Sprawl; closing cannot carry the weight |

---

## Steel-Man Insertion

For high-stakes argument, the Structure Engineer should add a `rebuts` edge from a "best counter-argument" node to the primary claim, then a follow-on node that addresses it. Arguments that don't address counter-arguments lose to readers who already disagree.

---

## Definition of Done

The argument graph passes when:

- Every claim has at least one `supports` edge from evidence or premise (except where the user explicitly marks a claim as `rhetoric`).
- No assertion stack of length > 3.
- Escalation curve is positive through to the conclusion.
- Hidden assumptions are surfaced or accepted as shared.
- The conclusion is not pure summary.
- Steel-man counter-argument is addressed in high-stakes contexts.
