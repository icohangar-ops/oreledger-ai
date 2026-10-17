
import json, pathlib, sys
from .reconcile import reconcile
from .ledger import Ledger
from .extract import mode
def load_pack():
    return json.loads((pathlib.Path(__file__).parent.parent/"data"/"sample_pack.json").read_text())
def main():
    pack=load_pack(); report=reconcile(pack["pairs"])
    print(f"Mode: {mode()} (AMD endpoint not connected — TokenFactory key pending organiser)" if mode()=="fixture" else f"Mode: {mode()}")
    print(f"Documents: {pack['documents']} | Pairs checked: {report.pairs_checked} | Clean: {report.clean} | Exceptions: {len(report.exceptions)}")
    for e in report.exceptions: print(f"  [{e.kind}] {e.pair_id} {e.invoice_number} exposure=${e.exposure_usd:,.2f} — {e.detail}")
    print(f"Cash at risk: ${report.cash_at_risk_usd:,.2f}")
    led=Ledger("/tmp/oreledger-ledger.db")
    if report.exceptions:
        h=led.record(report.exceptions[0].pair_id, report.exceptions[0].invoice_number, "REQUEST_EVIDENCE", "demo-approver", "Demo decision — assay evidence requested")
        print(f"Record decision: REQUEST_EVIDENCE for {report.exceptions[0].pair_id} -> ledger hash {h[:16]}...")
    print("DEMO OK")
if __name__=="__main__": main()
