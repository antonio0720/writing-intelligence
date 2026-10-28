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

---

## v9: Conflicts and the Authorship Dossier

In v9 a detected conflict has a place to land. The authorship declaration checker (`scripts/wi-authorship.py`; a declaration checker, not an authorship verifier) records each piece of evidence with a `support_status` of `supported_by_reviewer`, `needs_source`, `conflicted` or `unadjudicated`.

| Conflict outcome here | `support_status` in the dossier |
|---|---|
| `contradiction`, `scope_mismatch` or `fact_drift` unresolved, or `flag_for_user` pending | `conflicted` |
| `block`, or a claim whose only support is a stale or lower-priority source | `needs_source` |
| A reviewer adjudicated and the resolution carries a rationale | `supported_by_reviewer` (a person's declared judgment, not a verification of truth) |
| Detection has not been run on this claim | `unadjudicated` |

Rules that follow from this:

- **Claim coverage.** Every consequential claim that the v4 claim classifier finds in the draft must overlap an anchored evidence span. One safe anchor cannot carry three claims, and a claim sitting in a conflicted pair has no clean anchor to borrow.
- **A strict-arena submission cannot rest on `needs_source` or `conflicted` evidence.** In `audit`, an unresolved status on a submission in a strict arena (`journalism`, `academic`, `legal`, `government`) is a HOLD (`SUPPORT_UNRESOLVED`); outside those arenas the checker does not hold on it, so the editorial obligation remains. The resolution strategies above are how the status is moved, never a way to hide it.
- **`a_wins` and `merge` do not silently erase the loser.** Keep the superseded source in the dossier with its digest, so the trace shows what was set aside and why (principle WI9-I). A stale source is flagged by a changed `sha256` (`SOURCE_DIGEST_MISMATCH`).
- **Freshness is not truth.** The newer source wins by default under this file's procedure; that is a priority rule, and an exact excerpt match in the checker is a text anchor, not proof that the claim is true.
- **Experience conflicts.** If the author's recollection (`said_by_author`) contradicts a dated record (`sourced` or `measured`), do not average them. Mark `conflicted` and ask the author; a `planned` or `hypothetical` item cannot be promoted to resolve the dispute.
- **Tonal mismatch** stays non-blocking here. A voice comparison is a diagnostic, never evidence about who wrote the text.

None of this checks who wrote anything: every report carries `declaration_status: self_reported`.
