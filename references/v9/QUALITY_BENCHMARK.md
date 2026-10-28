# Writing Intelligence v9 — Authenticity Benchmark Specification

**Project author:** Antonio T. Smith Jr.  
**Organization:** Density6 LLC  
**Status:** Experimental test design; **no scores reported as measured yet**

## Test objective

Prove better preservation of human-author meaning, distinctive expression, domain specificity, and source integrity while avoiding manipulation of automated AI detectors. Claim `IMPROVED` only when blinded humans and the original author prefer the v9 result on predefined criteria without worse integrity. Claim `SHIPPED` only with reproducible receipt and independent readback.

## Test corpus — consent-based

| Cohort | Minimum cases | Material | Independent evaluation |
| --- | ---: | --- | --- |
| Journalist and expert commentary | 15 | Author-origin notes or recorded interviews, source policy, editor brief | Expert editor + author |
| Executive correspondence | 15 | Original human email, objective, context, consented revision | Editor + original author |
| Fiction | 15 | Original author scene, constraints, subsequent chapter, continuity ledger | Reader + author |
| Technical and institutional | 15 | Signed-off requirements, source documents, original draft | Domain reviewer + author |

**Total proposed:** 60 cases, evaluated with identical source material. These are test targets, not a claim that samples have been collected or trials have occurred.

## Comparison arms

- **A:** Original author text (where available).
- **B:** Unmodified v8 output from the same source and prompt.
- **C:** v9 proposal workflow output, with all evidence and author edits logged.
- **D:** Author-only manual revision (optional reference; do not assign fabricated credit).

Use anonymous, randomized labels for blind reviews. Keep source provenance separately. Reviewers must not be asked to guess "was this written by AI?" as the success criterion.

## Scores with operational meaning

Rate 1–5 with a short justification:

1. **Original thought:** Specific idea, technical mechanism, experience, or claim that the source author actually contributed.
2. **Evidence integrity:** Source-anchored first-person and third-party factual claims; no false numbers, events, or quotes.
3. **Voice fidelity:** Recognizable syntax, priorities, register, and counterarguments relative to consented authentic samples.
4. **Narrative or argumentative consequence:** Each paragraph makes the next one necessary.
5. **Reader usefulness:** Right substance and length for the actual venue and intended action.
6. **Natural phrasing:** Readability and conversational credibility, without artificial error insertion.
7. **Uncertainty discipline:** Preserves real unknowns and scope limitations.
8. **Editorial restraint:** Does not inflate adjectives, complexity, emotional tone or abstract conclusions.

The author should separately accept, partially accept, or reject the semantic change in each paragraph. Do not average human judgments into a false universal "100% human" score.

## Quantitative integrity invariants

- **0** invented autobiographical incidents, professional qualifications, quotes or measurements.
- **0** known violations of human-only publication requirements.
- **0** silent changes to protected factual meaning.
- **100%** of explicitly claimed factual anchors are resolvable to declared source excerpts; this verifies text correspondence only, not whether the sources are true.
- **100%** of evaluated outputs retain a declared provenance state (`human_authored`, `ai_assisted`, or `ai_generated`); this is a disclosure control, not authorship authentication.
- **100%** of shipped-wave claims require tests, negative controls, dependency checks and independent readback.

## Real errors to catch

- Fabricated anecdote derived from a business-plan example.
- "We built" substituted for "we plan to build."
- Generic first-person authority substituting for evidence.
- Contradiction between the user's opinion and the rewritten conclusion.
- A quote presented as verbatim that originated as a model paraphrase.
- Three parallel "not X but Y" sections with no actual inferential development.
- Mechanical cadence changes that harm comprehension.
- A detector claiming something is human despite clear AI-origin provenance.
- A human-only editor receiving AI-produced prose because the operator clicked Send.

## Review protocol

Before review, seal the source digest, prompt, original draft, output, contribution log, model configuration if applicable, reviewer instructions, and run date. Every editor rates independently before discussion. Report per-cohort medians and distributions, disagreements, and strongest negative examples. The program fails if any critical integrity invariant breaks, even when editorial ratings rise. Revise with a new version and rerun the full regression set.

## Definition of success

v9 passes an editorial pilot only when source owners explicitly accept semantic fidelity, independent editors show a material preference under blinded conditions, and negative-control provenance/eligibility tests remain reliable. *Detector percentage is recorded only as optional context and never optimized.*

**Program state:** NOT YET EXECUTED.
