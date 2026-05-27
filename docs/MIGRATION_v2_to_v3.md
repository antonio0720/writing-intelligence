# Migrating from Writing Intelligence v2.0 → v3.0

v3.0 is a category jump, but it is **not** a breaking release. Your v2.0 prompts continue to work. The 7-pass kernel is preserved inside the 11-pass kernel. This guide walks you through what's new, what changed, and where to expand your practice.

## TL;DR

- **Nothing breaks.** All v2.0 prompts continue working.
- **Add 4 passes**: Pass 0 (Intake Contract), Pass 2 (Corpus Governance), Pass 8 (Arena Delivery), Pass 11 (Memory & Benchmark Update).
- **Add 1 mandatory engine for high-stakes work**: the Epistemic Ledger.
- **Voiceprints become measurable**: build a fingerprint, get drift detection.
- **Genre packs can stack**: declare multi-pack stacks with collision resolution.
- **Output gets multi-arena**: one approved piece → many delivery bundles.

---

## What Stays the Same

| v2.0 Capability | v3.0 Status |
|---|---|
| All 19 v2.0 rewrite operators | Preserved + 5 new |
| All 7 v2.0 scoring rubrics | Preserved + 2 new |
| All 16 v2.0 genre packs | Preserved + 11 new |
| 7 voiceprints | Preserved + 1 new (`courageous_builder`) |
| 7-pass kernel | Preserved inside 11-pass kernel |
| Anti-pattern libraries | Preserved |
| Positive construction patterns | Preserved |
| Fiction Intelligence Engine | Preserved, extended into Narrative Intelligence Engine |
| Academic mode | Preserved |
| Test suite | Preserved + 4 new test files |

## What's New

### 11-Pass Kernel

Where v2.0 had 7 passes, v3.0 has 11. The four new passes:

- **Pass 0 (Intake Contract)**: every request becomes a structured task object
- **Pass 2 (Corpus & Context Ingestion)**: explicit source mapping
- **Pass 8 (Genre & Arena Alignment)**: deliver-arena packaging
- **Pass 11 (Memory & Benchmark Update)**: regression discipline

### Epistemic Ledger (Mandatory for High-Stakes)

In v2.0, fact-discipline was an integrity layer. In v3.0, it's a structured ledger.

If you write academic, medical, legal, government, grant, or financial content, the ledger is **mandatory** and the system will refuse to ship a delivery bundle if it contains a fabricated claim or an unsafe source.

To opt-in for non-mandatory work:

```
Run the kernel with epistemic ledger enabled. Emit the ledger.
```

### Voice Fingerprinting

v2.0 voiceprints were qualitative ("cold authority, strategic compression"). v3.0 voice fingerprints are quantitative:

- Average sentence length and variance
- Compression ratio
- Abstraction tolerance
- Metaphor density
- Question frequency
- Top-5 transitions
- Dominant syntactic structures
- Authority posture (0-100)

You can build a fingerprint from your own writing samples:

```
Build a measurable voice fingerprint from these three writing
samples. Save it as my baseline.

[paste 3 samples, 500+ words each]
```

Once a baseline exists, every output is compared. Drift is detected and surfaced.

### Genre Stacking

v2.0 chose one genre pack. v3.0 stacks them:

```
Apply grant_nofo + church_leadership + government_brief. Primary
is grant_nofo; church_leadership is secondary; government_brief
is modulator. Resolve collisions.
```

The Genre Marshal handles the conflict matrix automatically.

### Arena Delivery

One approved piece becomes many delivery bundles:

```
Take this approved memo. Repackage as: LinkedIn post (1,200 chars),
Twitter thread (8 tweets), YouTube short script (90 seconds),
newsletter section (450 words). Preserve voice fingerprint.
```

The Delivery Packager enforces channel constraints. It cannot invent content.

### Schemas

11 JSON Schema files in `schemas/` define every pass artifact. This enables:

- CLI execution
- MCP server execution
- Web app integration
- CI writing checks
- Automated scoring
- Reproducible outputs

If you don't care about programmatic integration, ignore this. If you do, see `docs/api/API_SPEC.md` and `docs/mcp/MCP_SPEC.md`.

### Benchmark Discipline

v3.0 ships with 60 benchmark cases across 12 categories. A release cannot ship until aggregate results meet the gates. You can run benchmark cases yourself:

```
Run benchmark case GRANT-04. Compare to v2 baseline.
```

### Operator Certification

Optional. Free. See `certification/README.md`. Three tiers: Apprentice → Operator → Architect.

---

## Where to Start (by Use Case)

### "I just want better prose."

Keep doing what you were doing in v2.0. Add this to your prompts:

```
Run the v3.0 kernel. Emit scorecard.
```

### "I write grants."

Add the grant_nofo pack to your prompts:

```
Apply grant_nofo + investor_precision. High-stakes. Emit
epistemic ledger and delivery bundle.
```

### "I run a small business."

Add the small_business_operator pack:

```
Apply small_business_operator + courageous_builder voice.
Emit clean + scorecard.
```

### "I write fiction."

Add storyworld memory:

```
Initialize a storyworld memory for [project]. Run the full
kernel on this chapter. Update the memory after.
```

### "I lead a church."

Add the church_leadership pack:

```
Apply church_leadership + sermon. Emit sermon notes structure.
```

### "I create content."

Add cross-arena repackaging:

```
Apply social_media + newsletter + youtube_script. Repackage
this approved piece for LinkedIn, Twitter, newsletter section,
and a YouTube short. Preserve voice fingerprint.
```

### "I'm a developer integrating this."

Read `docs/api/API_SPEC.md` and `docs/mcp/MCP_SPEC.md`. Skim `schemas/` to understand the artifact shapes.

---

## What's Removed

Nothing. v3.0 is purely additive.

## What's Deprecated

Nothing yet. Deprecations will be announced in `CHANGELOG.md` per `governance/VERSIONING.md`.

## Where to Read Next

- `README.md` — public positioning
- `SKILL.md` — kernel doctrine
- `CHEATSHEET.md` — one-page reference
- `USER_GUIDE.md` — 250+ prompts
- `schemas/README.md` — machine layer
- `agents/README.md` — agent layer
- `benchmarks/README.md` — quality discipline
- `governance/RFC_PROCESS.md` — contribute

---

## Author

Antonio T. Smith Jr. / Density6 LLC
