# OreLedger AI — Assay & Invoice Auditor

For AMD Developer Hackathon: ACT III (lablab) · Track: Intelligent Industry · Team Cubiczan (solo)

OreLedger helps a small critical-minerals buyer's CFO office stop paying for metal that was never delivered. It pairs supplier invoices with independent assay certificates, extracts the payable terms, recomputes what should be paid with deterministic math, and routes only the exceptions — overbilling, grade shortfall, duplicate invoice — to a human approver with a signed audit ledger. **The agent never pays and never emails a supplier.**

## Honest status (read first)
- **Fixture mode is the default and is clearly badged.** The AMD TokenFactory key has not yet been issued to this entrant ("Your email is not registered for API key distribution" at notebooks.amd.com/tokenfactory); the organiser has been asked to add the login email. No AMD GPU numbers are claimed anywhere in this repo.
- **AMD path is built and configurable, not faked:** set `VLLM_BASE_URL` (your own vLLM/ROCm endpoint on AMD Developer Cloud) or `AMD_TOKENFACTORY_BASE_URL` + `AMD_API_KEY` + `MODEL_NAME` in `.env` (see `.env.example`) and extraction calls that OpenAI-compatible endpoint. `scripts/benchmark_rocm.py` runs the real reconciliation workload and reports measured timings for whichever mode is active — in fixture mode it says so.
- All data is **synthetic** (`data/sample_pack.json`: 20 invoice + 20 assay documents = 40 documents, with ground truth). No real company data, no PII, no API keys in git.

## Quick start (no GPU, no network)
```bash
python -m oreledger.demo        # CLI cash-at-risk desk
python -m pytest tests/ -q      # test suite (use a venv: pip install -r requirements.txt)
streamlit run app.py            # optional UI (requires streamlit)
python scripts/benchmark_rocm.py
```

## Sample result (fixture pack, real output of the demo)
- 20 pairs checked · 17 clean · 3 exceptions
- GRADE_SHORTFALL, DUPLICATE_INVOICE, OVERBILLING
- **Cash at risk: $1,429,433.37** (sum of the three exception exposures on the synthetic pack — sample data, not a customer claim)

## How it works
1. **Extract** — fixture extractor, or an open model (Qwen2.5/Qwen3-Instruct class) served on AMD via vLLM/ROCm / TokenFactory, returning schema-validated JSON (`oreledger/extract.py`). Malformed model JSON is rejected.
2. **Reconcile (deterministic, not LLM)** — payable = weight × assay grade × payable % × price; tolerance ±0.5pp grade, ±1% amount; duplicate-invoice detection (`oreledger/reconcile.py`).
3. **Human ledger** — approve / reject / request-evidence per exception, written to an append-only, hash-chained SQLite ledger (`oreledger/ledger.py`).

## Tests
Reconciliation math incl. tolerance edges, duplicate detection, schema validation rejecting malformed JSON, ledger append, and the full fixture pack (17 clean / 3 exceptions / $1,429,433.37 at risk).

MIT licensed. Built for the AMD Developer Hackathon ACT III; AMD, ROCm and vLLM are the intended production extraction path once the event key is issued.
