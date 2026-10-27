# Writing Intelligence v9 — Authentic Voice & Authorship Provenance (PROPOSAL)

**Status:** Experimental proposal, **not** the published v9 release. This branch does not change the v8 release, `SKILL.md`, or the canonical v4–v8 runtime. **Project author:** Antonio T. Smith Jr. — Density6 LLC. **Date:** 2026-10-27.

**Full editorial protocol:** [`EDITORIAL_PROTOCOL.md`](EDITORIAL_PROTOCOL.md). **Wave states:** [`WAVES.yaml`](WAVES.yaml).

## Mission

Enable authors and editors to produce distinctive, credible, source-grounded writing while preserving **who actually wrote it**. Do **not** promise prose that is "100% human" when a model wrote it, a 0% AI detector score, or eligibility for a human-only venue based on surface style. A detector result is a noisy diagnostic, not a provenance record.

The trigger was an AI-generated three-part essay about miniature worlds: the content answered the questions but relied on hypothetical models instead of the author's confirmed experiences, evenly structured arguments, mirror-image contrasts, and a polished abstraction layer. A commercial detector returned "68% possible AI." That number is reported as a user observation, **not** independently validated authorship probability or baseline for optimizing a detector.

## v9 first principles — additions to, not replacements for, the 18 laws

- **WI9-A SOURCE BEFORE STYLE:** Author-supplied memories, notes, transcripts, drafts and source documents precede polishing. No invented "I did" scenes.
- **WI9-B VOICE IS EVIDENCE:** An author's voice is measured from consented authentic samples and reviewed by that author. Style stats alone cannot authenticate origin.
- **WI9-C CONCRETE BEFORE CADENCE:** Identify the actual actor, location/context, decision, friction, consequence and uncertainty where the sources support them. Do not add random sentence lengths or planted typos.
- **WI9-D DISTINCTIVE THOUGHT:** Test whether the paragraph offers an author's specific experience, disagreement, revision, mechanism, or bounded insight. Rewriting a platitude elegantly is insufficient.
- **WI9-E NO BORROWED MEMORY:** Hypothetical scenarios remain labeled hypothetical. A company roadmap does not prove a project was built or an outcome measured.
- **WI9-F AUTHORSHIP IS NOT A SOUND:** `human_authored`, `ai_assisted`, and `ai_generated` are distinct declarations. A voice mimic cannot change them.
- **WI9-G VENUE CONTRACT FIRST:** Human-only rules block AI-written and AI-rewritten submission packages, even if an author manually clicks Send. Research briefs may be created separately.
- **WI9-H DETECTOR HUMILITY:** Never optimize to a vendor score, call its percent a factual authorship fraction, or claim a score guarantees acceptance. Record vendor/version/date as optional diagnostics only.
- **WI9-I TRACEABLE TRANSFORMATION:** Preserve source and every edit; declare whether a change is mechanical proofreading, suggested edit, authored revision or substantive generation.
- **WI9-J REVIEW, DON'T AUTO-PUBLISH:** Source checks do not authenticate a person's identity or mental authorship. Release decisions remain scoped human judgments.

## Prototype included

`scripts/wi-authorship.py audit --input dossier.json` reads a JSON dossier and local text sources. It checks exact source anchors, optional SHA-256, consent flags, firsthand-source eligibility, claimed document origin, declared contribution history, draft passage-to-evidence links and venue policy. It **does not rewrite** prose, rate it "human," perform detector evasion, or certify authorship. It never turns an AI draft into a human-authored document. `REVIEW` means a limited checklist passed; it is **not publication authorization**.

### Dossier format

```json
{
  "schema": "wi9-authorship-1",
  "document": {
    "path": "draft.txt",
    "origin": "ai_generated",
    "arena": "journalism",
    "venue_policy": "human_only",
    "intended_use": "research_demo"
  },
  "evidence": [
    {
      "id": "observation-1",
      "claim": "The writer personally built miniature environments.",
      "kind": "firsthand",
      "source_path": "notes.txt",
      "exact_excerpt": "I have personally built miniature environments.",
      "source_origin": "human_authored",
      "consent": true,
      "sha256": null
    }
  ],
  "contribution_log": [
    {"kind": "ai_research"}
  ],
  "document_claim_anchors": [],
  "voice_samples": []
}
```

Paths resolve relative to the dossier directory. Sources are not sent to a service. The `origin` and `consent` entries are **self-declarations**, not facts independently verified by the tool. The checker returns HOLD for a human-only submission whose origin is not human-authored or whose declared contribution history includes AI-generated or substantively AI-rewritten prose. Consequential submissions must carry a contribution history and exact draft passage-to-evidence links; missing/unanchored firsthand claims also HOLD. It reports missing voice samples as a non-blocking advisory. It **cannot prove** whether a self-declared human-only manuscript was actually written by a person.

## Planned architecture (no false shipped claims)

| Wave | Name | Exit condition | Status |
|---|---|---|---|
| WI9-00 | Baseline & evidence audit | Reproduce existing v8 tests; capture bounded defect and input SHA | PLANNED |
| WI9-01 | Authorship contract | Machine-readable venue policy, human/AI contribution history, meaningful disclosure | PROTOTYPE |
| WI9-02 | Firsthand material vault | Opt-in private author notes, exact anchors, consent + redaction, no external uploads | PLANNED |
| WI9-03 | Voice baseline | 3+ consented samples / >=500 words each; compare to human blind judgments, not detectors | PLANNED |
| WI9-04 | Thought fidelity | Preserve author claims, uncertainty and point of view across revisions | PLANNED |
| WI9-05 | Craft repair | Correct overbalanced transitions, hollow contrasts and unsupported examples based on meaning | PLANNED |
| WI9-06 | Human-only venue gate | Enforce research-only vs pitch modes and author declaration, refusal negative tests | PROTOTYPE |
| WI9-07 | Editorial benchmark | Author-rated fidelity, originality of observation, evidence accuracy, editor-rated usefulness | PLANNED |
| WI9-08 | Integration | Additive integration into `wi.py`, CLI docs, schema, regression and versioned release | PLANNED |
| WI9-09 | Independent review & rollout | Artifact verification, negative controls, external review, owner's release decision | PLANNED |

### Measurement, not mythology

Compare each candidate with (a) the author's original material, (b) the original AI draft, and (c) an author revision, using blinded human editorial judgments and anchored claim preservation. Measures: claim-level evidence coverage; unsupported autobiographical claims (target: **zero**); venue-policy violations (target: **zero**); author's rating of whether the ideas are genuinely theirs; external editor ratings of specificity/clarity; number of factual distortions introduced; transformations disclosed; author acceptance. Report denominators, uncertainty and source provenance. **No target for AI detector score.**

### Adversarial negative controls

1. A human-only venue plus an AI-generated/AI-assisted submission **HOLD** even when the detector gives 0%.
2. A first-person experience backed only by hypothetical model text **HOLD**.
3. A source claim with wrong exact quote or digest **HOLD**.
4. A source lacking explicit consent **HOLD**.
5. A human-authored claim is **self-declared**, never certified by a file label.
6. No randomly inserted typos, fabricated admissions, staged personal scenes or detector-driven paraphrasing.
7. Existing v4–v8 releases, packages and tests remain unmodified until the proper integration wave.

## Required correction to existing craft guidance

`references/anti_patterns/cadence.md` currently says to alternate sentence lengths by formula to avoid a detector. `references/anti_patterns/structures.md` even gives a purported statistical "human" variance target and instructs making the pattern look random. Those prescriptions conflict with the later v7 ban on evasion and can actively reduce authorial fidelity. WI9-05 should replace this with the rule: **revise for meaning, voice, clarity and evidence; let cadence result from the author's thinking and genre.** Detector-oriented rewriting has no release role.

## Venue example: HARO miniature worlds

The author confirmed experience building, collecting and designing physical miniatures, digital worlds, and scale simulations. The organizational blueprint describes game design and infrastructure research; it is not a dated account of a completed specific build. An invented "solar community model" is illustrative, not firsthand. An AI-generated essay remains AI-generated regardless of how natural it sounds. For a human-only journalist, the permitted output is source research and interview prompts, not an AI-written email for submission.

## Decision

**PROPOSAL ONLY.** Prototype tests are separate from author ownership, editor signoff, ethical eligibility, or a version-9 release. Review the PR, check the independent tests and accept/reject each program wave explicitly.
