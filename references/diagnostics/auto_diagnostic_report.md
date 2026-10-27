# Auto-Diagnostic Report Format

## Purpose

When the user requests a score, audit, diagnostic, or grade, output a
structured report following this format. The report should be ruthlessly
honest, specific enough to act on, and organized for rapid scanning.

---

## Report Structure

### 1. Header Block

```
═══════════════════════════════════════════════════
WRITING INTELLIGENCE DIAGNOSTIC REPORT
═══════════════════════════════════════════════════
Document:    [title or first 10 words]
Word count:  [N]
Genre:       [detected or declared]
Voice:       [detected or declared]
Audience:    [detected or declared]
Date:        [timestamp]
═══════════════════════════════════════════════════
```

### 2. Score Summary

```
SCORE: [N]/100  |  GRADE: [S/A/B/C/D/F]
──────────────────────────────────────────────────
Clarity ................ [N]/10
Specificity ............ [N]/10
Rhythm ................. [N]/10
Voice Integrity ........ [N]/10
Argument Strength ...... [N]/15
Evidence Discipline .... [N]/15
Density ................ [N]/10
Audience Fit ........... [N]/10
Memorability ........... [N]/5
Structural Control ..... [N]/5
──────────────────────────────────────────────────
```

### 3. Auto-Fail Check

```
AUTO-FAIL CONDITIONS:
[✓] or [✗] Hard-ban phrases (3+ = fail)      Found: [N]
[✓] or [✗] Predictable filler                 Detected: [yes/no]
[✓] or [✗] Undifferentiated run (same job/weight) Span: [P/S]
[✓] or [✗] Zero domain vocabulary             Found: [N] domain terms
[✓] or [✗] Unsupported universal claim        Found: [N]
[✓] or [✗] Fabricated citation                Found: [N]
[✓] or [✗] Dictionary definition opening      Detected: [yes/no]
[✓] or [✗] Summary conclusion                 Detected: [yes/no]

FAIL STATUS: [PASS / FAIL — score capped at 65]
```

### 4. Violation Heatmap

Mark each paragraph with its violation density:

```
VIOLATION DENSITY BY PARAGRAPH:
──────────────────────────────────────────────────
P1  ████░░░░░░  4 violations  [cadence lock, soft-ban ×2, abstraction float]
P2  ██░░░░░░░░  2 violations  [recursive restatement, weak opening]
P3  ░░░░░░░░░░  0 violations  ✓ CLEAN
P4  ██████░░░░  6 violations  [hard-ban ×1, fake depth ×2, evidence desert, 
                                uniform sentences, dead metaphor]
P5  █░░░░░░░░░  1 violation   [closing collapse]
──────────────────────────────────────────────────
HOTTEST PARAGRAPH: P4 — recommend full rewrite
```

### 5. Statistical Profile (descriptive only)

These counts describe the draft. They are not targets: no number here is
raised or lowered for its own sake, and none predicts or is tuned against an
AI-detector score. A count earns attention only when it points at a reading
problem a person can name.

```
STATISTICAL PROFILE:
──────────────────────────────────────────────────
Sentence count:          [N]
Mean sentence length:    [N] words
Sentence length std dev: [N] words
Min sentence length:     [N] words
Max sentence length:     [N] words
Sentences ≤6 words:      [N] ([N] per 500 words)
Sentences ≥30 words:     [N] ([N] per 500 words)

Paragraph count:         [N]
Mean paragraph length:   [N] sentences
Para length std dev:     [N] sentences
1-sentence paragraphs:   [N]
6+ sentence paragraphs:  [N]

Vocabulary:
  Unique words per 500:  [N]
  Domain-specific terms: [N]
  Most repeated word:    "[word]" × [N]

Transitions:
  Most used transition:  "[phrase]" × [N]
  Transition variety:    [N] unique transitions
──────────────────────────────────────────────────
```

### 6. Reader Experience

```
READER EXPERIENCE:
──────────────────────────────────────────────────
Where does a reader lose the thread?   [span + reason]
Where is the point buried?             [span + reason]
Where does the prose assert nothing
  a reader could check or use?         [span + reason]
Where does rhythm hide which sentence
  carries the weight?                  [span + reason]
Opening: does it start on the subject? [yes/no + span]
Closing: does it earn its last line?   [yes/no + span]

Detector score: NOT MEASURED, NOT TARGETED. An external detector result may be
archived as an observation; it never changes a finding or a fix.
──────────────────────────────────────────────────
```

### 7. Critical Violations (Detail)

List every critical and severe violation with:
- **Location**: Paragraph number + sentence number
- **Type**: Which failure mode (from failure_modes.md)
- **Severity**: Critical / Severe / Moderate / Minor
- **Quoted text**: The specific passage (keep under 15 words)
- **Fix**: Specific instruction for repair

```
CRITICAL VIOLATIONS:
──────────────────────────────────────────────────
1. P4/S2 | F-03: Hard-ban phrase | CRITICAL
   "Here's the thing about..."
   FIX: Delete opener. Start with the claim directly.

2. P4/S4-S7 | F-02: Predictable filler | CRITICAL
   4 consecutive sentences restate one point at one altitude
   FIX: Keep the sentence that carries the point; replace the restatements
        with the mechanism or the evidence, or cut them. [needs source] where a
        fact is missing.

3. P1/S1 | F-13: Opening weakness | SEVERE
   "In today's digital landscape..."
   FIX: Replace with specific data point, named actor, or scene.
──────────────────────────────────────────────────
```

### 8. Strength Callouts

Don't just flag problems. Name what works:

```
STRENGTHS:
──────────────────────────────────────────────────
+ P3: Evidence paragraph with named source, specific data, honest qualifier
+ P2/S4: Strong sentence — memorable, specific, earned
+ Section 2: Argument escalation works — each paragraph builds on the last
+ Closing line of P5: Lands well. Reader carries it forward.
──────────────────────────────────────────────────
```

### 9. Recommended Next Actions

Prioritized list of improvements, ordered by impact:

```
RECOMMENDED ACTIONS (by impact):
──────────────────────────────────────────────────
1. [HIGHEST IMPACT] Rewrite P4 entirely — 6 violations, 
   including 1 critical
2. Replace opening sentence with concrete specificity
3. Inject variance: add 2 short sentences (≤6 words) and 
   1 long sentence (≥30 words)
4. Add 1 domain-specific term per 300 words
5. Replace closing summary with implication or challenge
──────────────────────────────────────────────────
```

### 10. Pass Recommendation

```
COMPILER RECOMMENDATION:
──────────────────────────────────────────────────
[  ] Ready for publication
[  ] One more pass needed — focus on: [specific area]
[✓] Significant revision required — priority: [specific fix]
[  ] Full rewrite recommended
──────────────────────────────────────────────────
```

---

## Abbreviated Report Mode

For quick checks, return only:

```
SCORE: [N]/100 | GRADE: [X] | UNSOURCED CLAIMS: [N]
Top 3 violations: [list]
Top fix: [most impactful single action]
```

---

## Usage Triggers

Output the full report when:
- User says "score this" / "grade this" / "audit this" / "diagnose this"
- User submits a draft and asks "how is this?"
- User explicitly requests a scorecard

Output the abbreviated report when:
- User asks a quick question about quality
- The report is supplementary to a rewrite (rewrite is the primary output)

Output NO report when:
- User asks for a clean rewrite only
- User asks for a specific transformation (compress, transfer, etc.)
- User is in drafting mode and hasn't asked for evaluation
