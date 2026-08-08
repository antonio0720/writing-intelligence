# Writing Intelligence v6 — Definition Libraries

The twenty documents in this directory describe the objects a v6 workspace **holds**, the operations that move it from one state to the next, and the evidence a third party needs to check that the move was legitimate. They are the v6 successor to `../v5/`, and they differ from v5 in one structural way that is visible in every file: **a v6 document is a library of definitions, not a single object.**

Validate against a named member of a document's `$defs`. Never validate against a document root. A root here carries no `type`, no `properties` and no `required`, because it is not describing a thing — it is holding the things.

---

## Why the definitions are grouped

v5 is one file per object type, each file standalone, with no cross-file `$ref` anywhere. That is the cleaner arrangement and v6 does not use it.

The reason is a hard limit rather than a preference. A Writing Intelligence skill bundle is installed as an archive with a **200-file ceiling**, and the bundle carries scripts, references, packs and prompts alongside the schemas. v6 governs roughly two hundred distinct object types on its own. One file per type consumes the entire budget for schemas and leaves nothing for the code that reads them, so the bundle cannot be installed at all — which means the schemas would be correct, complete, and unusable.

Grouping is therefore an **architectural constraint that the schema layout is obliged to satisfy**, not a taste call about file organisation, and it is written down here so that a later contributor who is tempted to split `claim.schema.json` into ten files knows what breaks when they do.

The grouping is by **governed concern**, not by alphabet or by size. `argument.schema.json` holds `Argument`, `Warrant`, `Defeater` and `Counterargument` together because a defeater that is separated from the argument it attacks is a fragment; `common.schema.json` holds the primitives every other document needs because a digest pattern restated in twenty places is nineteen chances for one of them to drift.

---

## The twenty documents

| Document | What it governs | Exported `$defs` |
| --- | --- | --- |
| `common.schema.json` | The primitives every other document rests on: identifiers, digests, exact decimal quantities, and the four-member reliability basis that replaces confidence scoring. | `DigestRef`, `LogicalId`, `SchemaId`, `ActorId`, `GrantId`, `RefName`, `Realm`, `ReliabilityBasis`, `Verified`, `Measured`, `Judged`, `HumanDeclared`, `Timestamp`, `TimePoint`, `Unit`, `Quantity`, `Jurisdiction` |
| `time.schema.json` | Bitemporality — when something was true in the world, and when the workspace came to know it — and the query shape that reads a graph as of a pair of instants. | `ValidInterval`, `KnowledgeInterval`, `TemporalQuery` |
| `actor.schema.json` | Who or what took an action, kept distinguishable by kind so that a human declaration and a machine assertion are never merged into an anonymous "someone". | `ActorKind`, `Actor`, `PublicKeyRef` |
| `authority.schema.json` | Capability grants as the single source of permission, the scope and constraints attached to a grant, and the receipt that records which grant authorised which act. | `Capability`, `AuthorityScope`, `AuthorityConstraint`, `CapabilityGrant`, `AuthorityReceipt`, `ApprovalRule` |
| `graph_root.schema.json` | The commitment at the top of a workspace: the Merkle roots over nodes and edges that make the whole graph state a single checkable digest. | `GraphRoot`, `NodeIndexRoot`, `EdgeIndexRoot` |
| `semantic_commit.schema.json` | A committed change to the graph, its parents, and the merge result when a commit has two of them. | `SemanticCommit`, `CommitParents` |
| `graph_delta.schema.json` | What changed between two graph states, classified by semantic weight so that a reworded claim and a reversed claim are never reported as the same size of change. | `GraphDelta`, `StateTransition`, `EdgeRef`, `SemanticDeltaClass`, `SemanticDelta` |
| `semantic_node.schema.json` | The node envelope every governed object is carried in, its type tag, and the reference shape other objects use to point at one. | `SemanticNode`, `NodeType`, `NodeRef` |
| `claim.schema.json` | The claim atom — a proposition split into structured quantity, scope, modality, polarity and attribution, with the wording held separately as a surface hint. | `ClaimAtomV6`, `EntityRef`, `SemanticValue`, `Modality`, `Polarity`, `CertaintyClass`, `CausalRelation`, `ScopeConstraint`, `Qualifier`, `SurfaceHints` |
| `meaning.schema.json` | The other things a document asserts besides claims: definitions, premises, promises, obligations, forecasts, targets, assumptions, exceptions and open questions. | `Definition`, `Term`, `Premise`, `Constraint`, `Promise`, `Obligation`, `Recommendation`, `Hypothesis`, `Forecast`, `Metric`, `Target`, `Assumption`, `Exception`, `Question` |
| `argument.schema.json` | How claims support each other: the inference rule in use, the warrant that licenses it, the defeaters that undercut or rebut it, and the counterarguments raised against it. | `Argument`, `InferenceRule`, `Warrant`, `Defeater`, `DefeaterEffect`, `DefeaterStatus`, `Counterargument`, `AttackTarget`, `CounterargumentDisposition` |
| `proposal.schema.json` | A proposed change bound to the exact target state it was written against, so that it goes stale rather than silently re-attaching to a state nobody reviewed. | `Proposal`, `ProposalStatus`, `EvidenceChange`, `EvidenceChangeKind`, `ProposalDependency`, `DependencyRelation` |
| `decision.schema.json` | The human act of accepting, rejecting or deferring a proposal, the votes that composed it, and the modified replacement when acceptance was conditional. | `Decision`, `DecisionOutcome`, `ApprovalState`, `ApprovalVote`, `VoteEffect` |
| `conflict.schema.json` | Three-way semantic merge, the sixteen kinds of conflict it can surface, and the resolution record — conflicts are preserved and named, never split down the middle. | `MergeResult`, `MergedState`, `ThreeWayOutcome`, `SemanticConflict`, `SemanticConflictKind`, `ConflictStatus`, `ResolutionRequirement`, `ConflictResolution`, `ResolutionChoice`, `RequiredAuthority`, `MergeStrategy` |
| `simulation.schema.json` | What a change would do before it is made: what breaks, what is provably unaffected, what could not be examined, and what the repair would cost. | `SimulationRequest`, `SimulationReport`, `UnaffectedReport`, `UnaffectedBasis`, `UnexaminedNode`, `UnexaminedReason`, `RepairPlan`, `RepairAction`, `RepairKind`, `CostVector`, `SafetyOrdering`, `SafetyCriterion`, `UnsatisfiableObligation` |
| `proof.schema.json` | Obligations, the verification results that discharge them, judgment records kept separate from verification, and the invalidation that fires when a discharged obligation stops holding. | `ProofObligation`, `ProofObligationKind`, `ObligationStatus`, `BasisKind`, `VerificationResult`, `CheckOutcome`, `EngineIdentity`, `JudgmentRecord`, `ProviderRef`, `JudgmentAssessment`, `JudgmentDisagreement`, `DisagreementStatus`, `DisagreementTreatment`, `ObligationWaiver`, `Invalidation`, `InvalidationKind`, `InvalidationSeverity` |
| `constraint.schema.json` | The twenty non-negotiable constraints C001–C020, when each is evaluated, what a violation of one looks like, and why a skipped evaluation is never a passing one. | `ConstraintId`, `ConstraintDeclaration`, `EnforcementLevel`, `EvaluationPhase`, `ConstraintViolation`, `ViolationReview`, `ReviewScope`, `ConstraintEvaluation`, `SkippedConstraint`, `SkipReason` |
| `extension.schema.json` | Third-party adapters, plugins and domain packs: what each may reach, what resources it may consume, and how a derived artifact records what it was derived from. | `AdapterManifest`, `PluginManifest`, `CapabilityProfile`, `FilesystemAccess`, `ResourceLimits`, `DeterminismProfile`, `DerivationRecord`, `PackManifest`, `PackRef`, `ConceptMapping`, `MappingRelation` |
| `compile.schema.json` | Turning a governed graph into an artifact: the build plan, the compiler identity, the source map from rendered text back to the claims behind it, and the mission and voice contracts the render was held to. | `BuildPlan`, `CompilerIdentity`, `ArtifactSet`, `Artifact`, `RenderSourceMap`, `RenderMapping`, `ArtifactLocator`, `RenderFinding`, `RenderFindingKind`, `MissionContract`, `EvidenceMode`, `VoiceContract`, `MeasuredFeature`, `ExecutionPlan`, `ExecutionStep`, `ExecutionStepKind` |
| `release.schema.json` | What was shipped and how somebody else checks it: the manifest, the declared omissions, the Merkle closure over its dependencies, signatures, redaction records and migration receipts. | `ReleaseManifest`, `ArtifactDescriptor`, `CapabilityReport`, `UnavailableCheck`, `DeclaredOmission`, `OmissionStatus`, `ReleaseVerdict`, `ClosureLeaf`, `InclusionProof`, `MerkleSibling`, `SiblingPosition`, `SignatureEnvelope`, `CapsuleManifest`, `CapsuleMode`, `RedactionRecord`, `RedactionMethod`, `SignedDeltaPackage`, `MigrationReceipt`, `Reinterpretation`, `EffectClass` |

---

## The cross-reference convention

Grouping definitions makes cross-file references unavoidable, so the convention is fixed rather than left to each author.

A reference to a definition in another document is a **relative URI reference** naming the file and the definition:

```json
{ "$ref": "common.schema.json#/$defs/DigestRef" }
```

A reference within the same document is a **local JSON pointer**, never a self-naming relative reference:

```json
{ "$ref": "#/$defs/Quantity" }
```

Three rules hold across the directory:

- **Relative, never absolute.** The `$id` of every document is an `https://writing-intelligence.dev/...` URL, but no `$ref` uses one. A validator resolves relative references against the base `$id`, so the same files work unchanged from a checkout, from an installed bundle and from an offline air-gapped copy. An absolute reference would make the directory require the network to be understood.
- **Every referenced definition exists.** A `$ref` pointing at a definition that was renamed or moved does not fail loudly at authoring time — most validators fail only when a document is actually validated against, and a rarely-exercised branch can carry a dangling reference for a long time. The table above is the authoritative export list; a definition not in it is not referenceable from outside its document.
- **No cycles between documents that a resolver must unwind eagerly.** `authority` and `compile` both reference `release.schema.json#/$defs/EffectClass`, and `semantic_commit` references `conflict.schema.json#/$defs/MergeResult`, because the definition belongs where the concern lives — an effect class is a property of a release and a merge result is a property of a merge, regardless of who needs to name one.

Where a shape is needed in more than one document and belongs to no one of them in particular, it goes in `common.schema.json`. `Quantity`, `DigestRef` and `ReliabilityBasis` are there for that reason: a decimal that is restated per document is a decimal that will eventually be restated as a binary float somewhere, and a digest pattern restated per document is a pattern that will eventually be relaxed in one file and not the others.

---

## Conventions

Every schema document in this directory:

- declares `"$schema": "https://json-schema.org/draft/2020-12/schema"`;
- declares `"$id": "https://writing-intelligence.dev/schemas/v6/<name>.schema.json"`;
- carries a `title` ending in `V6`;
- carries a `description` that says what the document is **for** and states explicitly that it is a definition library;
- gives every definition and every field its own `description` explaining why the field exists, not restating its name;
- names a `required` array on every closed object;
- sets `"additionalProperties": false` wherever the shape is closed;
- constrains digests as `^sha256:[0-9a-f]{64}$` and logical ids as a lowercase UUID string, both by `$ref` into `common.schema.json` rather than by repeating the pattern;
- uses `oneOf` with a `const` discriminator where a value has variants that carry different fields, so that an unrecognised variant fails validation instead of validating as the permissive branch;
- expresses states that have a "we could not tell" case as three, four or five valued enumerations rather than booleans, because a boolean forces an unmeasured result into one of the two measured ones and the choice of which is always wrong somewhere.

## Author

Antonio T. Smith Jr. / Density6 LLC
