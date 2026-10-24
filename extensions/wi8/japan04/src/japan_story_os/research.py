"""Offline safe research cards, folklore variants, and untrusted-input discipline."""
import re
from .contracts import ContractError, require

INJECTION_INDICATORS=(r'ignore (?:all )?previous instructions',r'(?:system|developer) prompt',r'send (?:the|all) (?:files|drafts|manuscripts)',r'upload .*secret',r'\bapi[ _-]?key\b')

def source_card(source, *, quotation=None, max_quote_chars=180):
    require(source.get('id') and source.get('title'),'source id/title missing')
    # Keep excerpts small by default; do not copy copyrighted sources into an exported pack.
    if quotation and (source.get('rights') in ('restricted','permission_required') or len(quotation)>max_quote_chars):
        quotation=None
    return {'id':source['id'],'title':source['title'],'kind':source.get('kind','unknown'),
            'status':source.get('status','NEEDS_SOURCE'),'rights':source.get('rights','unknown'),
            'retrieved_at':source.get('retrieved_at'),'publisher':source.get('publisher'),
            'locator':source.get('locator'),'scope':source.get('scope',{}),
            'excerpt':quotation,'excerpt_protected':quotation is None,'authoritative':False}

def quarantine_report(text):
    if not isinstance(text,str):raise ContractError('text must be string')
    matches=[p for p in INJECTION_INDICATORS if re.search(p,text,re.I)]
    return {'untrusted_data':True,'instruction_authority':'none', 'possible_injection':bool(matches),
            'matched_patterns':matches, 'allow_tool_instructions':False, 'allow_network':False}

def research_suggestion(claim, sources):
    ids=claim.get('source_refs',[])
    present=[source_card(sources[i]) for i in ids if i in sources]
    return {'claim_id':claim['id'], 'research_status':claim.get('source_status','NEEDS_SOURCE'),
            'evidence':present,'creative_seed':'OPTIONAL_INVENTION_NOT_EXTERNAL_FACT',
            'unknowns':([] if present else ['no accessible source']), 'verified_by_this_tool':False}
