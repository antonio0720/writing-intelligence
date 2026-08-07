# Policy as Code

**Status: executable — `wi.policy.yaml` is read by `gate`, `test` and `bundle`.**

Evidence discipline in v4 was a mode you stated at the top of a report. It was correct, it was honest, and it lived in a sentence. A sentence cannot be hashed, cannot be attached to a release, and cannot be compared against the sentence someone else was working under six months ago.

v5 makes policy an object.

Read this with [`PROOF_CARRYING_RELEASE.md`](PROOF_CARRYING_RELEASE.md), which binds a policy digest into every release manifest, and [`CONSTITUTION.md`](CONSTITUTION.md), whose laws policy may tighten and may never override.

---

## Table of contents

1. Why policy is a file
2. The policy document
3. The five evidence modes as presets
4. Authority policy for teams
5. Plugins may tighten, never loosen
6. Waivers
7. Offline mode
8. What is executable and what is specified

---

## 1. Why policy is a file

**Status: executable — `wi.policy.yaml`.**

When policy is a file, it becomes a **hash-addressed dependency of the release**. Three consequences follow, and each one is the answer to a question that has no good answer otherwise.

| Because policy is hashed | The question it answers |
|---|---|
| The release manifest carries `policy_digest` | *Under what rules was this document checked?* |
| Changing the policy changes the digest, and the gate is re-evaluated | *Would it still pass under the rules we use now?* |
| Two projects can be compared by comparing two digests | *Are we holding these two documents to the same standard?* |

**A policy that lives in someone's head cannot be attached to a release manifest.** That is the whole argument. An organization whose evidence standard is a shared understanding among four experienced people has a real standard right up until one of them leaves, and it has no way to demonstrate the standard to anyone outside the four — which is precisely the audience a proof-carrying release exists for.

The reciprocal rule matters as much: **changing the policy invalidates nothing about the past and everything about the present.** A release built under `policy_digest` A remains verifiable under A forever; a hostile reviewer can read A in the bundle and judge whether it was strict enough. What changing the policy does is force re-evaluation of the *current* workspace. Loosening a rule does not retroactively bless documents that failed under the stricter one, and tightening a rule does not silently retract attestations already issued. Both are recorded state changes, and `wi gate` recomputes from the policy in force.

---

## 2. The policy document

**Status: executable — read by `gate`, `test` and `bundle`.**

```yaml
version: 1

evidence:
  # The baseline discipline for every claim in this project.
  default_mode: strict

  # A "truth claim" asserts that something is true of the world without
  # naming what makes it true. It is prohibited outright: not downgraded,
  # not flagged, not permitted with a warning.
  truth_claim: prohibited

  # Which basis a claim may rest on, per claim class. A class absent from
  # this map falls back to default_mode's basis set.
  allowed_basis:
    statistical:   [verbatim_span, structured_data]
    legal:         [verbatim_span]
    medical:       [verbatim_span, structured_data]
    financial:     [verbatim_span, structured_data]
    attribution:   [verbatim_span]
    definitional:  [verbatim_span, author_declaration]
    experiential:  [author_declaration]
    fictional:     [canon_registry]

proposals:
  # Semantic delta classes that may be applied without a human decision.
  auto_accept:
    - wording_only

  # Everything here requires a recorded human decision, always.
  require_human:
    - scope
    - quantity
    - time
    - entity
    - attribution
    - certainty
    - causality
    - legal_force
    - obligation
    - recommendation
    - definition
    - canon

sources:
  injection:
    # A high-severity injection finding quarantines the source. It does not
    # produce a warning the author can scroll past.
    quarantine_on_high: true

  freshness:
    # Per-selector age limits. A source older than its limit is not wrong;
    # it is flagged stale, and the gate treats stale support per §3.
    default_days: 1095
    rules:
      - selector: "statute|regulation|rule|CFR|USC"
        max_age_days: 180
      - selector: "market|pricing|valuation|rate"
        max_age_days: 90
      - selector: "clinical|trial|guideline|dosage"
        max_age_days: 365
      - selector: "census|ACS|BLS|county metrics"
        max_age_days: 730

release:
  # Conditions that produce BLOCK. The release cannot proceed.
  block_on:
    - unresolved_citation
    - source_contradiction
    - invalid_anchor
    - protected_term_violation

  # Conditions that produce HOLD. The author may proceed with a waiver.
  hold_on:
    - stale_claim
    - judgment_missing
    - waiver_required

privacy:
  # No network access unless a command is explicitly run without --offline
  # and policy is changed here. The default is deny, not prompt.
  network_default: deny

  # Telemetry never contains source text, draft text, claim surfaces,
  # quotes, filenames or author-supplied strings. There is no level at
  # which this becomes configurable.
  telemetry_content: never
```

Section by section:

**`evidence.default_mode`** sets the baseline. Everything else in the section narrows it for particular claim classes; nothing widens it past what the mode permits.

**`evidence.truth_claim: prohibited`** is the sharpest line in the file. A sentence that asserts something about the world and names nothing that makes it true is not a weak claim to be flagged — it is a claim shape this project refuses to emit. The repair is always available and always cheap: attach an anchor, attribute the assertion to a named source, qualify it, or mark it as the author's own declaration under their own authority. All four are honest. Leaving it floating is not.

**`evidence.allowed_basis`** exists because claim classes are not equally forgiving. An experiential claim — *I sat in that waiting room for three hours* — cannot have a verbatim span and should not need one; the honest basis is the author's own declaration, recorded as `human-declared`. A legal claim has exactly one acceptable basis, because a paraphrase of a statute is a new statute. Collapsing these into one rule would either make the system useless for memoir or dangerous for filings.

**`proposals.auto_accept`** contains one entry and should stay that way. `wording_only` is the only delta class where applying a change without asking cannot move an assertion — and it is, for exactly that reason, the class an over-eager classifier reaches for. Under Law E, uncertainty resolves away from `wording_only`, which means a misclassification lands in `require_human` and costs a click rather than a career.

**`sources.injection.quarantine_on_high`** implements Law F at the policy layer. The quarantine boundary is architectural and sits at the adapter; this switch governs what the *gate* does when the scanner returns a high-severity finding. Setting it false is a real option for a project whose sources are all internally authored, and it is a change that shows up in the policy digest of every release afterward.

**`sources.freshness`** is per-selector because a uniform age limit is always wrong in one direction. Three years is generous for a pricing table and absurd for a census cross-tabulation. The selectors match against source metadata and claim class; the limits are the operator's to set. A source past its limit is not rejected — it is stale, and staleness is a `hold_on` condition, which means a human sees it and decides.

**`release.block_on` and `release.hold_on`** are the gate. The split is the v4 verdict language made configurable without being made negotiable: the four `block_on` conditions are the ones where proceeding is not a judgment call, and moving any of them into `hold_on` is a change every future reviewer can see in the bundle.

**`privacy.network_default: deny`** means the tool does not reach the network to be helpful. Not to check a link, not to resolve a DOI, not to fetch a favicon.

**`privacy.telemetry_content: never`** is the one line in this file with no legitimate other value. Counts, error codes, durations and version strings may be collected where an operator has configured collection. Source text, draft text, claim surfaces, quotes, filenames and author-supplied strings never leave the machine. A configurable version of this setting would be an invitation, and the invitation is the problem.

---

## 3. The five evidence modes as presets

**Status: executable — mode presets read by `gate`.**

v4 named five evidence modes. v5 keeps all five, in force, unchanged in meaning — and expresses them as **policy presets rather than adjectives**. A mode is a named set of values for the fields in §2, so "we ran this in strict" becomes a statement with a digest behind it instead of a recollection.

| Mode | Preset | Apply when |
|---|---|---|
| `off` | No claim extraction, no gate. Craft passes only. | Fiction, poetry, personal writing, brainstorming |
| `light` | Claims extracted and listed. No verdict, no blocking. | Blog posts, marketing, internal notes |
| `standard` | Claims classified; unsupported high-risk claims flagged; verdict advisory. | **Default.** Business writing, technical docs, proposals |
| `strict` | Every factual claim needs a resolvable anchor or a stated qualification. Verdict enforced. | Grants, NOFO responses, policy, journalism, investor material |
| `regulated` | Strict, plus: contradictions block rather than hold, and every proceed-anyway is a recorded waiver. | Medical, legal, regulatory, compliance |

The difference between `strict` and `regulated` is worth stating exactly, because it is one field and one behavior: `source_contradiction` moves from `hold_on` to `block_on`, and `waiver_required` becomes reachable on every hold rather than only on evidence holds. Nothing else changes. A mode that changed a dozen things at once would be a mood, not a policy.

**Escalation is automatic and unasked.** Sight of any of these in the work or the request escalates the project to `strict`:

> grant · NOFO · RFP · funder · IRB · regulatory · clinical · filing · prospectus · due diligence · expert report · court · compliance · audit · fact-check

**Why escalation is automatic.** The author who most needs `strict` is the one least likely to ask for it, because they are in the middle of a deadline and the mode is not the thing on their mind. Every item on that list names a context where a reader is adversarial by role — a reviewer paid to find the weakness, a regulator, opposing counsel. Waiting to be asked would mean the discipline arrives exactly when it is not needed. Escalation is announced in the report so the author can move it back down deliberately, which is a different act from never having raised it.

---

## 4. Authority policy for teams

**Status: specified for the multi-actor mechanisms; single-actor policy is executable.**

A solo author is their own reviewer, and the policy above is complete for them. The moment a second person can accept a change, *who may accept what* becomes a question the record has to answer.

```yaml
authority:
  legal_force_change:    requires: legal_reviewer
  financial_figure_change: requires: evidence_reviewer
  canon_retcon:          requires: canon_editor
  final_release:         requires: owner
```

Each rule binds a semantic delta class — the classes from Law H — to a role that must be the deciding actor. A proposal classified `legal_force` cannot be accepted by anyone who does not hold `legal_reviewer`, regardless of who is at the keyboard and regardless of how the request is phrased.

The roles:

| Role | May |
|---|---|
| `owner` | Everything, including changing this policy and cutting a final release |
| `author` | Write, propose, and accept changes not reserved to another role |
| `editor` | Propose and accept craft changes; not reserved delta classes |
| `evidence_reviewer` | Accept changes to figures, anchors and evidence state |
| `legal_reviewer` | Accept changes that alter legal force or obligation |
| `canon_editor` | Accept changes to canonical facts in a constructed world |
| `release_manager` | Build, bundle and attest; not accept semantic changes |
| `viewer` | Read the workspace and its proof state; change nothing |
| `automation` | Act under a configured rule, as `automated_policy`, never as a person |

The review states a node may occupy:

| State | Means |
|---|---|
| `draft` | Being written; not yet offered for review |
| `proposed` | A change exists, bound to a target state, awaiting a decision |
| `in_review` | A named reviewer has taken it up |
| `accepted` | A decision record exists, bound to the exact target state |
| `rejected` | A decision record exists declining the change |
| `superseded` | A later state replaced this one for the same logical id |
| `stale` | A dependency moved; the state's proof no longer applies |
| `waived` | A hold was passed under a recorded waiver |
| `released` | Included in an attested release |

**Why this is load-bearing.** Two documents look identical: the one where a lawyer read the indemnification sentence and approved it, and the one where the sentence changed and nobody with standing to object saw it. The difference between them is the entire question of authorship, and it is the first thing asked when the document is challenged. Roles are how that question gets an answer that is not a memory.

`automation` is a real role with real authority and it is honestly not a person. It exists so that *the system did this under a rule you configured* is sayable without a human's name appearing on a decision they never made.

---

## 5. Plugins may tighten, never loosen

**Status: specified.**

Genre packs, language packs, renderers and judgment providers all arrive as plugins. Each carries a manifest:

```yaml
id: wi.genre.grant_nofo
version: 2.1.0
kind: genre            # genre | language | renderer | judgment
requires:
  core: ">=5.0.0 <6.0.0"
capabilities:
  - read_graph
  - propose_changes
  - declare_required_sections
digest: sha256:6b41c0d9...73ea
```

The rule, in three clauses:

1. **A plugin cannot override a constitutional law.** No manifest field, no capability, no version pin makes Law D optional. The laws are in [`CONSTITUTION.md`](CONSTITUTION.md) and there is no plugin-visible interface through which they can be reached.
2. **A plugin may tighten policy.** A grant pack may require anchors on claims the base policy would permit unanchored. A medical pack may narrow `allowed_basis` for a claim class. A renderer may declare structural commitments the build must satisfy. All of this is welcome and all of it is recorded.
3. **A plugin may not loosen a hard invariant** unless the user explicitly changes policy, in their own policy file, in a mode that admits the change. A plugin that wants a looser rule may *request* it; the request appears to the user as a policy change with a diff and a new digest, decided by a person.

**Why this is load-bearing.** A plugin is code someone else wrote, installed for a reason unrelated to evidence discipline — a genre pack for the section structure, a renderer for the output format. If installing it could relax the gate, then the evidence standard of every project becomes the minimum of every plugin anyone ever added, and no one would ever notice the moment it dropped. Tightening compounds safely. Loosening compounds into nothing.

`capabilities[]` is an allowlist, not a description. A plugin that did not declare `propose_changes` cannot propose changes, and a plugin's digest is recorded in the lockfile so the code that ran is the code that was reviewed.

---

## 6. Waivers

**Status: waiver records executable; multi-actor authority binding specified.**

Every proceed-anyway is a record. Not a flag, not a suppressed warning, not a config line that turns a check off — a record, bound to an exact claim state, naming who, when and why.

```json
{
  "waiver_id": "w-0004",
  "claim_id": "c-0006",
  "claim_state_digest": "sha256:9c0241ff8b7e3a06d15c4f92e08b73aa1d6c5f30e94b28a7c013d6f85b2ea44f",
  "hold_reason": "waiver_required",
  "actor": {"id": "a.smith", "role": "evidence_reviewer", "type": "team_member"},
  "recorded_at": "2026-03-18T21:04:11Z",
  "reason": "Figure confirmed by phone with the county administrator; written confirmation expected before the April filing.",
  "expires_at": "2026-04-15T00:00:00Z",
  "status": "active"
}
```

**A waiver goes stale when the claim it excuses changes.** `claim_state_digest` is what makes that mechanical: the waiver covers one state, and the moment the claim atom's digest moves, the waiver's `status` becomes `stale` and the hold returns. It does not carry forward, and it cannot be made to carry forward by editing a date.

That is the difference between a waiver and a suppression. A suppression says *stop telling me about this claim*. A waiver says *I, named, on this date, for this stated reason, accepted this exact assertion in this exact form*. Change the assertion and the acceptance no longer describes anything. The person who waived a figure of 11,800 did not waive a figure of 12,400, and no honest record can pretend otherwise.

`expires_at` is optional and, when present, is enforced independently of staleness. A waiver granted pending written confirmation should not outlive the confirmation window just because nobody edited the sentence.

---

## 7. Offline mode

**Status: executable — `wi --offline`.**

```
$ python3 scripts/wi.py --offline gate
```

`--offline` is a guarantee, not a preference. Under it:

| Guaranteed | Meaning |
|---|---|
| No DNS | No name resolution is attempted, for any purpose |
| No remote model | No judgment provider is contacted |
| No telemetry | Nothing is emitted, at any verbosity |
| No external source retrieval | A source that references a URL records the reference; it does not fetch it |
| No public signing log | No transparency log submission, no key server lookup |
| Local parsers only | Every extraction runs in-process or in a local sandboxed process |
| Deterministic checks | Quotation, numeric, date, entity, citation resolution, anchor integrity |
| Cached judgments only | A judgment recorded earlier may be *read*; none may be produced |

The consequence that matters:

```
$ python3 scripts/wi.py --offline gate

# Release gate: HOLD

Evidence mode: `regulated` · 41 claim atoms · 6 sources

## Holding (1)

**c-0017** — judgment required by policy, no judgment capability available

> Reviewers have consistently characterized the program's intake process as
> the least burdensome among comparable regional efforts.

  Policy `evidence.allowed_basis.attribution` requires a paraphrase-support
  judgment for this claim shape. Running offline; no cached judgment exists
  for state sha256:4f81...0c22.

  Repair:
    · quote the reviewer language verbatim and anchor it  [cheapest]
    · attribute the characterization to a named source in the text
    · qualify the claim to what the deterministic checks can support
    · re-run with a judgment capability available
    · record a waiver bound to this claim state

Checks run: quotation · numeric · date · entity · citation resolution · anchor integrity.
Not run: paraphrase support — WI_JUDGMENT_UNAVAILABLE, offline.
```

**Never silently weaken policy to make offline green.** The temptation is obvious and the failure is total: if `--offline` quietly dropped the requirements it could not satisfy, then the most constrained environment — the air-gapped review room, the secure facility, the flight — would produce the most permissive verdicts, and the word `RELEASE` would mean the least exactly where it was trusted the most. HOLD with a named reason is the correct output. It tells the author what is missing, what it would take, and four ways to proceed today.

---

## 8. What is executable and what is specified

| Mechanism | Status |
|---|---|
| `wi.policy.yaml` parsed and enforced by `gate`, `test` and `bundle` | Executable in `scripts/wi.py` |
| `policy_digest` bound into the release manifest | Executable in `scripts/wi.py` |
| The five evidence-mode presets and automatic escalation | Executable in `scripts/wi.py` |
| `evidence.truth_claim`, `allowed_basis`, `proposals` classification gating | Executable in `scripts/wi.py` |
| `sources.injection.quarantine_on_high` and freshness rules | Executable in `scripts/wi.py` |
| `release.block_on` / `hold_on` evaluation | Executable in `scripts/wi.py` |
| `privacy.network_default` and `telemetry_content` | Executable in `scripts/wi.py` |
| `wi --offline` and its guarantees | Executable in `scripts/wi.py` |
| Waiver records bound to a claim state, with staleness | Executable in `scripts/wi.py` |
| Role list, review states and `authority` role binding | Specified |
| Plugin manifests, capability allowlists and digest pinning | Specified |

---

## Related documents

- [`CONSTITUTION.md`](CONSTITUTION.md) — the laws policy may tighten and may never override
- [`PROOF_CARRYING_RELEASE.md`](PROOF_CARRYING_RELEASE.md) — where `policy_digest` is bound into a release
- [`WORKSPACE.md`](WORKSPACE.md) — the lockfile that pins plugin and renderer digests
- [`RELIABILITY_TYPES.md`](RELIABILITY_TYPES.md) — why a judgment can never satisfy a `verified` requirement
- [`CANONICAL_HASHING.md`](CANONICAL_HASHING.md) — how the policy digest is computed
- [`../v4/ACCOUNTABILITY_LAYER.md`](../v4/ACCOUNTABILITY_LAYER.md) — the five evidence modes in their original form
- [`../v4/SOURCE_HYGIENE.md`](../v4/SOURCE_HYGIENE.md) — the quarantine behavior this policy switches on
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
