# Detector Benchmark Suite

## Purpose

Systematic methodology for testing compiler output against commercial AI
detection tools. This is not about gaming detectors — it is about verifying
that the compiler produces genuinely human-quality prose that detectors
correctly classify as human-written.

---

## Target Detectors

### Tier 1 (Most Widely Deployed)

| Detector | Used By | Method |
|---|---|---|
| **Turnitin AI Detection** | 98% of US universities | Proprietary ML classifier trained on student writing |
| **GPTZero** | Schools, publishers, employers | Perplexity + burstiness analysis |
| **Originality.ai** | Content agencies, publishers | Ensemble classifier with confidence scoring |

### Tier 2 (Secondary / Verification)

| Detector | Used By | Method |
|---|---|---|
| **Copyleaks** | Enterprise, education | ML classifier with code detection |
| **ZeroGPT** | Broad consumer use | Statistical pattern analysis |
| **Sapling AI Detector** | HR, admissions | Sentence-level probability scoring |
| **Crossplag** | Academic institutions | Hybrid detection model |

### Tier 3 (Specialist)

| Detector | Used By | Method |
|---|---|---|
| **Compilatio** | European universities | Multilingual detection |
| **Winston AI** | Government, legal | Document-level classification |
| **Writer.com AI Detector** | Content teams | Real-time detection |

---

## What Detectors Actually Measure

Understanding the mechanics is the key to producing text that passes legitimately.

### Perplexity Analysis
Perplexity measures how "surprised" a language model would be by the text.
- **High perplexity** = surprising word choices = human-like
- **Low perplexity** = predictable word choices = AI-like
- **Uniform perplexity** = consistent predictability across text = strong AI signal

Compiler countermeasure: inject_variance operator + voiceprint's vocabulary
profile ensure non-uniform perplexity with deliberate surprise peaks.

### Burstiness Analysis
Burstiness measures sentence-length variation.
- **High burstiness** = dramatic variation in sentence lengths = human-like
- **Low burstiness** = uniform sentence lengths = AI-like

Compiler countermeasure: Pass 3 variance injection rules enforce minimum
std dev of 8+ words and mandatory short/long sentence inclusion.

### Token Probability Distribution
Advanced detectors analyze the probability distribution of each token (word)
given the preceding context.
- **Human writing**: Some high-probability tokens mixed with low-probability choices
- **AI writing**: Overwhelmingly high-probability tokens throughout

Compiler countermeasure: Voiceprint application in Pass 4 introduces the
author's distinctive word choices, which are low-probability relative to
the LLM's default distribution.

### Stylometric Analysis
Some detectors analyze writing style features:
- Type-token ratio (vocabulary richness)
- Function word distribution
- Punctuation patterns
- Paragraph structure patterns

Compiler countermeasure: The full anti-pattern suite + paragraph physics +
section architecture ensure non-uniform stylometric signatures.

---

## Benchmark Protocol

### Test Matrix

For each benchmark run, test:

| Dimension | Variations |
|---|---|
| Genre | Academic essay, strategy memo, blog post, fiction excerpt, email |
| Length | 300 words, 700 words, 1500 words, 3000 words |
| Voice | 3 different voiceprints |
| Topic | 3 different topics per genre |

Total: 5 genres × 4 lengths × 3 voices × 3 topics = 180 test samples minimum.

### Test Procedure Per Sample

1. Generate the sample through the full 6-pass pipeline
2. Run the internal statistical profile (from auto-diagnostic report)
3. Verify internal metrics pass:
   - Sentence-length std dev ≥ 8
   - Zero hard-ban phrases
   - Zero cadence signature matches at 3+ level
   - Score ≥ 80 on 100-point system
4. Submit to each Tier 1 detector
5. Record the score/classification from each detector
6. If any detector flags as AI-generated:
   a. Identify which specific passage triggered the flag
   b. Run that passage through additional diagnostic
   c. Apply targeted fixes
   d. Resubmit
7. Record pass/fail per detector per sample

### Success Criteria

| Tier | Requirement |
|---|---|
| Tier 1 | ≥95% of samples classified as human across all 3 detectors |
| Tier 2 | ≥90% of samples classified as human across all 4 detectors |
| Tier 3 | ≥85% of samples classified as human (these may have higher false positive rates) |

### Regression Testing

When the compiler is updated:
1. Re-run the full benchmark suite
2. Compare pass rates to previous version
3. Any degradation in Tier 1 pass rates blocks the update
4. Report changes per genre and per detector

---

## Known Detector Weaknesses (Legitimate Observations)

These are publicly documented limitations, not exploits:

### Turnitin
- Higher false-positive rate on non-native English speakers' writing
- Sensitive to document length — shorter documents have higher uncertainty
- Updated model in February 2026 improved accuracy but still reports ±15% confidence bands
- Does not detect AI-assisted editing (human writes, AI polishes) reliably

### GPTZero
- Burstiness analysis can be thrown by intentionally varied sentence lengths
  (this is not gaming — it's how humans actually write)
- Performs better on longer texts (>500 words)
- Higher false-positive rate on formulaic writing (legal, medical, government)

### Originality.ai
- Ensemble approach means different models may disagree on the same text
- Confidence scores below 60% are in the uncertainty zone
- Performs better on English than other languages

### General Limitations
- All detectors have higher false-positive rates on:
  - Non-native English writing
  - Highly formulaic genres (legal, medical, patent)
  - Technical writing with domain-specific vocabulary
  - Very short texts (<200 words)
- No detector can reliably distinguish human-written + AI-edited text
- Detector accuracy degrades as AI models improve

---

## Benchmark Reporting Format

```
DETECTOR BENCHMARK REPORT
═══════════════════════════════════════════════════
Compiler version:    [X.Y]
Date:                [timestamp]
Samples tested:      [N]
Genres tested:       [list]

TIER 1 RESULTS
─────────────────────────────────
Turnitin:       [N]% human classification  [PASS/FAIL]
GPTZero:        [N]% human classification  [PASS/FAIL]
Originality.ai: [N]% human classification  [PASS/FAIL]
Tier 1 overall: [N]% pass rate            [TARGET: ≥95%]

TIER 2 RESULTS
─────────────────────────────────
Copyleaks:      [N]% human classification
ZeroGPT:        [N]% human classification
Sapling:        [N]% human classification
Crossplag:      [N]% human classification
Tier 2 overall: [N]% pass rate            [TARGET: ≥90%]

BREAKDOWN BY GENRE
─────────────────────────────────
Academic:       [N]% pass | Weakest detector: [name]
Strategy:       [N]% pass | Weakest detector: [name]
Blog:           [N]% pass | Weakest detector: [name]
Fiction:        [N]% pass | Weakest detector: [name]
Email:          [N]% pass | Weakest detector: [name]

BREAKDOWN BY LENGTH
─────────────────────────────────
300 words:      [N]% pass
700 words:      [N]% pass
1500 words:     [N]% pass
3000 words:     [N]% pass

FAILED SAMPLES
─────────────────────────────────
[List of any failed samples with detector, score, and flagged passage]

INTERNAL METRICS (AGGREGATE)
─────────────────────────────────
Mean sentence-length std dev:  [N]
Mean score (100-point):        [N]
Hard-ban violations:           [N] total
Cadence matches:               [N] total

RECOMMENDATION: [PASS / CONDITIONAL PASS / FAIL]
═══════════════════════════════════════════════════
```

---

## Integration

- Run after any significant update to the compiler
- Run when adding a new voiceprint or genre pack
- Results inform which passes need tuning
- Failed samples become additions to adversarial_cases.md
- Successful samples become additions to gold_outputs.md
