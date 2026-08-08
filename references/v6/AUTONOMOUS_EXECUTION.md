# Autonomous Execution

**Status: specified.** No worker runtime, scheduler, capability token issuer or event log ships in v6.0.0. Several of the *actions* an execution step dispatches to are executable — `wi propose`, `wi simulate`, `wi decide`, `wi commit`, `wi constraints`, `wi capsule` and `wi verify-release` — and the fact that a step's action runs today does not mean the plan that orders it, the token that bounds it, or the log that replays it runs. Those are described here as a contract, not reported as a feature.

An agent that works on a document unattended is not a new kind of writer. It is a new kind of *writer's assistant with the keys to the building*, and every guarantee in v4 and v5 was written on the assumption that a human was standing at the moment of consequence. This document says what has to be true before that assumption can be relaxed, and what specifically must never be relaxed with it.

Read this with [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) for Laws A, C, J and K, [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md) for the isolation reasoning this document extends from providers to workers, and [`CAPABILITY_SECURITY.md`](CAPABILITY_SECURITY.md) for how the same capability discipline applies to adapters and plugins.

---

**Contents:** the shape problem · Law P · the execution plan · the step vocabulary · effect classes · the capability token · why a worker is not sovereign · the loop · replayability · the event envelope · the event vocabulary · why the log is not the graph · failure and abandonment · executable and specified.

---

## 1. The shape problem

**Status: specified.**

The default architecture for autonomous work is a loop. A model receives a goal, chooses a tool, calls it, reads the result, chooses again, and stops when it decides it is finished. The loop is easy to build, easy to demonstrate, and structurally unable to answer the four questions this project exists to answer.

| Question | Why the loop cannot answer it |
|---|---|
| *What was this run permitted to do?* | The permission set is whatever the tool registry happened to contain at the moment the loop asked. It was never declared, so it cannot be compared against what the run actually did. |
| *What did it actually do?* | A transcript of tool calls is a record of one execution ordering. It does not distinguish a call that read a file from a call that wrote one, and nothing in the transcript's shape forces that distinction to be made. |
| *Would it have done the same thing again?* | The loop's next step is a function of the model's state, which is not recorded and not reproducible. Replaying the transcript replays the outputs, not the decisions. |
| *Which of its outputs are load-bearing?* | Everything the loop produced is in one undifferentiated stream. A discarded intermediate reads exactly like a committed result. |

None of those failures is a bug in a particular implementation. They follow from the shape: a loop declares nothing in advance, so there is nothing to check its behavior against afterwards.

**The replacement is a plan.** Work is a directed acyclic graph of typed steps, produced before execution begins, checked against a capability token before any step runs, and executed by a scheduler that refuses steps the plan did not declare. The plan is an object with a digest. It can be reviewed before it runs, compared to what ran, and stored beside the result.

This is not a restriction on what an autonomous worker can accomplish. A plan may contain hundreds of steps, may be regenerated mid-run when a step returns something the planner did not anticipate, and may fan out across every document in a workspace. What it may not do is take an action nobody declared, which is the only property that makes the rest of the system's guarantees survive the removal of the human from the moment of consequence.

---

## 2. Law P

**Status: specified.** This document implements the v6 constitutional law reproduced here. Where the two disagree, the constitution wins and this document is a defect.

> **Law P — Autonomous work is a declared, bounded, replayable execution plan.**
>
> An autonomous run executes only steps its plan declares, only within the capabilities its token grants, and only in an order the plan's dependency graph permits. Every step declares its effect class before it runs. Every step's inputs, outputs and refusals are recorded as immutable events. A run is replayable from those events against the same immutable inputs, and the record of what a run saw, asked, received and changed survives any later change to the model, the provider, the plan or the graph.

Three clauses carry the weight, and each of them exists because of a specific failure that is otherwise silent.

**"Only steps its plan declares."** Without it, the token is the only bound, and a token is coarse. A worker granted `graph.read` to check citations can, under a loop, read every draft in the workspace including ones nobody asked it to look at. The plan is what makes the grant narrow enough to be meaningful — the token says what class of thing is permitted, and the plan says which specific things this run touches.

**"Declares its effect class before it runs."** Without it, effects are discovered by watching, and watching is not available on the run that matters. §5 is the whole of this clause.

**"Replayable from those events."** Without it, an autonomous run is a claim about the past that nobody can check. A model changes behind a stable name — this happens, it is documented in [`../v5/JUDGMENT_TIER.md`](../v5/JUDGMENT_TIER.md) §6 as provider drift — and every judgment that run made becomes unreproducible at exactly the moment somebody wants to contest it. Immutability of the record is what converts *the worker decided this* from an assertion into evidence.

---

## 3. The execution plan

**Status: specified.**

```json
{
  "plan_id": "plan-01j9m4q2r7t0v3x6z9b2d5f8h1",
  "plan_digest": "sha256:5b90e7a1c4d8f302b6a9e1c4d7f0a3b6c9e2f5a8b1d4e7f0a3c6b9d2e5f8a1c4",
  "format": "wiplan/1",

  "workspace_id": "ws-0192f3a1-7c40-7b2e-9f16-2a5c9d0e4b31",
  "branch": "worker/citation-sweep-0031",
  "base_state": "sha256:c9f4a1e77b0d3a26e4f81b0c5d9e2a7f4b8c1d6e9f2a5b8c1d4e7f0a3b6c9e2f",

  "goal": {
    "stated_by": {"type": "human", "id": "a.smith"},
    "text": "Every claim atom in chapter 4 that is supported by paraphrase should carry a verbatim span instead, where one exists in the anchored passage.",
    "goal_digest": "sha256:2e8b1c4f7a0d3b6e9c2f5a8b1d4e7f0a3c6b9d2e5f8a1c4d7f0a3b6c9e2f5a8b"
  },

  "token": "cap-01j9m4q2r7t0v3x6z9b2d5f8h2",
  "token_digest": "sha256:9a2c5f8b1d4e7f0a3c6b9d2e5f8a1c4d7f0a3b6c9e2f5a8b1d4e7f0a3c6b9d2e",

  "steps": [
    {
      "step_id": "s-001",
      "kind": "Retrieve",
      "effect": "ExternalRead",
      "depends_on": [],
      "declares": {
        "reads": ["source.version:sha256:3d81c9…", "source.version:sha256:b7a241…"],
        "writes": []
      },
      "budget": {"wall_ms": 20000, "bytes": 8388608}
    },
    {
      "step_id": "s-002",
      "kind": "DeterministicCheck",
      "effect": "Pure",
      "depends_on": ["s-001"],
      "check": "anchor_integrity",
      "declares": {"reads": ["a-0141", "a-0142", "a-0143"], "writes": []},
      "budget": {"wall_ms": 5000}
    },
    {
      "step_id": "s-003",
      "kind": "Transform",
      "effect": "Pure",
      "depends_on": ["s-002"],
      "transform": "requote_from_anchored_span",
      "declares": {"reads": ["c-0011", "a-0141"], "writes": []},
      "budget": {"wall_ms": 5000}
    },
    {
      "step_id": "s-004",
      "kind": "Propose",
      "effect": "ProposalWrite",
      "depends_on": ["s-003"],
      "declares": {"reads": ["c-0011"], "writes": ["authorship.proposal"]},
      "budget": {"wall_ms": 2000}
    },
    {
      "step_id": "s-005",
      "kind": "Simulate",
      "effect": "Pure",
      "depends_on": ["s-004"],
      "declares": {"reads": ["plan:proposals"], "writes": []},
      "budget": {"wall_ms": 15000}
    },
    {
      "step_id": "s-006",
      "kind": "AwaitDecision",
      "effect": "None",
      "depends_on": ["s-005"],
      "declares": {"reads": [], "writes": []},
      "await": {"required_actor_types": ["human", "authorized_editor"],
                "timeout_behavior": "abandon"}
    }
  ],

  "regeneration": {
    "permitted": true,
    "max_regenerations": 4,
    "requires_new_digest": true,
    "may_widen_token": false
  },

  "created_at": "2026-06-02T10:14:07Z",
  "created_by": {"type": "automated_policy", "id": "wi-planner", "version": "6.0.0"}
}
```

Four fields carry properties worth stating outright.

**`base_state` pins the plan to a graph state.** A plan generated against a workspace and executed after that workspace moved is a plan whose reasoning is about a document that no longer exists. The scheduler compares `base_state` before the first step and refuses the run if it has drifted, with the drifted states named. This is [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) Law I applied to intent rather than to proof: a plan is a dependency-bearing object like any other.

**`declares.reads` and `declares.writes` are per step, not per run.** A run-level declaration is close to useless — it collapses to *this run touches chapter 4*, which is true of a citation sweep and equally true of a rewrite that deletes the chapter. Per-step declaration is what lets the scheduler refuse a specific read, and what lets a reviewer see, before execution, that step `s-003` reads one claim and one anchor and writes nothing.

**`regeneration.may_widen_token` is false and there is no value that makes it true.** A planner that can widen its own grant has a grant of everything, reachable in as many regenerations as it takes to ask. Regeneration exists because plans meet reality — a retrieval returns a source that was replaced, a check fails in a way the planner did not anticipate — and the correct response is a new plan with a new digest under the *same* token. A goal that genuinely requires more authority than the token carries is a goal that stops and asks.

**`timeout_behavior` on an `AwaitDecision` step may be `abandon` or `hold`. It may not be `proceed`.** A decision that times out into acceptance is not a decision, and Law A does not have a duration after which it stops applying. §9 covers what abandonment leaves behind.

The Rust sketch of the plan's core types, given that v6 is the compiled-core line:

```rust
pub struct ExecutionPlan {
    pub plan_id: PlanId,
    pub plan_digest: Digest,
    pub workspace_id: WorkspaceId,
    pub branch: BranchName,
    pub base_state: Digest,
    pub goal: Goal,
    pub token: CapabilityTokenId,
    pub token_digest: Digest,
    pub steps: Vec<ExecutionStep>,
    pub regeneration: RegenerationPolicy,
}

pub struct ExecutionStep {
    pub step_id: StepId,
    pub kind: StepKind,
    /// Declared before execution. The scheduler enforces it; the step does not
    /// get to discover its own effect class while running.
    pub effect: EffectClass,
    pub depends_on: Vec<StepId>,
    pub declares: Declaration,
    pub budget: Budget,
}

pub struct Declaration {
    pub reads: Vec<NodeRef>,
    pub writes: Vec<NodeTypeRef>,
}
```

---

## 4. The step vocabulary

**Status: specified.** The step *kinds* are a closed set. The commands several of them dispatch to are executable at v6.0.0 and are named in the last column so the distinction is legible without a changelog.

| Kind | Does | Effect class | Dispatches to |
|---|---|---|---|
| `Retrieve` | Obtains bytes the plan named — a source version, a blob, an ingested capture | `ExternalRead` | ingestion path |
| `DeterministicCheck` | Runs one named check against one node state | `Pure` | `wi verify`, `wi constraints` — executable |
| `Judgment` | Asks one typed question of one named provider about hashed inputs | `JudgmentCall` | judgment gateway — no provider ships |
| `Transform` | Produces candidate text or structure from declared inputs | `Pure` | compiler passes |
| `Propose` | Writes an `authorship.proposal` bound to a target state | `ProposalWrite` | `wi propose` — executable |
| `Simulate` | Computes what a set of proposals would do if accepted, without accepting them | `Pure` | `wi simulate` — executable |
| `AwaitDecision` | Blocks until a permitted actor decides, or the run abandons | `None` | `wi decide` — executable |
| `Compile` | Renders an artifact from a graph state | `ArtifactWrite` | renderer set |
| `VerifyRelease` | Recomputes a closure and compares it to an attestation | `Pure` | `wi verify-release` — executable |

**The set is closed on purpose.** An open vocabulary — a `Custom` kind, a `Tool` kind, an escape hatch for "anything else the worker needs" — makes the effect declaration unenforceable, because the scheduler cannot know what a step it has never seen is going to do. Every capability a worker needs is either one of these nine or it is a change to this table, and a change to this table is visible.

Three of the nine are worth separating explicitly, because collapsing them is the obvious economy and each collapse costs a guarantee.

**`Transform` and `Propose` are separate steps.** A transform produces candidate text. A proposal binds that text to a target state with a reason and a semantic delta. Merging them means every transform writes a proposal, including the eleven the worker generated and discarded, and an author opens a review queue containing a dozen candidates for one sentence with no signal about which the worker actually stood behind.

**`Propose` and `AwaitDecision` are separate steps.** This is Law A stated as scheduling. A worker may write a proposal without any human present; that is the whole point of autonomy. It may not proceed past the decision barrier, and the barrier is a step so that the plan *shows* where the human is required before the run starts, rather than discovering it at the moment the worker wants to continue.

**`Simulate` is not `Compile`.** Simulation computes consequences — which proofs a set of proposals would invalidate, which gates would change verdict, how large the resulting repair frontier would be — without producing an artifact and without touching a target state. It is `Pure` because it writes nothing, and that purity is why a worker may run it freely and why its output can be shown to a human as part of a decision rather than after one.

---

## 5. Effect classes

**Status: specified.**

Every step declares one effect class. The scheduler enforces the declaration: a step that attempts an operation outside its declared class is terminated, its partial output is discarded, and the attempt is recorded as an event.

| Class | Permits | Forbids |
|---|---|---|
| `Pure` | Reading declared graph state and computing over it | Any I/O. No filesystem, no network, no provider call, no clock, no random source. |
| `ExternalRead` | Reading declared bytes — a blob handle, an ingested source version | Writing anything. Reading bytes the plan did not declare. |
| `JudgmentCall` | One request to one named provider about hashed inputs | Writing graph state. Reading anything the request did not carry. |
| `ProposalWrite` | Writing `authorship.proposal` objects | Writing a target state. Writing a decision. Writing a result. |
| `AuthoritativeWrite` | Writing a node state onto a branch the token names | Writing to a branch the token does not name. Writing without a decision that covers it. |
| `ArtifactWrite` | Writing rendered bytes to a declared output path | Reading anything not declared. Any network operation. |
| `Signature` | Producing a signature over a declared digest | Everything else. A signature step does nothing but sign. |

**Why the declaration must precede execution.** An effect discovered by observation is an effect discovered on a run that already happened. Instrumentation that reports *this step made a network call* is useful for the next run and worthless for this one, and "this one" is the run that shipped. The declaration inverts it: the scheduler knows what the step is permitted to do before the step does anything, so the enforcement point is ahead of the consequence rather than behind it.

Three specific failures the classes exist to prevent, each of which is invisible without them.

**A provider call cannot hide inside a "pure" step.** A transform that calls a model to improve a sentence, declared `Pure`, produces output that looks exactly like deterministic output and enters the record with no provider name, no `prompt_template_hash` and no `input_hashes`. Every guarantee in [`../v5/JUDGMENT_TIER.md`](../v5/JUDGMENT_TIER.md) rests on a judgment being *labelled* as one; an unlabelled judgment is a judgment that has been promoted to a verification by omission. Under the effect classes, the call fails — `Pure` has no provider handle — and the failure is loud on the first run rather than silent forever.

**A network fetch cannot hide inside a renderer.** Renderers legitimately want remote things: a webfont, a remote image, a stylesheet, a link the layout engine would like to resolve. Every one of those makes the rendered artifact a function of a network response nobody recorded, which means the artifact is not reproducible and the digest in its attestation describes a build that cannot be repeated. `ArtifactWrite` forbids network operations for the same reason the ingestion sandbox does in [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md) §3: a remote dependency at render time is a remote dependency in the release. Assets are ingested first, as sources, with digests.

**A signature cannot happen as a side effect of a release build.** This is the sharpest of the three. A build step that signs when it happens to have a key available produces signatures nobody decided to produce, over artifacts nobody reviewed, at times nobody chose — and a signature's entire meaning is that somebody stood behind the thing at the moment of signing. `Signature` is its own effect class, its own step kind is absent from the vocabulary in §4 on purpose, and the reason is in [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) §8: the signer runs outside the worker runtime and receives only a digest, an actor identity, a release target and an authorization receipt. A worker cannot reach it. There is no arrangement of plan steps that produces a signature, which is the correct number of arrangements.

```rust
pub enum EffectClass {
    Pure,
    ExternalRead,
    JudgmentCall,
    ProposalWrite,
    AuthoritativeWrite,
    ArtifactWrite,
    Signature,
}

impl EffectClass {
    /// The scheduler's admission test. A step is admitted only if every
    /// capability its kind requires is both granted by the token and
    /// permitted by the declared effect class.
    pub fn permits(&self, op: Operation) -> bool {
        match (self, op) {
            (EffectClass::Pure, Operation::ReadGraph { .. }) => true,
            (EffectClass::Pure, _) => false,

            (EffectClass::ExternalRead, Operation::ReadGraph { .. }) => true,
            (EffectClass::ExternalRead, Operation::ReadBlob { declared, .. }) => declared,
            (EffectClass::ExternalRead, _) => false,

            (EffectClass::JudgmentCall, Operation::CallProvider { .. }) => true,
            (EffectClass::JudgmentCall, _) => false,

            (EffectClass::ProposalWrite, Operation::ReadGraph { .. }) => true,
            (EffectClass::ProposalWrite, Operation::WriteNode { node_type, .. }) => {
                node_type == NodeType::AuthorshipProposal
            }
            (EffectClass::ProposalWrite, _) => false,

            (EffectClass::Signature, Operation::Sign { .. }) => true,
            (EffectClass::Signature, _) => false,

            _ => false,
        }
    }
}
```

The final `_ => false` is the load-bearing line. A capability model whose default is permission grants every operation somebody forgot to think about, and the operations nobody thought about are exactly the ones an attacker looks for. Default deny means a new operation is unreachable until a maintainer writes the arm that reaches it, in a diff.

---

## 6. The autonomous worker capability token

**Status: specified.**

```json
{
  "token_id": "cap-01j9m4q2r7t0v3x6z9b2d5f8h2",
  "format": "witoken/1",

  "issued_to": {
    "type": "automated_policy",
    "id": "wi-worker",
    "version": "6.0.0",
    "instance": "worker-7f3a"
  },
  "issued_by": {"type": "human", "id": "a.smith"},
  "issued_at": "2026-06-02T10:13:52Z",
  "expires_at": "2026-06-02T14:13:52Z",

  "workspace_id": "ws-0192f3a1-7c40-7b2e-9f16-2a5c9d0e4b31",

  "granted": [
    "graph.read",
    "source.read",
    "check.run",
    "transform.run",
    "simulate.run",
    "proposal.write",
    "branch.write:worker/citation-sweep-0031",
    "event.append",
    "capsule.inspect"
  ],

  "denied": [
    "decision.sign",
    "authority.delegate",
    "release.sign",
    "branch.main.write",
    "policy.write",
    "waiver.write",
    "source.approve",
    "remote.push",
    "token.issue",
    "network.any"
  ],

  "scope": {
    "branches": ["worker/citation-sweep-0031"],
    "structure_subtree": ["structure.chapter:0192f3a1-7c40-7b2e-b004-1c7e2a9d0f43"],
    "max_proposals": 60,
    "max_judgment_calls": 0,
    "max_wall_ms": 900000
  },

  "token_digest": "sha256:9a2c5f8b1d4e7f0a3c6b9d2e5f8a1c4d7f0a3b6c9e2f5a8b1d4e7f0a3c6b9d2e"
}
```

**The `denied` list is written out even though the grant is already closed.** `granted` is exhaustive — anything absent from it is refused — so `denied` adds no enforcement. It is there because a token is read by people, and an operator scanning a grant list is looking for what is *there*. The explicit denial of the five capabilities that would make a worker sovereign is the one thing an operator needs to be able to confirm at a glance, and confirming an absence is harder than confirming a presence. Where `granted` and `denied` conflict, `denied` wins; a token containing a capability in both lists is rejected at issue as a defect in whoever generated it.

**Expiry is mandatory and short.** A token with no expiry is a standing grant, and a standing grant survives the operator who issued it, the run it was issued for, and the reason it was needed. Four hours is not a security ceiling — it is the observation that an autonomous run which cannot finish inside a working afternoon is a run that should be reporting to somebody. Renewal is a new token, issued by a human, recorded.

**`max_judgment_calls: 0` is the default and it is stated rather than omitted.** A zero here means this run is entirely deterministic, which is a strong and checkable property: every output it produces can be reproduced by anyone with the same inputs, without a provider, forever. Raising it above zero is a decision with a consequence — the run's outputs now depend on named third-party infrastructure — and making that decision visible in the token is where it belongs.

**`network.any` is denied to workers unconditionally.** Retrieval reads bytes that were already ingested. A worker that could fetch is a worker that could exfiltrate, could pull an unapproved source into scope, and could turn a prompt injection in a supplied document into an outbound request. [`../v5/NON_GOALS.md`](../v5/NON_GOALS.md) already forbids autonomous source approval; denying the network is the same refusal at the layer below, where it is enforceable rather than aspirational.

---

## 7. A worker does not need main-write authority to be useful

**Status: specified.**

This is the architectural point that makes the rest of it affordable.

The instinct, when designing an autonomous system, is that a worker's usefulness scales with its authority — that a worker which cannot commit to `main` is a worker that has not really done anything. That instinct is wrong here, and the reason is specific to what this system produces.

**The expensive part of the work is not the write.** It is the retrieval, the anchoring, the checking, the transformation, the simulation of consequences and the assembly of a reviewable proposal. Those are the hours. The write is a decision, and a decision takes a person a few seconds when the material in front of them is good.

So the division is:

| The worker does | The human does |
|---|---|
| Reads every source and resolves every anchor | Reads the proposals that survived |
| Runs every deterministic check the plan declares | Decides |
| Produces candidate transformations | |
| Writes proposals bound to exact target states | |
| Simulates what accepting each would invalidate | |
| Ranks by repair cost and evidence strength | |
| Reports what it could not do and why | |

A worker with `proposal.write` and a branch of its own can do all of column one. It can run for hours, across a whole manuscript, on a schedule, unattended. What it produces is a branch full of bound proposals and a simulation of their consequences, which is exactly the material a decision needs.

**What this buys is that aggressive autonomy stops being dangerous.** A worker that cannot write a target state, cannot sign a decision, cannot delegate authority, cannot write policy, cannot record a waiver and cannot approve a source has, as its maximum achievable outcome, a branch nobody merged and a queue nobody accepted. That is a wasted afternoon of compute. It is not a compromised document, and it is not an authorship claim nobody made.

This is the same one-directional permission design as the plugin model in [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md) §7 — *a plugin may tighten policy, never loosen a hard invariant* — applied to workers. A compromised worker's ceiling is noise. The alternative, where a worker can commit and is trusted not to overreach, makes every worker a full-authority component and makes Law J a convention.

**The merge is where authority lives, and the merge is a human act.** `wi merge` is executable at v6.0.0 and it requires a decision record naming a permitted actor for each consequential state it carries across. A worker branch merges the way any branch merges: through a decision that a person signs, against states whose digests are recorded, with conflicts reported rather than resolved by preference.

---

## 8. The loop

**Status: specified.**

The thirteen stages, with what each may and may not do. The scheduler advances a stage only when the previous stage's steps have all terminated — completed, refused or abandoned — and every stage transition is an event.

### OBSERVE

**May:** read the workspace state, the branch head, the open proposal set, the current gate verdict, the constraint set from `wi constraints`, and the outstanding repair frontier.
**May not:** write anything, including a note about what it observed. Observation that mutates is not observation.

The stage exists so that a plan is generated against a known state rather than against a stale cache. It ends by pinning `base_state`.

### PLAN

**May:** produce an `ExecutionPlan` whose steps are drawn from the closed vocabulary and whose declared reads and writes are within the token's scope.
**May not:** produce a step whose effect class the token does not grant. The planner does not get to discover at execution time that it needed a capability; a plan that requires an ungranted capability is refused at admission, whole, before any step runs.

A refused plan is an event with the missing capability named. That is the correct output — a run that stops before doing anything, saying precisely what authority it would have needed, is a useful run.

### RETRIEVE

**May:** read declared source versions and blobs through the read-only handle described in [`CAPABILITY_SECURITY.md`](CAPABILITY_SECURITY.md) §5.
**May not:** fetch. Reach a source the plan did not declare. Approve a source. Ingest a new one.

A source the plan needs and the workspace does not have is a stop, not a fetch.

### PRODUCE

**May:** run `Transform` steps against declared inputs, producing candidate text and structure in memory.
**May not:** write any of it to the graph. Production is candidate generation; nothing produced here has an identity yet.

### DIFF

**May:** classify each candidate against the state it would replace, emitting the semantic delta from [`../v5/SEMANTIC_DIFF.md`](../v5/SEMANTIC_DIFF.md) Law H.
**May not:** classify a change as `wording_only` under uncertainty. Law E resolves away from it, and a worker is exactly the actor that would be tempted, because `wording_only` is the classification that carries existing proofs forward and therefore the one that makes a run look clean.

A candidate whose delta the worker cannot classify is escalated, not defaulted.

### PROPOSE

**May:** write `authorship.proposal` objects, each bound to a target state digest, each carrying `before`, `after`, `why`, the semantic delta and the predicted proof impact.
**May not:** write a target state. Write a decision. Batch proposals in a way that hides the batch — Law A's requirement that a batch be shown as a batch survives into autonomous operation without modification.

### SIMULATE

**May:** compute, for the proposal set, which proofs would be invalidated, which gates would change verdict, what the resulting repair frontier would be, and which obligations from the concept registry would move.
**May not:** apply anything. Cache the simulation as if it were a result. Present a simulation as a verification — a simulated gate verdict is a statement about a hypothetical state and is rendered as one.

`wi simulate` is executable at v6.0.0; the worker's use of it is not.

### VERIFY

**May:** run every deterministic check the plan declares against the current state, and record results.
**May not:** run a judgment call unless the token's `max_judgment_calls` is above zero and the plan declared the step. Emit a `verification.result` from any judgment, ever — the type boundary from [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) §4 does not soften for autonomous runs.

### DECIDE

**May:** wait. Notify. Present the proposal set, the simulation and the checks.
**May not:** decide. `decision.sign` is denied on every worker token and there is no configuration that grants it. An `AwaitDecision` step that times out abandons or holds; it does not proceed.

This is the stage the whole design exists to protect. Everything before it is preparation, and preparation is what a machine is for.

### COMMIT

**May:** write accepted proposals onto the worker's own branch, as `AuthoritativeWrite` steps, bounded to `branch.write:<name>` from the token.
**May not:** write to `main`. Write a state no decision covers. Carry a decision forward onto a target state that has moved since the decision was taken.

### COMPILE

**May:** render artifacts from the committed branch state to declared output paths.
**May not:** reach the network. Read an asset that was not ingested. Vary its output on anything not in the graph — a renderer that reads the clock produces a different artifact every run, and an artifact digest that changes without the content changing makes attestation meaningless.

### ATTEST

**May:** compute a `release.attestation` over each artifact and its recomputed proof closure, and build a `.wiab` bundle or a `.wic` capsule.
**May not:** sign. Attestation is a computation over state; signing is a statement by a person or a key that person controls, and §5 keeps them apart.

### VERIFY AGAIN

**May:** run `wi verify-release` against the bundle it just produced, offline, as an independent check that the thing it built verifies.
**May not:** treat its own attestation as the verification. The final stage exists because a build that produces an attestation and never checks it has tested nothing — the same reasoning that makes [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md) §9 require negative fixtures. A run whose final verification fails reports a failed run, and the bundle it produced is retained as evidence of the failure rather than deleted.

---

## 9. Replayability

**Status: specified.**

> **An autonomous run is an event-sourced record replayable from immutable inputs.**

The property being bought: a future change to the model, the provider, the planner, the check implementation or the graph cannot erase what the old run saw, asked, received and changed.

Three things make it hold.

**Inputs are immutable and content-addressed.** Every source version a run read is pinned by `sha256(raw bytes)`. Every graph state it read is pinned by `state_digest`. Every provider request it made carried `input_hashes`. A replay resolves those addresses; if any of them is missing from the object store, the replay reports which one and stops, rather than substituting the current version — which would be a replay of a different run wearing the old run's identity.

**Non-determinism is confined to `JudgmentCall`, and its outputs are recorded verbatim.** A `Pure` step replays to the same output by construction. A `JudgmentCall` does not, and this is where the record earns its cost: the event carries the request digest, the provider identity, the model identifier, the prompt template hash and the response bytes exactly as returned. A replay does not re-ask. It reads what was answered. The distinction between *this run would produce the same result today* and *this is what the run actually did* is the distinction between reproduction and evidence, and only the second is available for a run that involved a model.

**The record is append-only and its ordering is internal.** Events carry a monotone sequence number per run and a `prev_event_digest`, forming a hash chain. Ordering does not depend on any clock. A missing event breaks the chain and is detectable; a reordered event breaks the chain and is detectable; a deleted tail is detectable only if somebody knows the run's terminal event digest, which is why the run's terminal digest is what a capsule or a bundle records.

**What replay does not give you.** It does not tell you the run was correct, and it does not tell you the run would happen the same way against today's graph. It tells you what happened, checkably, from immutable inputs. That is a narrower claim than "reproducible" and it is the claim that survives a provider changing behind a stable name.

---

## 10. The event envelope

**Status: specified.**

```json
{
  "event_id": "ev-01j9m4q3s8u1w4y7a0c3e6g9j2",
  "run_id": "run-01j9m4q2r7t0v3x6z9b2d5f8h3",
  "seq": 41,
  "prev_event_digest": "sha256:1d4e7f0a3c6b9d2e5f8a1c4d7f0a3b6c9e2f5a8b1d4e7f0a3c6b9d2e5f8a1c4d",

  "event_type": "step.refused",
  "occurred_at": "2026-06-02T10:31:18Z",

  "plan_digest": "sha256:5b90e7a1c4d8f302b6a9e1c4d7f0a3b6c9e2f5a8b1d4e7f0a3c6b9d2e5f8a1c4",
  "step_id": "s-014",

  "actor": {"type": "automated_policy", "id": "wi-worker",
            "version": "6.0.0", "instance": "worker-7f3a"},

  "subject": {
    "logical_id": "0192f3a1-7c40-7b2e-9f16-2a5c9d0e4b31",
    "node_type": "meaning.claim_atom",
    "state_digest": "sha256:9f2c1d47ab3e58b0c6d19e4f7a2b8c35de60f19a4c7b2e8d0f3a6b9c1d4e7f20"
  },

  "detail": {
    "reason_code": "WI_EFFECT_CLASS_VIOLATION",
    "declared_effect": "Pure",
    "attempted_operation": "CallProvider",
    "capability_required": "judgment.call",
    "capability_granted": false
  },

  "event_digest": "sha256:c19f4a02de7b8365a1c4d0e3f6a9b2c5d8e1f4a7b0c3d6e9f2a5b8c1d4e7f0a3"
}
```

The envelope follows the webhook shape in [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md) §8 and inherits its privacy rule without exception: **the envelope carries identities, digests, codes and counts. It does not carry source text, draft text, quoted evidence or provider prose.** An event log is a record of a run, retained for as long as the run's evidence is retained, frequently exported for review, and frequently read by people who are entitled to know that a step was refused and not entitled to read the paragraph it was refused over.

Provider outputs are the one thing that must be retained verbatim for §9 to hold, and they are retained in the object store as content-addressed objects, referenced from the event by digest, subject to the same profile rules a capsule applies in [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) §6. The event says *the provider returned the object with this digest*. The object is disclosed, or not, by a separate decision.

---

## 11. The event vocabulary

**Status: specified.**

| Event type | Emitted when |
|---|---|
| `run.started` | A plan is admitted and the first step is eligible |
| `run.plan_admitted` | The plan's digest, token digest and base state passed admission |
| `run.plan_refused` | Admission failed — the missing capability or drifted state is named |
| `run.regenerated` | A new plan digest replaced the previous one, with the trigger recorded |
| `run.completed` | Every step terminated and the final verification stage ran |
| `run.abandoned` | The run stopped without completing, with the cause recorded |
| `step.started` | A step became eligible and began |
| `step.completed` | A step terminated normally, with its output digest |
| `step.refused` | A step attempted an operation its effect class or token forbids |
| `step.budget_exceeded` | A step exceeded wall time, byte or call budget; partial output discarded |
| `step.failed` | A step terminated abnormally, with the error envelope |
| `capability.denied` | A capability check failed, independent of which step asked |
| `retrieval.resolved` | A declared source version resolved to bytes, with its digest |
| `retrieval.unresolved` | A declared source version was not present in the object store |
| `check.result` | A deterministic check produced a result, with the result digest |
| `judgment.requested` | A judgment request was assembled, with its input hashes |
| `judgment.returned` | A provider returned a record, with the response object digest |
| `judgment.discarded` | A returned record failed one of the five validation conditions |
| `proposal.written` | A proposal was written, bound to a target state digest |
| `decision.awaited` | An `AwaitDecision` barrier was reached |
| `decision.recorded` | A permitted actor decided; the decision digest is recorded |
| `decision.timed_out` | The barrier expired under `abandon` or `hold` |
| `commit.written` | A state was written to the run's branch under a covering decision |
| `artifact.compiled` | An artifact was rendered, with its byte digest |
| `attestation.built` | An attestation and its closure digest were computed |
| `verification.final` | The run verified its own output, with the verdict |

**`judgment.discarded` is in the list for the same reason `run.plan_refused` is.** A record of what a run *did not* accept is the only way to distinguish a run where no judgment was needed from a run where five were returned and four were thrown away for failing validation. Law C at the level of a run: what did not happen is part of the account.

---

## 12. Why the event log is not the graph

**Status: specified.**

They are frequently confused, and the confusion produces two specific defects.

| | Event log | Graph |
|---|---|---|
| Holds | What happened, in order, including what was refused and discarded | What is true now, and what it depends on |
| Shape | Append-only chain, one per run | Versioned state store, one per workspace |
| Contains rejected work | Yes, permanently | No |
| Contains discarded judgments | Yes | No |
| Answers | *What did this run do?* | *What does this document assert, and what supports it?* |
| Enters a proof closure | No | Yes |
| Retention | Bounded by run-evidence policy | Bounded by workspace policy |

**The log must never enter a proof closure.** A run that requested five judgments and discarded four has four discarded records in its log. Those records exist, they are real, they are retained — and they support nothing. A closure that pulled from the log would pull them in, and a reviewer reading the closure would find provider verdicts that the core rejected sitting beside verdicts it accepted, with no structural difference between them. The closure is built from graph state by the rules in [`../v5/AUTHORSHIP_GRAPH.md`](../v5/AUTHORSHIP_GRAPH.md) §5 and from nothing else.

**The graph must never be reconstructed by replaying the log.** This is the second defect and it is more tempting, because event sourcing invites exactly that move. It is wrong here because a run's log contains work that was proposed and rejected, and a replay that applies the log applies the rejections as though they were acceptances — the human decision is a *filter* on the log, not a step in it. The graph is the authoritative state. The log is the account of how a particular run behaved on the way to changing it, including every path it took that changed nothing.

Both structures are necessary and neither is derivable from the other. The log tells you a worker tried to widen a scope at 10:31 and was refused. The graph does not contain that, correctly, because nothing about the document changed. The graph tells you a claim is supported by an anchor into a source version. The log does not contain that, correctly, because it was true before the run started.

---

## 13. Failure and abandonment

**Status: specified.**

A run stops for one of five reasons, and the five are not interchangeable.

| Cause | State left behind | Correct next action |
|---|---|---|
| `completed` | Branch with committed states, artifacts, attestation, final verdict | Review the branch; merge or discard |
| `abandoned_timeout` | Branch with proposals awaiting a decision that never came | Decide, or discard the branch |
| `abandoned_capability` | Branch with whatever completed before the refusal; the refused step named | Issue a token that covers it, or narrow the goal |
| `abandoned_drift` | Nothing; the run refused at admission because `base_state` moved | Regenerate the plan against the current state |
| `failed` | Branch with completed steps; the failing step's error envelope | Read the envelope; this is a defect report |

**Partial output from a terminated step is discarded, never used.** This is the ingestion rule from [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md) §3 applied one layer up, and the reasoning is identical: a transform killed at 60% has produced 60% of a rewrite, and 60% of a rewrite presented as a proposal is a proposal whose relationship to its stated reason nothing downstream can check.

**An abandoned run's branch is retained.** Deleting it on abandonment destroys the evidence of what the worker did with the hours it was given, which is the material an operator needs to decide whether the token was too narrow, the goal too broad, or the planner wrong. A branch nobody merged costs storage. A run nobody can examine costs the ability to improve the next one.

---

## 14. What is executable and what is specified

| Mechanism | Status |
|---|---|
| `ExecutionPlan`, the step vocabulary, effect classes, the admission test | Specified |
| The capability token, its grant closure, expiry and scope | Specified |
| The worker runtime and scheduler | Specified — none ships |
| The thirteen-stage loop and its per-stage permissions | Specified |
| The event envelope, the event vocabulary, the hash chain | Specified |
| Replay from immutable inputs | Specified |
| `wi propose`, `wi proposals`, `wi decide`, `wi commit`, `wi log` | Executable in `scripts/wi.py` at v6.0.0 |
| `wi simulate` — consequence computation over a proposal set | Executable in `scripts/wi.py` at v6.0.0 |
| `wi constraints` — the constraint set a plan is checked against | Executable in `scripts/wi.py` at v6.0.0 |
| `wi verify-release` — the final stage's check | Executable in `scripts/wi.py` |
| Any judgment provider a `Judgment` step could call | **None ships.** Unchanged from v5.0. |
| Signing, in any stage, by any actor | Specified — see [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) §8 |

The distinction that matters in that table: the *actions* a plan orders are, in several cases, commands that run today. The plan, the token, the scheduler, the effect enforcement and the event log are not. A reader who takes the executable rows as evidence that autonomous operation ships has read the table the way the loop architecture reads a transcript — as a list of things that happened, with no account of what bounded them.

---

## Related documents

- [`CAPABILITY_SECURITY.md`](CAPABILITY_SECURITY.md) — the same capability discipline applied to adapters and plugins
- [`PROOF_CAPSULES.md`](PROOF_CAPSULES.md) — what an `ATTEST` stage produces, and why signing sits outside the runtime
- [`FEDERATION.md`](FEDERATION.md) — why a worker's `remote.push` is denied, and what arrives instead
- [`PACKAGE_SYSTEM.md`](PACKAGE_SYSTEM.md) — packs a plan may depend on, and their digests in a closure
- [`../v5/CONSTITUTION.md`](../v5/CONSTITUTION.md) — Laws A, C, I, J and K, which this document does not relax
- [`../v5/SECURITY_MODEL.md`](../v5/SECURITY_MODEL.md) — the isolation reasoning extended here from providers to workers
- [`../v5/JUDGMENT_TIER.md`](../v5/JUDGMENT_TIER.md) — the gateway a `Judgment` step calls, and provider drift
- [`../v5/AUTHORSHIP_GRAPH.md`](../v5/AUTHORSHIP_GRAPH.md) — the proof closure the log must never enter
- [`../v5/SEMANTIC_DIFF.md`](../v5/SEMANTIC_DIFF.md) — the classification the `DIFF` stage emits
- [`../v4/PROPOSAL_PROTOCOL.md`](../v4/PROPOSAL_PROTOCOL.md) — Law A in its original form, unchanged by autonomy
- [`../../README.md`](../../README.md) — the project

---

*Author: Antonio T. Smith Jr. · Density6 LLC · MIT.*
