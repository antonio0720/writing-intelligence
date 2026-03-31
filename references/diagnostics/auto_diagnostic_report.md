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
[✓] or [✗] Perplexity flatness               Detected: [yes/no]
[✓] or [✗] Sentence-length uniformity         Std dev: [N]
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

### 5. Statistical Profile

```
STATISTICAL PROFILE:
──────────────────────────────────────────────────
Sentence count:          [N]
Mean sentence length:    [N] words
Sentence length std dev: [N] words  [TARGET: ≥8]
Min sentence length:     [N] words
Max sentence length:     [N] words
Sentences ≤6 words:      [N] ([N] per 500 words) [TARGET: ≥1 per 500]
Sentences ≥30 words:     [N] ([N] per 500 words) [TARGET: ≥1 per 500]

Paragraph count:         [N]
Mean paragraph length:   [N] sentences
Para length std dev:     [N] sentences [TARGET: ≥2]
1-sentence paragraphs:   [N]
6+ sentence paragraphs:  [N]

Vocabulary:
  Unique words per 500:  [N]  [TARGET: ≥150]
  Domain-specific terms: [N]
  Uncommon words:        [N]  [TARGET: ≥2 per 300]
  Most repeated word:    "[word]" × [N]

Transitions:
  Most used transition:  "[phrase]" × [N]  [TARGET: ≤2 per 1000]
  Transition variety:    [N] unique transitions
──────────────────────────────────────────────────
```

### 6. AI Detection Risk Assessment

```
AI DETECTION RISK:
──────────────────────────────────────────────────
Perplexity uniformity:    [LOW/MEDIUM/HIGH] risk
Sentence burstiness:      [LOW/MEDIUM/HIGH] risk
Vocabulary predictability: [LOW/MEDIUM/HIGH] risk
Transition homogeneity:   [LOW/MEDIUM/HIGH] risk
Structural uniformity:    [LOW/MEDIUM/HIGH] risk
Opening pattern:          [LOW/MEDIUM/HIGH] risk
Closing pattern:          [LOW/MEDIUM/HIGH] risk

OVERALL DETECTION RISK:   [LOW/MEDIUM/HIGH]

[If HIGH]: Specific passages flagged:
  - Lines [N-N]: Sentence-length cluster (all 15-18 words)
  - Lines [N-N]: Vocabulary flatness (zero surprises in 5 sentences)
  - Lines [N-N]: LLM list rhythm detected
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

2. P4/S4-S7 | F-02: Perplexity flatness | CRITICAL
   4 consecutive sentences, all 16-18 words, all S-V-O
   FIX: Vary lengths (aim: 8, 24, 6, 31). Change structures.

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
SCORE: [N]/100 | GRADE: [X] | DETECTION RISK: [LOW/MED/HIGH]
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
