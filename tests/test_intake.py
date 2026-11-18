from app.engine import evaluate
from app.errors import BusinessError
from app.config import ROOT
import pytest

def test_bom_real(sample):
    # TRAP-02
    assert sample['records'][0]['id']=='E1'
def test_gb18030_real():
    # TRAP-01
    s=evaluate({'dataset':'legacy'});assert s['encoding']=='gb18030';assert s['records'][0]['rule']=='常规'
def test_member_leading_zero(sample):
    # TRAP-08
    assert sample['records'][0]['member']=='00001'
def test_repeated_header(sample):
    # TRAP-04
    assert sample['counts']['repeated_header']==1
def test_column_bad(sample):
    # TRAP-05
    assert next(x for x in sample['quarantine'] if x['id']=='BADCOL')['code']=='COLUMN_COUNT'
def test_duplicate_conflict(sample):
    # TRAP-14
    assert len([x for x in sample['quarantine'] if x['code']=='DUPLICATE_CONFLICT'])==2
def test_empty_three():
    # TRAP-18
    for text,code in [('', 'EMPTY_FILE'),('\n\n','BLANK_FILE'),((ROOT/'sample_data/clean.csv').read_text().splitlines()[0]+'\n','HEADER_ONLY')]:
        with pytest.raises(BusinessError) as e:evaluate({'csv_text':text})
        assert e.value.code==code
