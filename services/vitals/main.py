from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import sqlite3
from services.common.security import get_user
from datetime import datetime

app = FastAPI(title="Vitals Service")

DB = "vitals.db"
conn = sqlite3.connect(DB, check_same_thread=False)
conn.execute("""
             CREATE TABLE IF NOT EXISTS vitals(
                                                  id INTEGER PRIMARY KEY,
                                                  user_id TEXT,
                                                  temp REAL,
                                                  pulse INTEGER,
                                                  oxygen REAL,
                                                  recorded_at TEXT
             )
             """)

class VitalIn(BaseModel):
    temp: float
    pulse: int
    oxygen: float

@app.post("/vitals")
def record_vitals(v: VitalIn, user=Depends(get_user)):
    conn.execute(
        "INSERT INTO vitals(user_id,temp,pulse,oxygen,recorded_at) VALUES(?,?,?,?,?)",
        (user, v.temp, v.pulse, v.oxygen, datetime.now().isoformat())
    )
    conn.commit()
    return {"ok": True}

@app.get("/vitals")
def list_vitals(user=Depends(get_user)):
    cur = conn.execute(
        "SELECT temp,pulse,oxygen,recorded_at FROM vitals WHERE user_id=? ORDER BY id DESC",
        (user,)
    )
    return [
        {"temp": t, "pulse": p, "oxygen": o, "when": w}
        for (t, p, o, w) in cur.fetchall()
    ]
