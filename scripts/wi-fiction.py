#!/usr/bin/env python3
"""Writing Intelligence: proposed v8 fiction extension CLI (additive, noncanonical).

Stdlib Python 3.8+. Does not mutate an existing .wi workspace or manuscript.
"""
import argparse
import json
import sys
from pathlib import Path
from fiction_v8.engine import audit, catalog, digest, load_json, release_gate, text_signals, validate


def dump(payload, out=None):
    s=json.dumps(payload,indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if out:
        dest=Path(out)
        if dest.exists():
            raise ValueError('refusing to overwrite existing output: '+str(dest))
        dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(s,encoding='utf-8')
        print('wrote '+str(dest))
    else:sys.stdout.write(s)


def main(argv=None):
    p=argparse.ArgumentParser(description='WI fiction audit — signals, typed constraints, and human editorial gates (NOT v8 release)')
    sp=p.add_subparsers(dest='command',required=True)
    for cmd in ('validate','audit','gate'):
        c=sp.add_parser(cmd);c.add_argument('--input',required=True,help='wi.fiction.manuscript/v1 JSON')
        if cmd in ('audit','gate'):
            c.add_argument('--text',help='Optional UTF-8 manuscript .txt/.md for textual heuristics')
            c.add_argument('--out',help='New output report (refuses overwrite)')
        if cmd=='gate':
            c.add_argument('--mode',choices=('draft','editorial','publication'),default='draft')
            c.add_argument('--study',help='External human reader-study JSON for publication')
    t=sp.add_parser('text-signals');t.add_argument('--text',required=True);t.add_argument('--out')
    e=sp.add_parser('explain-rule');e.add_argument('rule_id')
    sp.add_parser('catalog')
    a=p.parse_args(argv)
    if a.command=='catalog':dump(catalog());return 0
    if a.command=='explain-rule':
        x=next((r for r in catalog()['rules'] if r['id']==a.rule_id),None)
        if not x:p.error('unknown rule '+a.rule_id)
        dump(x);return 0
    if a.command=='text-signals':
        source=Path(a.text).read_text(encoding='utf-8')
        signal={'schema':'wi.fiction.text-signals/v1','text_sha256':digest({'text':source}),'findings':text_signals(source),
                'limitation':'Heuristics are review leads, not proof of prose defects.'}
        dump(signal,a.out);return 0
    data=load_json(a.input)
    errs=validate(data)
    if a.command=='validate':
        dump({'valid':not errs,'errors':errs,'input_digest':digest(data)});return 0 if not errs else 2
    manuscript=Path(a.text).read_text(encoding='utf-8') if a.text else None
    report=audit(data,manuscript)
    if a.command=='audit':
        dump(report,a.out);return 2 if report['schema_errors'] or report['summary'].get('DEFECT') else 0
    study=load_json(a.study) if a.study else None
    out=release_gate(data,report,study,a.mode)
    dump({'audit':report,'gate':out},a.out)
    return 2 if out['verdict']=='BLOCK' else 3 if out['verdict']=='HOLD' else 0


if __name__=='__main__':
    try:sys.exit(main())
    except (ValueError,KeyError,json.JSONDecodeError,UnicodeError,OSError) as e:
        print('WI_FI_INPUT_ERROR: '+str(e),file=sys.stderr);sys.exit(2)
