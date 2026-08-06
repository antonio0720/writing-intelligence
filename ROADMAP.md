# Roadmap

Writing Intelligence is a living project. **v4.0 shipped August 2026.** Here's where it goes next.

Built by **Antonio T. Smith Jr. / Density6 LLC**

---

## v4.0 — Released (August 2026)

**Accountable Authorship System.** The accountability layer above the craft kernel: six operating laws, proposal-based redlines, verbatim span lock, prompt-injection defense on supplied sources, language tiers, voice consent, surface awareness, stated non-goals — and `scripts/wi.py`, a stdlib-only deterministic verifier that runs offline and air-gapped.

Everything listed in the README and `CHANGELOG.md`.

> **Note on numbering.** Earlier roadmaps reserved v4.0 for *Multimodal Writing Intelligence*. Accountability turned out to be the thing that had to ship first — a system that writes across more modalities while still unable to prove a claim is a bigger version of the same problem. Multimodal work moved to **v5.0** and is unchanged in scope.

---

## v3.0 — Released (May 2026)

**Sovereign Writing Operating System.** 11-pass governed kernel. 12 engines. 12 specialist agents. 11 machine-readable schemas. 27 genre packs. Voice fingerprinting. Genre stacking. Epistemic ledger. Arena delivery. Benchmark regression. Storyworld memory. Operator certification. Formal governance.

---

## v3.1 — Reference Implementations (partially shipped)

### REST API Reference Implementation

- [x] Containerized TypeScript service — `services/api/`
- [x] Routes: compile · score · voice · benchmark · repackage · manifest
- [x] Per-tenant auth, rate limits, input sanitization
- [x] Deterministic kernel with test suite
- [ ] OpenAPI 3.1 document *(`docs/api/API_SPEC.md` documents the surface in prose, not as an OpenAPI artifact)*
- [ ] Hosted demo endpoint (rate-limited)
- [ ] Webhook event format for CI/CD writing checks

### CLI Reference Implementation

- [x] Deterministic verification CLI — `scripts/wi.py` (`preserve` · `scan-sources` · `extract-claims` · `verify` · `gate`)
- [x] CI-friendly exit codes — `gate --exit-code` returns 0/1/2
- [ ] Pass-level CLI: `cat draft.md | wi --pass=6 --voice=sovereign_commander`
- [ ] `wi benchmark --against v3.0 --threshold 70%`
- [ ] Single-binary distribution

### MCP Server Reference Implementation

- [ ] Python FastMCP server exposing the 11-pass kernel
- [ ] Node/TypeScript MCP SDK reference implementation
- [ ] Real-time scoring endpoint
- [ ] Voiceprint matching endpoint
- [ ] Genre detection endpoint
- [ ] Epistemic ledger endpoint
- [ ] Arena repackage endpoint

*(`docs/mcp/MCP_SPEC.md` specifies the interface. No implementation ships yet.)*

---

## v4.1 — The Judgment Tier (Target: Q4 2026)

The deterministic tier says outright that it cannot judge paraphrase. That is the single largest gap in v4, and closing it is the next priority.

- [ ] Paraphrase support detection — a claim supported by a source that does not share its wording
- [ ] Entailment classification with a stated confidence basis, never a bare percentage
- [ ] `stale` status wired to content hashing so a verified claim that was later edited is caught automatically
- [ ] Conflict detection *between* supplied sources, surfaced at intake rather than at gate
- [ ] Bibliography-aware citation resolution for `[12]`-style references
- [ ] Waiver ledger — every proceed-anyway recorded with who, when and why

---

## v4.2 — Multilingual Foundation (Target: Q1 2027)

Language tiers ship in v4.0 and are honest about what they cannot measure. This makes the measurements exist.

### Language Packs

- [ ] Spanish, Portuguese, French, German anti-patterns and cadence signatures
- [ ] Arabic writing conventions pack
- [ ] Mandarin writing conventions pack
- [ ] Tokenizer integration so Tier 2 and Tier 3 scripts get real word metrics

### Multilingual Voice and Genre

- [ ] Bilingual voice handling (code-switching awareness)
- [ ] Register calibration for non-English academic conventions
- [ ] Cross-language voice fidelity scoring
- [ ] Localized sermon traditions (AME, Pentecostal, Catholic, Coptic, Latino evangelical)
- [ ] International grant conventions (EU, African Union, multilateral)
- [ ] Government brief conventions (UK / Westminster, EU institutions, OECD)

---

## v4.3 — Collaborative Team Voice (Target: Q2 2027)

### Shared Voiceprint Libraries

- [ ] Team voice fingerprint storage
- [ ] Brand voice enforcement across contributors
- [ ] Multi-author continuity tracking
- [ ] Cross-author voice drift detection

### Editorial Workflow Integration

- [ ] Pull-request-style review for writing
- [ ] Annotated redline as merge artifact
- [ ] Gate-blocked publishing — `BLOCK` stops the merge

### Live Detector Benchmarks

- [ ] Automated benchmark pipeline against public detectors
- [ ] Per-release detector pass-rate verification

*Detector benchmarking measures whether well-built prose is misclassified. It is not evasion work — see `references/v4/NON_GOALS.md`.*

---

## v5.0 — Multimodal Writing Intelligence (Target: 2027)

### Beyond Text

- [ ] Voice fingerprinting from audio samples (podcasts, sermons, speeches)
- [ ] Storyboard graph integration (text-to-image-to-text continuity)
- [ ] Video script ↔ shot list bidirectional binding
- [ ] Audio-drama production manifest (text-to-radio-play)

### Storyworld Operating System

- [ ] Full storyworld memory with multi-book series support
- [ ] Canon arbitration (canonical / sanctioned / fan-tier)
- [ ] Transmedia release pipeline (novel → audio drama → AR experience → game cutscene)

### Adaptive Skill Learning

- [ ] Per-user voice fingerprint refinement over time
- [ ] Per-team genre weighting auto-tuning
- [ ] Personal benchmark history with regression alerts

---

## Permanent non-goals

These are not unbuilt features. They are refusals, and they do not move. Full reasoning in `references/v4/NON_GOALS.md`.

- **Detector evasion.** Never.
- **Source generation.** The system will not construct a citation, ever.
- **Truth verification.** It verifies support within supplied sources. It cannot tell you the source is right.
- **Absolute quality scores.** There is no universal writing number.

---

## How to Influence the Roadmap

1. **Star the repo** — signals demand
2. **Open an issue** — describe what you need and why
3. **Open an RFC** — propose substantive additions per `governance/RFC_PROCESS.md`
4. **Submit a PR** — build it yourself per `CONTRIBUTING.md`
5. **Share results** — run it on your writing, share what worked and what it got wrong

The roadmap is driven by community need, not a corporate product schedule. What gets built next depends on what people actually use and ask for.

---

*[github.com/antonio0720/writing-intelligence](https://github.com/antonio0720/writing-intelligence)*
