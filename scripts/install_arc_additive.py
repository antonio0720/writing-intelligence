#!/usr/bin/env python3
"""Fail-closed additive installer. Dry-run by default, no GitHub mutation."""
from pathlib import Path
import argparse
import os
import shutil
import sys

ROOT=Path(__file__).resolve().parent.parent
# Intentionally exclude README/source/receipts/fixtures. Source licensing and
# integration of fixtures must be reviewed separately by the owner.
PREFIXES=('scripts/wi-arc.py','scripts/arc_v8/','schemas/v8/arc_',
          'references/v8/ARC_', 'references/v8/ENDING_', 'references/v8/EDITORIAL_',
          'references/compiler/arc_', 'references/genre_packs/fiction_arc_',
          'rules/arc_', 'plans/v8-arc.', 'docs/ADAPTER_CONTRACT.md',
          'docs/MERGE_CONTRACT.md', 'docs/OWNER_CROSSWALK.md',
          'docs/SCHEMA_AND_LIMITS.md', 'docs/TEST_AND_RELEASE.md',
          'tests/v8_arc/', 'benchmarks/cases/arc_', '.github/workflows/wi8-arc-')

def matches(path):return any(path.startswith(p) for p in PREFIXES)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--target',required=True);p.add_argument('--apply',action='store_true')
    a=p.parse_args();target=Path(a.target).expanduser().resolve()
    if not target.is_dir() or not (target/'scripts/wi.py').is_file() or not (target/'schemas/v6/semantic_node.schema.json').is_file():
        p.error('target must be actual Writing Intelligence checkout with v6 core')
    candidates=[]
    for src in sorted(ROOT.rglob('*')):
        if not src.is_file() or '__pycache__' in src.parts:continue
        rel=src.relative_to(ROOT).as_posix()
        if matches(rel):candidates.append((src,rel))
    collisions=[rel for src,rel in candidates if (target/rel).exists()]
    if collisions:
        print('BLOCK: existing paths; refusing ALL writes\n'+'\n'.join(collisions),file=sys.stderr)
        return 2
    print('DRY RUN' if not a.apply else 'APPLY (additive only)',len(candidates),'paths')
    for src,rel in candidates:print(' +',rel)
    if a.apply:
        # Exclusive creation avoids overwriting an existing target path.
        for src,rel in candidates:
            dst=target/rel
            dst.parent.mkdir(parents=True,exist_ok=True)
            flags=os.O_WRONLY|os.O_CREAT|os.O_EXCL
            try:
                fd=os.open(str(dst),flags,0o644)
                with os.fdopen(fd,'wb') as out,src.open('rb') as inp:
                    shutil.copyfileobj(inp,out)
            except FileExistsError:
                print('STOP: concurrent path creation collision:',rel,file=sys.stderr)
                return 2
        print('FILES WRITTEN — manual canonical integration, tests and release checks still required')
    return 0

if __name__=='__main__':sys.exit(main())
