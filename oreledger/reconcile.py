
from dataclasses import dataclass, field
GRADE_TOL_PP=0.5
AMOUNT_TOL_FRAC=0.01

def payable_amount(weight_t, assay_grade_pct, payable_pct, price_usd_per_t):
    """Deterministic payable math — never LLM-generated."""
    return round(weight_t * (assay_grade_pct/100.0) * (payable_pct/100.0) * price_usd_per_t, 2)

@dataclass
class Exception:
    pair_id: str; invoice_number: str; kind: str; exposure_usd: float; detail: str

@dataclass
class Report:
    pairs_checked: int; clean: int; exceptions: list = field(default_factory=list)
    @property
    def cash_at_risk_usd(self): return round(sum(e.exposure_usd for e in self.exceptions),2)

def reconcile(pairs):
    seen={}; exceptions=[]; clean=0
    for p in pairs:
        computed=payable_amount(p["weight_t"], p["assay_grade_pct"], p["payable_pct"], p["price_usd_per_t_metal"])
        invoiced=float(p["invoiced_amount_usd"])
        if p["invoice_number"] in seen:
            exceptions.append(Exception(p["pair_id"], p["invoice_number"], "DUPLICATE_INVOICE", round(invoiced,2),
                f"Invoice number already seen on {seen[p['invoice_number']]}; duplicate payable amount at risk."))
            continue
        seen[p["invoice_number"]]=p["pair_id"]
        grade_diff=float(p["claimed_grade_pct"])-float(p["assay_grade_pct"])
        if grade_diff > GRADE_TOL_PP:
            exceptions.append(Exception(p["pair_id"], p["invoice_number"], "GRADE_SHORTFALL", round(max(invoiced-computed,0.0),2),
                f"Claimed grade {p['claimed_grade_pct']}% vs assay {p['assay_grade_pct']}% (diff {grade_diff:.2f}pp > {GRADE_TOL_PP}pp). Payable on assay = ${computed:,.2f}, invoiced = ${invoiced:,.2f}."))
            continue
        if computed and abs(invoiced-computed)/computed > AMOUNT_TOL_FRAC and invoiced>computed:
            exceptions.append(Exception(p["pair_id"], p["invoice_number"], "OVERBILLING", round(invoiced-computed,2),
                f"Invoiced ${invoiced:,.2f} exceeds assay-based payable ${computed:,.2f} by more than {AMOUNT_TOL_FRAC:.0%} tolerance."))
            continue
        clean+=1
    return Report(pairs_checked=len(pairs), clean=clean, exceptions=exceptions)
