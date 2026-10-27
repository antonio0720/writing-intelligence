#!/usr/bin/env python3
"""Writing Intelligence v9 experimental candidate composition contract.

Project owner: Antonio T. Smith Jr. / Density6 LLC

This module specifies model I/O and performs deterministic structural checks.
It is NOT a model backend or a complete semantic verification engine.
"""
import hashlib
import json
import re
from wi9_core import sha256, ORIGINS, RISKY_AI

CONTRACT = "wi9.compose/1"
OUTPUT = "wi9.candidate/1"


def prepare_request(dossier):
    """Create a model-neutral composition request, not an external send action.

    Human-only policy blocks an AI prose request entirely. This is independent
    of whether a commercial detector would classify the output as human.
    """
    if not isinstance(dossier, dict):
        return {"status": "HOLD", "reason": "DOSSIER_INVALID"}
    document = dossier.get('document', {})
    venue = dossier.get('venue', {})
    if not isinstance(document, dict) or not isinstance(venue, dict):
        return {"status": "HOLD", "reason": "CONTRACT_INVALID"}
    policy = venue.get('policy', 'unknown')
    mode = document.get('intended_use', 'unknown')
    if policy == 'human_only':
        return {"status": "HOLD", "reason": "HUMAN_ONLY_NO_GENERATED_PROSE",
                "alternative": "Research brief / questions only, written submission must originate with the person"}
    if policy == 'unknown':
        return {"status": "HOLD", "reason": "VENUE_POLICY_UNKNOWN"}
    if policy == 'disclosure_required' and not venue.get('disclosure_plan'):
        return {"status": "HOLD", "reason": "DISCLOSURE_PLAN_REQUIRED"}
    if mode not in ('research', 'internal_review', 'submission'):
        return {"status": "HOLD", "reason": "INTENDED_USE_INVALID"}
    evidence = dossier.get('evidence', [])
    if not isinstance(evidence, list) or not evidence:
        return {"status": "HOLD", "reason": "EVIDENCE_REQUIRED"}
    if any(not isinstance(e, dict) or e.get('consent') is not True or not isinstance(e.get('id'), str) or not e['id'] for e in evidence):
        return {"status": "HOLD", "reason": "EVIDENCE_INVALID"}
    cards = []
    seen = set()
    for e in evidence:
        if e['id'] in seen:
            return {"status": "HOLD", "reason": "DUPLICATE_EVIDENCE_ID"}
        seen.add(e['id'])
        cards.append({"id": e['id'], "claim": e.get('claim'), "kind": e.get('kind'),
                      "source_quote": e.get('exact_excerpt'), "source_origin": e.get('origin'),
                      "limitations": e.get('limitations', [])})
    # A structured, auditable request is preferred to long untrusted snippets in
    # a faux system prompt. All author materials remain untrusted source *data*.
    request = {
        "schema": CONTRACT,
        "mode": "draft_candidate_not_release",
        "arena": document.get('arena'),
        "intent": document.get('mission'),
        "venue": {"policy": policy, "disclosure_plan": venue.get('disclosure_plan')},
        "author_thesis": dossier.get('author_thesis'),
        "source_cards": cards,
        "requirements": [
            "Develop actual source-backed meaning before revising cadence.",
            "Do not construct first-person memories or data absent from the evidence cards.",
            "Do not promote planned or hypothetical work to completed work.",
            "Use direct quotations only when exactly present in the source card.",
            "Retain uncertainty, unresolved questions, and the author's counterargument.",
            "Return typed paragraph objects with evidence_ids and author_review_required=true.",
            "Never treat this output as authorization to submit or publish.",
        ],
        "expected_output_schema": OUTPUT,
        "origin_of_generated_candidate": "ai_generated"
    }
    return {"status": "REQUEST_READY", "request": request,
            "release_authorized": False,
            "limitations": "Model backend is NOT implemented here. Any response requires human review."}


def inspect_candidate(candidate, request):
    """Validate output structure and evidence *references*, not semantic truth."""
    errors = []
    if not isinstance(request, dict) or request.get('status') != 'REQUEST_READY':
        return {"status": "HOLD", "errors": ["REQUEST_INVALID"], "release_authorized": False}
    if not isinstance(candidate, dict) or candidate.get('schema') != OUTPUT:
        return {"status": "HOLD", "errors": ["CANDIDATE_SCHEMA_INVALID"], "release_authorized": False}
    paragraphs = candidate.get('paragraphs')
    if not isinstance(paragraphs, list) or not paragraphs:
        return {"status": "HOLD", "errors": ["PARAGRAPHS_REQUIRED"], "release_authorized": False}
    source_cards = {v['id']: v for v in request['request']['source_cards']}
    for i, p in enumerate(paragraphs):
        if not isinstance(p, dict):
            errors.append('PARAGRAPH_NOT_OBJECT:%d' % i)
            continue
        text = p.get('text')
        ids = p.get('evidence_ids')
        if not isinstance(text, str) or not text.strip():
            errors.append('TEXT_EMPTY:%d' % i)
            continue
        if not isinstance(ids, list) or not ids or any(not isinstance(v, str) or v not in source_cards for v in ids):
            errors.append('EVIDENCE_UNRESOLVED:%d' % i)
        if p.get('author_review_required') is not True:
            errors.append('REVIEW_FLAG_ABSENT:%d' % i)
        quotes = p.get('direct_quotes', [])
        if not isinstance(quotes, list):
            errors.append('QUOTE_LIST_INVALID:%d' % i)
            quotes = []
        for quote in quotes:
            if not isinstance(quote, dict) or not isinstance(quote.get('source_id'), str) or quote.get('source_id') not in source_cards:
                errors.append('QUOTE_SOURCE_INVALID:%d' % i)
                continue
            original = source_cards[quote['source_id']].get('source_quote')
            q = quote.get('exact_text')
            if not isinstance(q, str) or not isinstance(original, str) or q not in original or q not in text:
                errors.append('QUOTATION_UNVERIFIED:%d' % i)
        if p.get('asserts_firsthand') is True:
            if not any(source_cards[v].get('kind') == 'firsthand' and source_cards[v].get('source_origin') == 'human_authored' for v in ids if v in source_cards):
                errors.append('UNANCHORED_FIRSTHAND:%d' % i)
        if len(text) > 20000:
            errors.append('PARAGRAPH_SIZE_LIMIT:%d' % i)
    body = '\n\n'.join(p.get('text','') for p in paragraphs if isinstance(p, dict) and isinstance(p.get('text'), str))
    return {"status": "HOLD" if errors else "DRAFT_REVIEW_REQUIRED", "errors": errors,
            "candidate_sha256": sha256(body.encode('utf-8')), "release_authorized": False,
            "claim_scope": "References and direct quotes were checked; semantic entailment and full factual coverage are UNVERIFIED",
            "candidate_text": body if not errors else None}


def render_research_only(dossier):
    """A human-only outlet may receive a background research *plan*, never draft pitch text."""
    from wi9_core import editorial_plan
    result = editorial_plan(dossier)
    return {"status": "RESEARCH_ONLY", "source_questions": result['questions'],
            "author_owned_facts": result['author_owned_facts'],
            "submission_text": None}
