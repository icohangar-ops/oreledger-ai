
"""Honest benchmark harness. Fixture/CPU mode if no AMD endpoint; never fabricates AMD numbers."""
import json, time, statistics, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from oreledger.reconcile import payable_amount
from oreledger.extract import mode
pack=json.loads((pathlib.Path(__file__).parent.parent/"data"/"sample_pack.json").read_text())
times=[]
for p in pack["pairs"]:
    t0=time.perf_counter(); payable_amount(p["weight_t"],p["assay_grade_pct"],p["payable_pct"],p["price_usd_per_t_metal"]); times.append((time.perf_counter()-t0)*1000)
times.sort()
res={"mode":mode(),"note":"Fixture/CPU timing of deterministic reconciliation only. No AMD GPU numbers claimed — run on AMD Developer Cloud with VLLM_BASE_URL set for endpoint results.","docs":len(times),"p50_ms":round(statistics.median(times),4),"p95_ms":round(times[int(len(times)*0.95)-1],4)}
pathlib.Path("benchmarks/results.json").write_text(json.dumps(res,indent=2)); print(json.dumps(res,indent=2))
