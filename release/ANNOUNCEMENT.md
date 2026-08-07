# Writing Intelligence v5.0 — The Sentence You Can Defend

**By Antonio T. Smith Jr. — Founder & CEO, Density6 LLC**

---

Every writing tool on the market makes prose sound better.

Not one of them can tell you whether the sentence you are about to send is one you can defend.

That is the whole gap. A confident paragraph with a fabricated citation looks exactly like a confident paragraph with a real one. A number that was checked in March looks exactly like a number that was checked in March and then quietly edited in June. A hedge somebody tightened from *may reduce* to *reduces* looks like a copy edit and is a change of claim. The reader cannot tell the difference. Increasingly, neither can the author.

Fluency reads as diligence. That is the con, and nobody is running it on purpose.

---

## What v4 did, and where it stopped

v4 put a floor under it. Support had to be a verbatim span from a source you supplied, or the claim came back `needs_source`. Every edit arrived as a proposal with the original intact. Every supplied document got scanned for injection before it could reach anything. Every draft ended in `RELEASE`, `HOLD` or `BLOCK` with named repairs.

It worked, and it stopped at two places.

It verified a document **at a moment**. Nothing bound the check to the things it depended on, so an edit made three weeks later inherited a result that no longer applied. A green badge over changed text is worse than no badge at all.

And it could not hand anybody anything. The proof lived on your screen. A reader who did not trust you had no way to check it without trusting your tooling, which is the same thing.

---

## What v5 changes

v5 makes the account a thing that travels.

Every proof binds four dependencies: the exact source state, the exact anchor, the exact claim state, and the chain of accepted changes that produced the current wording. Change any one and the proof is stale — **unless the engine can prove the dependency was unaffected**. That exception is the whole reason it is usable rather than exhausting.

And the account packages into a `.wiab` bundle that a stranger verifies offline, by recomputing every digest, with no model and no network and no reason to trust whoever built it.

---

## Three things you can do that you could not do before

**1. Ask what a source change actually broke — and what it did not.**

Change one number in one source and `wi impact` reports, on the shipped fixture: one claim atom, one anchor, one paragraph, one document and one verification record went stale. And **four anchors are provably outside the change; five claim atoms are still verified.** Then it names the cheapest safe repair and costs it.

The negative half is the part that matters. Any system can turn a document red when a source moves. That system gets switched off in a week, and the rule it was enforcing goes with it.

**2. Ask what a rewrite did to the meaning.**

`wi diff --semantic` classifies `may reduce → reduces` as `certainty_strengthened` and `11,800 → 12,400` as `quantity_changed`, and says which proofs carry forward and which do not. A character diff reports typography. This reports whether you still have support for what the sentence now says.

**3. Hand someone proof they can check without trusting you.**

`wi bundle` builds the release. `wi verify-release` checks it on a machine that has never seen your workspace — archive integrity, object digests, artifact digest, graph reference integrity, proof dependencies, stale closure, manifest counts, core version. Change one number inside a sealed bundle and it fails with `WI_RELEASE_TAMPERED` and exits `2`. The regression suite proves that failure on every run, because a verifier that cannot fail is decoration.

There is a fourth thing, quieter than the others. Point at any line — `wi explain draft.md:5` — and get the claim, its status, its realm, every anchor with byte offsets and a quote digest, every check with its result, and what depends on it.

---

## What it will not do

These are refusals, not unbuilt features.

It will never construct a citation. There is no code path in which a well-formed anchor can be produced for a source that was never ingested. It does not verify truth — it verifies support **within the sources you supplied**, and it says so every single time proof appears, because an author who believes reality is being checked will trust it in exactly the situation where it cannot help. It will not evade detectors. It will not give you one blended score for the slide. Embeddings are candidate retrieval and never evidence: `11,800` and `12,400` are neighbours in embedding space and a career-ending difference in a grant narrative.

And it says what it did not do. `wi doctor` lists the eleven deterministic checks this machine can run, the one anchor type it has, and the seven capabilities it does not have with a reason for each. Paraphrase entailment is not evaluated by anything in this release, six of the seven anchor kinds do not execute, and there is no compiled core, no Workbench, no MCP server and no judgment provider. All of it is specified in twenty doctrine documents where every section is marked *executable* or *specified*, and none of it is described as shipping.

A release that only lists what it added is describing a system nobody stress-tested.

---

## Get it

One stdlib-only Python file. Python 3.8+. No dependencies, no account, no server, no API key, no telemetry. It runs air-gapped.

```bash
curl -O https://raw.githubusercontent.com/antonio0720/writing-intelligence/main/scripts/wi.py
python3 wi.py --version
python3 wi.py doctor
```

Or install the whole skill:

```bash
git clone https://github.com/antonio0720/writing-intelligence \
  ~/.claude/skills/writing-intelligence
```

Eight surfaces, with a matrix telling you exactly which half of the system each one can physically give you: [github.com/antonio0720/writing-intelligence](https://github.com/antonio0720/writing-intelligence)

Verify the claims above rather than believing them:

```bash
bash tests/v4/test_wi.sh     # 3 checks — the v4 adversarial floor
bash tests/v5/test_wi5.sh    # 32 checks — each one with a negative twin
```

---

## Free, MIT, and staying that way

No paid tier. No hosted dependency. No account gate arriving in version six.

The documents that most need this are the ones that cannot leave the building — sealed bids, pre-publication investigations, privileged work, unannounced filings. A tool that requires an account excludes exactly the people whose stakes justify it, and a proof that expires when a vendor does was never a proof.

If you write grants, sermons, filings, briefs, journalism, medical or legal copy, investor material, technical docs, or anything a hostile reader might question, it is yours. Free. Forever.

Use it. Then tell one person who has to defend what they write.

**Antonio T. Smith Jr.**
*August 7, 2026*
*Founder & CEO, Density6 LLC* · [densitysix.com](https://densitysix.com) · MIT
