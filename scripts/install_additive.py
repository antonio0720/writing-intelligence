#!/usr/bin/env python3
"""Collision-safe WI fiction overlay installer. Dry run unless --apply is supplied.

Only copies additive files into an existing checkout. No overwrite, no deletes,
no symlink traversal, no Git mutation; user must still review upstream changes.
"""
import argparse
import shutil
import sys
from pathlib import Path

EXCLUDED={'.DS_Store'}


def main():
    p=argparse.ArgumentParser(description='Install additive v8-fiction candidate files without overwriting')
    p.add_argument('--target',required=True,help='existing writing-intelligence clone root')
    p.add_argument('--apply',action='store_true',help='actually copy new files (default dry-run)')
    a=p.parse_args()
    root=Path(__file__).resolve().parent.parent
    target=Path(a.target).resolve()
    if not (target/'scripts/wi.py').is_file() or not (target/'SKILL.md').is_file():
        p.error('target is not an existing Writing Intelligence checkout (requires scripts/wi.py and SKILL.md)')
    if not target.is_dir() or target==root or root in target.parents or target in root.parents:
        p.error('source and target must be different non-nested directories')
    files=[f for f in root.rglob('*') if f.is_file() and not f.is_symlink() and not any(x in ('__pycache__','.git') for x in f.parts) and f.name not in EXCLUDED and not f.suffix=='.pyc']
    collisions=[];new=[]
    for f in sorted(files):
        dest=target/f.relative_to(root)
        if dest.exists() or dest.is_symlink(): collisions.append(str(f.relative_to(root)))
        else:new.append((f,dest))
    if collisions:
        print('REFUSE existing target files; no partial install:',file=sys.stderr)
        for c in collisions:print('  '+c,file=sys.stderr)
        return 2
    print(('APPLY' if a.apply else 'DRY RUN')+': %d new files, 0 collisions'%len(new))
    if a.apply:
        for src,dst in new:
            # Parents must not be symlinks, to avoid redirecting copy outside checkout.
            p=dst.parent
            while p!=target:
                if p.is_symlink():raise ValueError('symlink parent rejected: '+str(p))
                p=p.parent
            dst.parent.mkdir(parents=True,exist_ok=True)
            # Exclusive creation fails closed in a concurrent install.
            with src.open('rb') as stream, dst.open('xb') as out:shutil.copyfileobj(stream,out)
        print('COPIED; run tests and review diff. No Git commit or merge performed.')
    return 0


if __name__=='__main__':
    try:sys.exit(main())
    except (OSError,ValueError) as e:print('WI_FI_INSTALL_ERROR: '+str(e),file=sys.stderr);sys.exit(2)
