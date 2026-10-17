
import json, pathlib
from oreledger.reconcile import payable_amount, reconcile
from oreledger.extract import validate_extraction
from oreledger.ledger import Ledger
def pack(): return json.loads((pathlib.Path(__file__).parent.parent/"data"/"sample_pack.json").read_text())["pairs"]
def test_payable_math(): assert payable_amount(1000,25,80,10000)==2000000.0
def test_pack_exceptions():
    r=reconcile(pack()); assert r.pairs_checked==20; assert r.clean==17; assert len(r.exceptions)==3
    assert {e.kind for e in r.exceptions}=={"GRADE_SHORTFALL","DUPLICATE_INVOICE","OVERBILLING"}
    assert r.cash_at_risk_usd==1429433.37
def test_tolerance_edge():
    p=[{"pair_id":"X","invoice_number":"I1","weight_t":100,"claimed_grade_pct":10,"assay_grade_pct":10,"payable_pct":100,"price_usd_per_t_metal":1000,"invoiced_amount_usd":10050.0}]
    assert reconcile(p).clean==1  # within 1%
def test_schema_rejects_bad(): 
    try: validate_extraction({"supplier":1}); assert False
    except ValueError: pass
def test_ledger_append(tmp_path):
    led=Ledger(str(tmp_path/"l.db")); h=led.record("OL-001","INV-1","APPROVE","alice","ok"); assert len(h)==64; assert len(led.entries())==1
