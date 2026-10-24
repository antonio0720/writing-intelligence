#!/usr/bin/env python3
"""Fail-closed optional future installer. Default dry run, no overwrites."""
import argparse,subprocess,shutil,sys,tempfile,os
from pathlib import Path
BASE=Path(__file__).resolve().parent.parent
COMMIT='d4524f3caa5f75e005b23f94dcd1c71bb5002127'

def files():
    return sorted(p.relative_to(BASE) for p in BASE.rglob('*')
                  if p.is_file() and '__pycache__' not in p.parts and not p.name.endswith('.pyc'))

def main(argv=None):
    parser=argparse.ArgumentParser(description='Dry-run ZIP #3 install into an isolated repo extension path')
    parser.add_argument('--target',required=True,help='Existing repository checkout')
    parser.add_argument('--apply',action='store_true',help='Perform authorized additive copy only after all preconditions')
    parser.add_argument('--expected-head',default=COMMIT,help='Required exact repo git commit SHA')
    args=parser.parse_args(argv)
    repo=Path(args.target).expanduser().resolve()
    if not repo.is_dir() or not (repo/'scripts/wi.py').is_file():
        print('BLOCK: target must be an existing Writing Intelligence checkout',file=sys.stderr);return 2
    if args.apply:
        run=subprocess.run(['git','-C',str(repo),'rev-parse','HEAD'],capture_output=True,text=True)
        if run.returncode or run.stdout.strip()!=args.expected_head:
            print('BLOCK: repository HEAD differs from expected: do not silently retarget',file=sys.stderr);return 2
    dest=repo/'extensions/wi8/craft03'
    if dest.exists() or dest.is_symlink():
        print('BLOCK: destination already exists: never overwrite',file=sys.stderr);return 2
    rels=files()
    print('Target:',dest,'\nFiles:',len(rels),'\nMode:','APPLY' if args.apply else 'DRY_RUN')
    if not args.apply:return 0
    parent=dest.parent
    if parent.is_symlink():
        print('BLOCK: extension parent is symlink',file=sys.stderr);return 2
    parent.mkdir(parents=True,exist_ok=True)
    tmp=Path(tempfile.mkdtemp(prefix='.craft03-stage-',dir=parent))
    try:
        for rel in rels:
            t=tmp/rel;t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(BASE/rel,t)
        if dest.exists() or dest.is_symlink():raise FileExistsError('Concurrent destination appeared')
        os.rename(tmp,dest)
    except Exception as exc:
        shutil.rmtree(tmp,ignore_errors=True)
        print('BLOCK:',str(exc),file=sys.stderr);return 2
    print('INSTALLED_ADDONLY:',dest)
    return 0
if __name__=='__main__':sys.exit(main())
