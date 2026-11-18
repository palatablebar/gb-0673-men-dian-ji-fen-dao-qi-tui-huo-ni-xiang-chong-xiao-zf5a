from app.modules.lots.rules import build_lots

def test_issued_batches(sample):
    assert len(sample['lots'])==16
def test_issued_amount(sample):
    assert sum(x['issued'] for x in sample['lots'])==1580
def test_fefo_real(sample):
    assert [x['id'] for x in sample['lots'] if x['member']=='00001']==['E1','E2']
def test_expiry_equal_start(clean):
    row=dict(clean['records'][0],expires=clean['records'][0]['at']);lots,bad=build_lots([row]);assert lots==[];assert bad[0][1]=='INVALID_EXPIRY'
def test_timezone_equivalence(clean):
    row=dict(clean['records'][0],expires='2026-10-31T16:00:00Z');lots,bad=build_lots([row]);assert lots[0]['expires']=='2026-10-31T16:00:00+00:00'
def test_spend_not_lot(clean):
    assert build_lots([clean['records'][2]])==([],[])
def test_lots_order_invariant(clean):
    assert build_lots(clean['records'])==build_lots(list(reversed(clean['records'])))
