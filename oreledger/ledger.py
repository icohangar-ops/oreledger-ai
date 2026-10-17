
import sqlite3, hashlib, json, datetime
class Ledger:
    def __init__(self, path="ledger.db"):
        self.db=sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS decisions(id INTEGER PRIMARY KEY, pair_id TEXT, invoice_number TEXT, decision TEXT, approver TEXT, reason TEXT, ts TEXT, prev_hash TEXT, entry_hash TEXT)")
        self.db.commit()
    def record(self, pair_id, invoice_number, decision, approver, reason):
        if decision not in ("APPROVE","REJECT","REQUEST_EVIDENCE"): raise ValueError("invalid decision")
        ts=datetime.datetime.now(datetime.timezone.utc).isoformat()
        row=self.db.execute("SELECT entry_hash FROM decisions ORDER BY id DESC LIMIT 1").fetchone()
        prev=row[0] if row else "GENESIS"
        payload=f"{pair_id}|{invoice_number}|{decision}|{approver}|{reason}|{ts}|{prev}"
        h=hashlib.sha256(payload.encode()).hexdigest()
        self.db.execute("INSERT INTO decisions(pair_id,invoice_number,decision,approver,reason,ts,prev_hash,entry_hash) VALUES (?,?,?,?,?,?,?,?)",(pair_id,invoice_number,decision,approver,reason,ts,prev,h))
        self.db.commit(); return h
    def entries(self): return self.db.execute("SELECT pair_id,invoice_number,decision,approver,reason,ts,entry_hash FROM decisions ORDER BY id").fetchall()
