# Architecture Decision Record — Template

Use this template to record significant architectural decisions in Writing Intelligence.
ADRs live in `governance/adrs/` (created on demand).

An ADR is written for the person who arrives in two years, finds the decision inconvenient,
and needs to know whether it was reasoned or accidental. Write for them. The most valuable
line in most ADRs is the one naming the failure the decision prevents, because that is the
one a later reader cannot reconstruct from the code.

Keep it short. An ADR nobody finishes reading is an ADR nobody consults.

---

```markdown
# ADR-NNNN: <Title>

**Status**: proposed | accepted | superseded | deprecated
**Date**: YYYY-MM-DD
**Author**: <github handle>
**RFC**: # (if this decision came out of one)
**Supersedes**: ADR-NNNN (if applicable)
**Superseded by**: ADR-NNNN (if applicable)

## Context

The situation that requires a decision, and the forces at play. What is true today
that makes this a question? What breaks if nobody decides?

## Decision

What we decided to do. One paragraph. Present tense.

## The failure this prevents

Name it concretely. Not "improves consistency" — the specific thing that goes wrong
without this decision, and what it looks like on the screen of somebody who does not
know it went wrong. If the failure is loud, say so; a loud failure is a weaker
argument than a silent one and the ADR should be honest about which it is.

## Laws touched

The eighteen laws are in `references/v6/CONSTITUTION.md`. Name the letters, or write
`none`.

| Law | Implements / constrains / changes |
|---|---|
| <A–R> | |

A decision that *changes* a law is maintainer-led and needs an accepted RFC. A
decision that *implements* one is ordinary work. Say which.

## Digest impact

Tick exactly one. Silence is treated as an unanswered question, not as `none`.

- [ ] **None.** Evidence: `wi canon` over the fixture world before and after, unchanged
- [ ] **v6 state digest** — every object of the affected schema moves
- [ ] **Graph root** — every branch head, decision binding and simulation comparison
      restates
- [ ] **Capsule closure root** — every `.wic` already issued fails verification

Anything but the first is a MAJOR act. See `governance/VERSIONING.md`. State which
object kinds move and what a holder of an existing artifact should do.

## Capability impact

- New or renamed capability string(s), or `none`:
- Delta class(es) that would require it:
- Effect on existing grants:

`V6_CAPABILITIES` is closed at sixteen and `wi authority issue` refuses anything
outside it. The test for adding one is not whether it names something real — it is
whether any organization would grant one of a pair and withhold the other. Renaming
one turns every grant naming it into a grant nothing recognises.

## Negative fixture

The fixture that fails when this decision is reverted or its implementation disabled.

- Asserts:
- Disable this to make it red:
- Lives in:

If there is no such fixture, say so and say why. A decision whose implementation
cannot be shown failing has not been shown to do anything, and its green line is
indistinguishable from a broken one.

## Migration burden on existing capsules

What this costs somebody holding a `.wic`, a `.wiab`, a workspace or a decision
record produced before this decision. Answer even when the answer is `none`.

If a previously-verifying artifact now fails: state what it reports, why that wording
is wrong for what happened, and where the reader will find the explanation. A verifier
that cries tampering after an upgrade is a verifier nobody believes the next time.

## Consequences

### Positive
- ...

### Negative
- ...

### Neutral
- ...

## Alternatives considered

- **Option A**: <description>. Rejected because <reason>.
- **Option B**: <description>. Rejected because <reason>.

The rejected option somebody will propose again belongs here, with the reason stated
in a form that survives being read out of context.

## Implementation notes

How this gets built. Files affected. Order of operations. Anything that must land in
the same commit.

## Validation

How we know this was the right call. Benchmark cases, graph constraints, diagnostic
signals, or the specific command whose output changes.
```

---

## Reference ADRs

**v3.0 foundational** — authored as part of v3.0, to be added to `governance/adrs/`:

- ADR-0001: Adopt the 11-pass kernel as foundation
- ADR-0002: Make schemas first-class
- ADR-0003: Mandate the Epistemic Ledger in high-stakes domains
- ADR-0004: Adopt the Genre Stack Engine (multi-pack composition)
- ADR-0005: Decompose the kernel into specialist agents
- ADR-0006: Establish benchmark regression gates
- ADR-0007: Establish operator certification tiers

**v6.0 decisions worth recording**, each already reasoned in `references/v6/` and not yet
written up as an ADR:

- The semantic state is canonical and a rendering is a build (`EXECUTABLE_MEANING.md`)
- Domain separation between the v5 and v6 digests (`SEMANTIC_IR.md`, `CANONICAL_HASHING` in
  `references/v5/`)
- A graph root is pure state — no timestamp, no author, no counter
  (`SEMANTIC_VERSION_CONTROL.md`)
- Sixteen capabilities rather than four (`AUTHORITY_MODEL.md` §3)
- Delegation monotonicity checked at issue time rather than at use time
  (`AUTHORITY_MODEL.md` §6)
- Conflicts preserved rather than resolved (`MERGE_PROTOCOL.md` §5, `NON_GOALS.md` §10)
- Obligations derived from typed state rather than listed in a checklist
  (`PROOF_OBLIGATIONS.md`)
- Two bundles rather than one, and the 200-file ceiling as a build gate
  (`scripts/build-skill.sh`)
