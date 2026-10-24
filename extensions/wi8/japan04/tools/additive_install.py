#!/usr/bin/env python3
"""No-overwrite, pinned-HEAD additive installer. Runs locally; never pushes."""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PIN='d4524f3caa5f75e005b23f94dcd1c71bb5002127'

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',required=True)
    ap.add_argument('--expected-head',default=PIN)
    ap.add_argument('--apply',action='store_true')
    a=ap.parse_args(argv)
    repo=Path(a.repo).resolve()
    try:
        if not (repo/'.git').exists():raise ValueError('target is not a local Git checkout')
        current=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True,stderr=subprocess.DEVNULL).strip()
        if current != a.expected_head:raise ValueError('Git HEAD changed; do not retarget installation silently')
        dirty=subprocess.check_output(['git','-C',str(repo),'status','--porcelain','--untracked-files=all'],text=True).strip()
        if dirty:raise ValueError('Git checkout is not clean; refuse install')
        src=Path(__file__).resolve().parents[1]
        if src.is_symlink():raise ValueError('source package symlink refused')
        target=repo/'extensions/wi8/japan04'
        if target.exists() or target.is_symlink():raise ValueError('target already exists; no overwrite')
        if a.apply:
            base=target.parent
            base.mkdir(parents=True,exist_ok=True)
            # Defensively refuse symlinked parent components inside the repo.
            for parent in (repo/'extensions',repo/'extensions/wi8'):
                if parent.is_symlink():raise ValueError('symlink installation parent refused')
            fd,lock=tempfile.mkstemp(prefix='.jp04-install-lock-',dir=str(base))
            os.close(fd)
            stage=None
            try:
                stage=Path(tempfile.mkdtemp(prefix='.jp04-stage-',dir=str(base)))
                shutil.rmtree(stage)
                shutil.copytree(src,stage,symlinks=False)
                if target.exists() or target.is_symlink():raise ValueError('concurrent target appeared, refuse overwrite')
                os.rename(stage,target)
            finally:
                if stage and stage.exists():shutil.rmtree(stage)
                Path(lock).unlink(missing_ok=True)
        result={'status':'ADDITIVE_INSTALLED' if a.apply else 'DRY_RUN_ONLY','git_head':current,
                'destination':'extensions/wi8/japan04','core_files_modified':False,'remote_push':False,
                'official_v8_release':False}
        print(json.dumps(result,indent=2))
        return 0
    except (OSError,subprocess.CalledProcessError,ValueError) as ex:
        print(json.dumps({'status':'REFUSED','reason':str(ex)}),file=sys.stderr)
        return 2
if __name__=='__main__':raise SystemExit(main())
