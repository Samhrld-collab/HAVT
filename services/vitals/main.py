from fastapi import FastAPI, Depends
from pydantic import BaseModel, conint, confloat
import sqlite3
from services.common.security import get_user

app=FastAPI(title="Vitals Service")
DB="vitals.db"
conn=sqlite3.connect(DB, check_same_thread=False)
conn.execute("""CREATE TABLE IF NOT EXISTS vitals(
 id INTEGER PRIMARY KEY, appointment_id INT, temperature REAL, spo2 INT, note TEXT)""")

class VitalsIn(BaseModel):
    appointment_id:int
    temperature: confloat(ge=34, le=43)
    spo2: conint(ge=70, le=100)
    note:str=""

@app.post("/vitals")
def record(v:VitalsIn, user=Depends(get_user)):
    conn.execute("INSERT INTO vitals(appointment_id,temperature,spo2,note) VALUES(?,?,?,?)",
                 (v.appointment_id,v.temperature,v.spo2,v.note))
    conn.commit()
    return {"ok":True}

@app.get("/vitals/{appointment_id}")
def get_vitals(appointment_id:int, user=Depends(get_user)):
    cur=conn.execute("SELECT id,temperature,spo2,note FROM vitals WHERE appointment_id=?",(appointment_id,))
    return [{"id":i,"temperature":t,"spo2":s,"note":n} for (i,t,s,n) in cur.fetchall()]
