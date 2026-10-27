# Fiction quality score separation

**Status:** proposal; do not append an unvalidated score to the current 100-point Writing Intelligence scorecard.

Maintain four separate channels: **mechanical integrity** (can be independently retested), **narrative continuity** (typed canon/source-relative), **editorial judgment** (named reader's accountable interpretation), and **reader experience** (independent human data). Publication exports have a fifth operational channel, **format verification** (file, typography, glyph integrity, pagination, device/reflow testing).

Never collapse them into a single percentage or badge, particularly when any channel contains `UNKNOWN`. A system cannot infer emotional impact from word frequency, nor infer publication readiness from chapter score arithmetic. Gate reasons must cite rule IDs, stable evidence locations and exactly which independent validations were and were not run. A clean syntax export is not proof that the narrative ending works.

**v9 note.** The v9 proposal (PR #8, not a release) does not change fiction gates or this separation. The authorship declaration checker, the 334-rule editorial phrase catalog and the voice-sample statistics are non-fiction-oriented tools; none contributes a number to any of the channels above. In particular, a phrase-catalog hit in dialogue or narration is not a fiction defect by itself, and voice similarity or a detector's output is never a reader-experience measure. The fifth channel (format verification) and the `UNKNOWN`-stays-`UNKNOWN` rule are unchanged.
