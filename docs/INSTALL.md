# Install

Writing Intelligence v4 runs on six surfaces. They share one doctrine and differ in what they can physically do — whether a filesystem exists, whether scripts can run, whether work persists between turns.

Pick your surface, install once, then read [What each surface can do](#what-each-surface-can-actually-do) so you know which half of the system you are getting.

---

## 1. Claude Code — as a skill *(recommended)*

The fullest surface. Filesystem, scripts, persistence, and the deterministic verifier all available.

```bash
git clone https://github.com/antonio0720/writing-intelligence \
  ~/.claude/skills/writing-intelligence
```

Restart Claude Code. Confirm it loaded:

```bash
ls ~/.claude/skills/writing-intelligence/SKILL.md
```

**Project-scoped instead of user-scoped** — commit the skill into one repository so every collaborator gets it:

```bash
git clone https://github.com/antonio0720/writing-intelligence \
  .claude/skills/writing-intelligence
```

**Updating:**

```bash
cd ~/.claude/skills/writing-intelligence && git pull
```

The skill triggers on any writing, editing, auditing, fact-checking or verification request — including unnamed ones: *"clean this up"*, *"is this accurate"*, *"make this sound like me"*, *"will this hold up?"*

---

## 2. Claude.ai and Cowork — as an uploaded skill

1. Download **`writing-intelligence.skill`** from [Releases → latest](https://github.com/antonio0720/writing-intelligence/releases/latest).
2. In Claude: **Settings → Capabilities → Skills → Upload skill** (labelled **Settings → Skills** in some versions).
3. Select the downloaded `.skill` file.

The bundle is a zip containing the full doctrine payload — `SKILL.md`, all `references/`, `schemas/`, `agents/`, `docs/`, `tests/` and `scripts/wi.py`. It excludes the REST service and repository scaffolding, which are not useful inside a chat surface.

**Verify what you downloaded** before uploading:

```bash
unzip -l writing-intelligence.skill | head
shasum -a 256 writing-intelligence.skill
```

Compare the checksum against `writing-intelligence.skill.sha256`, published beside the bundle on the same release.

---

## 3. Claude Projects

Upload to project knowledge:

- `SKILL.md` *(required)*
- `references/` *(required for depth — v4 laws live in `references/v4/`)*
- `schemas/` *(if you want structured output)*
- `agents/` *(if you want the multi-agent board)*

Projects have no filesystem, so the deterministic verifier cannot run. Claim checking becomes a reasoned judgment rather than a string comparison, and the skill will say so rather than implying otherwise.

---

## 4. Any other LLM

Put the contents of `SKILL.md` in the system prompt. That single file carries the six laws, the evidence modes, the workflow and the pass structure.

Reference files load on demand when the model can read them. When it cannot, the skill is written to degrade honestly — it states which checks it could not run instead of performing them silently.

For a smaller context budget, `CHEATSHEET.md` is the compressed form.

---

## 5. CLI only — no model required

`scripts/wi.py` is the deterministic tier. **Stdlib-only Python 3.8+.** No pip install, no dependencies, no network calls, no model. It runs air-gapped.

```bash
curl -O https://raw.githubusercontent.com/antonio0720/writing-intelligence/main/scripts/wi.py
python3 wi.py --version
```

This is the half of v4 that does not require trusting anything. It compares strings, numbers and dates. See [Commands](#cli-commands).

---

## 6. REST service

`services/api/` is a containerized reference runtime.

```bash
cd services/api
npm install
npm test
npm run dev
```

Or:

```bash
docker build -t writing-intelligence-api services/api
docker run -p 8080:8080 writing-intelligence-api
```

**Scope, stated plainly:** this service implements the **v3 craft kernel** — the eleven passes, scoring, voice metrics and repackaging. It does **not** expose the v4 accountability tier. That tier has exactly one implementation, `scripts/wi.py`, and it stays that way on purpose: two implementations of a verification rule drift, and the one that drifts is invisible because both look correct.

See [`services/api/README.md`](../services/api/README.md) and [`docs/api/API_SPEC.md`](api/API_SPEC.md).

---

## What each surface can actually do

Doctrine is identical everywhere. Capability is not. Full reasoning in [`references/v4/SURFACES.md`](../references/v4/SURFACES.md).

| | Claude Code | Cowork | Claude.ai / Projects | CLI only | REST |
|---|:--:|:--:|:--:|:--:|:--:|
| Craft passes (v3) | ✅ | ✅ | ✅ | — | ✅ |
| Proposal redlines (Law A) | ✅ | ✅ | ✅ | — | partial |
| Snapshot original (Law B) | ✅ file | ✅ file | quoted in chat | ✅ file | — |
| Source injection scan (Law F) | ✅ script | ✅ script | reasoned | ✅ script | — |
| Claim extraction | ✅ script | ✅ script | reasoned | ✅ script | partial |
| **Verbatim span lock (Law D)** | ✅ **string compare** | ✅ **string compare** | reasoned | ✅ **string compare** | — |
| Numeric / date / citation checks | ✅ | ✅ | reasoned | ✅ | — |
| RELEASE / HOLD / BLOCK gate | ✅ | ✅ | advisory | ✅ | — |
| Exit codes for CI | ✅ | ✅ | — | ✅ | — |
| Persists between sessions | ✅ | ✅ | project only | ✅ | ✅ |

**"reasoned"** means the model performs the check by judgment rather than by comparison. That is a real check and it is weaker than a string comparison. The skill labels which one it ran — that labelling is Law C, and it is the difference between a tool you can rely on and one you merely feel good about.

---

## CLI commands

```bash
python3 scripts/wi.py --help
```

| Command | Does | Law |
|---|---|---|
| `preserve <file>` | Timestamped snapshot before editing | B |
| `scan-sources <paths...>` | Flag injection indicators, invisible text, bidi controls, encoded payloads | F |
| `extract-claims <doc> [--out]` | Build a claim ledger from a document | Proof §1–3 |
| `verify <ledger> <sources...>` | Span lock, quotation, numeric, date, citation resolution | D |
| `gate <ledger> [--mode] [--exit-code]` | Emit RELEASE / HOLD / BLOCK with repairs | E |

**Modes:** `light` · `standard` *(default)* · `strict` · `regulated`
**Exit codes** with `--exit-code`: `0` RELEASE · `1` HOLD · `2` BLOCK
**Numeric tolerance:** `verify --tolerance 0.01` allows 1% drift, for rounded figures.

### Use it as a git hook

Block a commit whose narrative no longer survives its own sources:

```bash
cat > .git/hooks/pre-commit <<'HOOK'
#!/usr/bin/env bash
set -e
python3 scripts/wi.py extract-claims narrative.md --out /tmp/c.json >/dev/null
python3 scripts/wi.py verify /tmp/c.json sources/ >/dev/null
python3 scripts/wi.py gate /tmp/c.json --mode strict --exit-code
HOOK
chmod +x .git/hooks/pre-commit
```

### Use it in CI

```yaml
- name: Verify claims
  run: |
    python3 scripts/wi.py extract-claims docs/whitepaper.md --out claims.json
    python3 scripts/wi.py verify claims.json sources/
    python3 scripts/wi.py gate claims.json --mode strict --exit-code
```

A `HOLD` exits 1 and fails the job. If you want holds to warn rather than fail, drop `--exit-code` and read the report.

---

## Verify your install

Whatever surface you chose, this is the check that matters:

```bash
bash tests/v4/test_wi.sh
```

```
PASS injection detected
PASS gate BLOCK
PASS statuses
```

Three passes means the deterministic tier catches a prompt injection, a fabricated citation, an inflated figure and a reshaped quotation on the shipped adversarial fixture. Anything less and the verifier is not doing its job — do not trust its verdicts until it does.

---

## Uninstall

```bash
rm -rf ~/.claude/skills/writing-intelligence      # Claude Code
```

Claude.ai / Cowork: **Settings → Capabilities → Skills →** remove the skill.

Nothing is written outside the skill directory. `wi.py` writes only where you point it: `preserve` creates a sibling `.original-<timestamp>` file, and `extract-claims` / `verify` / `gate` write only to the paths you pass in `--out`.

---

## Troubleshooting

**The skill does not trigger in Claude Code.**
Confirm `~/.claude/skills/writing-intelligence/SKILL.md` exists and that the YAML frontmatter at the top of the file is intact — the `name` and `description` fields are what the loader reads. Restart Claude Code after installing.

**`python3: command not found`.**
The verifier needs Python 3.8 or newer. On macOS it ships with the system; on Debian/Ubuntu, `apt install python3`. There are no other dependencies.

**`gate` returns HOLD on a document I believe is correct.**
That is usually right and worth reading before overriding. The most common causes are: a figure that appears in your source in a different form (`1,200` vs `1200` is handled; `1.2k` is not), a paraphrased claim with no verbatim span, or genuinely missing sources. The deterministic tier cannot judge paraphrase — it says so in its own output — so a `needs_source` on a well-paraphrased claim is a limit of the tier, not a verdict on your writing. Attach the source, qualify the claim, cut it, or proceed with a stated caveat.

**`gate` returns BLOCK on a citation I know is real.**
The citation resolves against *supplied sources only*. If you cited a paper you did not supply, it cannot resolve — correctly. Supply it, or state that the citation is external and unverified.

**Numbers flagged that clearly match.**
Try `verify --tolerance 0.01`. Percentages are canonicalized (`38%` → `0.38`), so a source stating `0.38` and a draft stating `38%` agree.

---

## Getting help

- **Bugs and detector benchmarks:** [Issues](https://github.com/antonio0720/writing-intelligence/issues) — templates exist for bug reports, new genre packs, new voiceprints, new anti-patterns and detector benchmarks.
- **Proposing changes to doctrine:** [`governance/RFC_PROCESS.md`](../governance/RFC_PROCESS.md)
- **Contributing:** [`CONTRIBUTING.md`](../CONTRIBUTING.md)
