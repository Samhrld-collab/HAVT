from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import sqlite3, requests
from services.common.security import get_user

app = FastAPI(title="Appointments Service")

DB = "appointments.db"
conn = sqlite3.connect(DB, check_same_thread=False)

# ---- Database setup ----
conn.execute("""CREATE TABLE IF NOT EXISTS clinicians(
                                                         id INTEGER PRIMARY KEY,
                                                         name TEXT
                )""")

conn.execute("""CREATE TABLE IF NOT EXISTS slots(
                                                    id INTEGER PRIMARY KEY,
                                                    clinician_id INT,
                                                    slot_time TEXT,
                                                    taken INT DEFAULT 0
                )""")

conn.execute("""CREATE TABLE IF NOT EXISTS appointments(
                                                           id INTEGER PRIMARY KEY,
                                                           user_id TEXT,
                                                           slot_id INT,
                                                           status TEXT
                )""")

# ---- Seed one clinician and a couple of slots ----
if not conn.execute("SELECT 1 FROM clinicians").fetchone():
    conn.execute("INSERT INTO clinicians(name) VALUES('Dr. Alice')")
    for t in ["2025-11-13 10:00", "2025-11-13 10:30"]:
        conn.execute("INSERT INTO slots(clinician_id, slot_time, taken) VALUES(1, ?, 0)", (t,))
    conn.commit()

# ---- Pydantic model ----
class BookIn(BaseModel):
    slot_id: int

# ---- Routes ----
@app.get("/slots")
def slots():
    cur = conn.execute("""
                       SELECT s.id, s.slot_time, c.name
                       FROM slots s
                                JOIN clinicians c ON c.id = s.clinician_id
                       WHERE s.taken = 0
                       """)
    # still return key "when" for frontend compatibility
    return [{"id": i, "when": w, "clinician_name": n} for (i, w, n) in cur.fetchall()]


@app.post("/appointments")
def book(b: BookIn, user=Depends(get_user)):
    cur = conn.execute("SELECT taken FROM slots WHERE id=?", (b.slot_id,))
    row = cur.fetchone()
    if not row:
        raise HTTPException(404, "slot not found")
    if row[0]:
        raise HTTPException(409, "slot already taken")

    conn.execute("UPDATE slots SET taken=1 WHERE id=?", (b.slot_id,))
    conn.execute(
        "INSERT INTO appointments(user_id, slot_id, status) VALUES(?, ?, ?)",
        (user, b.slot_id, "Confirmed"),
    )
    appt_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.commit()

    # fire-and-forget notification (optional)
    try:
        requests.post("http://localhost:8005/events", json={"type": "Booked", "appointmentId": appt_id})
    except Exception:
        pass

    return {"id": appt_id, "status": "Confirmed"}

@app.get("/my")
def my_appointments(user=Depends(get_user)):
    cur = conn.execute("""
                       SELECT a.id, s.slot_time, c.name, a.status
                       FROM appointments a
                                JOIN slots s ON s.id = a.slot_id
                                JOIN clinicians c ON c.id = s.clinician_id
                       WHERE a.user_id = ?
                       """, (user,))
    return [{"id": i, "when": w, "clinician_name": n, "status": s}
            for (i, w, n, s) in cur.fetchall()]

