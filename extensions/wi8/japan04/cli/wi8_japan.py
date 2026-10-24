#!/usr/bin/env python3
"""Offline Japan Story OS preview CLI. Does not modify GitHub or canonical .wi state."""
from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from japan_story_os.contracts import validate_project,empty_project,ContractError
from japan_story_os.analysis import analyze
from japan_story_os.migration import migrate_legacy
from japan_story_os.vault import DraftVault,ConflictError
from japan_story_os.studio import plan_request
from japan_story_os.release import preflight
from japan_story_os.research import quarantine_report


def load(path):
    with open(path,encoding='utf-8') as f:return json.load(f)

def show(record):
    print(json.dumps(record,indent=2,sort_keys=True,ensure_ascii=False,allow_nan=False))

def main(argv=None):
    ap=argparse.ArgumentParser(description='Japan Story OS — independent offline preview, NOT canonical Writing Intelligence')
    sub=ap.add_subparsers(dest='cmd',required=True)
    a=sub.add_parser('check');a.add_argument('project')
    a=sub.add_parser('preflight');a.add_argument('project')
    a=sub.add_parser('init');a.add_argument('vault')
    a=sub.add_parser('draft-save');a.add_argument('vault');a.add_argument('id');a.add_argument('text_file');a.add_argument('--revision',type=int)
    a=sub.add_parser('draft-read');a.add_argument('vault');a.add_argument('id');a.add_argument('--revision',type=int)
    a=sub.add_parser('draft-propose');a.add_argument('vault');a.add_argument('id');a.add_argument('before_sha');a.add_argument('text_file');a.add_argument('--reason',required=True)
    a=sub.add_parser('draft-decide');a.add_argument('vault');a.add_argument('proposal_id');a.add_argument('--actor',required=True);a.add_argument('--decision',choices=['accept','reject'],required=True)
    a=sub.add_parser('draft-history');a.add_argument('vault');a.add_argument('id')
    a=sub.add_parser('publish-preview');a.add_argument('vault');a.add_argument('id');a.add_argument('--metadata-file')
    a=sub.add_parser('migration-preview');a.add_argument('legacy_json')
    a=sub.add_parser('studio');a.add_argument('mode');a.add_argument('text_file');a.add_argument('--prose-proposals',action='store_true')
    a=sub.add_parser('untrusted-scan');a.add_argument('text_file')
    args=ap.parse_args(argv)
    try:
        if args.cmd=='check':
            report=analyze(load(args.project));show(report)
            return 2 if any(f['severity'] in ('defect','hold') for f in report['findings']) else 0
        if args.cmd=='preflight':show(preflight(load(args.project)));return 2
        if args.cmd=='init':v=DraftVault(args.vault);show({'status':'PRIVATE_LOCAL_VAULT_CREATED','path':str(v.root),'network':False});return 0
        if args.cmd in ('draft-save','draft-read','draft-propose','draft-decide','draft-history','publish-preview'):
            v=DraftVault(args.vault)
            if args.cmd=='draft-save':show(v.save(args.id,Path(args.text_file).read_text(encoding='utf-8'),args.revision));return 0
            if args.cmd=='draft-read':print(v.read(args.id,args.revision),end='');return 0
            if args.cmd=='draft-propose':show(v.propose(args.id,args.before_sha,Path(args.text_file).read_text(encoding='utf-8'),args.reason));return 0
            if args.cmd=='draft-decide':show(v.decide(args.proposal_id,args.actor,args.decision));return 0
            if args.cmd=='draft-history':show(v.history(args.id));return 0
            if args.cmd=='publish-preview':show(v.preview_publication(args.id,load(args.metadata_file) if args.metadata_file else {}));return 0
        if args.cmd=='migration-preview':show(migrate_legacy(load(args.legacy_json)));return 0
        if args.cmd=='studio':show(plan_request(args.mode,Path(args.text_file).read_text(encoding='utf-8'),allow_proposed_prose=args.prose_proposals));return 0
        if args.cmd=='untrusted-scan':show(quarantine_report(Path(args.text_file).read_text(encoding='utf-8')));return 0
    except (ContractError,ConflictError,OSError,ValueError,KeyError,UnicodeError) as exc:
        print(json.dumps({'status':'BLOCK','error':type(exc).__name__,'reason':str(exc)},ensure_ascii=False),file=sys.stderr)
        return 2
    return 2

if __name__=='__main__':raise SystemExit(main())
