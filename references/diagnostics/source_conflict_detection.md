# Source Conflict Detection

**Used by**: Corpus Auditor (Pass 2) and Evidence Prosecutor (Pass 5)

Source conflicts are the second leading cause of drift in long-running projects. A user-provided document says one thing; project memory says another; a web fetch says a third. v3.0 detects, classifies, and resolves these conflicts before they reach the draft.

---

## Conflict Kinds

| Kind | Definition |
|---|---|
| `contradiction` | Two sources directly disagree on a verifiable fact |
| `staleness` | One source has a fresher version of the same fact |
| `scope_mismatch` | One source's claim applies to a different scope than the other |
| `tonal_mismatch` | Sources agree on facts but assert them in incompatible voices |
| `fact_drift` | A claim drifted across versions of the same document |

---

## Resolution Strategies

| Strategy | When |
|---|---|
| `a_wins` | Source A is higher priority |
| `b_wins` | User explicitly chooses B |
| `merge` | Both perspectives valid, surfaced together |
| `flag_for_user` | Cannot resolve without input |
| `block` | Conflict is severe enough that delivery must wait |

---

## Detection Procedure

For each pair of sources that share a topic:

1. Extract claims from each source.
2. Match claims by topic.
3. Compare claims for verbatim agreement, semantic agreement, contradiction.
4. If contradiction: check freshness. Newer wins by default unless lower-priority.
5. If lower-priority is newer than higher-priority: flag for user.
6. If both stale: flag.
7. If tonal mismatch only: log but do not block.

---

## High-Risk Conflict Examples

- **Grant context**: prior-year outcomes vs. current-year audited outcomes — current wins, but prior must be acknowledged for trend.
- **Legal context**: superseded statute vs. current statute — current wins; prior is for historical context only.
- **Medical context**: superseded guideline vs. current — current wins; prior is contraindicated.
- **Financial context**: prior quarter vs. current — both kept but clearly dated.
- **Fiction context**: canonical vs. fan-tier — canonical always wins.

---

## Output

The Corpus Auditor's `corpus_map.conflicts` array logs every detected conflict with kind, resolution, and rationale. The Evidence Prosecutor reads this when deciding which claims to allow into the draft.

---

## Definition of Done

Detection passes when:

- Every cross-source claim pair has been checked
- Every conflict has a resolution or is flagged for the user
- No `block` conflict has been silently overridden
- Every resolution carries a rationale
