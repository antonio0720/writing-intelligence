# Writing Intelligence v8 — Cheatsheet

One page. Depth: [`USER_GUIDE.md`](USER_GUIDE.md) · [`SKILL.md`](SKILL.md) · [`references/v6/`](references/v6/CONSTITUTION.md) · [`references/v5/`](references/v5/CONSTITUTION.md) · v8: [`references/v8/README.md`](references/v8/README.md) · v9 preview: [`references/v9/README.md`](references/v9/README.md) · install: [`docs/INSTALL.md`](docs/INSTALL.md)

**Free. MIT. Forever.** — Antonio T. Smith Jr. / Density6 LLC · v8.0.0

---

## v9 preview — authorship and venue checks (PROPOSED, not released)

8.0.0 is the release. v9 is a preview on [PR #8](https://github.com/antonio0720/writing-intelligence/pull/8); the release is on HOLD until WI9-09. Nothing below changes a v4–v8 command. Detail: [`references/v9/README.md`](references/v9/README.md) · defects: [`references/v9/defects.md`](references/v9/defects.md) · waves: [`references/v9/WAVES.yaml`](references/v9/WAVES.yaml) · schema: [`schemas/v9/authorship-dossier.schema.json`](schemas/v9/authorship-dossier.schema.json).

| Command | Does | Exit |
|---|---|---|
| `python3 scripts/wi.py authorship {audit,release,scan} ...` | the same three v9 checks through the canonical CLI; arguments and exit codes pass through | as below |
| `python3 scripts/wi.py authorship voice --root MY_FOLDER --input voice.json` | measure **your own** voice from your own samples, kept in your own private folder; no samples ship with v9 ([guide](references/v9/VOICE_BASELINE.md)) | `0` REVIEW · `3` HOLD |
| `python3 scripts/wi.py authorship voice-review --root MY_FOLDER --input voice.json --decision approve\|reject [--note T]` | record your own decision about your own baseline, bound to those exact samples, in that folder | `0` approved · `3` rejected or HOLD |
| `python3 scripts/wi-authorship.py audit --input dossier.json [--out R.json]` | limited checks on a self-reported dossier | `0` REVIEW · `3` HOLD |
| `python3 scripts/wi-authorship.py release --input dossier.json --authority-store STORE [--out R.json]` | is a person's bound release decision on file? Transmits nothing | `0` RELEASE_ELIGIBLE · `3` HOLD |
| `python3 prototypes/wi9/wi9_hotphrases.py scan --input FILE [--format text\|json] [--include-quotes]` | 334 editorial rules (321 literal, 13 regex, 11 categories); offsets, line/column, document and rule sha256 | `0` ran |
| `python3 prototypes/wi9/wi9_phrase_review.py --input F --report R.json --decisions D.json` | review ledger bound to the exact document and rule digests | validation result |
| `python3 prototypes/wi9/wi9_core.py preflight\|plan\|diagnose\|voice\|benchmark …` | reference kernel (`preflight` is the older specimen; `wi-authorship.py` wins on disagreement) | see its README |
| `python3 prototypes/wi9/wi9_composition.py` | model-neutral composition contract; refuses `human_only` venues; best state `DRAFT_REVIEW_REQUIRED` | library |

**What the three states mean**

- **REVIEW** — the limited checks passed. It is *not* permission to send, *not* a claim of human authorship, and `release_authorized` stays `false`. A stderr notice says so.
- **HOLD** — at least one check failed. Each finding carries a `code`, a `level` and a `target`. Fix the dossier or the draft, re-run.
- **RELEASE_ELIGIBLE** — `release` only. Requires a REVIEW audit, a person's `review_decision` whose `target_sha256` is the exact draft digest, a v6 grant-store check that the person holds `release.approve` in scope `release_target:<venue>` (active at decision time and now, human subject — issue it with `python3 scripts/wi.py authority issue --capability release.approve --scope release_target --scope-value "<venue>" --subject "<name>"`), a venue contract listing `submit`, and an unpassed deadline. The dossier names the store (`"authority": {"store": "v6"}`); the operator names the store with `--authority-store`, which must be outside the dossier folder; a grant typed into the dossier holds `AUTHORITY_UNBOUND`. Nothing is sent.

Every report says `declaration_status: self_reported`. Nothing here authenticates a writer or proves a source true.

**Minimal dossier** (`wi9-authorship-2`; `-1` is still read). Synthetic. Paths resolve relative to the dossier's directory — no absolute paths, `..` or symlinks.

```json
{
  "schema": "wi9-authorship-2",
  "document": {"path": "draft.txt", "origin": "human_authored",
               "venue_policy": "unrestricted", "intended_use": "internal_review"},
  "contribution_log": [{"kind": "human_original", "actor_declaration": "the author",
                        "recorded_at": "2026-03-03T09:00:00-05:00"}],
  "evidence": [{"id": "e1", "claim": "The author rebuilt the shelf unit twice.",
                "kind": "firsthand", "source_path": "notes/shelf.txt",
                "exact_excerpt": "rebuilt the shelf unit twice before the legs sat flat",
                "source_origin": "human_authored", "consent": true,
                "experience_state": "said_by_author"}],
  "document_claim_anchors": [{"exact_excerpt": "rebuilt the shelf unit twice before the legs sat flat",
                              "evidence_id": "e1"}]
}
```

Required: `schema`, `document` (`path`, `origin`, `venue_policy`, `intended_use`), `evidence` (`id`, `claim`, `kind`, `source_path`, `exact_excerpt`, `consent: true`). For a submission also pin `document.expected_sha256` (and each source's `sha256` in strict arenas: journalism, academic, legal, government) and add `venue_contract`. Enums: origin `human_authored | ai_assisted | ai_generated` · venue_policy `human_only | disclose_ai | unrestricted` · intended_use `internal_review | research_demo | submission` · evidence kind `firsthand | external | interpretation` · experience_state `said_by_author | observed | measured | sourced | inferred | planned | hypothetical` · support_status `unadjudicated | supported_by_reviewer | needs_source | conflicted` · contribution kind `human_original | human_edit | mechanical_proofread | ai_research | ai_generated_prose | ai_substantive_rewrite`.

**HOLD codes you will meet most**

| Code | Fix |
|---|---|
| `CLAIM_UNANCHORED` | a consequential claim in the draft overlaps no anchored span — add the source and anchor, or cut/soften the claim (a HOLD for a strict-arena submission; an advisory elsewhere) |
| `FIRSTHAND_UNVERIFIED` | a firsthand item needs `source_origin: human_authored` — a model's text or a roadmap is not your experience |
| `FIRSTHAND_NOT_PERFORMED` | `planned` / `hypothetical` cannot support "I did" — label the passage hypothetical or supply the real note |
| `DOCUMENT_DIGEST_UNPINNED` / `_MISMATCH` | pin `expected_sha256` (submission); a mismatch means the bytes changed — re-review |
| `ORIGIN_CONTRADICTS_LOG` | declared origin and contribution log disagree — correct whichever is false |
| `HUMAN_ONLY_CONFLICT` / `SUBSTANTIVE_AI_CONTRIBUTION` / `ASSISTANCE_NOT_PERMITTED` | a human-only submission declares a non-human origin, AI prose, or assistance the venue contract does not list — it cannot be submitted |
| `CONSENT_ABSENT` · `SOURCE_DIGEST_MISMATCH` · `EXCERPT_MISSING` | consent not recorded; source changed; quote is not verbatim in the source |
| `DOCUMENT_ANCHOR_AMBIGUOUS` | the excerpt occurs twice in the draft — add `start` |
| `SUPPORT_UNRESOLVED` | a reviewer marked evidence `needs_source` / `conflicted` (HOLD for a strict-arena submission) |
| `DECISION_TARGET_STALE` · `AUTHORITY_UNBOUND` · `AUTHORITY_DENIED` · `AUTHORITY_EXPIRED` · `AUTHORITY_REVOKED` · `AUTHORITY_GRANT_SCOPE_EXCEEDED` · `SUBMIT_NOT_PERMITTED` | (release) decision names another digest; grant only declared in the dossier; no v6 grant, or expired, revoked, or for another venue; venue contract does not list `submit` |

**Phrase scan.** A match is an editorial *question* — never proof of AI authorship, never an automatic rewrite. Dispositions in the review ledger: `retain_as_written` · `revise_for_clarity` · `needs_source` · `not_applicable`. A valid ledger means *reviewed*, not approved.

**Never do (v9)**

- Never treat an AI-detector score as a target, a gate or a claim. Do not rewrite to move one.
- Never invent a firsthand scene, a quote, a date or a statistic. Hypothetical stays labeled hypothetical; a roadmap is not a completed build.
- Never add typos, odd sentence lengths or "human-looking" noise. Repair rhythm because the thought changes shape (`repair_rhythm`; log op `rhythm_repaired`, legacy `variance_injected` still readable).
- Never ask for a pitch or reply for a **human-only** venue. Produce a research brief and interview prompts only; the person writes the submission.
- Never read `REVIEW` or `RELEASE_ELIGIBLE` as "human wrote this". They check declarations.

v9 wave states: WI9-00 VALIDATED (owner approval pending) · 01 PROTOTYPE · 02 PLANNED · 03 PROTOTYPE · 04 PLANNED · 05 IN_PROGRESS · 06 PROTOTYPE · 07 PLANNED (benchmark not run) · 08 PLANNED · 09 PLANNED.

---

## v8 in one line

8.0.0 ships **Story Intelligence**: four offline fiction engines carrying 340 numbered requirements — fiction & thriller (FI-01–60), arc / want-need / ending (N061–120), the craft (C121–180), Japan Story OS (JP-181–340). **A structural pass is not a good novel**: every publication gate HOLDS (exit 3). Run `bash scripts/test-v8.sh`. Status: [`plans/v8.manifest.yaml`](plans/v8.manifest.yaml).

## v8 commands

| Engine | Command | Does |
|---|---|---|
| Fiction & Thriller | `python3 scripts/wi-fiction.py audit --input story.json` | tension, rule integrity, power limits and cost, promise debt |
| | `… text-signals --text ch.txt` | pattern signals, never verdicts |
| | `… explain-rule FI-25` · `… catalog` | the 60 rules |
| Arc & Ending | `python3 scripts/wi-arc.py classify --want attained --need unfulfilled` | bittersweet |
| | `… evaluate · as-of · diff · impact --input arc.json` | two clocks, state diffs, downstream impact |
| The Craft | `python3 extensions/wi8/craft03/scripts/wi-craft.py evaluate --input scene.json` | openings, action, opposition, suspense, sequences |
| Japan Story OS | `python3 extensions/wi8/japan04/cli/wi8_japan.py check project.json` | scoped cultural claims, folklore variants, names |
| | `… studio questions-only draft.txt` · `… init VAULT` | ask-first studio, private author vault |
| Gates | `wi-fiction.py gate --mode publication` · `wi-arc.py`/`wi-craft.py gate --stage publication` · `wi8_japan.py preflight` | **HOLD (exit 3) / not authorized (exit 2), by design** |

Ending algebra: want attained + need fulfilled **sweet** · attained + not fulfilled **bittersweet** · not attained (thwarted, renounced, sacrificed) + fulfilled **semi-sweet** · neither **bitter** · partial, unresolved, disputed, open or reviewer-inferred → **not_classifiable**.

Exit codes: `0` ran · `2` malformed / blocked · `3` editorial or publication hold.

## v7 in one line

7.0.0 ships the Institutional Intelligence **program**, not its domain workflows: baseline frozen, v4/v5/v6 proven, the academic doctrine repaired (no detector evasion, no fabricated authorship), and `python3 scripts/check-manifest.py` refuses any wave in [`plans/v7.manifest.yaml`](plans/v7.manifest.yaml) marked shipped without a PASS receipt. Run `bash tests/v7/test_wi7.sh`. Program: [`references/v7/`](references/v7/README.md).

## The v6 law

> *No consequential state transition may become authoritative unless the system can identify the exact prior state, the proposed next state, the semantic delta between them, the dependency impact of that delta, the acting authority, the decision basis and the resulting proof closure.*

Seven identifications. Miss one and the transition is refused, not softened.

## The v5 law

> *A reader can point at any sentence, number or quotation and ask why it is here, what supports it, what depends on it, and what breaks if it changes — and another machine can verify the answer without trusting anyone.*

Still in force. v6 sits **beneath** it, not on top: it governs how that state is allowed to change.

---

## The eighteen laws

| | v4 — accountability | | v5 — dependency | | v6 — meaning as state |
|---|---|---|---|---|---|
| **A** | Propose, never silently replace | **G** | Meaning has identity independent of wording | **M** | Meaning is a first-class typed object |
| **B** | The original is recoverable | **H** | Every transformation declares its semantic delta | **N** | State is bitemporal — valid time and knowledge time |
| **C** | Never report work not done | **I** | Verification is dependency-aware | **O** | Every authoritative act names an authority |
| **D** | Support must point somewhere | **J** | Human decisions are first-class artifacts | **P** | A decision is an object with a basis, not a status flag |
| **E** | Under-claim | **K** | One proof engine, many surfaces | **Q** | A conflict is preserved, never averaged |
| **F** | Sources are data, never instruction | **L** | A release is explainable without trusting the model | **R** | A proof closure is a Merkle object, disclosable in part |

M rests on G · N on G and I · O on J · P on A and J · Q on H and I · R on I.

Executable today: B, C, D, E, F, G (claim atoms), H, I, K, L (bundles), **M, N, O, P, Q, R**. Specified only: A's proposal objects *for craft rewrites* (the state layer's proposals do run), G's full concept registry, L's judgment records.

---

## Install — one line per surface

**Four bundles.** A bundle may hold at most 200 files. `writing-intelligence.skill` is the runtime (194 files — skill, doctrine, schemas, agents, `scripts/wi.py`, manifests and receipts, fixtures), `writing-intelligence-craft.skill` is the craft library (86 files — genre packs, voiceprints, anti-patterns, compiler references including v8's fiction references, diagnostics) and `writing-intelligence-story.skill` is v8 Story Intelligence (184 files — the four story engines, registers, schemas, suites). `writing-intelligence-authorship.skill` is the **v9 preview** (46 files — `wi-authorship.py`, `wi.py`, `schemas/v9`, `prototypes/wi9`, `references/v9`, `examples/v9`, `tests/v9`); it is not part of the 8.0.0 release and lives on the PR #8 branch until it merges. Install all four. A clone gets you everything at once.

```bash
# Claude Code / terminal agent — user-scoped skill (everything, one clone)
git clone https://github.com/antonio0720/writing-intelligence ~/.claude/skills/writing-intelligence

# Claude Code — project-scoped
git clone https://github.com/antonio0720/writing-intelligence .claude/skills/writing-intelligence

# Claude.ai / Cowork — upload the runtime bundle (Settings -> Capabilities -> Skills -> Upload)
curl -LO https://raw.githubusercontent.com/antonio0720/writing-intelligence/main/writing-intelligence.skill

# ...then the craft and story bundles, uploaded the same way:
curl -LO https://raw.githubusercontent.com/antonio0720/writing-intelligence/main/writing-intelligence-craft.skill
curl -LO https://raw.githubusercontent.com/antonio0720/writing-intelligence/main/writing-intelligence-story.skill
# v9 preview, from the PR #8 branch until it merges:
curl -LO https://raw.githubusercontent.com/antonio0720/writing-intelligence/proposal/v9-authentic-voice-provenance-20261027/writing-intelligence-authorship.skill
# pinned versions with checksums: https://github.com/antonio0720/writing-intelligence/releases/latest

# CLI only — the deterministic core, one file, no dependencies
curl -O https://raw.githubusercontent.com/antonio0720/writing-intelligence/main/scripts/wi.py && python3 wi.py --version

# Any other LLM — put SKILL.md in the system prompt (CHEATSHEET.md if context is tight)

# Air-gapped review — copy wi.py + the .wiab onto the machine, then:
python3 wi.py --offline verify-release release.wiab
```

If only the runtime is present, the craft doctrine summarized in [`SKILL.md`](SKILL.md) still governs and the genre packs are one clone away. Degraded, and honestly degraded.

---

## Commands — the v4 floor and the v5 graph

`python3 scripts/wi.py <cmd>` · stdlib-only Python 3.8+ · no network, no model, no dependencies.

| Command | Does | Writes | Exit |
|---|---|---|---|
| `preserve <file>` | Timestamped snapshot before editing (Law B) | `<file>.original-<stamp>` | 0 · 2 missing |
| `scan-sources <paths...>` | Injection, invisible text, bidi, encoded payloads (Law F) | stdout · `--json` | 0 |
| `extract-claims <doc> [--out]` | v4 sentence-level claim ledger | ledger JSON | 0 · 2 error |
| `verify <ledger> <sources...>` | Span lock, quotation, numeric, date, citation (Law D) | ledger JSON, in place | 0 · 2 error |
| `gate <ledger> [--mode] [--exit-code] [--root]` | RELEASE / HOLD / BLOCK with repairs | stdout · `--out` | 0 · with `--exit-code`: 0/1/2 |
| `init [dir] [--title] [--mode] [--force]` | Create `.wi/` workspace + `wi.project.yaml` | `.wi/`, project file, `sources/ drafts/ outputs/` | 0 |
| `ingest <paths...>` | Content-address sources, record versions | `.wi/objects/`, `.wi/workspace.db` | 0 · 2 error |
| `atomize <document> [--out]` | Split sentences into claim atoms | `.wi/graph/ledger-*.json` | 0 · 2 error |
| `anchor <ledger> <sources...> [--tolerance]` | Bind atoms to evidence anchors, run checks | ledger JSON, in place | 0 · 2 error |
| `graph [--json]` | Node and edge tables for the workspace | stdout | 0 · 2 no workspace |
| `impact <source> [--apply] [--json]` | Minimum repair frontier after a source change | marks stale nodes with `--apply` | 0 · 2 error |
| `diff <before> <after> --semantic [--json]` | Classify what a rewrite did to meaning | stdout | 0 · 2 without `--semantic` |
| `test [--tests] [--ledger] [--json]` | Writing tests and concept contracts | stdout | 0 pass · 1 any fail |
| `explain <path[:line]>` | Why this sentence is here: atoms, anchors, checks, dependents | stdout | 0 · 2 no workspace |
| `bundle <out> [--artifact] [--profile] [--mode] [--allow-block]` | Proof-carrying `.wiab` release | the `.wiab` | 0 · 2 at BLOCK |
| `verify-release <bundle> [--json]` | Verify a `.wiab` offline, no model | stdout | 0 valid · 2 tampered |
| `doctor [--json]` | What this surface can and cannot do | stdout | 0 |

Global: `--version` · `--offline` (asserts no network; this build never opens one). Any `WI_` error exits `2`.

---

## Commands — the v6 runtime

Sixteen new subcommands. Same binary, same rules: offline, stdlib only, no model. Every one of these runs.

| Command | Does | Writes | Exit |
|---|---|---|---|
| `canon <path> [--schema] [--show] [--json]` | Canonical form + domain-separated v5 and v6 state digests | stdout | 0 · 2 error |
| `branch [list\|create\|switch\|delete] [name] [--source] [--switch]` | Semantic branches. A branch is a ref — nothing is copied | `.wi/` refs | 0 · 2 error |
| `propose [--node] [--payload] [--from-ledger] [--type] [--realm] [--why] [--actor]` | A change bound to an exact prior state digest | proposal records | 0 · 2 stale binding |
| `proposals [--branch] [--status]` | open · accepted · rejected · deferred · superseded · applied | stdout · `--json` | 0 |
| `simulate [--proposal] [--branch] [--actor]` | What a change would do, before it exists. **Writes nothing** | nothing | 0 · 2 nothing to simulate |
| `decide <proposal> --accept\|--reject\|--defer --actor [--reason]` | Records an authorized decision and its basis (Law P) | decision record | 0 · 2 denied, stale or unknown |
| `commit -m <message> [--actor] [--branch]` | Applies accepted proposals as **one transaction** | new semantic commit | 0 · 2 nothing accepted, or conflict |
| `log [--branch] [--limit]` | Semantic commit history with graph roots | stdout | 0 |
| `merge <branch> [--into] [--actor] [--dry-run]` | Conflict-preserving merge (Law Q). Never averages | merge commit, or nothing | 0 clean · 2 conflict |
| `conflicts [--branch] [--resolve] [--take ours\|theirs] [--actor]` | List unresolved conflicts; resolve one by a named human choice | resolution record | 0 · 2 bad resolve |
| `authority {list,issue,delegate,revoke,check}` | Capability grants: subject, capability, scope, window (Law O) | grant records | 0 permitted · 1 denied |
| `obligations [--branch] [--node] [--mode]` | What must be proved before this can be released | stdout | 0 |
| `as-of [--valid-at] [--known-at] [--node] [--branch]` | Bitemporal query — what was true, and what we knew (Law N) | stdout | 0 |
| `constraints [--branch]` | The graph constraint engine, C001–C020 | stdout | 0 pass · 2 any failed |
| `capsule {create,inspect,verify} [path] [--out] [--select] [--profile] [--hash-only]` | Merkle proof closure and selective disclosure — `.wic` (Law R) | the `.wic` | 0 verified · 2 tampered |
| `why <node> [--branch]` | Backward: the sentence, the node, its anchors, decisions and dependents | stdout | 0 · 2 unknown node |

`--profile` on a capsule: `full` · `redacted` · `hash-only` · `selective`. A redacted leaf still proves it was inside the producer's closure.
Delegation is **monotone**: `authority delegate` can only narrow. Nobody can hand on more than they hold.
`simulate` is the one command that is guaranteed to change nothing. It reports how many nodes are **provably unaffected** with the same prominence as the ones that are.

---

## Exit codes

| Code | Meaning |
|---|---|
| **0** | RELEASE — nothing outstanding, or the query answered yes |
| **1** | HOLD — proceed deliberately (`gate --exit-code`, `test` failure, `authority check` answering no) |
| **2** | BLOCK — a hostile reader can prove it, **or a state transition was refused** |

A refused transition is a `2`. `decide` without a grant, `commit` onto a moved root, `merge` across a semantic conflict, `capsule verify` on tampered bytes, `verify-release` on a broken digest — all `2`. The system does not have a code for *"changed it anyway"*.

`authority check` is a **query**, not a transition: it exits `1` when the answer is no. `decide` under the same denial exits `2`, because that one was trying to move something.

---

## First ten minutes

Runs as written against the shipped fixture. Set `WI` to your checkout.

```bash
WI="python3 $HOME/writing-intelligence/scripts/wi.py"
cd /tmp && rm -rf tenmin && cp -r "$HOME/writing-intelligence/tests/v5/world" tenmin && cd tenmin

# --- the v5 floor: sources in, meaning out, anchors bound -----------------
$WI init --title "Delta Regional Capacity" --mode strict
$WI ingest sources/
$WI atomize drafts/report.md
$WI anchor .wi/graph/ledger-*.json sources/

# --- authority before writing --------------------------------------------
$WI authority issue --subject antonio --capability claim.accept --scope workspace
$WI authority check  --subject antonio --capability claim.accept        # PERMITTED
$WI authority check  --subject nobody  --capability claim.accept        # denied, exit 1

# --- propose, look before you leap, then decide ---------------------------
$WI propose --from-ledger .wi/graph/ledger-*.json --actor antonio --why "initial capacity narrative"
$WI proposals --status open
$WI simulate --branch main --actor antonio      # SIMULATION ONLY — main is unchanged

$WI proposals --status open --json \
  | python3 -c 'import sys,json;print("\n".join(p["proposal_id"] for p in json.load(sys.stdin)["proposals"]))' \
  | while read -r p; do $WI decide "$p" --accept --actor antonio; done

# --- one transaction, one root -------------------------------------------
$WI commit -m "Anchor the capacity narrative" --actor antonio
$WI log --limit 3

# --- branch, merge, and what merge refuses to do -------------------------
$WI branch create review --switch      # a ref; nothing was copied
$WI branch switch main
$WI merge review --actor antonio       # clean here; exit 2 and no movement on a conflict
$WI conflicts                          # and `--resolve <id> --take ours|theirs --actor NAME`

# --- ask the graph questions ---------------------------------------------
$WI why "$($WI graph --json | python3 -c 'import sys,json;print(json.load(sys.stdin)["nodes"][0]["logical_id"])')"
$WI obligations --mode strict          # what must be proved before release
$WI constraints                        # C001-C020: evaluated / not evaluated / failed
$WI as-of --known-at 2026-01-01T00:00:00
$WI canon .wi/graph/ledger-*.json --show

# --- close it out --------------------------------------------------------
$WI gate .wi/graph/ledger-*.json --mode strict --exit-code
$WI capsule create --out out/delta.wic --profile full && $WI capsule verify out/delta.wic
$WI bundle out/delta.wiab --artifact drafts/report.md --mode strict && $WI verify-release out/delta.wiab
```

To see the conflict-preserving merge on a real disagreement — 11,800 against 12,400, and the engine declining to say *"approximately 12,000"* — see the worked example in [`README.md`](README.md).

---

## Claim statuses

| Status | Means | standard | strict | regulated |
|---|---|:--:|:--:|:--:|
| `supported` | The assertion appears verbatim in a supplied source | pass | pass | pass |
| `quote_verified` | A quotation matches the source character for character | pass | pass | pass |
| `span_supported` | Every checkable component sits in **one span of one source**; entailment not judged | pass | pass | **hold** |
| `candidate_support` | Components found across the corpus, **not co-located** | advisory | **hold** | **hold** |
| `author_asserted` | Your own observation; you are the source | pass | pass | pass |
| `inference` | Reasoning from facts, not a fact | pass | pass | pass |
| `recommendation` | Advice, not an assertion about the world | pass | pass | pass |
| `needs_source` | No verbatim support found for a checkable component | advisory | **hold** | **hold** |
| `conflicted` | A supplied source says something incompatible | hold | hold | **BLOCK** |
| `unsafe` | A citation resolves to nothing supplied | **BLOCK** | **BLOCK** | **BLOCK** |
| *stale* | Verified against a superseded source version | hold | hold | **BLOCK** |

**Verdicts:** `RELEASE` nothing outstanding · `HOLD` proceed deliberately · `BLOCK` a hostile reader can prove it.
**Repairs offered on every flag:** attach a source · qualify to match the sources · cut · proceed with a stated caveat (records a waiver).

Coverage counts `supported` + `quote_verified` + `span_supported`. Not `candidate_support`.

---

## Semantic delta classes — `wi diff --semantic`

| Proof impact | Classes |
|---|---|
| **invalidates** | `quantity_changed` · `unit_changed` · `date_changed` · `temporal_scope_changed` · `entity_changed` · `attribution_changed` · `certainty_strengthened` · `negation_changed` · `causality_added` · `scope_broadened` · `obligation_added` · `citation_binding_changed` |
| **re-check required** | `certainty_weakened` · `causality_removed` · `scope_narrowed` · `obligation_removed` · `recommendation_changed` |
| **unaffected** | `wording_only` · `compression` · `expansion` |

Modal lattice: `may` < `should` < `will` / `is` < `must`. Hardening invalidates; softening asks for a re-check.
Deterministic classes only. Paraphrase equivalence is judgment-tier and is **not evaluated** — the diff says so on its last line.

The state layer adds `node_created`, and carries the same table into `wi propose`, `wi simulate` and `wi merge`. A class in the **invalidates** row is what turns a merge into a conflict instead of a fast-forward.

---

## Evidence modes

| Mode | Gate behavior | Use for |
|---|---|---|
| `off` | No extraction, no gate. Craft passes only | Fiction, poetry, personal, brainstorming |
| `light` | Claims listed. `needs_source` / `candidate_support` do not hold | Blog, marketing, internal notes |
| `standard` | **Default.** Those two are advisory | Business, technical, proposals |
| `strict` | Every factual claim needs an anchor or a stated qualification | Grant, NOFO, policy, journalism, investor |
| `regulated` | Strict + `span_supported` holds + conflicts and stale claims block | Medical, legal, regulatory, compliance |

Auto-escalate to `strict` on sight — **skill-layer discipline, not `wi.py`**: grant · NOFO · RFP · funder · IRB · regulatory · clinical · filing · prospectus · due diligence · expert report · court · compliance · audit · fact-check.

`wi gate --mode` takes `light|standard|strict|regulated`. It does **not** read `evidence.default_mode` from `wi.project.yaml` — pass it every time. `wi obligations --mode` takes `standard|strict|regulated` and derives the proof set the same way.

---

## Reliability types

| Type | Produced by | Never rendered as |
|---|---|---|
| `verified` | A deterministic comparison that executed and passed | A percentage · "true" · "accurate" · a claim about the world |
| `measured` | A quantity against a stated baseline, denominator visible | A bare number · a score without its rubric |
| `judged` | A reasoned assessment by a **named** provider | `verified` · "high confidence" · anything unattributed |
| `human-declared` | A named human asserting on their own authority | `verified` · "verified by the team" |

`judged` is produced **nowhere** — no judgment provider ships. The type names how a result was produced, never how sure anyone is. **No percentage without a denominator.**

`wi constraints` obeys the same discipline: **evaluated**, **not evaluated**, **failed**. There is no fourth status and no aggregate score, because an average across those three would hide the ones nobody could run.

---

## `WI_` error codes

Graph and release, from v4 and v5:

| Code | Cause | Repair |
|---|---|---|
| `WI_INPUT_INVALID` | No workspace; missing project file; tabs in YAML; bad argument | `wi init`, or fix the named file |
| `WI_SOURCE_UNREADABLE` | Path does not exist | Correct the path; re-ingest |
| `WI_SOURCE_VERSION_MISSING` | `wi impact` on a file never ingested | `wi ingest <path>` first |
| `WI_BUILD_FAILED` | `wi bundle` with no ledger, or a missing `--artifact` | `wi atomize` then `wi anchor`; check the path |
| `WI_GRAPH_INTEGRITY` | A blob the index references is missing from `.wi/objects/` | Copy the whole `.wi/`, or re-ingest and re-anchor |
| `WI_RELEASE_TAMPERED` | Bundle bytes do not match the manifest digest | Do not repair. Get the bundle again |

State transitions, new in v6 — every one of these is emitted by `scripts/wi.py`:

| Code | Cause | Repair |
|---|---|---|
| `WI_AUTHORITY_DENIED` | The actor holds no grant for this capability in this scope | `wi authority issue`, or act as someone who holds one |
| `WI_AUTHORITY_EXPIRED` | The grant's window closed before the act | Re-issue with a current window |
| `WI_AUTHORITY_REVOKED` | The grant was withdrawn, and revocation is retroactive to the act | Nothing to repair here. Get a new grant |
| `WI_GRANT_SCOPE_EXCEEDED` | A delegation tried to widen what the parent held | Narrow it. Delegation is monotone downward only |
| `WI_PROPOSAL_STALE` | The bound prior state digest no longer matches the graph | `wi propose` again against the current state |
| `WI_DECISION_STALE` | The proposal moved between the decision and the commit | Re-decide against what is actually there now |
| `WI_SEMANTIC_CONFLICT` | Two branches assert incompatible meaning for one node | `wi conflicts --resolve` — a named human picks. Nothing merges by itself |
| `WI_TRANSACTION_CONFLICT` | The graph root moved under an in-flight commit | Re-run the commit against the new root |
| `WI_POLICY_REJECTED` | The act is legal but the workspace policy forbids it | Change the policy deliberately, or do not do it |

Every one of these exits `2`. None of them has a `--force`.

Full v5 registry: [`references/v5/CANONICAL_HASHING.md`](references/v5/CANONICAL_HASHING.md). Authority semantics: [`references/v6/AUTHORITY_MODEL.md`](references/v6/AUTHORITY_MODEL.md) · [`references/v6/CAPABILITY_SECURITY.md`](references/v6/CAPABILITY_SECURITY.md). Merge semantics: [`references/v6/MERGE_PROTOCOL.md`](references/v6/MERGE_PROTOCOL.md).

---

## Full pipeline in nine lines

Runs as written against the shipped fixture. Set `WI` to your checkout.

```bash
WI="python3 $HOME/writing-intelligence/scripts/wi.py"
cd /tmp && rm -rf demo && cp -r "$HOME/writing-intelligence/tests/v5/world" demo && cd demo
$WI init --title "Delta Regional Capacity" --mode strict
$WI ingest sources/
$WI atomize drafts/report.md
$WI anchor .wi/graph/ledger-*.json sources/
$WI test
$WI gate .wi/graph/ledger-*.json --mode strict --exit-code
$WI bundle out/delta.wiab --artifact drafts/report.md --mode strict && $WI verify-release out/delta.wiab
```

Then, to see the rest:

```bash
$WI explain drafts/report.md:5                              # claim, anchor, source sentence, checks
$WI diff drafts/report.md drafts/report-v2.md --semantic    # may reduce -> reduces, 11,800 -> 12,400
sed -i.bak 's/11,800/11,240/' sources/outcomes_report.txt
$WI impact sources/outcomes_report.txt --apply              # repair frontier; 4 anchors provably unaffected
$WI gate .wi/graph/ledger-*.json --mode strict              # now HOLD
$WI graph ; $WI doctor
```

---

## CI

**Pre-commit hook** — block a commit whose narrative no longer survives its sources:

```bash
cat > .git/hooks/pre-commit <<'HOOK'
#!/usr/bin/env bash
set -e
python3 scripts/wi.py ingest sources/ >/dev/null
python3 scripts/wi.py atomize drafts/narrative.md >/dev/null
python3 scripts/wi.py anchor .wi/graph/ledger-*.json sources/ >/dev/null
python3 scripts/wi.py test
python3 scripts/wi.py gate .wi/graph/ledger-*.json --mode strict --exit-code
HOOK
chmod +x .git/hooks/pre-commit
```

**GitHub Actions:**

```yaml
- name: Writing gate
  run: |
    python3 scripts/wi.py ingest sources/
    python3 scripts/wi.py atomize drafts/narrative.md
    python3 scripts/wi.py anchor .wi/graph/ledger-*.json sources/
    python3 scripts/wi.py test
    python3 scripts/wi.py gate .wi/graph/ledger-*.json --mode strict --exit-code

- name: Graph invariants hold
  run: python3 scripts/wi.py constraints

- name: Nothing is waiting on a human
  run: python3 scripts/wi.py conflicts

- name: Release bundle verifies
  run: python3 scripts/wi.py verify-release dist/release.wiab
```

`gate --exit-code` → **0** RELEASE · **1** HOLD · **2** BLOCK. `test` → **1** on any failure, including an assertion this tier does not implement. `verify-release` → **2** on tamper. `constraints` → **2** if any constraint failed. Drop `--exit-code` if you want holds to warn rather than fail.

CI cannot produce a `human-declared` record and cannot approve anything. It holds no capability grant, so it cannot run `wi decide` and cannot resolve a conflict. A green build means the deterministic tier found nothing blocking. It does not mean anybody read it.

---

## The v4 floor — still works standalone, no workspace

```bash
python3 scripts/wi.py preserve draft.md
python3 scripts/wi.py scan-sources sources/
python3 scripts/wi.py extract-claims draft.md --out c.json
python3 scripts/wi.py verify c.json sources/
python3 scripts/wi.py gate c.json --mode strict --exit-code
```

`gate` takes either ledger and reports accordingly. The craft kernel — 11 passes, 12 engines, 12 agents, 27 genre packs, 8 voiceprints, 24 rewrite operators, language tiers — is unchanged from v3/v4. See [`SKILL.md`](SKILL.md).

Nothing in v4 or v5 changed in v6. Every v4 and v5 command, exit code and digest is byte-identical, and every fixture from both still verifies.

---

## What is specified but not executable in this build

`paraphrase entailment` (no judgment provider anywhere) · `pdf_region` · `sheet_range` · `audio_time` · `video_time` · `image_region` anchors · external signing (Sigstore, C2PA) · Workbench · MCP server · REST v5 and v6 endpoints (`services/api/` is the v3 craft runtime).

New in v6, specified in full and **not shipping**: the compiled Rust/WASM core · compiler backends and render source maps · multimodal evidence adapters · the plugin host · judgment providers · semantic remotes and federation · watch mode · autonomous workers · the migration and package systems.

Each has a document under [`references/v6/`](references/v6/README.md) that says what it will do and states plainly that it does not do it yet.

`wi doctor` prints this list on the machine you are standing on. That report is Law C as protocol: a surface states what it cannot do rather than degrading quietly into looking like it did it.

---

## What it refuses

**Fabrication** — it will never construct a citation; absent support is `needs_source`.
**Truth verification** — it checks support *within your supplied sources*; a wrong source yields a supported, false claim.
**Paraphrase judgment** — no provider ships, and every output that could hide that says so.
**Detector evasion** — anti-slop is craft, not laundering.
**Blended scores** — no percentage without a denominator, no averaging across reliability types.
**Model authorship** — a model may never write a verification, sign a decision, or appear as an author or contributor.

New in v6:

**Averaging a conflict** — 11,800 and 12,400 never become "approximately 12,000". There is no flag to pick a side. A human picks, by name, and the record says so.
**Acting without an authority** — no grant, no transition. Delegation narrows and never widens.
**A universal truth score** — no gauge, no health percentage, no single number over the graph.
**Silent auto-merge of consequential state** — a clean merge is fast, a conflicted one stops.
**Rewriting history** — commits, decisions and grants append. Revocation is a new record, not an erasure.
**Cloud dependency in the constitutional path** — the parts that decide anything run offline, on your machine, with no model.

Full list, with the reasoning for each: [`references/v6/NON_GOALS.md`](references/v6/NON_GOALS.md).

---

**Antonio T. Smith Jr. / Density6 LLC** · MIT · v7.0.0
