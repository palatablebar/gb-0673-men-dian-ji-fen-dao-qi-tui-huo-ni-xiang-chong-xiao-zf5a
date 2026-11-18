from app.modules.refund.rules import audit_refunds
from app.modules.consumption.rules import replay
from copy import deepcopy

def test_expired_not_revived(sample):
    r=next(x for x in sample['refund_audit'] if x['id']=='R1');assert r['restored']==20;assert r['expired_refund']==10
def test_refund_cap_real(sample):
    assert next(x for x in sample['quarantine'] if x['id']=='BAD3')['code']=='REFUND_CAP'
def test_other_member_refused(sample):
    assert next(x for x in sample['quarantine'] if x['id']=='BAD4')['code']=='REFUND_REFERENCE'
def test_reverse_allocation(sample):
    r=next(x for x in sample['point_ledger']['refunds'] if x['id']=='R1');assert [(x['lot'],x['points']) for x in r['allocations']]==[('E2',20),('E1',10)]
def test_audit_tamper_detected(sample):
    l=deepcopy(sample['point_ledger']);l['refunds'][0]['restored']=11;rows,issues=audit_refunds(l);assert len(issues)==1
def test_cumulative_partial_refund_cap(clean):
    rows=[dict(x) for x in clean['records'] if x['member']=='00001'];rows.append(dict(rows[3],id='R-extra',points=100,at='2026-11-02T12:00:00+00:00'));r=replay(rows,[x for x in clean['lots'] if x['member']=='00001'],clean['context']['as_of']);assert r['errors'][-1][1]=='REFUND_CAP'
def test_all_verified_real(sample):
    assert len(sample['refund_audit'])==15;assert sample['refund_issues']==[]
