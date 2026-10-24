# Arc/Ending Projection Pass (Additive Specification)

**Status:** stand-alone prototype implemented for typed fixture exports; integrated v8 compiler pass **not implemented**.

The compiler sees a normalized, read-only projection of already-authorized `fictional_canon` rather than inferring arbitrary inner needs from prose. It emits candidate `ending` interpretations and review findings; only a human writer using the canonical authority/proposal machinery may accept new canon. The pass must never modify storyworld nodes itself.

**Order of operation:** resolve current canonical root → export ordered scene/event references and attributed character interpretations → validate temporal/provenance invariants → select per-character terminal want and need → derive eligible quadrants → cross-reference action witnesses → calculate local impact suggestions → report unresolved editorial judgments → request independent reader study if release-targeted.

**No compulsory dramaturgical formula:** beginning/midpoint/finale are causal concepts, not percentages. A flat character arc is valid if pressure transforms something consequential around the character, and anti-transformative literary fiction is valid even without such a transformation if the intended reader experience works. Only formal contradictions are eligible for deterministic failure.

**Outputs:** `wi.arc.report/v1` findings with requirement IDs, character ending projections, local scope/coverage, limitation list and a digest of the projection itself. Aesthetic score is absent by design. No installed v7 `wi.py` command has been extended here.
