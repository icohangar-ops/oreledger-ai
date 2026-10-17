# lablab Submission Copy — OreLedger AI (AMD Developer Hackathon: ACT III)
Status: DRAFT — not submitted. Participation: Online. Track: Intelligent Industry.

**Title (38 chars):** OreLedger AI — Assay & Invoice Auditor

**Short description:** OreLedger pairs supplier invoices with independent assay certificates, recomputes payable metal deterministically, and routes only overbilling, grade-shortfall and duplicate exceptions to a human-signed audit ledger.

**Long description:** A small critical-minerals buyer can pay for metal that was never delivered: a supplier invoice priced at a claimed 22% grade, while the independent assay certificate says 18%, is a $517,000 gap on one shipment, usually found weeks later in a spreadsheet. OreLedger AI ingests invoice and assay-certificate pairs, extracts supplier, invoice number, metal, weight, grade and price terms with an open model on the intended AMD path (vLLM/ROCm on AMD Developer Cloud, or the event TokenFactory API, both OpenAI-compatible and configured by environment variables), then recomputes the payable amount deterministically — payable = weight x assay grade x payable % x price — within ±0.5pp grade and ±1% amount tolerances, with duplicate-invoice detection. Clean pairs auto-match; only exceptions reach a human, who approves, rejects, or requests evidence, with every decision written to an append-only, hash-chained audit ledger. The agent never pays and never emails a supplier. In the committed synthetic 40-document pack (20 invoices + 20 assays, ground truth included), 17 pairs match clean and 3 exceptions carry $1,429,433.37 of cash at risk: grade shortfall $517,000, duplicate $300,000, overbilling $612,433.37 (sample data, not a customer claim). Honest status: the TokenFactory key is pending the organiser ("email not registered for API key distribution"), so the judge-ready demo runs in clearly badged fixture mode today, with the AMD endpoint and benchmark harness ready to point at AMD the moment the key is issued; no GPU benchmark numbers are claimed. Buyer: CFO/controller at a junior miner or metals trader, priced per reconciled shipment. Public MIT repo, 5 pytest tests passing, CLI and Streamlit demos.

**Tags:** AMD Developer Cloud, AMD ROCm, vLLM, Qwen2.5, Python, Streamlit, Intelligent Industry, critical minerals, invoice reconciliation

**Cover image:** ../oreledger-video/thumbnail.png (1280x720)
**Demo video:** ../oreledger-video/demo.mp4 (178s, 1280x720) — YouTube upload still needed by submitter (not uploaded)
**Pitch deck:** ../oreledger-video/pitch-deck.pdf (9 slides)
**GitHub (public):** https://github.com/icohangar-ops/oreledger-ai
**App URL:** ⚠️ STILL NEEDED — no hosted URL yet. Judges can run locally: `python -m oreledger.demo` (no GPU/network) or `streamlit run app.py`. Hosting (HF Spaces/Streamlit Cloud) should be added before submitting.
**Participation:** Online
