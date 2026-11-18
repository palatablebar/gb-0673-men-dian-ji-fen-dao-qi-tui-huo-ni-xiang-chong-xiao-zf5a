from app.modules.archive.rules import decide
from app.archive import serialize
from copy import deepcopy
import zipfile,io,json

def test_ready_real(sample):
    assert sample['archive']['status']=='可归档'
def test_members_real(sample):
    assert sample['archive']['members']==15
def test_member_balance_real(sample):
    assert sample['archive']['balances'][0]=={'member':'00001','remaining':30}
def test_bad_point_balance_blocks(sample):
    s=deepcopy(sample);s['balance']['points_balanced']=False;assert decide(s)['status']=='待复核'
def test_refund_audit_blocks(sample):
    s=deepcopy(sample);s['refund_issues']=['R1'];assert decide(s)['status']=='待复核'
def test_bundle_contains_failed_events(sample):
    z=zipfile.ZipFile(io.BytesIO(serialize(sample)));e=json.loads(z.read('evidence.json'));assert len(e['quarantine'])==7
def test_archive_seal_changes(sample):
    s=deepcopy(sample);s['point_ledger']['lots'][0]['remaining']+=1;assert decide(s)['seal']!=sample['archive']['seal']
