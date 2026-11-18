from app.modules.consumption.rules import replay

def test_fefo_allocation_real(sample):
    spend=next(x for x in sample['point_ledger']['spends'] if x['id']=='S1');assert [(x['lot'],x['points']) for x in spend['allocations']]==[('E1',100),('E2',20)]
def test_no_partial_on_failure(sample):
    assert next(x for x in sample['quarantine'] if x['id']=='BAD2')['code']=='INSUFFICIENT_POINTS';assert next(x for x in sample['archive']['balances'] if x['member']=='00002')['remaining']==70
def test_late_refund_then_spend(sample):
    assert next(x for x in sample['archive']['balances'] if x['member']=='00001')['remaining']==30
def test_spend_at_expiry_exclusive(clean):
    rows=[dict(clean['records'][0]),dict(clean['records'][2],at='2026-10-31T16:00:00+00:00',points=1)];lots=[x for x in clean['lots'] if x['id']=='E1'];r=replay(rows,lots,clean['context']['as_of']);assert r['spends']==[];assert r['expired']==100
def test_future_earn_not_spendable(clean):
    row=dict(clean['records'][2],at='2026-09-01T00:00:00+00:00',points=1);r=replay([row,clean['records'][0]],[clean['lots'][0]],clean['context']['as_of']);assert r['errors'][0][1]=='INSUFFICIENT_POINTS'
def test_order_invariant_replay(clean):
    a=replay(clean['records'],clean['lots'],clean['context']['as_of']);b=replay(list(reversed(clean['records'])),clean['lots'],clean['context']['as_of']);assert a==b
def test_zero_left_after_full_spend(clean):
    rows=[clean['records'][0],dict(clean['records'][2],points=100)];r=replay(rows,[clean['lots'][0]],clean['context']['as_of']);assert r['lots'][0]['remaining']==0;assert r['spends'][0]['points']==100
