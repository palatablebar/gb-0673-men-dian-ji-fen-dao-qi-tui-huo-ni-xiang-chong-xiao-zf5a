from app.modules.policy.rules import normalize
from app.errors import BusinessError
import pytest

def test_rule_real(sample):
    assert sample['records'][0]['rule']=='常规'
def test_sentinel_real(sample):
    # TRAP-07
    assert next(x for x in sample['quarantine'] if x['id']=='BAD1')['code']=='MISSING_VALUE'
def test_utc_real(sample):
    # TRAP-11
    assert sample['records'][0]['at']=='2026-10-01T01:00:00+00:00'
def test_fullwidth_points(clean):
    # TRAP-06
    assert normalize(dict(clean['records'][0],points='１,０００'),clean['context'])['points']==1000
def test_fraction_refused(clean):
    with pytest.raises(BusinessError):normalize(dict(clean['records'][0],points='1.2'),clean['context'])
def test_rule_end_exclusive(clean):
    # TRAP-23
    with pytest.raises(BusinessError) as e:normalize(dict(clean['records'][0],at='2027-01-01T00:00:00+08:00'),clean['context'])
    assert e.value.code=='RULE_EXPIRED'
def test_unknown_rule(clean):
    with pytest.raises(BusinessError):normalize(dict(clean['records'][0],rule='不存在'),clean['context'])
