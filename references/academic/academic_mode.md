# Academic Mode

## Purpose

This module extends the writing compiler for college and scholarly contexts.
It adds discipline-specific reasoning, rubric compliance, citation intelligence,
authorship provenance, and anti-hallucination rules. Under v9 (a proposal on PR #8, not a release) it also yields to the institution's integrity policy: see "v9: Academic Integrity" at the end of this file.

---

## Course Rubric Compiler

Before drafting, extract from the assignment prompt:

1. **Prompt verbs**: argue, analyze, compare, evaluate, describe, explain, discuss, assess, critique, synthesize
2. **Grading criteria**: What does the rubric actually reward? (thesis clarity, evidence quality, source diversity, counterargument engagement, formatting, citations)
3. **Hidden expectations**: Length signals (3-5 pages ≠ 10 pages), source count expectations, required types of sources (primary vs secondary, peer-reviewed vs popular)
4. **Prohibited moves**: "Do not summarize the plot" / "Avoid personal anecdotes" / "Do not use first person"
5. **Required evidence types**: Textual evidence, statistical, experimental, historical, interview-based
6. **Citation style**: APA, MLA, Chicago, discipline-specific
7. **Target depth**: Survey-level vs deep-dive on narrow claim

Map every section of the draft to a rubric criterion. If a criterion has no
corresponding section, the draft is incomplete.

---

## Claim-Evidence Binding

Tag every paragraph:

- **Claim**: The paragraph's argument or sub-argument
- **Evidence**: Source material, data, quotes, examples supporting the claim
- **Explanation**: How the evidence supports the claim (the interpretation)
- **Implication**: What follows from this for the broader argument

Fail any paragraph that:
- Only claims (no evidence)
- Only presents evidence (no interpretation)
- Presents evidence that doesn't connect to the paragraph's claim
- Contains a claim that contradicts evidence in another paragraph

---

## Citation Intelligence

### Coverage Audit
- Every factual claim must have a citation within 2 sentences
- Every quoted phrase must have an immediate in-text citation
- Every paraphrased idea must have attribution

### Source Quality Ranking
- Tier 1: Peer-reviewed journals, primary sources, government data
- Tier 2: Academic books, institutional reports, established journalism
- Tier 3: Trade publications, reputable news, expert blogs
- Tier 4: Wikipedia, social media, opinion pieces, anonymous sources
- Flag if more than 30% of citations are Tier 3 or below

### Paraphrase Distance
- A paraphrase must change both vocabulary AND sentence structure
- Swapping 2-3 words in an otherwise identical sentence is not paraphrasing — it's plagiarism
- Rule: If you covered the original and wrote from memory, would it come out this close? If not, rewrite.

### Over-Quotation Detection
- Flag if direct quotes exceed 15% of total word count
- Flag block quotes not preceded by introduction AND followed by analysis
- Every quote must earn its direct-quote status. If the exact words don't matter, paraphrase.

---

## Discipline-Specific Reasoning

### Humanities
Primitives: symbol, motif, contrast, irony, diction, tone, arc, subtext, close reading
Evidence type: Textual — specific passages, word choices, structural observations
Avoid: Plot summary presented as analysis. Personal reaction without textual grounding.

### Social Sciences
Primitives: structure, agency, norm, institution, stratification, causation, correlation
Evidence type: Studies, datasets, survey data, case analysis
Avoid: Confusing correlation with causation. Citing methodology without evaluating it.

### STEM
Primitives: variable, control, method, hypothesis, result, limitation, replication
Evidence type: Experimental data, mathematical proof, peer-reviewed findings
Avoid: Vague language where precision is possible. "Significant" without statistical context.

### History
Primitives: chronology, causation, continuity, rupture, contingency, source evaluation
Evidence type: Primary sources (letters, documents, artifacts), secondary analyses
Avoid: Presentism (judging past by present values without acknowledgment). Treating secondary sources as fact without evaluation.

### Philosophy
Primitives: premise, conclusion, validity, soundness, objection, steelmanning, thought experiment
Evidence type: Logical argument, textual evidence from philosophers, counterexample
Avoid: Asserting without arguing. Dismissing opposing views without engaging them.

### Business
Primitives: option, tradeoff, incentive, risk, feasibility, implementation, ROI
Evidence type: Case studies, financial data, market analysis, comparable precedents
Avoid: Recommendation without risk assessment. Feasibility claims without resource analysis.

---

## Anti-Hallucination Rules (ABSOLUTE)

1. Do not invent quotations. If you can't find the exact words, paraphrase and cite the source.
2. Do not invent page numbers. If you don't know the page, cite the work without a page number.
3. Do not invent studies. Every "study found that..." must name the study.
4. Do not invent statistics. Every number must be traceable to a source.
5. Do not pretend certainty. If the evidence is mixed, say so.
6. Do not cite a source you did not read. If working from a secondary source, say "as cited in."

Violation of any rule above is an automatic fail condition.

---

## Authorship Proof Layer

For contexts where a course, journal or institution asks how the work was produced, keep an honest record of the work as it actually happened. This layer documents a person's real process; it does not manufacture a history. A log written after the fact to look like drafting, or a revision trail produced by a model, is a false record.

### Draft Provenance
Maintain a log: outline → rough draft → revision 1 → revision 2 → final.
Each version should show meaningful changes, not cosmetic ones.

### Revision Fingerprint
Document what changed between drafts and why. "Moved counterargument to paragraph 4 because it addressed the reviewer's strongest objection before my weakest evidence."

### Idea Origin Map
For each major claim, identify:
- Student's original idea
- Idea from lecture or class discussion (name the date/topic)
- Idea from a source (cite it)
This makes the intellectual work traceable.

### Oral Defense Prep
Generate 10 questions a professor would likely ask about this paper:
- "Why did you choose this thesis over alternatives?"
- "How does your argument handle [specific counterargument]?"
- "What's the weakest point in your evidence?"
- "If you had another 2,000 words, what would you add?"
- "How does [Source A]'s framework compare to [Source B]'s?"

---

## Class-Note Anchoring

Ground the paper in the specific class context:

- Use the professor's terminology (not synonyms from the internet)
- Reference assigned readings by name
- Engage with class debates and discussions
- Frame the argument within the course's intellectual trajectory
- Acknowledge the specific lens the course applies (Marxist, feminist, empiricist, etc.)

This is not a way to appear original. It is the ordinary discipline of a student who attended the class: the course vocabulary, assigned readings and debates are what the argument is actually about. Do not insert them from a syllabus the student has not engaged with; a reference to a lecture the student did not hear is an invented memory.

---

## Paragraph Blueprints (Academic)

### Thesis Paragraph
Claim → Context → Scope → Roadmap (optional, only if the paper is long enough)

### Close-Reading Paragraph
Quote (short) → Observation about diction/structure/imagery → Interpretation → Connection to thesis

### Compare/Contrast Paragraph
A's position → B's position → Point of divergence → Significance of divergence

### Literature Review Paragraph
Source summary → Evaluation of method/scope → Gap identification → How this paper fills the gap

### Method Paragraph
Approach → Justification → Limitations acknowledged

### Rebuttal Paragraph
Strongest counterargument → Concession (what's true) → Pivot (where it fails) → Counter that survives

### Conclusion Paragraph
Synthesis (not summary) → Implication → Earned question or challenge

---

## Revision Stack (Academic)

Run these passes in order:

1. **Rubric pass**: Does every criterion have corresponding content?
2. **Evidence pass**: Is every claim supported? Every source real?
3. **Structure pass**: Do sections build? Is the thesis in the right place?
4. **Paragraph pass**: Does every paragraph have a job and perform it?
5. **Voice pass**: Does this reflect how this student writes and thinks? (Compared with the student's own consented samples, never as proof of authorship.)
6. **Citation pass**: Format correct? Coverage complete? Paraphrase distance sufficient?
7. **Compression pass**: Can any paragraph lose 20% without damage?
8. **Final polish pass**: Anti-slop check. Rhythm repaired from meaning, not from quotas. Opening and closing audit.

---

## v9: Academic Integrity

The policy of the course, journal or institution comes first (principle WI9-G). Everything above is subordinate to it.

**1. Read the policy before drafting.** Identify which of three situations applies, and record it: the assignment or venue is **human-only** (no AI drafting, rewriting or paraphrasing of submitted text); it allows AI **with disclosure** (state what was used for, in the form the venue asks); or it is **unrestricted** for this use. If the policy is unknown or ambiguous, ask the instructor or editor. Do not guess in the permissive direction.

**2. Human-only means the student's own sentences.** In a human-only context the system may explain a concept, find the questions a rubric asks, check that a student's own citations are formatted correctly, and quiz the student; it must not write or rewrite the submitted prose. "Writing in the student's voice" does not change who wrote it. Passing a draft through a rewriting step to hide its origin is a misrepresentation.

**3. Disclosure is specific.** Where disclosure is allowed or required, name the tool, the task (for example "suggested a clearer topic sentence in paragraph 3; the student rewrote it") and the extent. A contribution log distinguishes mechanical proofreading, a suggested edit, an authored revision and substantive generation (principle WI9-I). The authorship dossier checker (`scripts/wi-authorship.py`, experimental) can record this; it is a declaration checker, every report states `declaration_status: self_reported`, and it cannot verify that a student wrote anything.

**4. No invented citations.** The Anti-Hallucination Rules above are absolute and sharpened here: every source named has been read and exists; every quotation is copied from the source with its location; "as cited in" is used for a secondary source; if a source cannot be found, the claim is cut or marked `needs_source`, never given a plausible reference. In the dossier model, each consequential claim must overlap an anchored evidence span, and a source whose bytes have changed since it was pinned is stale.

**5. Authorship statements.** An "I wrote this" or "no AI was used" statement is the student's own declaration and is made by the student. The system does not make it for them, and a clean phrase-catalog scan or a low detector reading is not evidence for it. Detector readings are noisy, are not a record of authorship, and are not used as a target.

**6. When not to fix.** A phrase-catalog hit in an academic draft is an editorial question. "A growing body of research suggests ..." stays when the next sentences name the studies (`generic_claim` asks whether a source, date or sample can be identified). "It should be noted that the sample excludes participants under 18" is a limitation, not padding. A direct quotation is left exactly as the source has it even when it contains a flagged phrase. Record the call with `retain_as_written`, `revise_for_clarity`, `needs_source` or `not_applicable` in the review ledger (`prototypes/wi9/wi9_phrase_review.py`).

**7. Fiction and creative writing courses.** v9 does not change fiction gates. The venue rule in point 2 still applies to a creative-writing assignment's integrity policy.
