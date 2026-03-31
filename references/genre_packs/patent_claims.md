# Genre Pack: Patent Claims & IP Writing

## Weighting Adjustments

| Category | Weight Modifier | Reason |
|---|---|---|
| Specificity | +5 | Claims define the boundary of legal protection; vagueness = vulnerability |
| Clarity | +5 | Examiners, judges, and juries must parse every word |
| Argument Strength | +5 | Prior art arguments must be airtight |
| Evidence Discipline | +3 | Every assertion of novelty must be grounded |
| Density | +3 | Patent documents are read word-by-word by adversaries |
| Rhythm | -8 | Patent prose follows functional conventions, not aesthetic ones |
| Memorability | -8 | Precision is the exclusive virtue |

## Architecture

### Utility Patent Application

1. **Title**: Descriptive, not marketing. "System and Method for [Functional Description]"
2. **Cross-References**: Related applications, continuations, provisionals
3. **Field of the Invention**: One sentence identifying the technical domain
4. **Background**: Prior art landscape. What exists. What doesn't work. What gap remains.
   - NEVER admit your own invention is obvious in hindsight
   - Frame the gap as a technical problem, not a market opportunity
5. **Summary**: High-level description of the invention solving the identified gap
6. **Brief Description of Drawings**: Figure list with one-line descriptions
7. **Detailed Description**: Full technical disclosure enabling one skilled in the art to practice the invention
   - Describe every embodiment
   - Describe every alternative
   - Use consistent terminology (same component = same name throughout)
8. **Claims**: The legally operative section. Everything else supports this.

### Claim Structure

#### Independent Claims
Broadest protection. Three parts:
- **Preamble**: "A system for..." / "A method comprising..." / "A non-transitory computer-readable medium..."
- **Transitional phrase**: "comprising" (open-ended, allows additional elements), "consisting of" (closed, limits to listed elements), "consisting essentially of" (middle ground)
- **Body**: Elements listed with relationships specified

#### Dependent Claims
Narrow from an independent claim. Add specificity.
"The system of claim 1, wherein the processor further performs..."

### Claim Drafting Rules

1. **Antecedent basis**: First mention uses "a" or "an." Subsequent mentions use "the" or "said."
   "A processor configured to receive a signal" → "The processor transmits the signal"

2. **Definiteness**: Every term must have one clear meaning in context. If a term could be ambiguous, define it in the specification.

3. **Breadth strategy**: Independent claims as broad as prior art allows. Dependent claims create fallback positions if the independent claim is narrowed.

4. **Means-plus-function**: "Means for [function]" invokes 35 U.S.C. § 112(f) and limits the claim to disclosed structures. Use deliberately or avoid entirely.

5. **Method claims**: Use active gerunds: "receiving," "processing," "transmitting," "generating," "determining." Each step is a verb phrase.

6. **System claims**: Define components and their interconnections. "A first module configured to [function], operatively coupled to a second module configured to [function]."

7. **No negative limitations unless necessary**: "Without X" is harder to enforce than "comprising Y."

## Voice Notes

### Patent Prose Conventions
- Use "embodiment" not "version" or "implementation"
- Use "configured to" not "designed to" or "intended to"
- Use "operatively coupled" or "in communication with" for connections
- Use "plurality" for "more than one"
- Use "substantially" for approximate equality (legally meaningful term)
- Use "at least one" not "one or more" (both work, pick one and be consistent)
- Avoid: "important," "novel," "inventive," "unique" — the examiner decides novelty
- Avoid: Absolute terms ("always," "never," "must") unless technically accurate
- Avoid: Marketing language entirely

### Specification Principles
- Enable: Enough detail that a skilled practitioner could build it
- Describe: Every element of every claim must appear in the specification
- Best mode: Disclose the best way to practice the invention (required in US)
- Written description: Prove you possessed the invention at the time of filing

### Prior Art Discussion
- Acknowledge prior art honestly (withholding known prior art is inequitable conduct)
- Distinguish on technical grounds, not commercial grounds
- Frame prior art limitations as technical problems, not competitive failings
- Never disparage prior art — describe its limitations factually

## Section-Specific Guidance

### Background Section Strategy
The background establishes WHY the invention matters by framing the problem.

Do:
- Describe the technical problem with specificity
- Identify what prior art approaches exist
- Identify the specific technical limitation those approaches share
- Make the gap feel like a genuine technical barrier, not an oversight

Don't:
- Admit the solution is obvious
- Use "it would be desirable to..." (signals obviousness)
- Describe the market opportunity (examiner doesn't care)
- Overstate the problem (undermines credibility)

### Claims Section Strategy
- Claim 1: Broadest independent method claim
- Claim 2-5: Dependent method claims adding specificity
- Claim 6: Broadest independent system claim (mirrors Claim 1)
- Claim 7-10: Dependent system claims
- Claim 11: Computer-readable medium claim
- Claim 12+: Additional embodiments and variations

### Continuation / CIP Strategy
- File continuations to pursue different claim scope from the same priority date
- CIPs for new matter that builds on the original disclosure
- Provisional applications to establish early priority dates

## Common Failures

- Claims that are too narrow (protect nothing competitors care about)
- Claims that are too broad (prior art will invalidate them)
- Missing antecedent basis (indefinite claims are invalid)
- Specification that doesn't support the claim language
- Background section that makes the invention sound obvious
- Inconsistent terminology between specification and claims
- Failure to disclose alternative embodiments (limits claim interpretation)
- Method claims with no clear order of operations
- System claims with no clear interconnections between components
