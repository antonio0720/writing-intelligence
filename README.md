# Writing Intelligence

**The most advanced writing compiler ever open-sourced.**

52 files. 42,264 words. A 6-pass compilation pipeline that produces prose with authorial identity, argument force, epistemic discipline, and zero AI residue — because language is how the poor build power and the middle class keep it.

**Free. For everyone. Forever.**

Created by **[Antonio T. Smith Jr.](https://density6.com)** — Founder & CEO of [Density6 LLC](https://density6.com)

---

## The Problem

Every AI writing tool on the market does the same thing: removes AI tells. They strip phrases, flag structures, and clean surfaces. The result is prose that doesn't sound like AI — but doesn't sound like anyone, either.

Clean generic prose is still generic prose. And generic prose still gets flagged by detectors, rejected by editors, and ignored by readers.

## The Solution

Writing Intelligence doesn't scrub. It compiles.

Every piece of writing passes through a 6-pass pipeline that enforces voice, argument structure, evidence discipline, paragraph architecture, and sentence-level variance. The output reads as authored — because the system enforces the same standards a great human editor would.

| Pass | Name | What It Does |
|---|---|---|
| 0 | **Mission Lock** | Declare intent, audience, voice, genre before writing a word |
| 1 | **Diagnostic Scan** | Identify AI residue, argument gaps, cadence repetition, vagueness |
| 2 | **Structural Rewrite** | Fix section order, paragraph sequence, thesis placement |
| 3 | **Sentence Surgery** | Anti-slop rules with hard/soft/earned-exception tiers |
| 4 | **Voice Restoration** | Reinject authorial identity so cleanup doesn't flatten |
| 5 | **Stress Test** | Interrogate for weakness, genericity, cuttable content |

The difference between removal and compilation is the difference between a spell-checker and a compiler. One catches mistakes. The other builds systems.

---

## What's Inside

### Anti-Pattern Engine (7 files)
150+ banned phrases organized into hard bans, soft bans, and earned exceptions. 9 structural anti-patterns. 59 cadence signatures across 6 categories. Fake depth detection. Fake authority detection. Genre-specific cliché libraries covering academic, corporate, self-help, tech, political, sermon, fiction, and sales writing.

### Positive Construction System (4 files)
What no other writing skill has. Nine paragraph blueprints with physics auditing. Twelve strong opening and closing types. Six evidence integration techniques with ten enforcement rules. Eight scene grounding methods with an abstraction ladder framework.

### Voiceprint Engine (8 files)
Seven pre-built voice profiles — sovereign commander, literary recursive, sermon (Black church tradition), investor precision, founder manifesto, academic rigorous, and casual sharp — plus a custom voiceprint builder that extracts voice from writing samples.

### Genre Packs (14 files)
Domain-specific compilation rules for strategy, fiction, sales, academic, speech, sermon, email, pitch deck, legal positioning, cinematic narration, dialogue, government brief, medical writing, and patent claims.

### Diagnostics (4 files)
100-point scoring rubric across 10 axes with 8 auto-fail conditions. 14 reversible rewrite operators. 25 categorized failure modes. Auto-diagnostic report format with violation heatmaps and AI detection risk assessment.

### Compiler Core (6 files)
Section architecture. Continuity tracking. Style transfer engine. Auto-mode pipeline configuration. Multi-session Project Memory File. Cross-document consistency auditing.

### Academic Mode (2 files)
Course rubric compiler. Claim-evidence binding. Citation intelligence. Anti-hallucination rules. Authorship proof layer. Class-note anchoring. 8-pass revision stack. 10 discipline-specific reasoning primitive libraries.

### Test Suite (5 files)
Benchmark inputs. Adversarial detector stress tests. Before/after examples. Genre-calibrated gold outputs. Full detector benchmark methodology for 7 commercial tools.

---

## Install

**Claude.ai**: Settings → Skills → Install from file → select `writing-intelligence.skill` from [Releases](https://github.com/writing-intelligence/writing-intelligence/releases)

**Claude Code**:
```bash
git clone https://github.com/writing-intelligence/writing-intelligence .claude/skills/writing-intelligence
```

**Claude Projects**: Upload `SKILL.md` and the `references/` folder to project knowledge.

**Any LLM**: Include `SKILL.md` in your system prompt. Reference files load on demand.

Then write. The skill triggers on any writing, editing, rewriting, scoring, or style transfer task.

---

## Scoring (100 Points)

| Category | Points | What It Measures |
|---|---|---|
| Clarity | 10 | Every sentence parses on first read |
| Specificity | 10 | Named actors, numbers, examples — not abstraction |
| Rhythm | 10 | Sentence-length variance, paragraph cadence |
| Voice Integrity | 10 | Sounds like a specific author, not a model |
| Argument Strength | 15 | Premises support conclusions under pressure |
| Evidence Discipline | 15 | Claims backed by real, verifiable sources |
| Density | 10 | Every sentence earns its place |
| Audience Fit | 10 | Register matches the reader |
| Memorability | 5 | Lines a reader would quote |
| Structural Control | 5 | Sections do their declared jobs |

**95–100**: Signature-grade. **90–94**: Elite. **80–89**: Strong. **70–79**: Usable. **Below 70**: Rewrite.

---

## Comparison

| Capability | stop-slop | deslop | **Writing Intelligence** |
|---|---|---|---|
| Files | 4 | ~6 | **52** |
| Words | ~2,500 | ~4,000 | **42,264** |
| Phrase bans | ~40 | ~30 categories | **150+, tiered** |
| Structural patterns | ~6 | ~6 | **59 total** |
| Voiceprints | 0 | 0 | **7 + custom builder** |
| Genre packs | 0 | 0 | **14** |
| Paragraph architecture | No | No | **9 blueprints + physics** |
| Argument topology | No | No | **Yes** |
| Epistemic integrity | No | No | **Yes** |
| Academic mode | No | No | **Full** |
| Style transfer | No | No | **Any genre ↔ any genre** |
| Multi-session memory | No | No | **Project Memory File** |
| Rewrite operators | No | No | **14 commands** |
| Scoring | 50 pts / 5 axes | 50 pts / 5 axes | **100 pts / 10 axes / 8 auto-fails** |
| Approach | Subtractive | Subtractive | **6-pass compiler** |

---

## File Structure

```
writing-intelligence/
├── SKILL.md                                  # 6-pass compiler core
├── references/
│   ├── anti_patterns/                        # 7 files — detection library
│   ├── positive_patterns/                    # 4 files — construction system
│   ├── voiceprints/                          # 8 files — voice profiles + builder
│   ├── genre_packs/                          # 14 files — domain-specific rules
│   ├── diagnostics/                          # 4 files — scoring + operators + failures
│   ├── compiler/                             # 6 files — architecture + memory + transfer
│   └── academic/                             # 2 files — college writing + disciplines
└── tests/                                    # 5 files — benchmarks + adversarial + gold
```

52 files. Every one earns its place.

---

## Contributing

Pull requests welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

New anti-patterns, voiceprints, genre packs, before/after examples, detector results, discipline primitives, and bug reports all improve the system.

---

## License

[MIT](LICENSE). Use it, fork it, extend it, teach with it, build on it.

Credit appreciated: **Antonio T. Smith Jr. / Density6 LLC**

---

## Author

**Antonio T. Smith Jr.** is the Founder and CEO of [Density6 LLC](https://density6.com) and the inventor of Operational Machine Consciousness (OMC) and Existential Recursive Intelligence (ERI). He builds sovereign infrastructure across AI automation, institutional trading, financial literacy gaming, publishing, and revenue operating systems.

Writing Intelligence was built because the existing tools stopped at removal. This starts where they stop. It compiles prose with authorial identity, argument discipline, and structural integrity — the way writing is supposed to work.

It's free because access to powerful language shouldn't depend on what you can afford. The student at 2 AM and the executive before the board meeting deserve the same tool.

**[density6.com](https://density6.com)** · **[@AntonioTSmithJr](https://twitter.com/AntonioTSmithJr)**

---

*Writing should sound like a person wrote it. This makes sure it does.*
