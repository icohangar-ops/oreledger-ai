
"""Streamlit UI: streamlit run app.py  (core logic is UI-independent and tested without Streamlit)."""
import json, pathlib
try:
    import streamlit as st
except ImportError:
    raise SystemExit("Streamlit not installed. Run the CLI demo instead: python -m oreledger.demo")
from oreledger.reconcile import reconcile
from oreledger.ledger import Ledger
from oreledger.extract import mode
st.set_page_config(page_title="OreLedger AI", layout="wide")
st.title("OreLedger AI — Assay & Invoice Auditor")
st.warning("Fixture mode — AMD endpoint not connected (TokenFactory key pending organiser). Synthetic data only.") if mode()=="fixture" else st.success(f"AMD endpoint mode: {mode()}")
pack=json.loads((pathlib.Path(__file__).parent/"data"/"sample_pack.json").read_text())
report=reconcile(pack["pairs"])
c1,c2,c3=st.columns(3); c1.metric("Pairs checked", report.pairs_checked); c2.metric("Clean", report.clean); c3.metric("Cash at risk", f"${report.cash_at_risk_usd:,.2f}")
st.subheader("Exception queue — agent never pays, a human signs")
led=Ledger("ledger.db")
for e in report.exceptions:
    st.write(f"**{e.kind}** · {e.pair_id} · {e.invoice_number} · exposure ${e.exposure_usd:,.2f} — {e.detail}")
    col1,col2=st.columns(2)
    if col1.button(f"Record decision: Request evidence ({e.pair_id})", key=e.pair_id):
        h=led.record(e.pair_id, e.invoice_number, "REQUEST_EVIDENCE", "approver", "Requested assay evidence from UI"); st.success(f"Ledger entry {h[:16]}...")
st.subheader("Audit ledger"); st.write(led.entries())
