# Writing Intelligence v3.1 — REST Reference Runtime

A real, **deterministic**, tested Node/TypeScript implementation of the Writing Intelligence
v3.0 doctrine's REST surface (spec: `docs/api/API_SPEC.md`). It runs the 11-pass compilation
kernel with **zero LLM and zero ML dependencies** (Law 10) — pure rules + scoring.

- **Stack:** Node 20+, TypeScript, Express, ESM. Runs via **tsx** (no build step). Tests via **vitest**.
- **Author:** Antonio T. Smith Jr. / Density6 LLC · MIT.

## Scope: this service is the v3 craft kernel, not the v4 accountability tier

The repository is at **v4.0.0**. This service is not, and the gap is deliberate.

It implements the **craft** half — the eleven passes, scoring, voice metrics, banned-phrase
detection, arena repackaging. It does **not** expose the v4 accountability layer: no span
lock, no claim ledger, no source-injection scanning, no `RELEASE / HOLD / BLOCK` gate.

That tier has exactly one implementation — [`scripts/wi.py`](../../scripts/wi.py) — and it
stays that way on purpose. Two implementations of a verification rule drift, and the one that
drifts is invisible, because both look correct right up until they disagree about something
that matters. A second copy here would be the first thing to rot and the last thing anyone
would think to check.

If you need v4 checks in a pipeline, shell out to `wi.py`. It is stdlib-only, has no
dependencies, and returns exit codes 0/1/2 for RELEASE/HOLD/BLOCK — see
[`docs/INSTALL.md`](../../docs/INSTALL.md).

## Run

```bash
cd services/api
npm install
npm start          # tsx src/server.ts → http://localhost:4090
npm test           # vitest (31 tests)
npm run typecheck  # tsc --noEmit (0 errors)
```

Auth is a bearer token. Set `WI_API_TOKENS=tok1,tok2`. If unset, the dev token `dev-wi-token`
is allowed and a warning is logged. Optional `x-wi-tenant` header namespaces + salts results.

```bash
curl -s localhost:4090/health
curl -s -X POST localhost:4090/compile \
  -H 'authorization: Bearer dev-wi-token' -H 'content-type: application/json' \
  -d '{"request_text":"Rewrite this.","draft_text":"In today'\''s fast-paced world, we leverage cutting-edge synergy. Book a call today.","intake_overrides":{"arena":"blog_post"}}'
```

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/compile` | Run all 11 passes. 200 / 400 / 422 (ambiguity) / 423 (delivery blocked) / 429 / 500. |
| POST | `/score` | Score a raw draft (no rewrite). |
| POST | `/voice/fingerprint` | Build a `VoiceFingerprintV3` from `{voice_id, samples[]}`. |
| POST | `/voice/drift` | Drift report vs a supplied `baseline_fingerprint`. |
| POST | `/repackage` | Pass-8-only: one `DeliveryBundleV3` per target arena. |
| POST | `/benchmark/run` | Run a benchmark case (`ai_slop_rewrite` implemented). |
| GET | `/manifest` | `agents/agent_manifest.yaml` as JSON + `{version, git_sha}`. |
| GET | `/schemas/:id` | Return a JSON Schema (404 if unknown). |
| GET | `/health` | `{status, version, git_sha}` — no auth. |

## The 11-pass kernel (what is real, not stubbed)

- **Pass 0 Intake** (`passes/intake.ts`) — deterministic mode/intent/audience/voice/arena/policy defaults; `high_stakes` detection. User overrides always win.
- **Pass 1 Mission Lock** (`passes/missionLock.ts`) — success condition + ambiguity (empty input, contradictory word counts) → the 422 path. Missing citations are **not** a 422; they resolve to a 423 block, never a silent guess.
- **Pass 3 Diagnostic** (`passes/diagnostic.ts`) — 165-phrase hard-ban bank (`bannedPhrases.ts`) + passive ratio, sentence-length variance, abstract-noun density, em-dash overuse, AI-opener detection, cadence-flatness runs, deletion-seam + fragment metrics.
- **Pass 5 Epistemic Ledger** (`claimScan.ts`) — extracts claims (numbers, superlatives, universals, factual assertions), classifies class + source status, computes the summary. **The safety gate:** an unsupported factual/numeric claim under `citations_required` / zero-fabrication, or any `unsafe` claim, sets `delivery_block`.
- **Pass 6 Sentence Surgery** (`passes/sentenceSurgery.ts`) — removes/replaces bans to a **fixpoint** (a replacement can expose a shorter ban), emits a `ProseRewriteLogV3`, produces the clean asset with zero residual hard bans.
- **Pass 7 Voice** (`voiceMetrics.ts`) — deterministic fingerprint metrics + drift deltas/direction.
- **Pass 8 Arena** (`passes/arena.ts`) — 20-arena channel-constraint table + satisfaction check.
- **Pass 9 Stress** (`passes/stress.ts`) — reader/editor/skeptic/detector → blocking reasons + soft flags.
- **Pass 10 Score + Delivery** (`passes/score.ts`, `passes/delivery.ts`) — composite scorecard (prose / epistemic / arena / v3_composite, 0–100) + `DeliveryBundleV3` with `release` / `hold_for_review` / `block`.
- Passes 2 (corpus), 4 (architecture), 11 (memory) are recorded in `passes_run`; v1 is stateless, so memory persistence is intentionally a no-op (the benchmark endpoint covers regression).

## Determinism

- `task_id = "wi_v3_" + sha256(canonical({tenant, request})).slice(0,16)`.
- Every artifact/response carries `content_hash = sha256(canonicalJSON(artifact − timestamps))`.
- `created_at` / `ran_at` / `duration_ms` never feed a hash. Same input → same `task_id` + `content_hash` on every run (proven in `tests/determinism.test.ts`). Two tenants get distinct `task_id`s for the same body.

## Honest v1 limitations (heuristics, labelled in code)

- `metaphor_density`, `vocab_tier`, `authority_posture`, `abstraction_tolerance`, `domain_vocab_per_500w` are **heuristics** — marker counts and ratio bands, not semantic understanding.
- Claim classification is rule-based (numbers/superlatives/universals/inflated verbs/citation markers). It flags the checkable, load-bearing cases; it is not a fact-checker.
- The deterministic rewrite deletes/replaces slop; it can leave grammatical seams a human editor would smooth. The scorer penalizes this (deletion aggressiveness + seam/fragment metrics), which is exactly why the `ai_slop_rewrite` benchmark lands in the doctrine's 78–92 band rather than a naive ~95.
- `/voice/drift` requires a supplied `baseline_fingerprint`; there is no server-side voice store in v1 (stateless), so it will not fabricate drift against an unknown `baseline_voice_id`.

## Docker

Build context must be the **repo root** (the manifest + schema routes read `agents/` and `schemas/`):

```bash
docker build -f services/api/Dockerfile --build-arg WI_GIT_SHA=$(git rev-parse --short HEAD) -t wi-api .
docker run -p 4090:4090 -e WI_API_TOKENS=your-token wi-api
```

`WI_REPO_ROOT` (default `/app` in the image) tells the service where `agents/` + `schemas/` live.
