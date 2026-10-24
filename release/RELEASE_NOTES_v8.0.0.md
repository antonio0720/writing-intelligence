# Writing Intelligence v8.0.0 — Story Intelligence

**v4–v7 built an evidence standard for prose that makes claims. v8 holds fiction to the same standard — and refuses, permanently, to let a structural pass stand in for a good novel.**

Free. Open source. MIT. Forever.

---

## What this release is, plainly

Four independently built and tested packages, folded into one release. 340 numbered requirements. Four offline engines, stdlib-only Python, read-only against the manuscript, deterministic.

| Part | Requirements | Engine |
|---|---|---|
| Fiction & Thriller Intelligence | FI-01–FI-60 (B001–B060) | [`scripts/wi-fiction.py`](https://github.com/antonio0720/writing-intelligence/blob/v8.0.0/scripts/wi-fiction.py) |
| Arc, Want/Need & Ending Intelligence | N061–N120 | [`scripts/wi-arc.py`](https://github.com/antonio0720/writing-intelligence/blob/v8.0.0/scripts/wi-arc.py) |
| The Craft — openings, action, opposition, suspense, sequences | C121–C180 | [`extensions/wi8/craft03/`](https://github.com/antonio0720/writing-intelligence/blob/v8.0.0/extensions/wi8/craft03/README.md) |
| Japan Story OS | JP-181–JP-340 | [`extensions/wi8/japan04/`](https://github.com/antonio0720/writing-intelligence/blob/v8.0.0/extensions/wi8/japan04/README.md) |

| Wave | What | Status |
|---|---|---|
| WI8-R0 | Additive merge — four fail-closed installers, zero collisions, nothing dropped | **Shipped** — [receipt](https://github.com/antonio0720/writing-intelligence/blob/v8.0.0/plans/receipts/WI8-R0.json) |
| WI8-R1 | The four engines from one tree — `scripts/test-v8.sh` 19/19, every publication gate holds, 340 requirements counted, v4–v7 unchanged | **Shipped** — [receipt](https://github.com/antonio0720/writing-intelligence/blob/v8.0.0/plans/receipts/WI8-R1.json) |
| WI8-R2 | Three bundles under the 200-file ceiling, reproducible, v8 passing inside the extracted story bundle | **Shipped** — [receipt](https://github.com/antonio0720/writing-intelligence/blob/v8.0.0/plans/receipts/WI8-R2.json) |
| FI8-03 → FI8-06, WI8-00 → WI8-43 | Canonical integration into `wi.py` and the v6 graph, manuscript extraction, reader trials, cultural review, EPUB/print proof | **Planned — not built** |

## The rule

**A structural pass is not a good novel.** Mechanical consistency, interpretive signal, human editorial judgment and independent reader reception are four states, and no engine promotes one into another. Fiction, arc and craft publication gates return **HOLD (exit 3)**; the Japan Story OS preflight refuses with exit 2. By design.

## Install — three bundles

```bash
curl -LO https://raw.githubusercontent.com/antonio0720/writing-intelligence/main/writing-intelligence.skill
curl -LO https://raw.githubusercontent.com/antonio0720/writing-intelligence/main/writing-intelligence-craft.skill
curl -LO https://raw.githubusercontent.com/antonio0720/writing-intelligence/main/writing-intelligence-story.skill
```

Claude.ai and Cowork: **Settings → Capabilities → Skills → Upload skill**, once per file. Claude Code: `git clone https://github.com/antonio0720/writing-intelligence ~/.claude/skills/writing-intelligence`.

## What did not change

Every v4, v5, v6 and v7 command, exit code, digest and bundle format. v4 3/3, v5 32/32, v6 70/70, v7 12/12. No migration. MIT.

## Read more

[`references/v8/README.md`](https://github.com/antonio0720/writing-intelligence/blob/v8.0.0/references/v8/README.md) · [`plans/v8.manifest.yaml`](https://github.com/antonio0720/writing-intelligence/blob/v8.0.0/plans/v8.manifest.yaml) · [`CHANGELOG.md`](https://github.com/antonio0720/writing-intelligence/blob/v8.0.0/CHANGELOG.md) · [`USER_GUIDE.md`](https://github.com/antonio0720/writing-intelligence/blob/v8.0.0/USER_GUIDE.md)

Antonio T. Smith Jr. — Founder & CEO, Density6 LLC
