"""OreLedger AI — Streamlit Community Cloud entry point.

Run locally:  streamlit run streamlit_app.py
Cloud:        repo icohangar-ops/oreledger-ai, branch main, main file streamlit_app.py

Fixture-mode demo by default. No secrets required. If AMD endpoint env vars
(VLLM_BASE_URL or AMD_TOKENFACTORY_BASE_URL / AMD_API_KEY / MODEL_NAME) are
present in Streamlit secrets / environment, the status badge reflects that;
no keys are committed to this repo.
"""
import json
import os
import pathlib
import tempfile

import streamlit as st

from oreledger.reconcile import reconcile
from oreledger.ledger import Ledger
from oreledger.extract import mode


def main():
    st.set_page_config(page_title="OreLedger AI", layout="wide")
    st.title("OreLedger AI \u2014 Assay & Invoice Auditor")

    if mode() == "fixture":
        st.warning(
            "Fixture mode \u2014 AMD endpoint not connected (TokenFactory key pending "
            "organiser). Synthetic data only."
        )
    else:
        st.success(f"AMD endpoint mode: {mode()}")

    root = pathlib.Path(__file__).parent
    pack = json.loads((root / "data" / "sample_pack.json").read_text())
    report = reconcile(pack["pairs"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Documents", pack.get("documents", len(pack["pairs"]) * 2))
    c2.metric("Pairs checked", report.pairs_checked)
    c3.metric("Clean", report.clean)
    c4.metric("Cash at risk", f"${report.cash_at_risk_usd:,.2f}")

    st.subheader("Exception queue \u2014 agent never pays, a human signs")
    # Streamlit Cloud's app directory may be read-only / ephemeral, so keep the
    # demo ledger in the OS temp dir (matches oreledger.demo's /tmp behaviour).
    ledger_path = os.path.join(tempfile.gettempdir(), "oreledger_ledger.db")
    led = Ledger(ledger_path)

    if not report.exceptions:
        st.info("No exceptions in this pack.")
    for e in report.exceptions:
        st.write(
            f"**{e.kind}** \u00b7 {e.pair_id} \u00b7 {e.invoice_number} \u00b7 "
            f"exposure ${e.exposure_usd:,.2f} \u2014 {e.detail}"
        )
        col1, _col2 = st.columns(2)
        if col1.button(
            f"Record decision: Request evidence ({e.pair_id})", key=f"req-{e.pair_id}"
        ):
            h = led.record(
                e.pair_id,
                e.invoice_number,
                "REQUEST_EVIDENCE",
                "approver",
                "Requested assay evidence from UI",
            )
            st.success(f"Ledger entry {h[:16]}...")

    st.subheader("Audit ledger")
    entries = led.entries()
    if entries:
        st.dataframe(
            entries,
            column_config={
                0: "Pair",
                1: "Invoice",
                2: "Decision",
                3: "Approver",
                4: "Reason",
                5: "Timestamp (UTC)",
                6: "Entry hash",
            },
            hide_index=True,
        )
    else:
        st.write("No decisions recorded yet in this session. Use a button above.")

    st.caption(
        "Synthetic fixture pack: 20 invoice + 20 assay documents. "
        "Deterministic reconciliation (not LLM math): payable = weight \u00d7 assay "
        "grade \u00d7 payable % \u00d7 price. The agent never pays and never emails a supplier."
    )


if __name__ == "__main__":
    main()
