"""Permission-aware creative-studio interface: no autonomous manuscript rewriting."""
from .contracts import AUTHOR_MODES,ContractError

WRITE_MODES={'edit','co-create','surprise'}

def plan_request(mode, author_text, scope='scene', allow_proposed_prose=False):
    if mode not in AUTHOR_MODES:raise ContractError('unsupported studio mode')
    if not isinstance(author_text,str):raise ContractError('author_text must be string')
    if scope not in ('sentence','scene','chapter','world','series','research'):raise ContractError('unsupported scope')
    proposed = mode in WRITE_MODES and bool(allow_proposed_prose)
    return {'mode':mode,'scope':scope,'input_text_unchanged':author_text,'may_offer_prose_proposal':proposed,
            'may_rewrite_original':False,'requires_author_acceptance':proposed,
            'critic_questions_only':mode=='questions-only','network_access':False,
            'public_visibility':False,'canon_write_permission':False,'automatic_quota':False,
            'status':'PLAN_ONLY_NOT_GENERATED'}

def compare_paths(choices):
    if not isinstance(choices,list) or len(choices)<2:raise ContractError('two or more creative paths required')
    if len(set(choices))!=len(choices):raise ContractError('creative paths must be distinct')
    return [{'path':c,'tradeoffs_unassessed':True,'author_selected':False} for c in choices]
