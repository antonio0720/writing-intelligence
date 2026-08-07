# The Concept Registry

The Semantic ABI. A stable contract for the concepts an organization is externally accountable for, enforced across every artifact that mentions them.

**Status: executable — `wi test`.**

Software has an ABI because a caller and a callee that disagree about a struct layout produce a crash rather than a silent wrong answer. Prose has never had one. Two documents that disagree about what a number means produce a silent wrong answer, delivered to a reader who has no way to detect it, usually years after anyone could say which document was right.

Read this with [`SEMANTIC_IR.md`](SEMANTIC_IR.md) — a registered concept is a `meaning.*` node with a stable identity — and [`STALENESS.md`](STALENESS.md), which propagates a registry change to every use site.

---

## 1. The problem

An organization does not have one document.

It has a policy book, a pitch deck, a website, an FAQ, a training guide, a set of contracts, a social content calendar, a video script library and a page of executive talking points. Nine artifact families, six owners, four tools, and no shared definition of anything.

So the same concept drifts:

| Artifact | What it says |
|---|---|
| Policy book, ch. 4 | "the program has operated since 2019" |
| Pitch deck, slide 3 | "seven years of operation" |
| Website, About page | "founded 2018" |
| FAQ | "we launched in the spring of 2019" |
| Training guide | "the program's first full year was 2020" |
| Contract, recital B | "the Program, established January 1, 2019" |
| Executive talking points | "almost a decade" |

Nobody lied. Six of the seven are defensible readings of a genuinely fuzzy history. But one of them is in a contract, one of them is in front of a funder, and there is no artifact anywhere in the organization that states what the answer is.

**The registry makes the concept the primary object and every artifact a use site.** Change the concept once and every use site is either correct, mechanically updated, or reported as failing. That is the whole idea, and everything below is the mechanism.

---

## 2. The registry

**Status: executable in `scripts/wi.py`.**

```yaml
# .wi/concepts.yaml
schema_version: wi-concepts-1

concepts:

  program_start:
    kind: temporal
    value: 2019-01-01
    granularity: day
    definition: >
      The date the program began serving households under its own
      operating authority. Not the date of incorporation, and not the
      date of the first grant award.
    realm: external_fact
    anchors: [a-0021]
    definition_state: sha256:5c0e19a4…
    owner: program_operations

  service_area_counties:
    kind: integer
    value: 7
    invariant: "must equal the row count of counties.csv"
    definition: >
      Counties in which the program holds an active service agreement
      as of the current fiscal year.
    realm: external_fact
    anchors: [a-0044]
    definition_state: sha256:9b41c70d…
    owner: program_operations

  annual_award_ceiling:
    kind: money
    amount: 2400000
    currency: USD
    basis_year: 2026
    definition: >
      The maximum total award a single subrecipient may receive across
      all instruments in one fiscal year, exclusive of in-kind support.
    realm: external_fact
    legal_force: representation_in_funding_application
    anchors: [a-0102]
    definition_state: sha256:1f77ab30…
    owner: finance

  household:
    kind: defined_term
    definition: >
      One or more persons occupying a single dwelling unit and sharing
      a budget for food and housing costs, counted once per fiscal year
      regardless of the number of services received.
    allowed_aliases:   [households, the household, HH]
    forbidden_aliases: [family, families, client, clients, case, cases, unit]
    realm: external_fact
    definition_state: sha256:be31d0f2…
    owner: program_operations
```

### 2.1 Allowed aliases, forbidden aliases, and why the second list exists

A renderer may use an allowed alias for brevity. `HH` in a table header is not a different concept from `household`, and forcing the full term into a column that is four characters wide produces worse documents, not more rigorous ones. Allowed aliases are registered so that a use site written with one still binds to the concept and still participates in impact analysis.

The forbidden list is the interesting half. It exists because **when a stronger synonym is invented, the terminology test fails.**

`family` is not a synonym for `household`. It is warmer, it is shorter, it reads better in a grant narrative, and it asserts something the registered definition does not — a relationship between the occupants. `client` imports a service relationship. `case` imports a file. Each substitution is a small improvement in prose and a small unregistered change in what is being claimed, and the sum of forty such improvements across nine artifact families is an organization whose headline number means something different in every document that carries it.

The registry does not forbid the words. It forbids them **as renderings of this concept**, and the check is deterministic: a use site bound to `household` that renders as `families` fails `no_old_brand_term`-style terminology assertion with the concept, the site and the offending token named.

`definition_state` is the digest of the canonical definition payload. It is what a `uses_term` edge binds to, so a change to the definition text — not to its formatting — puts all 900 use sites into `review` under the per-edge policy in [`STALENESS.md`](STALENESS.md).

---

## 3. Document contracts

**Status: executable in `scripts/wi.py`.**

A registry entry says what a concept is. A contract says which artifacts are obligated to it.

```yaml
# .wi/contracts.yaml
contracts:

  - id: ct-001
    concept: program_start
    assert: equals
    value: 2019-01-01
    applies_to:
      - "manuscript/**/*.md"
      - "deck/**/*.yaml"
      - "web/**/*.html"
      - "contracts/**/*.docx"
    severity: block

  - id: ct-002
    concept: service_area_counties
    assert: equals
    value: 7
    applies_to: ["manuscript/**/*.md", "deck/**/*.yaml", "social/**/*.md"]
    severity: hold

  - id: ct-003
    concept: annual_award_ceiling
    assert: equals
    value: {amount: 2400000, currency: USD, basis_year: 2026}
    applies_to: ["contracts/**/*.docx", "manuscript/ch-11-*.md"]
    severity: block

  - id: ct-004
    concept: household
    assert: term_binding
    applies_to: ["**/*.md", "**/*.html", "**/*.yaml"]
    exempt:
      - path: "manuscript/ch-02-voices.md"
        reason: "Quoted interview transcripts; participants' own words are preserved."
        approved_by: a.rivera@example.org
    severity: hold
```

Globs scope obligation, and scoping is not a convenience. A social post is not held to the contract's currency-basis-year precision, and a contract recital is not held to the social calendar's brevity. Applying every assertion to every file produces a wall of failures on artifacts that were never in scope, which is the pattern that gets test suites deleted.

The `exempt` block is a recorded human decision with a reason and a named approver — never a silent skip, and never a pattern-matched exclusion nobody signed.

---

## 4. Writing tests

**Status: executable — `wi test`.**

This is the headline feature of the concept registry: **software tests for prose.**

Not a style score. Assertions, in a file, in version control, that pass or fail against a manuscript the way a unit test passes or fails against a function.

```yaml
# .wi/tests/suite.yaml
schema_version: wi-tests-1

# ---------- structural ----------------------------------------------------

- id: every_promise_chapter_has_fiscal_identity
  group: structural
  description: Every chapter that makes a promise states who is financially bound.
  select: "chapter[type=promise]"
  require:
    node: fiscal_identity
    within: self
  severity: block

- id: no_orphan_footnotes
  group: structural
  description: Every footnote is referenced, and every reference resolves.
  assert: bijection
  between: ["footnote.definition", "footnote.reference"]
  severity: hold

# ---------- evidence ------------------------------------------------------

- id: every_strict_claim_has_support
  group: evidence
  description: In strict scopes, every factual claim atom carries a resolvable anchor.
  select: "meaning.claim_atom[realm=external_fact][evidence_policy=strict]"
  assert: "evidence.coverage == 1.0"
  report: enumerate_failures
  severity: block

- id: no_conflicting_defined_terms
  group: evidence
  description: No registered term has two live definitions.
  select: "meaning.definition"
  assert: "count(definitions_per_term) == 1"
  severity: block

# ---------- arithmetic ----------------------------------------------------

- id: sources_equal_uses
  group: arithmetic
  description: The budget's sources column totals to its uses column.
  table: "budget_summary"
  assert: "sum(column.sources) == sum(column.uses)"
  tolerance: {absolute: 1.00, currency: USD}
  tolerance_reason: "Per-line rounding to whole dollars across 214 lines."
  severity: block

# ---------- canon ---------------------------------------------------------

- id: no_character_post_death_without_exception
  group: canon
  description: A character does not act after their death event.
  select: "canon.character"
  assert: "no scene.narrates(action_by=character) with timeline_point > character.death_event"
  unless: "scene.has_exception in [flashback, vision, unreliable_narrator, resurrection_rule]"
  severity: hold

# ---------- terminology ---------------------------------------------------

- id: no_old_brand_term
  group: terminology
  description: The pre-2025 program name does not appear in published artifacts.
  forbidden: ["Regional Uplift Initiative", "RUI", "the Uplift program"]
  applies_to: ["**/*.md", "**/*.html", "deck/**/*.yaml"]
  exempt: ["manuscript/appendix-c-history.md"]
  severity: hold
```

The five groups, and what each one catches:

| Group | Asserts about | Catches |
|---|---|---|
| structural | The shape of the work | A promise chapter with no party bound to it; a footnote pointing at nothing |
| evidence | Anchors and coverage | An unsupported claim in a scope that requires support |
| arithmetic | Numbers that must reconcile | A budget that does not balance; a percentage that does not derive from its inputs |
| canon | Constructed-world consistency | A dead character with a line in chapter 40 |
| terminology | Registered concept renderings | A retired brand name in a live deck; `families` where `households` was registered |

**The design rule: writing tests should be small, composable and visible in release reports.**

*Small*, because a test that asserts six things names none of them when it fails. `every_promise_chapter_has_fiscal_identity` asserts exactly one thing and its failure message is a chapter number and a missing node.

*Composable*, because the groups overlap in real documents and must not have to know about each other. The budget test does not know what a canon rule is. The canon rule does not know what an anchor is. Each is a predicate over a graph query, and predicates compose.

*Visible in release reports*, because a test that only runs in CI is a test that only protects the pipeline. The suite's results — every test, its group, its status, and the enumerated failures — appear in the release report a human reads and in the `.wiab` bundle a stranger verifies offline. A passing suite that nobody sees is indistinguishable from no suite.

---

## 5. Epistemic CI/CD

**Status: executable in `scripts/wi.py`.**

```bash
# .git/hooks/pre-commit
#!/bin/sh
python3 scripts/wi.py test --changed-only --exit-code || {
  echo "Writing tests failed. Run: python3 scripts/wi.py test --explain"
  exit 1
}
```

```yaml
# .github/workflows/writing.yml  (excerpt)
- name: Writing tests
  run: python3 scripts/wi.py test --exit-code

- name: Impact analysis on changed sources
  run: python3 scripts/wi.py impact --since origin/main --exit-code

- name: Release gate
  run: python3 scripts/wi.py gate --mode strict --exit-code
```

Exit codes are the same three the v4 gate has always used, because a build system that speaks a new dialect on each command is a build system nobody wires up:

| Code | Means | CI behavior |
|---|---|---|
| `0` | RELEASE — every test passed, nothing stale | Green |
| `1` | HOLD — failures at `hold` severity, or stale claims under strict | Fail the job; a human can clear it with a recorded waiver |
| `2` | BLOCK — failures at `block` severity, unresolvable citations, or contradictions | Fail the job; no waiver path in regulated mode |

`--changed-only` is what makes the pre-commit hook usable. Running 143 tests across 1,660 pages on every commit takes long enough that developers disable the hook within a week; running the tests whose graph queries intersect the changed nodes takes under a second, and the full suite runs in CI where nobody is waiting.

**Why a 1,660-page manuscript finally gets regression protection.** A book of that size is edited by more than one person over more than one year. Chapter 41 contradicts chapter 9 because the person editing chapter 41 has not read chapter 9 recently and cannot be expected to. Every software project has this problem and solved it decades ago: nobody proofreads a codebase for consistency, they assert the invariants and let a machine enforce them on every commit. Long-form writing has had no equivalent — the copyedit pass is a human re-reading the whole thing, which does not scale, does not repeat, and does not report what it checked. A test suite over an authorship graph is the first mechanism that behaves like a regression suite at the level that actually matters: what the document claims, not how it is spelled.

---

## 6. Coverage must have a denominator

**Status: executable in `scripts/wi.py`.**

```
$ python3 scripts/wi.py test --coverage

Evidence coverage   1,784 of 1,820 required claim atoms   (98.0%)

  denominator   claim atoms where realm=external_fact and evidence_policy=strict,
                at graph state sha256:71b4e8…
  excluded      412 rhetorical · 96 hypothetical · 240 author_observation ·
                1,106 fictional_canon   (realm-tagged; not required to anchor)

Missing (36) — enumerated:

  c-0418  ch-07 p-0902   "…serves the region's highest-need corridors."
  c-0419  ch-07 p-0903   "…a figure that has risen every year since."
  c-0733  ch-11 p-1140   "…the largest program of its kind in the state."
  …
  c-1802  ch-38 p-2214   "…most subrecipients report improved capacity."

  full list: .wi/reports/coverage_missing.json
```

**"Evidence coverage 98%" is not a statement until it is 1,784 of 1,820 and the 36 are on screen.**

The percentage alone fails three ways at once. It has no denominator, so a reader cannot tell whether the population is every sentence in the book or the eleven claims someone remembered to tag. It has no membership, so nobody can act on it. And it is a `measured` line rendered as if it were a summary judgment, which is the bare-percentage construction banned in [`RELIABILITY_TYPES.md`](RELIABILITY_TYPES.md).

**No dashboard number without clickable membership.** Every count this system prints resolves to a list, and every list resolves to nodes with locations. That rule is what separates a coverage report from a progress bar. A progress bar tells you how you are doing; a coverage report tells you what to do next, and the 36 rows above are the actual work.

The exclusions are itemized for the same reason. A denominator that quietly drops 1,106 canon claims and 240 author observations would post a better number by narrowing the population, and narrowing a population without saying so is how coverage metrics become theater everywhere they are used.

---

## 7. What this is not

Three refusals, each one a thing this feature will be mistaken for.

**It is not a style score.** No test in the suite has an opinion about sentence rhythm, word choice, register or elegance. The craft kernel does that work and its output is proposals, not verdicts. A writing test asserts a fact about what the document claims — a term binding, a total, a coverage requirement, a canon rule. A suite that passes says nothing about whether the prose is any good.

**It is not a quality number.** There is no aggregate. The suite reports per-test results, and it will never blend them, because a manuscript passing 142 of 143 tests is described by *which one failed* and by nothing else. `142/143` looks like a grade and behaves like one — it invites comparison across projects with different suites, and it lets a failing `block` test disappear into a healthy-looking ratio.

**It is not a substitute for a reader.** Every assertion in this document is something someone thought to write down. A test suite catches the drift you predicted and the drift that recurs; it has nothing to say about the paragraph that is technically accurate and completely misleading, the chapter that is consistent and unnecessary, or the sentence that will be read by a program officer as an admission. Those need a person, and a green suite must never be presented as though it stood in for one.

**Why the third refusal is stated last and stated plainly.** Automated checks quietly redefine what counts as review. The failure mode is not that people trust the tests too much in principle; it is that on the fourth deadline in a month, "the suite is green" becomes the answer to "did anyone read chapter 12," and nobody involved ever decided to make that trade.

---

## 8. What is executable and what is specified

| Mechanism | Status |
|---|---|
| The concept registry, alias lists and `definition_state` digests | Executable in `scripts/wi.py` |
| Document contracts with glob scoping, severities and recorded exemptions | Executable in `scripts/wi.py` |
| `wi test` and the five test groups above | Executable in `scripts/wi.py` |
| `--changed-only`, `--explain`, `--exit-code`, `--coverage` with enumerated membership | Executable in `scripts/wi.py` |
| Test results in release reports and in the `.wiab` bundle | Executable in `scripts/wi.py` |
| Arithmetic assertions over tables bound to a spreadsheet adapter | Specified — awaiting the `sheet_range` adapter in [`EVIDENCE_ANCHORS.md`](EVIDENCE_ANCHORS.md) |
| Terminology enforcement inside non-text renderings — audio, video, captions | Specified |
| Cross-workspace registries shared by several works | Specified |

---

## Related documents

- [`SEMANTIC_IR.md`](SEMANTIC_IR.md) — definitions, terms and constraints as `meaning.*` nodes
- [`STALENESS.md`](STALENESS.md) — what a definition change does to 900 use sites
- [`SEMANTIC_DIFF.md`](SEMANTIC_DIFF.md) — `definition_changed` and `terminology_changed`
- [`AUTHORSHIP_GRAPH.md`](AUTHORSHIP_GRAPH.md) — `defines`, `uses_term` and the canon family
- [`RELIABILITY_TYPES.md`](RELIABILITY_TYPES.md) — why coverage carries a denominator
- [`CONSTITUTION.md`](CONSTITUTION.md) — Law G, meaning has identity independent of wording
- [`../v4/PROOF_PROTOCOL.md`](../v4/PROOF_PROTOCOL.md) — the gate and its exit codes
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
