# OreLedger AI — Demo Script (~3 min)
1. **0:00 Problem** — A CFO pays an invoice priced at a claimed 22% grade; the independent assay says 18%. On one shipment that gap is $517,000 of metal never delivered, found weeks later in a spreadsheet.
2. **0:30 Ingest** — Load the synthetic 40-document pack (20 invoices + 20 assay certificates). Badge on screen: "Fixture mode — AMD endpoint not connected."
3. **1:00 Extraction + reconciliation** — Each pair is recomputed deterministically: payable = weight x assay grade x payable % x price. Show one clean pair auto-matched, then the queue: 17 clean, 3 exceptions.
4. **1:40 The three exceptions** — Grade shortfall ($517,000), duplicate invoice ($300,000), overbilling ($612,433.37). Cash at risk: $1,429,433.37 on this sample pack.
5. **2:20 Human decision** — Click "Record decision" / run the demo: a REQUEST_EVIDENCE decision is written to the hash-chained audit ledger. The agent never pays; a human signs.
6. **2:45 AMD path + close** — Show `.env.example` and `scripts/benchmark_rocm.py`: point `VLLM_BASE_URL` at a vLLM/ROCm endpoint on AMD Developer Cloud (or TokenFactory) and the same extraction runs on AMD. Honest note: the event TokenFactory key is pending the organiser, so today's numbers are fixture-mode and labelled as such. Buyer: CFO/controller at a junior miner or metals trader, priced per reconciled shipment.
