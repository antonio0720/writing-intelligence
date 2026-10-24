#!/usr/bin/env python3
"""Verifies the sealed archive payload contents against its own checksums.

Requires trust in the presented manifest; hashes show integrity relative to
that manifest, not independent authorship or upstream release authenticity.
"""
from pathlib import Path
import hashlib
import json
import sys

ROOT=Path(__file__).resolve().parents[4]  # standalone root when installed extension tree

def main():
    manifest=ROOT/'JAPAN04_SHA256SUMS.txt'
    if not manifest.exists():
        print('CHECKSUM_MANIFEST_NOT_FOUND; run from intact independent ZIP extraction',file=sys.stderr)
        return 2
    bad=[];seen=set()
    for raw in manifest.read_text().splitlines():
        if not raw.strip():continue
        digest,sep,name=raw.partition('  ')
        if sep!='  ' or len(digest)!=64:bad.append('malformed manifest line');continue
        target=ROOT/name
        if name.startswith('/') or '..' in Path(name).parts:bad.append('unsafe path');continue
        if name in seen:bad.append('duplicate entry '+name);continue
        seen.add(name)
        if target.is_symlink() or not target.is_file():bad.append('missing/symlink '+name);continue
        actual=hashlib.sha256(target.read_bytes()).hexdigest()
        if actual!=digest:bad.append('digest mismatch '+name)
    print(json.dumps({'status':'PASS' if not bad else 'FAIL','files_checked':len(seen),'errors':bad},indent=2))
    return 0 if not bad else 1
if __name__=='__main__':raise SystemExit(main())
