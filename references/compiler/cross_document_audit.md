# Cross-Document Consistency Auditing

## Purpose

When a writer produces multiple documents — a blog series, a grant suite,
a book with multiple manuscripts, a body of corporate communications —
those documents must be consistent with each other and internally coherent.
This module audits consistency ACROSS documents, complementing the
within-document checks in `continuity.md` and `memory_system.md`.

---

## Audit Dimensions

### 1. Voice Consistency Across Documents

Compare these metrics between any two documents by the same author:

| Metric | Acceptable Variance | Flag Threshold |
|---|---|---|
| Mean sentence length | ±3 words | ±5 words |
| Sentence length std dev | ±2 | ±4 |
| Vocabulary tier | Same tier | Drop/jump of 1+ tier |
| Contraction frequency | ±10% | ±25% |
| First-person frequency | ±20% | ±40% |
| Formality band | ±1 point | ±3 points |

**Exception**: Documents in different genres are expected to diverge.
A strategy memo and a sermon by the same author should differ. Compare
only within the same genre or apply genre-adjusted baselines.

### 2. Terminological Consistency

Across all documents in a corpus:

- **Same concept = same term**: If Document A calls it "Revenue Operating System,"
  Document B must not call it "sales platform" or "revenue engine" unless
  explicitly introducing a synonym.
- **Acronym consistency**: If "OMC" is defined as "Operational Machine Consciousness"
  in Document A, it cannot be "Optimized Machine Cognition" in Document B.
- **Branding lock**: Product names, company names, program names must be
  identical across all documents. Case-sensitive.

Audit protocol:
1. Extract all defined terms from each document
2. Build a master glossary
3. Flag any term used with different definitions across documents
4. Flag any concept referenced by different terms across documents

### 3. Factual Consistency

Claims made in one document must not contradict claims in another:

- **Numerical consistency**: Revenue figures, dates, percentages, counts
  must match across documents referencing the same data.
- **Historical consistency**: Events, timelines, sequences must agree.
- **Attribution consistency**: A quote attributed to one person in Document A
  cannot be attributed to someone else in Document B.
- **Position consistency**: If Document A argues position X, Document B should
  not argue not-X without explicitly acknowledging the evolution.

Audit protocol:
1. Extract all factual claims from each document
2. Cross-reference claims that share entities, dates, or subjects
3. Flag contradictions
4. Distinguish between genuine contradictions and context-dependent variations

### 4. Argument Continuity

Across a series of related documents (e.g., a book's chapters, a policy memo
series, a blog that builds an argument over time):

- **Progressive development**: Later documents should build on earlier ones,
  not restart from scratch.
- **No orphaned arguments**: An argument started in one document should be
  continued or concluded in a subsequent one.
- **No contradicted premises**: A premise accepted in Document A cannot be
  rejected in Document B without acknowledgment.
- **Thesis coherence**: All documents in a series should serve the same
  overarching thesis or narrative.

### 5. Audience Consistency

If multiple documents address the same audience:

- Vocabulary tier should be consistent
- Assumed knowledge should be consistent (don't define a term in Document 3
  that you used without definition in Document 1)
- Formality level should be consistent
- Emotional register should be compatible

If documents address DIFFERENT audiences on the SAME topic:
- Factual claims must agree
- Conclusions must align
- Differences should be in register and depth, not in substance

### 6. Formatting Consistency

Across a document suite:

- Heading hierarchy (H1/H2/H3 usage)
- Citation style
- List formatting (bullets vs. numbers vs. inline)
- Date formatting
- Number formatting (comma conventions, decimal conventions)
- Abbreviation conventions

---

## Cross-Document Audit Report Format

```
CROSS-DOCUMENT CONSISTENCY AUDIT
═══════════════════════════════════════════════════
Corpus:         [name or description]
Documents:      [count]
Total words:    [sum]
Audit date:     [timestamp]

VOICE CONSISTENCY
─────────────────────────────────
[Table of metrics per document with variance flags]
Status: [CONSISTENT / DRIFT DETECTED / INCONSISTENT]
Flagged docs: [list]

TERMINOLOGY CONSISTENCY
─────────────────────────────────
Terms audited:  [count]
Conflicts found: [count]
[List of conflicts with document references]

FACTUAL CONSISTENCY
─────────────────────────────────
Claims cross-referenced: [count]
Contradictions found:    [count]
[List of contradictions with document references]

ARGUMENT CONTINUITY
─────────────────────────────────
Threads tracked: [count]
Orphaned threads: [count]
Contradicted premises: [count]
[List of issues]

AUDIENCE CONSISTENCY
─────────────────────────────────
[Assessment per document pair]

FORMATTING CONSISTENCY
─────────────────────────────────
[List of deviations]

OVERALL STATUS: [CONSISTENT / ISSUES FOUND / INCONSISTENT]
PRIORITY FIXES: [ranked list]
═══════════════════════════════════════════════════
```

---

## Use Cases

### Book Manuscript
Audit all chapters against each other for character voice, timeline, terminology,
and thesis continuity. Run after completing each act/part.

### Grant Suite
Multiple grant applications referencing the same organization, mission, data.
All applications must present consistent organizational facts, financials,
and program descriptions even when targeting different funders.

### Brand Communications
Blog posts, emails, social media, press releases. Voice and terminology must
be consistent. Product descriptions must match. Claims must agree.

### Legal Document Suite
Contracts, memos, briefs referencing the same transaction or matter. Defined
terms must be identical. Facts must be consistent. Positions must align.

### Academic Paper Series
Multiple papers building on the same research. Methodology descriptions must
be consistent. Data references must agree. Earlier findings must be correctly
cited in later papers.

---

## Integration

- Pairs with `memory_system.md` for session-to-session tracking
- Pairs with `continuity.md` for within-document checks
- Results feed into `auto_diagnostic_report.md` as a supplementary section
- Terminology conflicts feed into the Project Memory File's terminology lock
