#!/usr/bin/env python3
"""Review ledger for experimental WI9 phrase diagnoses.

Project author: Antonio T. Smith Jr.
This validates decisions against an exact unchanged source; it never rewrites
prose or authorizes publication and makes no claim about AI detection.
"""
import argparse
import datetime
import hashlib
import json
from pathlib import Path

STATUS = {'retain_as_written', 'revise_for_clarity', 'needs_source', 'not_applicable'}
MAX_DECISIONS = 1000
MAX_FILE_BYTES = 2_000_000


def _review_time(value):
    """Offset-aware ISO 8601 not in the future, else None."""
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        when = datetime.datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        return None
    if when.tzinfo is None or when > datetime.datetime.now(datetime.timezone.utc):
        return None
    return when


def _hexsha(value):
    return isinstance(value, str) and len(value) == 64 and all(c in '0123456789abcdef' for c in value)


def _recomputed(text, report, pack):
    """The report must be what the scanner says about this text and rule pack.
    A hand-edited report (findings removed, digests copied) is refused."""
    from wi9_hotphrases import scan_text, DEFAULT_PACK
    pack = pack or DEFAULT_PACK
    for include_quoted in (False, True):
        fresh = scan_text(text, pack=pack, include_quoted=include_quoted)
        if fresh['rules_sha256'] == report.get('rules_sha256') and fresh['findings'] == report.get('findings'):
            return True
    return False


def audit_decisions(text, report, decisions, pack=None):
    """Bind judgment to exact span and digest; stale documents HOLD decisions."""
    issues = []
    doc_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
    if not isinstance(report, dict) or report.get('schema') != 'wi9.hotphrases.report/1':
        return {'status':'HOLD','issues':['REPORT_INVALID'],'release_authorized':False}
    if report.get('document_sha256') != doc_hash:
        issues.append('DOCUMENT_STALE')
    if not _hexsha(report.get('rules_sha256')):
        issues.append('RULES_DIGEST_MISSING')
    if not isinstance(decisions, dict) or decisions.get('schema') != 'wi9.editorial.review/1':
        return {'status':'HOLD','issues':['REVIEW_SCHEMA_INVALID'],'release_authorized':False}
    if decisions.get('document_sha256') != doc_hash:
        issues.append('REVIEW_DOCUMENT_STALE')
    if decisions.get('rules_sha256') != report.get('rules_sha256'):
        issues.append('REVIEW_RULESET_STALE')
    raw_items = decisions.get('decisions')
    if not isinstance(raw_items, list) or len(raw_items) > MAX_DECISIONS:
        return {'status':'HOLD','issues':['DECISIONS_INVALID_OR_OVERSIZE'],'release_authorized':False}
    hits = report.get('findings')
    if not isinstance(hits, list):
        return {'status':'HOLD','issues':['REPORT_FINDINGS_INVALID'],'release_authorized':False}
    targets = {(f['id'],f['start'],f['end'],f['excerpt']) for f in hits
               if isinstance(f,dict) and all(k in f for k in ('id','start','end','excerpt'))
               and isinstance(f['id'],str) and isinstance(f['excerpt'],str)
               and isinstance(f['start'],int) and isinstance(f['end'],int)}
    if 'DOCUMENT_STALE' not in issues and not _recomputed(text, report, pack):
        issues.append('REPORT_NOT_REPRODUCED')
    seen=set()
    reviewed=[]
    for i, item in enumerate(raw_items):
        if not isinstance(item, dict):
            issues.append('DECISION_NOT_OBJECT:%d'%i)
            continue
        target=(item.get('rule_id'),item.get('start'),item.get('end'),item.get('excerpt'))
        if not isinstance(target[0],str) or not isinstance(target[3],str) \
                or any(not isinstance(v,int) or isinstance(v,bool) for v in target[1:3]):
            issues.append('SPAN_INVALID:%d'%i)
            continue
        if target not in targets:
            issues.append('DECISION_TARGET_UNKNOWN:%d'%i)
        if target in seen:
            issues.append('DECISION_DUPLICATE:%d'%i)
        seen.add(target)
        if item.get('status') not in STATUS:
            issues.append('DECISION_STATUS_INVALID:%d'%i)
        if not isinstance(item.get('rationale'),str) or len(item['rationale'].strip()) < 12:
            issues.append('RATIONALE_MISSING:%d'%i)
        if not isinstance(item.get('reviewer'),str) or not item['reviewer'].strip():
            issues.append('REVIEWER_MISSING:%d'%i)
        if not isinstance(item.get('reviewed_at'),str) or not item['reviewed_at'].strip():
            issues.append('REVIEW_DATE_MISSING:%d'%i)
        elif _review_time(item['reviewed_at']) is None:
            issues.append('REVIEW_DATE_INVALID:%d'%i)
        reviewed.append(item)
    unreviewed = len(targets - seen)
    if unreviewed:
        issues.append('FINDINGS_UNREVIEWED:%d' % unreviewed)
    return {'schema':'wi9.editorial.review.report/1',
            'status':'HOLD' if issues else 'REVIEW', 'issues':issues,
            'total_flagged':len(hits), 'total_reviewed':len(reviewed),
            'review_coverage':round(len(seen.intersection(targets))/max(1,len(targets)),4),
            'release_authorized':False,
            'limitations':['Declared reviewer identity is not independently authenticated.',
                           'A reviewed editorial phrase is not proof of origin or source truth.',
                           'Review never triggers automated rewriting or submission.']}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',required=True)
    parser.add_argument('--report',required=True)
    parser.add_argument('--decisions',required=True)
    args=parser.parse_args(argv)
    try:
        for name in (args.input, args.report, args.decisions):
            if Path(name).stat().st_size > MAX_FILE_BYTES:
                raise ValueError('FILE_OVERSIZE: %s' % name)
        text=Path(args.input).read_text(encoding='utf-8')
        report=json.loads(Path(args.report).read_text(encoding='utf-8'))
        decisions=json.loads(Path(args.decisions).read_text(encoding='utf-8'))
        result=audit_decisions(text,report,decisions)
    except (OSError, ValueError, UnicodeError, TypeError, RecursionError) as exc:
        result={'status':'HOLD','issues':[str(exc)],'release_authorized':False}
    print(json.dumps(result,indent=2,sort_keys=True))
    return 3 if result['status']=='HOLD' else 0

if __name__=='__main__':
    raise SystemExit(main())
