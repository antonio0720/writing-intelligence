"""Local review gates and safety boundaries. No publication APIs exist."""
from .contracts import ContractError,validate_project
from .analysis import analyze

def preflight(project, author_accepted=False, guardian_approved=False, rights_reviewed=False, native_reviewed=False):
    report=analyze(project)
    holds=[f for f in report['findings'] if f['severity'] in ('hold','defect')]
    # Human review inputs here are local claims for planning, not verified grants.
    stage='PREVIEW_ONLY'
    reasons=['No public release/publishing operation exists in this module']
    if not author_accepted:reasons.append('Author has not accepted publication')
    if not guardian_approved:reasons.append('Guardian authorization not present')
    if not rights_reviewed:reasons.append('Independent rights review not recorded')
    if not native_reviewed:reasons.append('Japanese-language review not recorded')
    if holds:reasons.append('Unresolved structural or rights findings')
    return {'state':stage,'release_authorized':False,'distribution_performed':False,
            'consent_inputs_unverified':{'author':bool(author_accepted),'guardian':bool(guardian_approved)},
            'review_inputs_unverified':{'rights':bool(rights_reviewed),'native_language':bool(native_reviewed)},
            'reasons':reasons,'findings':report['findings']}

def derivative_preview(work_id, target, *, canonical_effect=False):
    if not isinstance(work_id,str) or not work_id:raise ContractError('work required')
    if target not in {'novel','manga','screenplay','anime','audio','game','ebook'}:raise ContractError('unknown target')
    if canonical_effect:raise ContractError('derivatives cannot change primary canon')
    return {'work_ref':work_id,'target_medium':target,'status':'DESIGN_ONLY',
            'source_canon_unchanged':True,'rights_clearance_not_assumed':True,
            'publication':False,'renderer_implemented':False}
