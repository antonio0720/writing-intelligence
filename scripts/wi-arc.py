#!/usr/bin/env python3
"""Standalone v8 fiction arc/ending projection evaluator, not a wi.py command."""
import argparse
import json
import sys
from pathlib import Path
from arc_v8.engine import validate, evaluate, classify, as_of, impact, gate, state_diff

ROOT=Path(__file__).resolve().parent.parent
MAX_BYTES=8*1024*1024

def load(path):
    path=Path(path)
    if path.stat().st_size>MAX_BYTES:raise ValueError('Input exceeds 8 MiB local evaluation bound')
    with path.open(encoding='utf-8') as f: return json.load(f)

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    s=p.add_subparsers(dest='command',required=True)
    for cmd in ('validate','evaluate','gate','as-of','impact','diff'):
        q=s.add_parser(cmd);q.add_argument('--input',required=True)
        if cmd=='gate':
            q.add_argument('--stage',choices=['mechanical','editorial','publication'],default='mechanical')
            q.add_argument('--reader-reviews')
        if cmd=='as-of':
            q.add_argument('--event',required=True);q.add_argument('--known-at',required=True)
        if cmd=='impact': q.add_argument('--changed',nargs='+',required=True)
        if cmd=='diff':
            q.add_argument('--start',required=True);q.add_argument('--end',required=True)
            q.add_argument('--known-at',required=True);q.add_argument('--character')
    c=s.add_parser('classify');c.add_argument('--want',required=True);c.add_argument('--need',required=True)
    c.add_argument('--closure',default='closed');c.add_argument('--need-basis',default='author_asserted');c.add_argument('--ending-basis',default='author_asserted')
    r=s.add_parser('rules');r.add_argument('--id')
    args=p.parse_args(argv)
    try:
        if args.command=='classify': out=classify({'want_outcome':args.want,'need_outcome':args.need,'closure':args.closure},args.need_basis,args.ending_basis)
        elif args.command=='rules':
            data=load(ROOT/'rules'/'arc_120_requirements.json')
            out=next((x for x in data['requirements'] if x['id']==args.id),None) if args.id else data
            if out is None: raise ValueError('Unknown rule id')
        else:
            doc=load(args.input)
            if args.command=='validate':
                findings=validate(doc);out={'valid':not findings,'findings':findings}
            elif args.command=='evaluate': out=evaluate(doc)
            elif args.command=='gate': out=gate(doc,load(args.reader_reviews) if args.reader_reviews else None,args.stage)
            elif args.command=='as-of': out=as_of(doc,args.event,args.known_at)
            elif args.command=='impact': out=impact(doc,args.changed)
            elif args.command=='diff': out=state_diff(doc,args.start,args.end,args.known_at,args.character)
        print(json.dumps(out,indent=2,sort_keys=True,ensure_ascii=False))
        if args.command=='validate':return 0 if out['valid'] else 2
        if args.command=='evaluate':return 0 if out['status']=='evaluated' else 2
        if args.command=='gate':return 0 if out['verdict']=='PASS_MECHANICAL_ONLY' else (2 if out['verdict']=='BLOCK' else 3)
        if args.command=='as-of':return 0 if out['status']=='projected' else 2
        if args.command in ('impact','diff'):return 0 if out['status']=='projection_only' else 2
        return 0
    except (OSError,ValueError,UnicodeError) as exc:
        print(json.dumps({'error':str(exc),'verdict':'BLOCK'},indent=2),file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())
