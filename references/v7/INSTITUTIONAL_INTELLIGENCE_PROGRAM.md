# Writing Intelligence v7 — The Institutional Intelligence Expansion

**Program identifier:** WI7-IIP
**Date:** 2026-10-21
**Status:** WI7-00, WI7-01, WI7-02 SHIPPED with receipts in 7.0.0 · WI7-03 … WI7-19 PLANNED — NOT IMPLEMENTED
**Baseline:** `antonio0720/writing-intelligence`, `main` at `b59ef9544e9da78bab3dfa8db2178d4e6b569d16`
**Owner of objectives:** Repository/platform owner
**Execution authority:** This plan grants none for external filings, solicitation submissions, investor outreach or deployment. Repository writes for 7.0.0 were authorized by the owner on 2026-10-21.
**Status source:** [`plans/v7.manifest.yaml`](../../plans/v7.manifest.yaml) — the only place a wave's status lives. Receipts: [`plans/receipts/`](../../plans/receipts/).
**Version decision:** [`RFC-0001-VERSIONING.md`](RFC-0001-VERSIONING.md) reconciles this program with the earlier v7.0 sovereign-runtime target. That runtime is preserved as the substrate (W13–W28 in `plans/v6.manifest.yaml`).

---

## 0. Executive decision and wave overview

**Mission:** Make Writing Intelligence the trusted environment for creating and governing work whose consequences are academic, legal, financial, contractual, regulatory, or institutional — not merely a place that produces polished prose.

**Market claim:** Companies should be able to discover, qualify for, prepare, defend, and track investor capital, government grants, procurement contracts, and major private-sector awards from a single evidence-governed operating environment. Doctoral researchers, attorneys, prosecutors, defense counsel, inventors, and institutions should use the same sovereign proof substrate through purpose-built domain workflows.

**What the program is not:** A promise of undetectable academic ghostwriting; a guarantee of legal correctness; a licensed broker-dealer; a law firm; a grant-award agency; a substitute for public procurement portals; or a guarantee of billions in investment or contract awards.

| Wave | Workstream | Primary outcome | Requires | Exit receipt | Status |
|---|---|---|---|---|---|
| WI7-00 | Constitutional recovery | Freeze baseline; prohibit repo-review loop | — | SHA, inventory, explicit gaps | **SHIPPED** |
| WI7-01 | Conflict repair | Resolve academic detector-evasion contradiction | 00 | Accepted RFC, adversarial tests | **SHIPPED** |
| WI7-02 | Reproducibility floor | Prove actual v4/v5/v6 behavior before extension | 00 | Tests, doctor, distribution audit | **SHIPPED** |
| WI7-03 | Product contracts | Define domain and opportunity invariants | 01, 02 | Schemas, policy matrices, negative tests | PLANNED |
| WI7-04 | Security/privacy foundation | Tenant, matter, academic, deal and bid isolation | 03 | Cross-boundary refusal drills | PLANNED |
| WI7-05 | Evidence adapters | PDF, DOCX, XLSX, court and solicitation anchors | 02, 04 | Digest-bound parsing, negative controls | PLANNED |
| WI7-06 | Doctoral Research OS | Govern research, dissertations and defenses | 03, 04, 05 | Academic policy and thesis pilot | PLANNED |
| WI7-07 | Legal Practice OS | Separate litigation, prosecution and defense | 03, 04, 05 | Jurisdictional, citation, discovery drills | PLANNED |
| WI7-08 | Capital Readiness OS | Investor-grade data rooms and large-round narratives | 03, 04, 05 | Reconciled diligence package | PLANNED |
| WI7-09 | Opportunity Intelligence | Provenance-rich opportunity intake and amendments | 03, 04, 05 | Freshness and contradiction tests | PLANNED |
| WI7-10 | Grants OS | Federal/state/local/foundation grant lifecycle | 06, 09 | Eligibility, package and status receipts | PLANNED |
| WI7-11 | Contract Capture OS | Federal/state/local/private bid lifecycle | 09 | Bid/no-bid, compliant response, submission proof | PLANNED |
| WI7-12 | Institutional Deals OS | Major private RFPs, partnerships, sponsorships | 08, 09 | Due diligence + authorized deal workflow | PLANNED |
| WI7-13 | Investor Participation | Consent-based discovery; regulated boundary | 04, 08 | Legal counsel gate, opt-in pilot | PLANNED |
| WI7-14 | Extensions | IP, science, policy, regulatory, real estate, nonprofit | 03, 04, 05 | Pack certification by domain | PLANNED |
| WI7-15 | Institutional Workbench | One multi-arena interface, one proof engine | 06–14 | Cross-surface parity, audit trail | PLANNED |
| WI7-16 | Governed autonomy | Bounded workers; submission grants; no silent decisions | 04, 09, 15 | Replayed authorized and refused workflows | PLANNED |
| WI7-17 | Reality learning integrations | Feedback without changing proof semantics | 15, 16 | Evidence changes future recommendation with audit | PLANNED |
| WI7-18 | Pilot, business validation | Demonstrate trusted workflows with actual users | relevant waves | Measured improvements and independent outcomes | PLANNED |
| WI7-19 | Certification and release | Secure, portable, reproducible domain products | 02, 04, 18 | Independent conformance and release checks | PLANNED |

**Interpretation:** These are program identifiers, deliberately not the v6 development waves W00–W28. Existing technical dependencies (W13 judgment gateway through W28 migration) remain authoritative. Parallel domain prototyping may happen only behind capability declarations; production claims wait for the required substrate.

---

## 1. Recovery checkpoint: proof we are not in a repository loop

### CP-00 — Repository baseline frozen

Observed: `main` at `b59ef9544e9da78bab3dfa8db2178d4e6b569d16`, read back from the public remote and from a fresh clone. Receipt: `plans/receipts/WI7-00.json`.

**Do not re-run the same repository search.** The baseline is closed unless (a) the branch SHA changes; (b) a named acceptance test fails and requires a bounded read of the affected file and its dependencies; or (c) new evidence identifies a material omission. Each new read records the exact question, path, reason, SHA and disposition. A new pass over the whole repository without one of those triggers is a defect.

### Receipts live in one place

The plan proposed a `.wi/programs/WI7-IIP/` layout. It was **not** created: the existing manifest contract already owns program status, and a second truth source would be the defect this program forbids. Receipts live in `plans/receipts/<wave>.json`; `plans/v7.manifest.yaml` names them; `scripts/check-manifest.py` reads them.

A receipt carries: checkpoint ID; program; baseline SHA; objective; commands; environment; observed result (exit codes, PASS counts, stdout digests); negative controls; an independent readback; the explicit unknown list; remaining issue; next authorized action. Values that were not measured remain `UNKNOWN` — a receipt with an empty required field cannot make a wave shipped.

### Stop/recovery state machine

`NOT_STARTED → IN_PROGRESS → {PASS | FAIL | BLOCKED}`. Only PASS authorizes dependent wave progression. From FAIL: investigate → root-cause → repair at the correct layer → re-test → regression → independent proof → a new receipt; a failed receipt is never relabeled. BLOCKED names a missing authority, dependency or evidence and a recovery action. A lost execution context resumes at the last PASS, not the latest narrative summary.

### Anti-stall limits

1. One bounded discovery pass per named unknown, then a finding, an unresolved question or BLOCKED.
2. No more than one unresolved authority/architecture question per checkpoint; record the others rather than reopening the whole investigation.
3. No plan-as-implementation: roadmap checkmarks cannot substitute for executable, independently read tests.
4. No unfalsifiable progress: every pass has a condition a negative control could disprove.
5. No release claim until artifact checksums, installation verification, deterministic tests, real adapter tests and release readback all pass.
6. No outcome claim (admission, award, financing, contract, case result) until recipient-side or authoritative independent evidence exists.

---

## 2. What the existing repository actually provides

From the pinned repository, and re-executed for WI7-02:

- **v3:** 11-pass craft kernel, voiceprints, genre packs.
- **v4:** accountable authorship; support must point to an exact ingested span; source content is not runtime instruction; no fabricated citations.
- **v5:** claim atoms, evidence anchors, semantic dependencies, minimum repair frontier, immutable proofs, release bundles, local verification.
- **v6:** bitemporal semantic state, scoped/expiring authority, proposals, counterfactual simulation, conflict-preserving merge, selective proof capsules.
- Domain packs already present: `academic`, `legal_positioning`, `pitch_deck`, `grant_nofo`, `government_brief`, `patent_claims`, `strategy`, `small_business_operator`, and others. `references/academic/academic_mode.md` specifies rubrics, citation discipline, originality provenance and oral-defense preparation.
- The core is MIT-licensed and offline-capable. A paid institutional service must not make false exclusivity claims over it.

**Not shipped:** judgment provider/gateway, PDF/XLSX/DOCX and media anchor execution, a stable multi-user Workbench, signatures, semantic remotes/federation, Rust/WASM parity, domain policy enforcement, government submission adapters, investor onboarding, legal filing support, a production-grade data room. `wi doctor` states these as specified-not-executable.

### The contradiction WI7-01 resolved

At the baseline, `references/genre_packs/academic.md` carried a section devoted to helping academic writing avoid AI detection — simulated class observations, planted imperfection — while `references/v4/NON_GOALS.md` and `ROADMAP.md` refuse detector evasion. The same framing appeared in `references/compiler/style_transfer.md` (a transfer chain aimed at being undetectable), `references/compiler/auto_mode.md` (a pass running academic evasion rules) and `references/voiceprints/custom_voiceprint_builder.md` (a voiceprint pitched as unflaggable by detectors). The exact retired phrases are listed in `tests/v7/test_wi7.sh`. All four were rewritten in 7.0.0 to demand authentic author-supplied observations, honest uncertainty and institution-compliant disclosure. `tests/v7/test_wi7.sh` fails if any of that language returns.

**Product interpretation:** "Private doctoral workspace" means confidentiality, local-first support, institution-aware consent and authentic student research ownership — not concealed AI use. Where a university, supervisor, funder or publisher requires disclosure, the workflow supports compliant disclosure. No AI-detection bypass marketing.

---

## 3. The market: a portfolio of consequential work

Priorities are hypotheses based on fit to existing capabilities, not measured TAM or customer demand.

| Arena | Primary customers | Consequential deliverables | Priority |
|---|---|---|---|
| Doctoral research | PhD, DBA, EdD, DNP candidates | Prospectus, proposal, IRB packet, systematic review, dissertation, oral defense | P0 |
| Research labs/universities | PIs, postdocs, research offices | Protocols, manuscripts, research grants, datasets, rebuttals | P1 |
| Legal — civil litigation | Firms, in-house counsel | Complaints, answers, discovery, motions, briefs, settlement materials | P0 |
| Legal — prosecution | Authorized government prosecutors | Disclosure inventories, charging/review memos, motions, trial preparation | P0 gated |
| Legal — criminal defense | Licensed defense teams, public defenders | Evidence indices, mitigation, discovery, motions, appeals | P0 gated |
| Capital readiness | Startups, growth companies, sponsors | Model, deck, data room, diligence, investor memo | P0 |
| Large-scale capital | Growth equity, infrastructure, project finance, PE/credit | Institutional memorandum, structured financing package, risk cases | P1 |
| Federal grants | Nonprofits, companies, research teams | NOFO match, compliant application, budgets, reports | P0 |
| State/local grants | Municipalities, nonprofits, small firms | State program applications, local programs, attachments | P0 |
| Federal contracts | Businesses, primes, subs | Capture plan, proposal, teaming, pricing, performance | P0 |
| State/local procurement | Texas and multi-state vendors | Qualification, sourcing, RFP/RFQ/IFB response | P0 |
| Private large contracts | Enterprise suppliers, contractors | Vendor prequalification, enterprise RFPs, MSA/SOW | P1 |
| Corporate M&A | Buyers, sellers, advisors | CIM, diligence, synergy thesis, risk register | P1 gated |
| Private equity/credit | Funds, portfolio companies | Credit memos, covenants, IC materials | P1 gated |
| Invention/IP | Inventors, R&D companies, patent counsel | Invention disclosures, prior-art matrices, patent drafts | P1 gated |
| Insurance/claims | Claims teams, adjusters, counsel | Claim packages, loss documentation, reserve memo | P1 |
| Regulatory affairs | Healthcare, energy, fintech, compliance | Regulatory responses, audits, licenses, remediation | P1 gated |
| Government policy/legislative | Agencies, government affairs | Fiscal notes, policy briefs, public comments | P2 |
| Expert testimony/forensics | Expert witnesses and their counsel | Expert reports, exhibits, deposition prep | P1 gated |
| Healthcare/research administration | Researchers, hospitals, clinical teams | Protocols, research reports, credentialing docs | P2 gated |
| Education beyond doctoral | Faculty, accreditation bodies | Accreditation self-study, curricular changes, tenure dossier | P2 |
| Philanthropy/endowments | Foundations, major gift teams | Case for support, impact reports, donor diligence | P1 |
| Infrastructure and construction | EPCs, developers, utilities | RFQ, feasibility, design narrative, bonding capacity | P1 |
| Cross-border commerce | Exporters, importers, international vendors | Tender documentation, trade compliance, multilingual bids | P2 |
| Nonprofit social impact | NGOs and coalitions | Logic models, audited outcomes, blended financing | P1 |
| Public-private partnerships | Sponsors, municipalities, concessions | Business case, procurement response, finance/operating plan | P2 gated |
| Corporate crisis/recovery | Restructuring teams, boards | Recovery proposals, creditor packages, incident narratives | P2 gated |

**Expansion clusters (brainstormed, not committed):** Sovereign Deal Room · Dissertation Defense Studio · Institutional Bid Exchange (never misrepresenting an official portal) · Research-to-Commercialization Path · Certified Evidence Library · Major Award Command · Counterparty Confidence Room · Board and Investment Committee Intelligence · Cross-Institutional Project Rooms.

**Selection rule:** prioritize the job with a costly failure, expensive expert review, repeatable evidence, and a verifiable endpoint. Do not assume the broadest audience is the first economic buyer.

---

## 4. Governing product architecture

```
CANONICAL WI MEANING/PROOF CORE (v4–v6, re-tested at WI7-02)
  immutable sources -> claim atoms -> evidence anchors -> argument/meaning graph
  -> bitemporal revisions -> scoped authorities -> simulations -> proof obligations
  -> human decisions -> governed artifacts -> selective proof capsules
                              |
           +------------------+------------------+
           |                  |                  |
     DOMAIN CONTRACTS   OPPORTUNITY STATE   PROOF/OUTPUT CONTRACTS
           |                  |                  |
   Doctoral · Legal · Capital · Grants · Procurement · Deals
           |
      INSTITUTIONAL WORKBENCH (surface; never proof authority)
           |
   permitted adapters: repositories, authoritative opportunity portals,
   institution-owned records, storage, authorized delivery endpoints
           |
   INDEPENDENT RECEIPTS / DECISIONS / OUTCOME RECONCILIATION
```

### Five governing rules

1. **One proof engine.** Domain packs derive obligations from canonical state; no UI reimplements `verified`.
2. **One authoritative owner per external fact.** A portal notice is a source snapshot; a customer declaration is customer evidence; a bank settlement is finance evidence.
3. **Capability and authority are separate.** Being able to prepare a filing does not make the system the signer, attorney, prosecutor, issuer, procurement officer or authorized representative.
4. **No semantic flattening.** A research hypothesis, binding legal rule, disputed witness statement, forecast cash flow, solicitation requirement and executed contract are different claim types.
5. **Proof is not outcome.** A proof capsule attests to internal integrity, not that an institution accepted, awarded, ruled or funded.

### Canonical domain objects (proposed for WI7-03)

```yaml
EvidenceObject:
  source_id: content_addressed
  origin: user|official_source|counterparty|external_attestation
  observed_at: timestamp
  valid_interval: [start, end]
  rights_and_handling: scoped_policy
  provenance: exact_locator_and_digest
  freshness_policy: explicit

InstitutionalOpportunity:
  kind: grant|public_contract|private_contract|equity|debt|research|other
  issuer_or_buyer: verified_or_declared_identity
  original_notice: EvidenceObject
  amendment_versions: [EvidenceObject]
  eligibility_rules: versioned_domain_policy
  stage: discovered|screened|qualified|go|no_go|drafting|review|submitted|acknowledged|awarded|declined|withdrawn|closed
  authority_for_next_effect: capability_grant

SubmissionAttempt:
  candidate_artifact_digest: sha256
  target_system: named_external_system
  submitter_identity: authorized_human_or_allowed_agent
  deadline_basis: source_and_timezone
  idempotency_key: canonical_key
  status: prepared|approved|attempted|confirmed|rejected|unknown
  receipt: externally_observed_or_null

Decision:
  actor: named_authorized_human
  scope: exact_capability_and_target
  knowledge_time: timestamp
  basis: evidence_refs
  target_graph_root: digest
  ruling: approve|reject|defer
```

These map onto the existing schema and v6 semantic IR first. Anything not representable becomes a versioned proposal and migration with parity tests — never an ad hoc field or an alternate writer in `scripts/wi.py`.

---

## 5. Doctoral Research OS (WI7-06)

**Target work:** prospectus → research question → literature review → theory/conceptual framework → methodology → human-subjects/IRB → data/evidence → analysis → chapters → committee revisions → oral defense → final deposit/publication.

- Program handbook, formatting guide, rubric, department policy, approved proposal and committee comments are versioned source objects.
- Research-question genealogy: every hypothesis traces to supporting and contradicting literature, design choices and the researcher's own decisions.
- Literature provenance with DOI resolution where available; a source not read remains a candidate, never a citation.
- Qualitative: pseudonymization, consent boundaries, codebook versions, disagreement matrices, memo trails, no invented interview findings.
- Quantitative: dataset hashes, variable dictionary, reproducible analysis specifications, figure lineage, no manufactured statistics.
- Mixed methods: evidence-type tags; themes never conflated with statistical inference.
- Chapter compiler: template, headings, tables/figures, citation style, source maps; compilation cannot alter findings.
- Committee feedback becomes typed change requests simulated across proposal, instrument, chapters and bibliography.
- Defense preparation grounded in the student's approved findings, uncertainty and limitations; a mock defense is rehearsal, never approval.
- Academic integrity mode: institution/funder/publisher AI-use policy, original-idea provenance, required acknowledgments. No promise that output is undetectable.

**Acceptance:** missing citation, fabricated source, wrong DOI, reversed result, invented interview, changed denominator, IRB-incompatible disclosure, altered statistical method, unsupported novelty and fake class observation each block or open an obligation. Passes only on a real author-permitted project with independent committee-style review.

---

## 6. Legal Practice OS (WI7-07) — three products, one accountability foundation

Never "100% accurate law". Target: 100% conformance to explicitly declared, independently tested gates for supported matter types, courts, dates and workflows. Unsupported courts, rule versions or environments refuse.

**6A Core practice:** court-specific filing requirements with effective dates; source-of-law hierarchy; adverse-authority duty and citator integration when licensed; matters as isolated workspaces with privilege/work-product handling, conflicts screens and holds; separation of stated fact, testimony, admission, disputed claim, holding, dictum, analogy and argument; filing authority reserved to identified humans.

**6B Prosecutor mode:** authorized teams only; discovery universe and disclosure obligations; exculpatory/impeachment issue spotting (Brady/Giglio), witness benefits, preservation, materiality and deadlines; the prosecutor decides; no agent may suppress adverse evidence; disclosed-versus-withheld ledgers with rationale and authority.

**6C Criminal-defense mode:** strict defense-only boundary; no import from prosecution tenants; challenges to probable cause, chain of custody, credibility, constitutional issues, forensic reproducibility, mitigation, appeal issues; client narrative, verified records, witness reports, hypotheses and arguments kept distinct; counsel reviews all strategy and filings.

**Negative controls:** fabricated precedent, overturned/nonbinding authority, expired rule, wrong court, missing adverse fact, altered quotation, wrong effective date, privilege leakage, sealed-evidence exposure, exculpatory omission, prosecution/defense cross-access, unauthorized submission — each with an exact expected refusal or `needs_review`.

**Reference boundary:** ABA Formal Opinion 512; DOJ Justice Manual §9-5. Both must be applied to current jurisdiction, rule and facts, and versioned.

---

## 7. Capital Readiness OS (WI7-08)

**Distinct sources:** bootstrapping · friends-and-family · angel · accelerator · seed · Series A–late stage · growth equity · PE · strategic corporate · sovereign/institutional fund · family office · debt · venture debt · project finance · infrastructure finance · revenue-based · philanthropic/PRI · government-backed. "Pitching billions" means diligence-grade readiness and correct structure, not arbitrary asks.

**Deliverables:** business case and sourced market thesis; model with sensitivity; a scenario book separating OBSERVED, ASSERTED, PREDICTED and SIMULATED; unit economics and cohorts; cap table and dilution with dates and counsel review; milestone capital plan and use of proceeds; institutional deck, memo, diligence answers, risk disclosure, conflicts log; per-recipient data room with expiry and selective disclosure capsules; an objection → correction → approved new version loop that never backdates a deck.

**Investor participation boundary (WI7-13):** start with issuer-owned rooms, preparation and consent-based discovery. No holding funds, routing trades, unreviewed recommendations, return promises, solicitation outside an exemption, or success-based placement fees without qualified securities counsel and any required registration. Rule 506(b) and 506(c) workflows need distinct solicitation and verification controls. Release gate: written counsel scope opinion, role determination, marketing review, privacy impact, qualification protocol, access restrictions, adverse drills, fee-model review; each country gated separately.

---

## 8. Opportunity Intelligence (WI7-09)

Discover authoritative opportunities, prove each is open and relevant, avoid spending bid capacity on non-qualifying work, and keep one versioned record of what the source required at decision time.

| Segment | Authoritative starting points | Critical distinction |
|---|---|---|
| US federal grants | grants.gov, agency funding pages | NOFO, eligibility, application package, AOR |
| US federal contracts | sam.gov/opportunities, agency portals | Solicitation, amendments, CLINs, FAR/agency terms |
| US spending context | usaspending.gov | Historical awards do not prove current availability |
| Texas grants | Comptroller grant resources, agency programs | Grant opportunity, not procurement bid |
| Texas contracts | ESBD, CMBL, DIR | ESBD search does not submit bids |
| City/county/local | Named buyer portals | Portal and registration vary by buyer |
| Prime-subcontracting | Prime notices, permissioned supplier opportunities | Flow-down terms, teaming |
| Private enterprise | Verified procurement pages, explicit invitations | Counterparty authenticity, NDA |
| International | Country procurement systems | No assumed equivalence of law, currency or process |

**Required source record:** notice ID, issuing authority, authoritative URL, snapshot digest, observed time, posted/updated/due time with timezone, amendment history, procurement type, open/closed state, place of performance, funding source, registrations, certifications, bonding, insurance, past performance, evaluation instructions.

**Lifecycle:** DISCOVERED → SOURCE_VERIFIED → ELIGIBILITY_CHECKED → BID_NO_BID → CAPABILITY_RESERVED → CAPTURE → PREPARE → COMPLIANCE_GATE → AUTHORIZED_SUBMISSION → RECEIPT_CONFIRMED → EVALUATION → AWARD/DECLINE → EXECUTION → PAYMENT/REPORTING → CLOSEOUT/LEARNING. Reject early on an unavailable source, expired deadline, missing registration or certification, no capacity, impossible insurance/bond, negative economics, conflict, prohibited communication, or no remaining bid capacity.

**Hard status semantics:** FOUND ≠ ELIGIBLE ≠ DRAFTED ≠ ATTEMPTED ≠ SUBMITTED (portal readback) ≠ AWARDED (issuer evidence) ≠ FUNDED (finance evidence) ≠ ATTRIBUTED (designed comparison).

**Capture economics:** model expected contribution — conditioned probability, qualification and proposal cost, bonding/insurance, fulfillment cost, cash conversion, working-capital peak, collection risk — labeled PREDICTED. A large contract with negative cash economics is not a win.

---

## 9. Grants OS (WI7-10)

Versioned NOFO requirement extraction and a one-to-one compliance matrix; eligibility by entity type, geography, match, status and scope; named Authorized Organization Representative; logic model, evaluation design, budget/narrative crosswalk, allowability, subrecipients, sustainability; source-locked numbers; funder-specific forms, limits and formats; preflight for unpublished amendments, conflicting dates, missing certifications and unapproved signatories. Submission only through supported authorized means with receipt readback — otherwise `READY_FOR_MANUAL_SUBMISSION`, never `SUBMITTED`. Post-award: agreements, deliverables, revisions, reports, reimbursement, closeout. Assistance awards, procurement contracts and private foundation grants stay distinct.

---

## 10. Contract Capture OS (WI7-11)

**Federal:** intake → capture decision → NAICS/PSC and set-aside fit → teaming → instruction/evaluation crosswalk → past performance → technical/management/staffing → cost/price → review → amendment acknowledgment → submission → debrief → execution, under the rules effective for that solicitation.

**State:** agency portals, commodity codes, vendor registration, program rules, HUB requirements where applicable (a Texas HUB is not a federal HUBZone), bonds, schedules, exceptions, questions.

**Local:** counties, cities, school districts, universities, utilities, transit; RFQ, RFP, IFB, cooperative and emergency procurement as distinct mechanisms.

**Private:** enterprise RFPs, supplier onboarding, security questionnaires, insurance evidence, pricing, NDA, MSA/SOW, vendor risk, change orders, receivables.

**Bid quality contract:** every mandatory requirement maps to a response section, a literal source and an evidence object. No claimed past performance, certification, team member, equipment, price, insurance limit or subcontractor commitment without a basis. The compliance gate blocks a missing bond or a forbidden exception regardless of prose quality.

---

## 11. Institutional Deals OS (WI7-12)

Joint ventures, sales partnerships, franchise, licensing, sponsorship, distribution, infrastructure delivery, technology transfer, IP commercialization and large enterprise procurement: partner qualification, entity verification, authority to negotiate, NDA handling, term comparison, unit economics, acceptance terms, exclusivity, milestones, dispute and exit, counterparty capacity, executed-agreement evidence. An unsigned term sheet is never binding contractual revenue.

---

## 12. Further domain engines (WI7-14)

**P1:** Invention & IP OS (no promise of patentability or title) · Scientific Publishing & Peer Review OS · Accreditation & Institutional Compliance OS · Insurance/Forensic Claim OS · Economic Development & Project Finance OS · Nonprofit Institutional Giving OS.
**P2:** Government Affairs & Public Policy OS · Healthcare/Clinical Research Governance · International Tender OS · M&A and Corporate Restructuring OS.

Every pack needs a typed semantic schema, evidence mode, license/security classification, professional reviewer requirement, output contract, negative tests and a real pilot. Domain names alone are not products.

---

## 13. Security and professional responsibility controls (WI7-04)

Encryption at rest and in transit; local/offline options; tenant and matter isolation; least-privilege expiring grants; consent-bound intake; permission to disclose by recipient; retention, deletion and holds; redaction; source quarantine and prompt-injection rejection; secrets outside proof objects; regulated-data audit; idempotent submission; time-bound decisions; integrity-bound receipts; emergency revocation; documented recoverability.

**Threat cases:** an adversarial PDF issuing commands; an invented legal authority; cross-issuer data-room access; privileged material sent to a general provider; a stale amendment; a resubmission after an ambiguous timeout; a fabricated thesis interview; estimated deal value published as revenue.

No claim of classified, CUI or HIPAA-regulated handling without the compliant environment and a scoped certification. Denied access, unauthorized submission, stale evidence, wrong policy and disclosure refusal each produce a negative-proof receipt; absence of a log entry is not evidence of safe failure.

---

## 14. Integration with the broader sovereign infrastructure

Proposed interfaces only; owner paths are not verified by this document. Writing Intelligence is authoritative for semantic claims and proof, not for every operational system.

| System | Candidate responsibility | Boundary |
|---|---|---|
| Reality-Reconciled Learning (RRL) | Turn outcome evidence into revised policies | Never alters historical proof or past decisions |
| Sovereign Cortex | Analysis, planning, proposals | Produces judgments and proposals, not verified facts or signatures |
| Unified Intelligence Plane (UIP) | Route typed evidence and state | Preserves provenance, type, authority and time |
| PULSE / DF-WPI / HELM | Observation, policy, routing, execution | Binds to real owner paths; no parallel coordinator |
| MIR / IOR / SIR | Execution planning, intervention, reconciliation | Each external effect authorized and receipted |
| Driftless front ends | Customer experience | Thin surface, no second proof engine |
| Finance/revenue owners | Invoice, cash, receivable, funding receipt | A rendered contract cannot write ledger reality |

Integration is complete only when the receiving owner independently reads and uses correctly typed evidence. **Learning experiment:** introduce a stale notice or contradicted financial fact, observe a correction proposal, obtain an authorized decision, and prove the next comparable work changes behavior.

---

## 15. Wave exit tests

- **WI7-00 — Freeze and reconcile.** Pin SHA, canonical branch, release policy, true test commands. Exit: baseline receipt and unknown list; fresh read returns the same SHA. Stop: no trusted SHA. **SHIPPED** — `plans/receipts/WI7-00.json`.
- **WI7-01 — Repair doctrine conflict and version naming.** Exit: exact revision diff, named approving authority, tests against fabricated classroom events and hidden-authorship promises. **SHIPPED** — `plans/receipts/WI7-01.json`, `RFC-0001-VERSIONING.md`, `tests/v7/test_wi7.sh`.
- **WI7-02 — Baseline verification.** doctor; v4/v5/v6 suites and both mutations; bundle built twice and compared; file and description limits; license metadata; release bytes match the intended install. **SHIPPED** — `plans/receipts/WI7-02.json`.
- **WI7-03 — Contract schemas.** Exit: schemas parse, property-based invariants, no domain conflation, rejected transitions stay rejected. Stop: two truth stores or missing authority fields.
- **WI7-04 — Privacy, tenancy, matter separation.** Exit: independent unauthorized read/write drills, redaction capsule, key revocation, isolation tests.
- **WI7-05 — Evidence and output infrastructure** (honors v6 W15–W19). Exit: deterministic anchors on real data; corrupt and adversarial files fail safely; changed inputs invalidate derived numbers.
- **WI7-06 — Doctoral Research OS.** Exit: defense-ready evidence map, author provenance, policy disclosure, negative tests, independent review.
- **WI7-07 — Legal Practice OS.** Exit: attorney-reviewed golden sets, current-law locators, disclosure drills, confidentiality tests; unsupported jurisdiction refuses.
- **WI7-08 — Capital Readiness OS.** Exit: independent reconciliation, sensitivity and cap-table tests, redacted diligence bundle; predictions separate from actuals.
- **WI7-09 — Opportunity Intelligence.** Exit: authoritative locators, deadline/timezone tests, amendment propagation, staleness reporting.
- **WI7-10 — Grants OS.** Exit: federal and state/local cases, all mandatory fields accounted for, receipts only when actually submitted.
- **WI7-11 — Contract Capture OS.** Exit: FAR-based, Texas ESBD and city/county cases; go/no-go economics; receipt or explicit manual handoff.
- **WI7-12 — Institutional Deals OS.** Exit: executed vs proposed separation, permissioned share logs.
- **WI7-13 — Investor Participation.** Exit: written legal clearance of activities, fees, disclosures, verification, retention, opt-ins and negative cases.
- **WI7-14 — Extension packs.** Exit: schema contract, named expert gate, adverse benchmarks, declared unsupported scope.
- **WI7-15 — Institutional Workbench.** Exit: identical verdicts across CLI/API/UI, no global truth score, no horizontal scroll, accessibility and mobile tests.
- **WI7-16 — Governed automation.** Exit: replayable agents execute only granted effects; ambiguous results marked UNKNOWN; no second effect without independent lookup.
- **WI7-17 — Outcome-linked learning.** Exit: held-out replay shows measured improvement, no historical overwrite.
- **WI7-18 — Real pilots.** Exit: objective improvements with denominators and external acknowledgment where relevant.
- **WI7-19 — Certify, release, operate.** Exit: clean install from the distributed bundle, independent verifier, SHA/build/test/release receipts, measured operating cost.

---

## 16. Independent acceptance and falsification matrix

| Claim | Evidence that supports it | Negative control that must fail |
|---|---|---|
| Research citations are governed | Exact source/version/span and reference resolution | Fabricated paper or altered quotation |
| Case law current for jurisdiction | Jurisdiction-effective sources + licensed citator | Reversed/overruled/out-of-jurisdiction case |
| Prosecution supports discovery | Attorney-verified disclosure ledger | Known exculpatory evidence ignored |
| Large investor readiness | Reconciled financials, cap table, approved room | Projection labeled audited cash |
| Federal grant eligible | Funder requirements and applicant credentials | Wrong entity or missing mandatory status |
| Bid submitted | Portal receipt naming artifact, ID and time | UI says sent, portal has no receipt |
| Contract won | Buyer-issued award or contract | Projected or nonbinding award |
| Funds received | Ledger, bank or payment evidence | Signed but unfunded agreement |
| Confidentiality enforced | Independent cross-tenant denial | Cross-matter ID lookup succeeds |
| External automation idempotent | Same key, exactly one confirmed effect | Retry duplicates submission |
| Learning changed execution | Controlled before/after replay | Old policy despite evidence update |
| Release verified | Distributed bytes match tested build | One-byte tampered artifact accepted |
| **Doctrine forbids detector evasion (7.0.0)** | `tests/v7/test_wi7.sh` scan of shipped doctrine | Planted evasion instruction is caught |
| **A shipped wave has a receipt (7.0.0)** | `scripts/check-manifest.py` on `plans/v7.manifest.yaml` | Missing, failed, incomplete or early receipt is refused |

"100%" is valid only for a defined, demonstrated deterministic invariant — never as a promise that every court rule, grant requirement or committee decision is solved.

---

## 17. Economics and sequencing

**Loop:** qualified demand → priced preparation → verified submissions/meetings → contract, award, fundraising or academic milestones → renewal → reusable institutional evidence → lower marginal cost per next transaction.

The scarce resource is domain expert verification and authoritative connector coverage, not tokens or drafting speed. **Go-to-market order (recommendation):** grant and procurement capture, doctoral research support and capital readiness first; legal as a gated pilot with licensed review; the investor marketplace last.

**Commercial layers (to be validated):** the MIT sovereign core; individual workspaces; professional/team workspaces; enterprise/institutional; high-touch expert services priced transparently, with contingency and referral models reviewed before offering.

**Measure in pilots:** contribution margin per vertical after expert review, compute, storage, onboarding, support and compliance; hours saved without higher disqualification; amendment-detection latency; errors caught before filing and false-positive burden per 100 obligations; conversion by eligibility cohort; time to defensible chapter and successful defense as confirmed by the institution; diligence rework and evidenced capital received; retention and consented evidence reuse.

**Stop conditions:** unit economics fail to cover domain assurance; false legal or financial claims escape gating; a regulated role cannot be cleared; customers will not supply required evidence; duplication of public tools costs more than differentiation; connector cost invalidates outcome economics; critical proof cannot be independently inspected.

---

## 18. Repository and IP strategy

- Keep the MIT license and notices accurate; no exclusivity claims over published code.
- Any change to version meaning, semantic core, license posture or compatibility goes through an RFC (RFC-0001 is the first).
- Institutional contracts may ship as separate versioned packages or services; clients can always export evidence, decisions and audit closures.
- Differentiate by workflows, source coverage, certified packs, support, verified operations and trusted distribution.
- Trademark and patent clearance happen separately. Clean-room provenance is preserved when external products are studied.
- License/BOM audit and pack checksum lockfiles. The 200-file bundle ceiling and the 1024-character skill description are checked on the real installer path at release time and never bypassed by raising a local threshold.

---

## 19. Checkpoint sequence

| CP | Required receipt | State at 7.0.0 |
|---|---|---|
| CP-00 | Main SHA frozen and read back | **PASS** — `plans/receipts/WI7-00.json` |
| CP-01 | Academic constitutional repair accepted | **PASS** — `plans/receipts/WI7-01.json` |
| CP-02 | Clean-checkout v4/v5/v6 tests | **PASS** — `plans/receipts/WI7-02.json` |
| CP-03 | v7 roadmap/versioning RFC accepted | **PASS** — `RFC-0001-VERSIONING.md` (recorded in the WI7-01 receipt) |
| CP-04 | Domain schemas and transition negative controls | NOT_STARTED |
| CP-05 | Security/tenant/authority gate | NOT_STARTED |
| CP-06 | Evidence adapters and source maps verified | NOT_STARTED |
| CP-07 | Doctoral/legal/capital pilots | NOT_STARTED |
| CP-08 | Grants/contracts connectors, qualifications and receipts | NOT_STARTED |
| CP-09 | Workbench cross-surface parity | NOT_STARTED |
| CP-10 | External outcomes and unit economics | NOT_STARTED |
| CP-11 | Independent release certification and deploy receipt | NOT_STARTED |

### Definition of done

v7 Institutional Intelligence is not done when the plan exists, domain names are added, a demo renders, a dissertation chapter is generated, a deck looks compelling or a bid PDF is produced. It is done within a declared scope when a real authorized user moves from a sourced institutional problem through a governed, economically admissible action to an independently evidenced external result; adverse cases reliably refuse; a third party can reconstruct what was true and authorized at every point; and comparable future work becomes demonstrably more reliable or economical without weakening the core.

---

## 20. Official references

**Repository (pinned):** [README](https://github.com/antonio0720/writing-intelligence/blob/b59ef9544e9da78bab3dfa8db2178d4e6b569d16/README.md) · [ROADMAP](https://github.com/antonio0720/writing-intelligence/blob/b59ef9544e9da78bab3dfa8db2178d4e6b569d16/ROADMAP.md) · [v6 manifest](https://github.com/antonio0720/writing-intelligence/blob/b59ef9544e9da78bab3dfa8db2178d4e6b569d16/plans/v6.manifest.yaml) · [v4 non-goals](https://github.com/antonio0720/writing-intelligence/blob/b59ef9544e9da78bab3dfa8db2178d4e6b569d16/references/v4/NON_GOALS.md) · [academic pack at baseline](https://github.com/antonio0720/writing-intelligence/blob/b59ef9544e9da78bab3dfa8db2178d4e6b569d16/references/genre_packs/academic.md) · [v6 surfaces](https://github.com/antonio0720/writing-intelligence/blob/b59ef9544e9da78bab3dfa8db2178d4e6b569d16/references/v6/SURFACES.md)

**Grants, procurement, law, securities:** [Grants.gov — how to apply](https://www.grants.gov/applicants/grant-applications/how-to-apply-for-grants) · [SAM.gov opportunities](https://sam.gov/opportunities) · [FAR Part 15](https://www.acquisition.gov/far/part-15) · [Texas vendor information](https://comptroller.texas.gov/purchasing/vendor/information.php/1000) · [Texas grant management](https://comptroller.texas.gov/purchasing/grant-management/) · [City of Houston supplier portal](https://houstontx.gov/bizwithhou/SupplierPortal.html) · [SEC Rule 506(c)](https://www.sec.gov/resources-small-businesses/exempt-offerings/general-solicitation-rule-506c) · [SEC broker-dealer guide](https://www.sec.gov/about/divisions-offices/division-trading-markets/division-trading-markets-compliance-guides/guide-broker-dealer-registration) · [ABA Formal Opinion 512](https://dev.americanbar.org/news/abanews/aba-news-archives/2024/07/aba-issues-first-ethics-guidance-ai-tools/) · [DOJ Justice Manual §9-5](https://www.justice.gov/jm/jm-9-5000-issues-related-trials-and-other-court-proceedings)

External snapshots are evidence about a source at an observed time — never a substitute for the current notice, local professional judgment or a completed authorized filing.

---

## 21. The checkpoint companion was transposed, not kept beside

The planning handoff carried an off-repository `Writing_Intelligence_v7_Execution_Checkpoints_2026-10-21.json` and `validate_wi7_checkpoints.py`. Their rules — a wave changed to PASS without a digest-bound receipt, complete positive and negative checks, an independent readback and passed dependencies fails validation — now live in `scripts/check-manifest.py` and `plans/v7.manifest.yaml`, and `tests/v7/test_wi7.sh` proves each rule fails when violated. There is one status source, not two.

**Operating law:** `SOURCE → QUALIFY → MODEL → AUTHOR → VERIFY → AUTHORIZE → EXECUTE → RECEIPT → RECONCILE → LEARN`.
