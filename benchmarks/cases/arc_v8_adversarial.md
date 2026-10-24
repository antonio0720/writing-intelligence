# Adversarial Cases — Want, Need, Arc and Ending v8

**Status:** 20 *authored acceptance scenarios*. Locally deterministic subsets are exercised by `tests/v8_arc/test_arc.py`; reader-facing/causal quality decisions are review protocols rather than tested model performance. All characters and situations below are newly invented examples.

| Case | Input challenge | Deterministic expected result | Non-automatable review question |
|---|---|---|---|
| ARC-01 | A rescuer achieves her named goal and acts on a new inner conviction | `sweet` only for author-asserted closed binary values | Did the conviction actually change? |
| ARC-02 | Rescuer renounces a medal and protects a friend | `semi_sweet` if goal/need references are explicit | Was a credible alternative available? |
| ARC-03 | Rival seizes the port but alienates her sister | `bittersweet` only as author reading | Do readers experience thematic irony? |
| ARC-04 | Councilor loses office and rejects reconciliation | `bitter` when both failures are closed | Does the ending feel imposed? |
| ARC-05 | Character achieves a *part* of the goal | `not_classifiable` | Would readers accept qualified closure? |
| ARC-06 | Reviewer infers private need; writer does not assert | `not_classifiable` | Which interpretation has stronger textual support? |
| ARC-07 | Ambiguous final scene is deliberate | `not_classifiable` | Does uncertainty feel purposeful? |
| ARC-08 | Flat hero keeps beliefs yet transforms a village | Arc stays flat; no forced conversion | Is environmental change earned? |
| ARC-09 | Corrupt hero wins everything external | Arc `corruption` independent of quadrant | Was early corruption potential planted? |
| ARC-10 | Disillusionment leads to wiser caution | Arc `disillusionment` admissible | Is change meaningful without optimism? |
| ARC-11 | Two POV heroes want incompatible futures | Per-character outcomes remain separate | Which arc is emotionally central? |
| ARC-12 | Want changes from promotion to family safety mid-book | Old revision persists in as-of; new revision later | Is causal replacement believable? |
| ARC-13 | Editor backfills a later goal into an earlier knowledge query | Future-known revision cannot appear | Did earlier published text disclose the original goal? |
| ARC-14 | Supposed transformation is said but not acted | `ARC_CLAIMED_CHANGE_NO_CHOICE` review signal | Is recognition itself sufficient here? |
| ARC-15 | A strange trauma is asserted as every choice's sole cause | Review warning if universal-claim annotation supplied | Is it psychologically credible or reductive? |
| ARC-16 | Ending focus points at a different character's need | Validation BLOCK | None; ownership invariant violated |
| ARC-17 | A causal link loops event 2 into event 1 | Validation BLOCK | None; chronology inconsistency |
| ARC-18 | High-tension book intentionally has no conventional midpoint | No forced midpoint failure | Does pressure nevertheless change? |
| ARC-19 | Reader sample loves the ending, writer intended tragedy | Separate reader results and intended valence | Does divergence enrich or undermine intent? |
| ARC-20 | Schema checks pass; publisher asks for certification | Always HOLD | Have rights, print export, proof and audience evidence been independently verified? |

## Scoring procedure

A case passes structurally if output equals the expected deterministic category / refusal and its source fixture, input digest and command are preserved. Interpretive cases are not given fabricated PASS ratings. To calibrate, recruit blinded readers, record the source revision and independent coder disagreements, and publish the confusion matrix with denominators; until then, human-quality scores are `UNKNOWN`.
