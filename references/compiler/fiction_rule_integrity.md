# Fiction Rule Integrity — additive FI-35 through FI-44 contract

**Status:** some explicit contradiction checks executable in the sidecar; canon integration and source adjudication specified.

## Rule tuple

Each consequential mechanism has `rule_id, canon_version, tier, allowed_operations, forbidden_operations, preconditions, scarce_resources, costs, failure_modes, authority, consent_scope, demonstrations, known_exceptions, valid_interval, knowledge_interval`.

Distinguish a physical inability from an institution's prohibition, a character's false belief, and an unreliable narrator's account. A statement marked `character_belief` cannot disprove an omniscient canonical rule. A paradox tagged `intentional` is not an accidental continuity error. This is the essence of FI-41, not a blanket ban on contradiction.

## State transition

An intervention is a tuple `(actor, operation, mechanism, preconditions, resources_before, resources_after, consequences, scene_id, canon_root)`. Before an intervention is allowed into accepted canon:

1. Resolve its mechanism against the selected canon root.
2. Prove operation is permitted and not in the forbidden set; if neither, label `UNKNOWN`, not 'allowed'.
3. Verify source of capability and required authority are not conflated.
4. Identify consumed resources and durable costs; distinguish deferred cost from vanished cost.
5. Compute what characters, institutions, and world objects must know or change next.
6. Record an intentional retcon as a new canon decision that supersedes a prior rule, with temporal scope and invalidation frontier.

The proposed sidecar presently enforces only direct `forbids` matching and explicit unpaid cost flags; full canon state-transition semantics are **not shipped**.

## Five clocks to retain

`event_time`, `record_time`, `observer_time`, `narration_time`, and `workspace_knowledge_time`. The first four are fictional chronology; the fifth is actual editorial provenance. Nonlinear narrative order is not a contradiction. The deterministic sidecar only flags record-before-event anomalies when `anticipatory_record` is absent; an editor must distinguish prophecy, fraud, simulation and genuine timeline mistakes.

## Power and ethics are separate

`capability = can do`, `authority = allowed to do`, `consent = affected subject permits`, `legitimacy = ethically and legally justified`. In a speculative thriller the antagonist may be able to break a law; this is a **character action** and potential moral conflict, not always a world-causality defect. The audit must never conflate the character's illegal act with the mechanism being physically impossible. FI-39 is an editorial analysis obligation, not software granting consent in the real world.

## Scientific claim boundaries

Scientific claims in exposition must be labeled `accepted_science`, `contested_hypothesis`, `fictional_extrapolation` or `invented_mechanism` in full implementation. Nothing in a work's fictional canon proves a fact about reality. To assert such a fact outside the story, use the existing external-source verification system.
