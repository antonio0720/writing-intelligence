# Release, trust boundaries, provenance and safety

## Threat model

Untrusted inputs: novels, synopses, proposed IR, reviewer JSON, imported world lore, generated suggestions, genre templates and arbitrary file paths. Trust boundaries: (1) raw text → typed annotations; (2) typed annotations → evaluated findings; (3) findings → approved edit; (4) approved canon → publication artifact; (5) artifact → actual reader experience.

Threats: prompt injection embedded in narrative text; fabricated human-reader responses; spoofed waivers; forged canon exception; manipulated source digest; stale manuscript after feedback; accidental modification of author originals; conflicting collaborative edits; vendor-dependent LLM judgment masquerading as verification; release based on print mock without export proof.

## Implemented defenses and limits

- Offline stdlib runtime makes no network requests and never evaluates narrative text as instructions.
- Audit inputs, policy and rule catalog have deterministic digests; exact byte-equality round-trips are possible for JSON. Anchor digest check runs when manuscript text is supplied.
- CLI writes output files only if destination does not already exist, to avoid overwriting existing artifacts.
- Installer refuses target file collisions and symlink parent paths; inspect the target before `--apply`.
- Invalid IDs or dangling canonical references return validation errors. Contradictory world powers and unpaid explicit costs block the sidecar gate.
- Unreviewed artistic requirements remain `UNASSESSED`; regex patterns cannot become `DEFECT` by a threshold alone.
- Sidecar waiver assertions **do not prove permission**. Publication/editorial gates cannot accept waivers as a substitute for required human judgments. A canonical authority adapter is still needed.

## Residual vulnerabilities (not solved by this package)

- The supplied JSON can be dishonest. Hashes preserve content integrity, not whether an annotation, person or reader exists. External identity validation and participant consent verification are not implemented.
- Basic regex scanning is English-oriented and can misclassify dialogue, quotation and multilingual manuscript rhythm. Profile thresholds are hypotheses, not literature laws.
- The provided JSON Schema is documentation and a contract for upstream `jsonschema` validators; the stdlib runtime implements an explicitly narrower cross-reference validator. Do not claim full JSON Schema runtime validation.
- No real EPUB, PDF, DOCX or print proofing code; rendering and metadata review must be independently performed.
- No upstream v4-v7 regression readback has been performed on the live repo in this package. It was reviewed through GitHub; the environment cannot clone the public repository by network, so regression requires installation into the authenticated checkout.

## Version/authority conditions

The proposed upgrade is subordinate to upstream law C (never report work not done), M (semantic canonical state), O (scoped authority), P (proposals first), Q (conflicts preserved) and R (dependency freshness). Do not set `plans/v7.manifest.yaml` waves to shipped based on this artifact. A real version increment requires accepted ADR/RFC, merging, full regression, workflow receipts, independent readback and release packaging.

## Privacy

Reader responses should be pseudonymized and contain only consented observations. Do not include raw identifiable reports, private emails, rights-protected passages or confidential manuscript excerpts in public CI artifacts. Public benchmark fixtures herein are synthetic **examples** and do not claim they were written or approved by actual beta readers.

## v9 preview: release and trust boundaries

*Preview (PR #8); proposed, not a release. v8.0.0 is the published version.*

v9 adds one boundary to the list above: a **declaration** is not authentication. `scripts/wi-authorship.py` reports `declaration_status: self_reported` and reads only bounded, symlink-free files under the dossier directory; it sends nothing. `RELEASE_ELIGIBLE` is a gate on a package, never a transmission, and it requires a person's decision bound to the exact draft digest and an unexpired grant. The checker cannot prove a self-declared human-only manuscript was written by a person.

Untrusted-input handling is unchanged: dossier text, manuscripts and phrase-scan inputs are data, never instructions. A detector score is not a trust signal in this model and is not used as a gate (WI9-H). Release remains on HOLD until WI9-09 (independent review and the owner's decision), and v8.0.0 stays the published version.
