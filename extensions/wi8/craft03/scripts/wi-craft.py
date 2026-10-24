#!/usr/bin/env python3
"""Standalone WI8 Craft diagnostic CLI. No upstream mutation."""
import argparse,json,sys
from pathlib import Path
from craft_v8.engine import evaluate,SCHEMA
ROOT=Path(__file__).resolve().parent.parent

def load(path):
    file=Path(path)
    if file.stat().st_size>8*1024*1024: raise ValueError('input exceeds 8 MiB')
    return json.loads(file.read_text(encoding='utf8'))

def main(argv=None):
    parser=argparse.ArgumentParser(description='WI8 Craft independent offline evaluator; no canonical writes')
    sub=parser.add_subparsers(dest='command',required=True)
    for name in ('evaluate','validate','as-of','gate'):
        x=sub.add_parser(name);x.add_argument('--input',required=True)
        if name=='as-of': x.add_argument('--known-at',required=True)
        if name=='gate': x.add_argument('--stage',choices=('mechanical','editorial','publication'),default='mechanical')
    r=sub.add_parser('rules');r.add_argument('--id')
    r=sub.add_parser('schema')
    args=parser.parse_args(argv)
    if args.command=='schema':
        print(SCHEMA);return 0
    if args.command=='rules':
        rules=json.loads((ROOT/'rules/craft_c121_c180.json').read_text())
        if args.id:
            selected=[r for r in rules['rules'] if r['id']==args.id]
            if not selected: parser.error('unknown rule ID')
            print(json.dumps(selected[0],indent=2));return 0
        print(json.dumps(rules,indent=2));return 0
    try:
        report=evaluate(load(args.input), getattr(args,'known_at',None))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({'structural_verdict':'BLOCK','error':str(exc)},indent=2));return 2
    print(json.dumps(report,indent=2,ensure_ascii=False))
    if report['structural_verdict']=='BLOCK':return 2
    if args.command=='gate' and args.stage in ('editorial','publication'):return 3
    return 0
if __name__=='__main__':sys.exit(main())
