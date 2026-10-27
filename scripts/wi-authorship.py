#!/usr/bin/env python3
"""Writing Intelligence v9 EXPERIMENTAL authorship and evidence audit.

Stdlib-only; never rewrites prose, certifies identity, or optimizes AI detector
scores. REVIEW means checks passed; it is NOT approval to publish or submit.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

SCHEMA = "wi9-authorship-1"
ORIGINS = {"human_authored", "ai_assisted", "ai_generated"}
VENUES = {"unrestricted", "disclose_ai", "human_only"}
KINDS = {"firsthand", "external", "interpretation"}
MAX_BYTES = 5_000_000


def digest(content):
    return hashlib.sha256(content).hexdigest()


def safe_read(root, relative):
    """Read a bounded UTF-8 local file without escaping the dossier directory."""
    if not isinstance(relative, str) or not relative:
        raise ValueError("source path is missing")
    base = root.resolve()
    p = (base / relative).resolve()
    try:
        p.relative_to(base)
    except ValueError:
        raise ValueError("source path escapes the dossier directory")
    data = p.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError("source file exceeds 5 MB")
    return data.decode("utf-8"), digest(data)


def analyze(dossier, root):
    findings = []

    def flag(code, level, message, target=None):
        findings.append({"code": code, "level": level, "message": message, "target": target})

    if dossier.get("schema") != SCHEMA:
        flag("SCHEMA_INVALID", "hold", "Expected wi9-authorship-1.")
    doc = dossier.get("document")
    if not isinstance(doc, dict):
        doc = {}
        flag("DOCUMENT_REQUIRED", "hold", "Document metadata required.")
    origin = doc.get("origin")
    venue = doc.get("venue_policy")
    intended = doc.get("intended_use")
    if origin not in ORIGINS:
        flag("ORIGIN_UNKNOWN", "hold", "Declare human_authored, ai_assisted, or ai_generated.")
    if venue not in VENUES:
        flag("VENUE_POLICY_UNKNOWN", "hold", "Declare unrestricted, disclose_ai, or human_only.")
    if intended not in {"submission", "research_demo", "internal_review"}:
        flag("INTENDED_USE_UNKNOWN", "hold", "Declare submission, research_demo, or internal_review.")
    if venue == "human_only" and intended == "submission" and origin != "human_authored":
        flag("HUMAN_ONLY_CONFLICT", "hold",
             "Human-only submissions cannot package AI-generated or AI-assisted authorship.")
    # Provenance is self-declared and must be complete enough to expose a
    # conflict. This cannot establish the truth of any human-authorship claim.
    contribution_log = dossier.get("contribution_log")
    if intended == "submission" and not isinstance(contribution_log, list):
        flag("CONTRIBUTION_LOG_REQUIRED", "hold",
             "Submissions require a contribution history; missing data cannot certify eligibility.")
        contribution_log = []
    elif contribution_log is None:
        contribution_log = []
    elif not isinstance(contribution_log, list):
        flag("CONTRIBUTION_LOG_INVALID", "hold", "contribution_log must be a list.")
        contribution_log = []
    for index, change in enumerate(contribution_log):
        tag = "contribution_log[%d]" % index
        if not isinstance(change, dict):
            flag("CONTRIBUTION_INVALID", "hold", "Contribution must be an object.", tag)
            continue
        kind = change.get("kind")
        if kind not in {"human_original", "ai_research", "ai_generated_prose",
                        "ai_substantive_rewrite", "human_edit", "mechanical_proofread"}:
            flag("CONTRIBUTION_KIND_INVALID", "hold", "Unknown contribution kind.", tag)
        if venue == "human_only" and intended == "submission" and kind in {
                "ai_generated_prose", "ai_substantive_rewrite"}:
            flag("SUBSTANTIVE_AI_CONTRIBUTION", "hold",
                 "A declared AI prose contribution conflicts with human-only venue rules.", tag)
    if venue == "human_only" and intended == "submission" and not contribution_log:
        flag("CONTRIBUTION_HISTORY_EMPTY", "hold",
             "Human-only submission needs an explicit authorship history.")

    if venue == "human_only" and intended == "research_demo" and origin != "human_authored":
        flag("RESEARCH_ONLY", "info", "AI material here is research-only, not a pitch.")
    if venue == "disclose_ai" and origin != "human_authored":
        flag("DISCLOSURE_NEEDED", "info", "AI contribution requires venue-appropriate disclosure.")

    document_hash = None
    try:
        body, document_hash = safe_read(root, doc.get("path"))
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        flag("DOCUMENT_NOT_READABLE", "hold", str(exc))

    # A source quote can exist while the submitted manuscript says something
    # entirely unrelated. Submission candidates must supply exact text anchors
    # into the candidate document, plus separate evidence anchors. Claims which
    # cannot be anchored exactly require human review, not a pass.
    passages = dossier.get("document_claim_anchors", [])
    if intended == "submission" and doc.get("arena") in {"journalism", "academic", "legal", "government"}:
        if not isinstance(passages, list) or not passages:
            flag("DOCUMENT_CLAIM_ANCHORS_REQUIRED", "hold",
                 "Consequential submissions must anchor claims to draft passages.")
    if passages is not None and not isinstance(passages, list):
        flag("DOCUMENT_CLAIM_ANCHORS_INVALID", "hold", "document_claim_anchors must be a list.")
        passages = []
    for index, passage in enumerate(passages or []):
        tag = "document_claim_anchors[%d]" % index
        if not isinstance(passage, dict):
            flag("DOCUMENT_ANCHOR_INVALID", "hold", "Anchor must be an object.", tag)
            continue
        snippet = passage.get("exact_excerpt")
        if not isinstance(snippet, str) or not snippet:
            flag("DOCUMENT_ANCHOR_EMPTY", "hold", "Document passage excerpt required.", tag)
        elif "body" not in locals() or snippet not in body:
            flag("DOCUMENT_ANCHOR_MISSING", "hold",
                 "Claim excerpt is absent from the submitted draft.", tag)
        if not passage.get("evidence_id"):
            flag("DOCUMENT_ANCHOR_UNLINKED", "hold",
                 "Draft passage must name its evidence item.", tag)

    evidence = dossier.get("evidence")
    if not isinstance(evidence, list):
        evidence = []
        flag("EVIDENCE_REQUIRED", "hold", "An evidence list is required.")
    if doc.get("arena") in {"journalism", "government", "legal", "academic"} and not evidence:
        flag("STRICT_EVIDENCE_EMPTY", "hold", "This arena requires sourced claims.")

    for i, item in enumerate(evidence):
        tag = f"evidence[{i}]"
        if not isinstance(item, dict):
            flag("EVIDENCE_INVALID", "hold", "Evidence item must be an object.", tag)
            continue
        if item.get("kind") not in KINDS:
            flag("KIND_UNKNOWN", "hold", "Choose firsthand, external, or interpretation.", tag)
        if item.get("consent") is not True:
            flag("CONSENT_ABSENT", "hold", "Explicit author consent is required.", tag)
        if item.get("kind") == "firsthand" and item.get("source_origin") != "human_authored":
            flag("FIRSTHAND_UNVERIFIED", "hold",
                 "Firsthand events cannot be inferred from AI text or a company roadmap.", tag)
        quote = item.get("exact_excerpt")
        if not isinstance(quote, str) or not quote:
            flag("EXCERPT_MISSING", "hold", "Exact supporting excerpt required.", tag)
            continue
        try:
            source, source_hash = safe_read(root, item.get("source_path"))
        except (OSError, UnicodeError, ValueError, TypeError) as exc:
            flag("SOURCE_NOT_READABLE", "hold", str(exc), tag)
            continue
        if quote not in source:
            flag("ANCHOR_MISSING", "hold", "Exact excerpt does not occur in the source.", tag)
        expected = item.get("sha256")
        if expected is not None and expected != source_hash:
            flag("SOURCE_DIGEST_MISMATCH", "hold", "Source bytes changed.", tag)
        if not item.get("claim"):
            flag("CLAIM_MISSING", "hold", "Claim description required.", tag)

    evidence_ids = {item.get("id") for item in evidence if isinstance(item, dict)
                    and isinstance(item.get("id"), str) and item.get("id")}
    for index, passage in enumerate(passages or []):
        if isinstance(passage, dict) and passage.get("evidence_id") not in evidence_ids:
            flag("DOCUMENT_EVIDENCE_NOT_FOUND", "hold",
                 "Draft anchor references no known evidence item.",
                 "document_claim_anchors[%d]" % index)

    samples = dossier.get("voice_samples", [])
    if not isinstance(samples, list):
        flag("VOICE_SAMPLES_INVALID", "hold", "voice_samples must be a list.")
        samples = []
    if len(samples) < 3:
        flag("VOICE_BASELINE_INSUFFICIENT", "advisory",
             "A measured personal voiceprint needs >=3 consented, human-authored samples of >=500 words.")
    for i, sample in enumerate(samples):
        tag = f"voice_samples[{i}]"
        if not isinstance(sample, dict) or sample.get("consent") is not True or sample.get("origin") != "human_authored":
            flag("VOICE_SAMPLE_INELIGIBLE", "hold", "Sample must be consented and human-authored.", tag)
            continue
        try:
            content, source_hash = safe_read(root, sample.get("path"))
        except (OSError, UnicodeError, ValueError, TypeError) as exc:
            flag("VOICE_SAMPLE_NOT_READABLE", "hold", str(exc), tag)
            continue
        count = len(re.findall(r"\b[\w'-]+\b", content))
        if count < 500:
            flag("VOICE_SAMPLE_TOO_SHORT", "advisory", "Sample has fewer than 500 words.", tag)
        if sample.get("sha256") is not None and sample["sha256"] != source_hash:
            flag("VOICE_SAMPLE_DIGEST_MISMATCH", "hold", "Voice sample changed.", tag)

    status = "HOLD" if any(f["level"] == "hold" for f in findings) else "REVIEW"
    return {
        "schema": "wi9-authorship-audit-1",
        "status": status,
        "document_sha256": document_hash,
        "declared_origin": origin,
        "venue_policy": venue,
        "intended_use": intended,
        "claim_count": len(evidence),
        "findings": findings,
        "limitations": [
            "Origin and consent declarations are not independently authenticated.",
            "Exact quote presence establishes a text anchor, not truth or lived experience.",
            "REVIEW does not authorize publication, submission or a claim of human authorship.",
            "No detector probability, bypass, rewriting, or authorship certification is performed."
        ],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    cmd = sub.add_parser("audit", help="Audit a local authorship/evidence dossier")
    cmd.add_argument("--input", required=True)
    cmd.add_argument("--out")
    args = parser.parse_args(argv)
    path = Path(args.input).resolve()
    try:
        dossier = json.loads(path.read_text(encoding="utf-8"))
        result = analyze(dossier, path.parent)
    except (OSError, ValueError, TypeError) as exc:
        result = {"schema": "wi9-authorship-audit-1", "status": "HOLD",
                  "findings": [{"code": "DOSSIER_INVALID", "level": "hold", "message": str(exc)}]}
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.out:
        Path(args.out).write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0 if result["status"] == "REVIEW" else 3


if __name__ == "__main__":
    raise SystemExit(main())
