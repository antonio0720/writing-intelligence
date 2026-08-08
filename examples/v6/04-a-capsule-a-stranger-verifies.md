# Example 04 — A Capsule A Stranger Verifies

**Commands**: `capsule create --profile selective` → `capsule inspect` → `capsule verify`
**Doctrine**: [`PROOF_CAPSULES.md`](../../references/v6/PROOF_CAPSULES.md)

Every transcript below was recorded on 2026-08-08 against `wi 6.0.0`, Python
3.11.15. It continues directly from the workspace built in
[`01-simulate-before-you-edit.md`](01-simulate-before-you-edit.md) — three claims
on `main`, the household figure corrected to 11,240.

---

## The situation

A funder is reviewing the grant. They want to check one figure: the household
count. They are entitled to see that claim and its provenance. They are not
entitled to the wait-time analysis, the county breakdown, the internal decisions,
the rejected proposals or the sources under licence.

Four things are true at once, and any format that ignores one of them is
dishonest:

1. The funder must be able to confirm the figure was part of what was attested,
   and not assembled afterwards for their benefit.
2. The organization must not have to disclose everything else.
3. A digest of a withheld state is not evidence about its content. It proves
   something with that digest was in the closure. It says nothing about what.
4. The organization must not be able to build an artifact that appears to prove
   more than it does — and that constraint has to be structural, because the
   organization is the one building it.

The fourth is the hard one. A producer who wants to overstate does not have to
lie about a digest. They only have to print a withheld source's digest in a
column headed *evidence*, and the reader does the rest.

---

## Build the capsule

```bash
cd ~/scratch/ex01
wi capsule create --out households.wic --select households --profile selective
```

```
wrote households.wic
  profile        selective
  closure root   sha256:d2892cd62af15325339a2032fb26a4ff7bcdebe8e19a312db40dcf687547eb38
  leaves         3 total, 1 disclosed, 2 redacted

A redacted leaf proves it was inside the producer's closure.
It does not prove you inspected its content, and this capsule
does not say otherwise.
```

Three leaves, one disclosed, two redacted. That last paragraph is printed by the
tool at the moment of creation — before anybody has a chance to describe the
artifact to a recipient in more flattering terms.

The file is 3.5 KB.

---

## What it declares about itself

```bash
wi capsule inspect households.wic
```

```
CAPSULE households.wic
  format           wic/1
  profile          selective
  core_version     6.0.0
  branch           main
  graph_root       sha256:be8d16b079973bf2ff14da735df70d2d17560400cd3a3ef47977ec5cd844093e
  closure_root     sha256:d2892cd62af15325339a2032fb26a4ff7bcdebe8e19a312db40dcf687547eb38
  leaf_count       3
  disclosed_count  1
  built_at         2026-08-08T01:45:28.191101+00:00

  declared omissions
    judgment.entailment      this core contains no judgment provider
    signature                external signing is specified and does not ship in 6.0.0

  does not prove
    - that the underlying sources are correct
    - that a redacted leaf's content was independently inspected
```

### The omissions are in the artifact, not in a covering email

`declared omissions` and `does not prove` are fields in the file. They travel
with it. A recipient who never reads the documentation, never speaks to the
producer, and opens the capsule six months later in a different organization
still gets them.

Two omissions are named here and both are the honest kind:

**`judgment.entailment`** — this build ships no judgment provider, so paraphrase
entailment was not evaluated. Not *passed*. Not silently omitted. Named, with the
reason.

**`signature`** — external signing is specified in the doctrine and does not ship
in 6.0.0. A reader might reasonably assume a cryptographic proof artifact is
signed. It is not, and the artifact is the thing that says so.

This is the mechanism the redaction contract requires. A capsule may prove *a
state with this digest was part of the producer's closure*. It may not claim, and
its rendering may not imply, that the recipient has independently verified the
underlying content — unless that content is disclosed.

### The redacted leaves say what they are worth

```json
{
  "disclosed": false,
  "does_not_prove": "anything about its content",
  "leaf_digest": "sha256:ff5aacbff2d98dfaad60036bfb52e9b43fff6ed8874da4060695d5d553ed6f3e",
  "logical_id": "counties",
  "proves": "this leaf was part of the producer's closure"
}
```

Every redaction carries both halves. `proves` and `does_not_prove` sit next to
each other, in the file, at the same level. There is no reading of that object in
which the digest is evidence about the county figure.

### The graph root ties it back to example 01

```
graph_root  sha256:be8d16b079973bf2ff14da735df70d2d17560400cd3a3ef47977ec5cd844093e
```

That is the same value example 01's simulation printed as its `candidate root`,
before the change existed, and the same value the commit reported as `next root`.
The root a simulation predicted is the root the capsule hands to a stranger.

---

## Verification, by somebody with nothing

Copy two files into an empty directory. No workspace, no network, no model, no
account:

```bash
mkdir stranger && cd stranger
cp /path/to/writing-intelligence/scripts/wi.py .
cp ~/scratch/ex01/households.wic .
ls -a
```

```
.  ..  households.wic  wi.py
```

```bash
python3 wi.py capsule verify households.wic
```

```
CAPSULE VERIFICATION — households.wic

  ok   capsule.format         format is 'wic/1'
  ok   leaf.digest            1 disclosed leaf digest(s) recomputed
  ok   state.digest           1 disclosed state(s) hash to the digest the leaf names
  ok   inclusion.proof        1 leaf/leaves proved to belong to closure root sha256:d2892cd62af1
  ok   closure.count          1 disclosed + 2 redacted against a declared 3 leaves

  closure root sha256:d2892cd62af15325339a2032fb26a4ff7bcdebe8e19a312db40dcf687547eb38

VERDICT VERIFIED

  this capsule proves membership in the producer's closure and the integrity of what it disclosed; it proves nothing about whether the sources are correct
```

Exit `0`.

Every line is a **recomputation**, not a lookup. `leaf.digest` re-hashes the leaf.
`state.digest` re-hashes the disclosed payload and compares it to what the leaf
claims. `inclusion.proof` walks the Merkle path to the root. The verifier does not
read a field saying the digests matched.

`wi doctor` on that machine reports `network disabled`, and `--offline` is
available as an explicit assertion:

```bash
python3 wi.py --offline capsule verify households.wic
```

Same result. Two files in a room with no network is the whole requirement.

### The verdict states its own limit

```
this capsule proves membership in the producer's closure and the integrity of
what it disclosed; it proves nothing about whether the sources are correct
```

That sentence is printed on success. Not on failure, not in a footnote, not in
the manual — on the line directly under `VERDICT VERIFIED`, where the word that
gets quoted is.

Support is verified within the sources supplied. If the outcomes report is wrong,
the claim reads supported and is false. The tool says so at the moment it is most
tempting to let a reader believe otherwise.

---

## Now break it

A verifier that cannot fail is decoration. Change the disclosed figure from
11,240 to 12,400 — the number from example 02's audit branch, which is a real
figure somebody might genuinely prefer:

```bash
python3 - <<'PY'
import json
c = json.load(open("households.wic"))
c["disclosed"][0]["state"]["payload"]["text"] = "The program served 12400 households in 2022."
c["disclosed"][0]["state"]["payload"]["quantities"][0]["coefficient"] = 12400
json.dump(c, open("tampered.wic","w"), indent=2, sort_keys=True)
PY

wi capsule verify tampered.wic
```

```
CAPSULE VERIFICATION — tampered.wic

  ok   capsule.format         format is 'wic/1'
  FAIL state.digest           disclosed state for households does not match the digest its leaf names; the bytes in this capsule are not the bytes that were attested
  ok   leaf.digest            1 disclosed leaf digest(s) recomputed
  ok   inclusion.proof        1 leaf/leaves proved to belong to closure root sha256:d2892cd62af1
  ok   closure.count          1 disclosed + 2 redacted against a declared 3 leaves

  VERDICT TAMPERED
```

Exit `2`.

### Read which check failed, and which did not

Four of the five still pass, and that is the interesting part.

The **format** is fine. The **leaf digest** recomputes. The **inclusion proof**
still reaches the closure root. The **counts** still add up. The forgery is a
well-formed capsule whose Merkle structure is intact.

`state.digest` is the one that fails, and the message says exactly why: *the
bytes in this capsule are not the bytes that were attested.* The disclosed
payload no longer hashes to the digest its own leaf names. To defeat that, an
attacker would need a preimage for SHA-256 — not a better forgery, a different
mathematics.

The word `VERIFIED` does not appear anywhere in that output. The regression suite
tampers with a capsule on every run and asserts its absence, because a verifier
that stays green when you break the thing it checks was never checking.

---

## What this example does not show

- **No signature.** The capsule is unsigned, says so in `declared_omissions`, and
  external signing does not ship in 6.0.0. This proves integrity and membership.
  It does not prove who produced it — anyone with the workspace could have.
- **No sources were disclosed, because none were ingested.** The claims here are
  `human_declared`. In a workspace with anchored evidence, a `selective` capsule
  can disclose source bytes for the claims under review. What ships in 6.0.0 for
  the ones it withholds is the redaction record above — `disclosed: false`, a
  `proves` string and a `does_not_prove` string, per leaf. The reliability-type
  transformation that would rename `verified` to `verified_by_producer` at the
  capsule boundary is **specified in `references/v6/PROOF_CAPSULES.md` §6 and
  does not ship** — that string is not in `scripts/wi.py`, and a reader who
  filters on it today would filter on nothing.
- **No judgment.** Paraphrase entailment was not evaluated, and the capsule says
  so rather than omitting the row.
- **A capsule is not a release bundle.** A `.wiab` is a whole release verified
  with `wi verify-release`. A `.wic` is a selectively disclosed proof of part of
  one. Different extensions, different jobs.

---

## Pattern to reuse

```bash
wi capsule create --out claim.wic --select NODE --profile selective
wi capsule inspect claim.wic     # read declared omissions before you send it
wi capsule verify claim.wic      # confirm what the recipient will see

# what the recipient runs, with wi.py and the capsule and nothing else:
python3 wi.py capsule verify claim.wic
```

**Your work stops depending on whether people trust you, and starts depending on
whether the digests match.**

Back to the [index](README.md).
