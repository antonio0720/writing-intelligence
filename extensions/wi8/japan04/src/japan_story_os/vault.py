"""Local-only author draft vault with CAS, immutable blobs and explicit decisions.

Not a replacement for v6 authorship state or graph. Intentionally no networking,
no real public publishing, no AI rewriting, and no credentials. A local workstation
may still need OS encryption and account isolation; this module does not supply
those protections or claim that disk bytes are encrypted.
"""
from __future__ import annotations
import hashlib
import json
import os
import stat
import tempfile
import uuid
from pathlib import Path
from .contracts import ContractError, nonempty

class ConflictError(RuntimeError):
    pass

def _hash(data):return hashlib.sha256(data).hexdigest()

def _safe_file(path:Path):
    if path.is_symlink(): raise ContractError('symlink refused')
    if path.exists() and not path.is_file():raise ContractError('not a regular file')

def _safe_workspace(path:Path):
    if path.is_symlink():raise ContractError('workspace symlink refused')
    path.mkdir(parents=True,exist_ok=True,mode=0o700)
    if not path.is_dir():raise ContractError('workspace must be directory')
    os.chmod(path,0o700)

def _atomic(path:Path,blob:bytes):
    _safe_file(path)
    fd,name=tempfile.mkstemp(prefix='.wi8-tmp-',dir=str(path.parent))
    try:
        os.fchmod(fd,0o600)
        with os.fdopen(fd,'wb') as f:
            f.write(blob);f.flush();os.fsync(f.fileno())
        os.replace(name,path)
        d=os.open(str(path.parent),os.O_RDONLY)
        try:os.fsync(d)
        finally:os.close(d)
    finally:
        if os.path.exists(name):os.unlink(name)

class DraftVault:
    def __init__(self,root):
        self.root=Path(root)
        _safe_workspace(self.root)
        for sub in ('objects','receipts','proposals'):
            p=self.root/sub
            if p.is_symlink():raise ContractError('unsafe vault directory')
            p.mkdir(exist_ok=True,mode=0o700)
            os.chmod(p,0o700)
        self.index=self.root/'index.json'
        if not self.index.exists(): _atomic(self.index,b'{"format":"wi8-japan04/vault-1","drafts":{},"proposals":{}}\n')
        _safe_file(self.index)

    def _read(self):
        _safe_file(self.index)
        state=json.loads(self.index.read_bytes())
        if state.get('format')!='wi8-japan04/vault-1':raise ContractError('vault version wrong')
        return state

    def _lock(self):
        lock=self.root/'.lock'
        # Intentionally fail when another process holds the lock; no silent retries.
        try:fd=os.open(str(lock),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        except FileExistsError:raise ConflictError('vault busy; reconcile lock owner before retry')
        return fd,lock
    def _unlock(self,handle):
        fd,path=handle;os.close(fd);path.unlink()

    def _blob_path(self,sha):
        if not isinstance(sha,str) or len(sha)!=64 or any(c not in '0123456789abcdef' for c in sha):raise ContractError('unsafe hash')
        return self.root/'objects'/sha

    def _write_blob(self,content:bytes):
        sha=_hash(content);p=self._blob_path(sha)
        if p.exists():
            _safe_file(p)
            if _hash(p.read_bytes())!=sha:raise ContractError('immutable blob corrupted')
        else:
            # Create without replacement. Race resistance is provided by the global vault lock.
            fd=os.open(str(p),os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
            with os.fdopen(fd,'wb') as f:f.write(content);f.flush();os.fsync(f.fileno())
        return sha

    def save(self, draft_id, text, expected_revision=None, origin='human_authored'):
        nonempty(draft_id,'draft_id')
        if not isinstance(text,str):raise ContractError('text required')
        if origin!='human_authored':raise ContractError('cannot infer authorship; import proposal instead')
        h=self._lock()
        try:
            state=self._read();drafts=state['drafts'];old=drafts.get(draft_id)
            actual=old['revision'] if old else None
            if actual!=expected_revision:raise ConflictError('stale revision; no draft updated')
            sha=self._write_blob(text.encode('utf-8'))
            revision=0 if old is None else actual+1
            history=list(old['history']) if old else []
            history.append({'revision':revision,'sha256':sha,'origin':origin,'decision_id':None})
            drafts[draft_id]={'revision':revision,'content_sha256':sha,'history':history}
            _atomic(self.index,(json.dumps(state,sort_keys=True,ensure_ascii=False)+'\n').encode())
            return {'draft_id':draft_id,'revision':revision,'sha256':sha,'origin':origin}
        finally:self._unlock(h)

    def read(self,draft_id,revision=None):
        state=self._read();draft=state['drafts'].get(draft_id)
        if not draft:raise KeyError(draft_id)
        if revision is None:sha=draft['content_sha256']
        else:
            entries=[h for h in draft['history'] if h['revision']==revision]
            if not entries:raise KeyError('revision')
            sha=entries[0]['sha256']
        p=self._blob_path(sha);_safe_file(p)
        data=p.read_bytes()
        if _hash(data)!=sha:raise ContractError('immutable blob digest mismatch')
        return data.decode('utf-8')

    def history(self,draft_id):
        state=self._read();return list(state['drafts'][draft_id]['history'])

    def propose(self,draft_id,before_sha,after_text,reason,actor='assistant'):
        if not isinstance(after_text,str):raise ContractError('proposed text required')
        nonempty(reason,'reason');nonempty(actor,'actor')
        h=self._lock()
        try:
            state=self._read();draft=state['drafts'].get(draft_id)
            if not draft:raise KeyError(draft_id)
            if draft['content_sha256']!=before_sha:raise ConflictError('proposal target changed')
            proposed_sha=self._write_blob(after_text.encode('utf-8'))
            pid='proposal-'+uuid.uuid4().hex
            state['proposals'][pid]={'draft_id':draft_id,'before_sha':before_sha,'after_sha':proposed_sha,'status':'pending','actor':actor,'reason':reason}
            _atomic(self.index,(json.dumps(state,sort_keys=True,ensure_ascii=False)+'\n').encode())
            return {'proposal_id':pid,'before_sha256':before_sha,'after_sha256':proposed_sha,'status':'pending',
                    'changes_committed':False,'needs_author_decision':True}
        finally:self._unlock(h)

    def decide(self,proposal_id,actor,decision):
        nonempty(actor,'actor')
        if actor!='author':raise ContractError('only author identity can accept creative rewrites')
        if decision not in ('accept','reject'):raise ContractError('decision must be accept or reject')
        h=self._lock()
        try:
            state=self._read();p=state['proposals'].get(proposal_id)
            if not p:raise KeyError(proposal_id)
            if p['status']!='pending':raise ConflictError('decision already recorded')
            draft=state['drafts'][p['draft_id']]
            if draft['content_sha256']!=p['before_sha']:raise ConflictError('draft changed since proposal')
            p['status']='accepted' if decision=='accept' else 'rejected'
            if decision=='accept':
                draft['revision']+=1;draft['content_sha256']=p['after_sha']
                draft['history'].append({'revision':draft['revision'],'sha256':p['after_sha'],'origin':'author_adopted_suggestion','decision_id':proposal_id})
            _atomic(self.index,(json.dumps(state,sort_keys=True,ensure_ascii=False)+'\n').encode())
            return {'decision':decision,'proposal_id':proposal_id,'changed':decision=='accept','author_decision':True}
        finally:self._unlock(h)

    def preview_publication(self, draft_id, metadata=None):
        metadata=metadata or {}
        # This method does not create or release a public artifact. It generates a preview only.
        personal={'legal_name','school','home_address','date_of_birth','contact_email','phone','minor_photo','schedule'}
        filtered={k:v for k,v in metadata.items() if k not in personal}
        return {'status':'NOT_PUBLISHED','stage':'local_preview_only','draft_sha256':_hash(self.read(draft_id).encode('utf-8')),
                'metadata':filtered,'suppressed_sensitive_fields':sorted(set(metadata)&personal),
                'external_effects':0,'requires_authorization':True,'publisher_connected':False}
