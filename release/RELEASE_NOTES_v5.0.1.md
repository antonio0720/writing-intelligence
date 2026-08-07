# Writing Intelligence v5.0.1

**Packaging only.** No change to the core, the doctrine, the schemas, or any verdict this system produces. If you already have v5.0.0 running from a clone, nothing about your results changes.

If you tried to **upload the v5.0.0 bundle and it was rejected, this is the release that fixes it.**

---

## What was broken

The `description` field in `SKILL.md`'s frontmatter was 1289 characters. The limit is 1024. A bundle over that limit is not degraded — it is rejected outright, so every install instruction in the repository was a claim that did not survive contact with the loader.

That is the exact failure this project exists to catch, pointed inward: a confident statement nobody had mechanically checked. The description was written to be thorough and never measured.

## What changed

**The description is now 964 characters**, with the full trigger vocabulary intact. What got cut was the architecture summary, not the activation surface — a skill description's job is to fire on the right request, not to explain the system. The skill still triggers on the unnamed cases: *"clean this up"*, *"is this accurate"*, *"check my sources"*, *"what breaks if this number changes"*, *"will this hold up"*.

**`scripts/build-skill.sh` now enforces the limits as build gates.** It parses the frontmatter rather than grepping it, and fails on:

- a description over 1024 characters — printing the over-count, so the fix is arithmetic rather than guesswork
- a name over 64 characters, or outside `[a-z0-9-]`
- a missing or unterminated frontmatter block
- an unquoted description containing `': '` — ambiguous YAML that parses in some loaders and not others, which is the worst class of bug available here because it works where the bundle is built and fails where it is installed

It also warns below 40 characters of headroom, so the next person adding a trigger phrase finds out before they ship.

This sits beside the file-count gate added in v5.0.0, which fails the build above 200 files. **Both limits are imposed by the installer, not by this repository.** The build script refuses to let either be raised in place of trimming, and says so in the failure message.

---

## Verify

```bash
python3 scripts/wi.py --version     # wi 5.0.1
bash tests/v4/test_wi.sh            # 3 checks
bash tests/v5/test_wi5.sh           # 32 checks
python3 scripts/wi.py doctor        # what this surface can and cannot do
```

The bundle attached to this release contains 182 files and a 964-character description. Both are checked at build time, and the build fails rather than publishing an artifact that cannot be installed.

---

## Install

- **Claude Code or any terminal agent:** `git clone https://github.com/antonio0720/writing-intelligence ~/.claude/skills/writing-intelligence`
- **Chat surfaces:** download `writing-intelligence.skill` from this release, then Settings → Capabilities → Skills → Upload skill
- **CLI only:** copy `scripts/wi.py` anywhere Python 3.8+ exists. One file, no dependencies, no network.

Full matrix: [`docs/INSTALL.md`](https://github.com/antonio0720/writing-intelligence/blob/main/docs/INSTALL.md)

---

MIT. Free forever. **Antonio T. Smith Jr. / Density6 LLC**
