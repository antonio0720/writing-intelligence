# Example 03 — Authority That Expires

**Commands**: `authority issue --expires` → `decide`
**Law**: O — authority is explicit, scoped and expiring
**Doctrine**: [`AUTHORITY_MODEL.md`](../../references/v6/AUTHORITY_MODEL.md)

Every transcript below was recorded on 2026-08-08 against `wi 6.0.0`, Python
3.11.15. The recording machine's UTC clock read `2026-08-08T01:44:25Z`, which
matters to how this example is built — see *How the clock is handled* below.

---

## The situation

A reviewer is brought in for two weeks in March to sign off on corrected figures
during a filing window. They are competent, trusted, and the right person for
those two weeks.

The two weeks end. The reviewer moves on. Nobody revokes anything, because
nobody is thinking about it — the filing shipped, the engagement is over, and
removing a permission is not a thing that appears on anybody's list.

Months later, a proposal is accepted under that reviewer's name.

Every organization has this. It is not a security incident and it usually is not
even a mistake — often it is the same person doing a favour. The problem is that
the record cannot distinguish *this was reviewed by somebody engaged to review
it* from *this was accepted by somebody who used to be*, and the difference is
the entire value of the signature.

Nobody is surprised to learn who made a change. They are surprised to learn that
person **could**.

---

## How the clock is handled

`wi` reads the real system clock and has no override. So a run recorded in August
cannot honestly claim to have happened in March.

What this example does instead is run the same transition twice, in two
workspaces that are identical in every respect **except the grant window**:

| | Window | Contains the recording instant? |
|---|---|---|
| Run A | `2026-08-01` → `2026-08-15` | Yes |
| Run B | `2026-03-01` → `2026-03-15` | No — closed five months earlier |

One variable. Everything else — the subject, the capability, the scope, the
issuer, the proposal, the payload — is byte-identical. Run B is the March grant,
and the refusal you see is the real one, dated by the tool itself.

---

## Setup, run twice

```bash
mkdir -p ~/scratch/ex03-open && cd ~/scratch/ex03-open      # and again for ex03-closed
alias wi="python3 /path/to/writing-intelligence/scripts/wi.py"

wi init --title "Delta Regional Capacity" --mode strict
wi authority issue --subject antonio --capability claim.accept \
   --scope workspace --issuer antonio --expires 2030-01-01T00:00:00+00:00

# baseline households = 11,800, accepted and committed by antonio
# then the change the reviewer is being asked to sign off on:
wi propose --node households --payload revised.json \
   --why "agency republished the count" --actor antonio
```

Both workspaces now hold one open proposal that moves the household figure from
11,800 to 11,240. The reviewer's job is to accept it.

---

## Run A — the window is open

```bash
wi authority issue --subject reviewer-march \
   --capability claim.accept.quantity_change --scope workspace --issuer antonio \
   --activates 2026-08-01T00:00:00+00:00 --expires 2026-08-15T00:00:00+00:00
```

```
issued bceb8b77-9e68-551b-9b33-48b184b2bdc2
  reviewer-march -> claim.accept.quantity_change in scope workspace
```

```bash
wi decide 3cfbc008-f9c9-5b6e-ada2-0db31ebfac24 --accept --actor reviewer-march
```

```
DECISION ACCEPTED
  proposal   3cfbc008-f9c9-5b6e-ada2-0db31ebfac24
  bound to   sha256:9b902e5c9f57fccbec6f34bdd4448fc300ffe0c2a90b314a83d730d331385da8
  actor      reviewer-march
  grant      bceb8b77-9e68-551b-9b33-48b184b2bdc2 (claim.accept.quantity_change)

Accepted is a decision, not an application. Run `wi commit`
to apply every accepted proposal as one transaction.
```

Exit `0`. The decision names the grant it exercised, which is the difference
between an audit trail that says *reviewer-march accepted this* and one that says
*reviewer-march accepted this, under a grant scoped to the workspace, in a window
that was open at the time*. Only the second answers somebody asking whether they
could.

---

## Run B — identical, except the window closed in March

```bash
wi authority issue --subject reviewer-march \
   --capability claim.accept.quantity_change --scope workspace --issuer antonio \
   --activates 2026-03-01T00:00:00+00:00 --expires 2026-03-15T00:00:00+00:00
```

```
issued bceb8b77-9e68-551b-9b33-48b184b2bdc2
  reviewer-march -> claim.accept.quantity_change in scope workspace
```

```bash
wi decide 54295762-47cc-5e8d-b0bf-0bcc55dd500c --accept --actor reviewer-march
```

```
WI_AUTHORITY_EXPIRED: reviewer-march holds claim.accept.quantity_change but the grant is not active at 2026-08-08T01:44:43.739930+00:00
    grants: ['bceb8b77-9e68-551b-9b33-48b184b2bdc2']
  repair:
    - re-issue the grant with a current window
```

Exit `2`.

Read the message. It does not say the reviewer has no authority — it says they
**hold** the capability and the grant is not active at this instant, and it prints
the instant. That is a different failure from never having been granted anything,
and the repair is different: one is a renewal, the other is a request. A single
"permission denied" sends both people nowhere.

---

## Nobody remembered anything

```bash
wi authority list --json
```

```
subject       reviewer-march
revoked_at    None
activates_at  2026-03-01T00:00:00+00:00
expires_at    2026-03-15T00:00:00+00:00
```

`revoked_at` is `None`. Nobody withdrew this grant. No offboarding checklist ran,
no admin remembered the engagement had ended, no quarterly access review caught
it. The refusal came from a date written down at the moment the grant was issued
— when the person issuing it knew exactly how long the engagement was, and was
the only person who would ever know that cheaply.

**Expiry is the part people want to drop and the part that pays for itself.** A
grant with no window is a grant that has to be revoked by somebody who remembers,
and remembering is the control that always fails — not dramatically, just quietly,
in the eighth month, when the person who would have remembered has also moved on.

The cost of getting it right was one flag at issue time.

---

## One thing to read carefully in `authority list`

```
  bceb8b77-9e68-551b-9b33-48b184b2bdc2  [active]
      reviewer-march -> claim.accept.quantity_change
      scope workspace
      issued by antonio  expires 2026-03-15T00:00:00
```

That is run B — the grant whose window closed in March — and the list prints
`[active]`.

The label reflects **revocation only**. This grant has not been revoked, so it is
not shown as revoked. It does not consult the window; the expiry is printed one
line below and the reader is expected to compare it.

The enforcing check is the one at decision time, and that one does consult the
window, which is why the same grant refused the transition a moment earlier.
When you want to know whether somebody can act right now, ask the transition, not
the listing.

---

## Two properties worth knowing

**A grant id is derived from its identity, not its window.** Both runs printed
`bceb8b77-9e68-551b-9b33-48b184b2bdc2` from the same subject, capability, scope
and issuer, despite different windows. That is what makes the comparison above
exact — the two runs differ in one input and nothing else.

**Re-issuing replaces the window in place.** Because the id is derived that way,
issuing the same grant again with a new expiry updates the existing grant rather
than creating a second one. Verified in a throwaway workspace: two issues, one
grant, the later window in force. That is what the refusal's own repair line —
*re-issue the grant with a current window* — actually does.

---

## The three other refusals

Expiry is one of four, and they are four rather than one because each sends a
person somewhere different. These are quoted from
[`release/RELEASE_NOTES_v6.0.0.md`](../../release/RELEASE_NOTES_v6.0.0.md), which
records them from a run of the tool; they were not re-recorded for this example.

**No grant at all** — the default state of every actor, including whoever created
the workspace:

```
WI_AUTHORITY_DENIED: antonio holds no capability grant
    required_capability: claim.accept
  repair:
    - issue one: wi authority issue --subject antonio --capability claim.accept --scope workspace
```

**A grant that does not reach** — right capability, wrong scope:

```
WI_GRANT_SCOPE_EXCEEDED: copyeditor holds claim.accept.quantity_change but not in this scope
    grants: ['0e55da5f-8b01-5697-8bde-71f966741401']
    requested_scope: {'kind': 'branch', 'value': 'main'}
  repair:
    - widen the scope, or decide on a branch you hold
```

**A grant that was revoked** — deliberately withdrawn, and the message says what
survives:

```
revoked 532aeeaa-a0d4-55e4-848b-f80a6b7cbd8f (ex-contractor -> claim.accept)
Existing decisions keep their receipts. Nothing new may be
authorized under this grant from now on (C020).
```

Revocation does not rewrite history. A decision taken while the grant was live
remains a valid decision; the revocation is its own fact with its own clock.
A deleted grant would make every action taken under it unexplainable, and the
audit question is usually asked about grants that no longer exist.

---

## What this example does not show

- **The refusal was recorded in August, not November.** The window is real, the
  refusal is real, and the instant in the error message is the true one. The
  check is a comparison against the expiry, so any instant past it refuses for
  the same reason — but this file does not contain a November transcript,
  because no November run was made.
- **Delegation monotonicity.** A child grant may narrow its parent in capability,
  scope and lifetime and never widen any of the three, checked at issue time.
  Transcripts are in the release notes; the assertions are in
  [`tests/v6/test_wi6.sh`](../../tests/v6/test_wi6.sh).
- **Quorum.** Multi-party approval is specified in the authority model and is not
  exercised here.
- **A judgment provider can never hold a grant at all.** That refusal fires at
  issue time and is constitutional rather than configurable (constraint C008).

---

## Pattern to reuse

```bash
# Give the window the real length of the engagement, at the moment you know it.
wi authority issue --subject REVIEWER --capability claim.accept.quantity_change \
   --scope workspace --issuer YOU \
   --activates 2026-03-01T00:00:00+00:00 --expires 2026-03-15T00:00:00+00:00

# To extend: re-issue with a new window. Same grant, new expiry.
```

Next: [`04-a-capsule-a-stranger-verifies.md`](04-a-capsule-a-stranger-verifies.md) —
handing the result to somebody outside the organization.
