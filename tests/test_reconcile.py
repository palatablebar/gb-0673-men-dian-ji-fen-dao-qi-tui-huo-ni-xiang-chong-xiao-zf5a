from app.modules.reconcile.rules import reconcile
from copy import deepcopy

def test_rows_balanced(sample):
    assert sample['balance']['input']==57;assert sample['balance']['accepted']==47;assert sample['balance']['quarantined']==7;assert sample['balance']['row_balanced']
def test_points_conservation(sample):
    b=sample['balance'];assert b['issued']==1580;assert b['remaining']==1010;assert b['points_balanced']
def test_expiry_count(sample):
    assert sample['balance']['expired']==10
def test_credits_exact(sample):
    assert sample['balance']['spent']==730;assert sample['balance']['refunded']==170
def test_balance_tamper(sample):
    s=deepcopy(sample);s['point_ledger']['lots'][0]['remaining']+=1;assert reconcile(s)['points_balanced'] is False
def test_row_tamper(sample):
    s=deepcopy(sample);s['counts']['input']+=1;assert reconcile(s)['row_balanced'] is False
def test_clean_no_isolation(clean):
    assert clean['balance']['quarantined']==0;assert clean['balance']['points_balanced']
