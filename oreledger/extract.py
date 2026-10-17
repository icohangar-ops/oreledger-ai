
import json, os, urllib.request

REQUIRED={"supplier":str,"invoice_number":str,"metal":str,"weight_t":(int,float),"assay_grade_pct":(int,float)}

def validate_extraction(obj):
    if not isinstance(obj, dict): raise ValueError("extraction is not a JSON object")
    for k,t in REQUIRED.items():
        if k not in obj or not isinstance(obj[k], t): raise ValueError(f"missing/invalid field: {k}")
    return obj

def mode():
    if os.getenv("VLLM_BASE_URL") or os.getenv("AMD_TOKENFACTORY_BASE_URL"): return "amd-endpoint"
    return "fixture"

def extract_from_fixture(pair): return validate_extraction(pair)

def extract_via_amd(text):
    """OpenAI-compatible call to a vLLM/ROCm or TokenFactory endpoint. Key from env only, never committed."""
    base=os.getenv("VLLM_BASE_URL") or os.getenv("AMD_TOKENFACTORY_BASE_URL")
    if not base: raise RuntimeError("No AMD endpoint configured (set VLLM_BASE_URL or AMD_TOKENFACTORY_BASE_URL)")
    key=os.getenv("AMD_API_KEY","")
    model=os.getenv("MODEL_NAME","Qwen/Qwen2.5-7B-Instruct")
    prompt="Extract supplier, invoice_number, metal, weight_t, assay_grade_pct as JSON only from:\n"+text
    body=json.dumps({"model":model,"messages":[{"role":"user","content":prompt}],"temperature":0}).encode()
    req=urllib.request.Request(base.rstrip("/")+"/chat/completions", data=body, headers={"Content-Type":"application/json", **({"Authorization":f"Bearer {key}"} if key else {})})
    with urllib.request.urlopen(req, timeout=60) as r: data=json.loads(r.read())
    return validate_extraction(json.loads(data["choices"][0]["message"]["content"]))
