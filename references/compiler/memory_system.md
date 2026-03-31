# Multi-Session Memory System

## Purpose

Maintain writing quality, voice consistency, and argument coherence across
multiple writing sessions for longform projects (books, doctrine documents,
multi-part series, recurring brand communications).

This system extends `continuity.md` with session-persistence protocols.

---

## Project Registration

At the start of any longform project, create a **Project Memory File** (PMF)
that persists across sessions. The PMF contains:

```
PROJECT MEMORY FILE
═══════════════════════════════════════════════════
Project:        [title]
Type:           [book / doctrine / series / brand]
Created:        [date]
Last updated:   [date]
Sessions:       [count]
Total words:    [running total]

VOICE PROFILE
─────────────────────────────────
Voiceprint:     [name or custom]
Mean sentence length:   [N] ± [std dev]
Vocabulary tier:        [accessible / standard / elevated]
Formality band:         [N]/10
Emotional temperature:  [cool / warm / hot / variable]
Humor frequency:        [none / rare / occasional / frequent]

TERMINOLOGY LOCK
─────────────────────────────────
[Term A] = always use this exact phrase
[Term B] = always use this exact phrase
[Term C] = never use (use [Term D] instead)
...

THESIS REGISTRY
─────────────────────────────────
Central thesis: [one sentence]
Sub-thesis 1:   [section/chapter] → [claim]
Sub-thesis 2:   [section/chapter] → [claim]
...

METAPHOR LOG
─────────────────────────────────
[Metaphor 1] — used in [section], meaning [X]
[Metaphor 2] — used in [section], meaning [X]
Banned metaphors: [any that have been retired]

CHARACTER REGISTRY (fiction)
─────────────────────────────────
[Character A]:
  Voice: [speech patterns, verbal tics, vocabulary]
  Knows: [what information they have at this point]
  Arc position: [where they are emotionally/narratively]
[Character B]:
  ...

TIMELINE (fiction / narrative)
─────────────────────────────────
[Event 1] — [date/time] — [chapter/section]
[Event 2] — [date/time] — [chapter/section]
...

EMOTIONAL ARC MAP
─────────────────────────────────
Section 1: [register] — [tension level 1-10]
Section 2: [register] — [tension level 1-10]
...
Target arc shape: [build / release / build-release-build / etc.]

COMPLETED SECTIONS
─────────────────────────────────
[Section 1]: [word count] | [score] | [key claims] | [unresolved threads]
[Section 2]: [word count] | [score] | [key claims] | [unresolved threads]
...

UNRESOLVED THREADS
─────────────────────────────────
[Thread 1]: Introduced in [section] — needs resolution by [section]
[Thread 2]: Introduced in [section] — needs resolution by [section]
...

SESSION LOG
─────────────────────────────────
Session 1: [date] | [sections worked] | [words added] | [key decisions]
Session 2: [date] | [sections worked] | [words added] | [key decisions]
...
```

---

## Session Start Protocol

At the beginning of each new writing session for a longform project:

### 1. Load Context
- Read the PMF
- Review the last session's log entry
- Review unresolved threads
- Review the emotional arc map to know where the next section sits

### 2. Continuity Check
Before writing new content, verify:
- [ ] Voice parameters match the established profile
- [ ] Terminology lock is active
- [ ] No contradiction with previous sections' claims
- [ ] Characters know only what they've learned so far (fiction)
- [ ] Emotional arc position is correct for this section
- [ ] Any metaphors being used aren't duplicating earlier ones unintentionally

### 3. Section Planning
For the upcoming section, declare:
- **Job**: Define / Prove / Contrast / Narrate / Warn / Persuade / Operationalize / Close
- **Connection to previous section**: How does this section follow from the last?
- **Connection to central thesis**: How does this section serve the main argument/narrative?
- **Target emotional register**: Where on the tension scale (1-10)?
- **Key claim or event**: What must this section accomplish?

---

## Session End Protocol

At the end of each writing session:

### 1. Update PMF
- Add new sections to Completed Sections with word count, score, key claims
- Update Timeline with any new events
- Update Character Registry with any new knowledge or arc progression
- Update Metaphor Log
- Add any new unresolved threads
- Update Emotional Arc Map
- Write session log entry

### 2. Continuity Audit
Run a quick check:
- [ ] Any terminology inconsistencies introduced this session?
- [ ] Any character knowledge violations? (knowing what they shouldn't)
- [ ] Any claims that contradict earlier sections?
- [ ] Any metaphors that collide with earlier ones?
- [ ] Voice metrics (sentence length, vocabulary) still within project range?

### 3. Next-Session Notes
Write 2-3 sentences about what the next session should accomplish and
any unresolved questions or decisions that need to be made.

---

## Cross-Section Consistency Checks

Run these at milestone intervals (every 5 chapters, every 10,000 words,
or at act/part boundaries):

### Voice Drift Check
Compare sentence-length stats, vocabulary tier, and formality band of recent
sections against the project baseline. Flag any section that deviates >20%
from the mean without narrative justification.

### Thesis Coherence Check
For each completed section, verify:
- Does it contain at least one connection to the central thesis?
- Do its sub-claims support or complicate the central thesis?
- Are there any claims that contradict the thesis without acknowledgment?

### Character Consistency Check (Fiction)
For each character who appeared in recent sections:
- Does their dialogue match their established speech patterns?
- Do they reference only information they should know at this point?
- Is their emotional state consistent with their arc position?

### Thread Tracking
Review unresolved threads:
- Are any approaching their resolution deadline?
- Have any been accidentally forgotten?
- Have any new threads been introduced without being logged?

### Redundancy Check
Compare section summaries. Are any two sections making essentially the same
point? If so, identify which is stronger and flag the other for revision
or removal.

---

## Recovery Protocol

If a session starts and the PMF is missing or incomplete:

1. Gather all existing sections/chapters
2. Reconstruct the PMF by analyzing:
   - Voice metrics from existing text
   - Terminology patterns
   - Thesis and sub-thesis extraction
   - Character voice analysis
   - Timeline reconstruction
   - Metaphor inventory
3. Flag any inconsistencies found during reconstruction
4. Present the reconstructed PMF for user verification before continuing

---

## Integration with Other Modules

- **Voiceprint system**: The PMF's voice profile IS a voiceprint. Apply it during Pass 4.
- **Section architecture**: Each section's declared job (from the PMF) is checked during Pass 2.
- **Scorecard**: Score each section independently AND score cross-section consistency.
- **Style transfer**: If a project requires genre changes between sections (e.g., a novel with epistolary chapters), the PMF tracks which genre pack governs which section.
- **Anti-patterns**: All anti-pattern checks apply per-section. The PMF adds cross-section checks that individual-section analysis can't catch.
