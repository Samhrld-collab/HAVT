from fastapi import FastAPI, Depends
from pydantic import BaseModel
import sqlite3
from services.common.security import get_user

app=FastAPI(title="Patients Service")
DB="patients.db"
conn=sqlite3.connect(DB, check_same_thread=False)
conn.execute("""CREATE TABLE IF NOT EXISTS patients(
 id INTEGER PRIMARY KEY, user_id TEXT UNIQUE, full_name TEXT, dob TEXT)""")

class PatientIn(BaseModel):
    full_name:str
    dob:str

@app.get("/me")
def get_me(user=Depends(get_user)):
    cur=conn.execute("SELECT id,user_id,full_name,dob FROM patients WHERE user_id=?",(user,))
    r=cur.fetchone()
    return None if not r else {"id":r[0],"user_id":r[1],"full_name":r[2],"dob":r[3]}

@app.post("/me")
def upsert_me(p:PatientIn, user=Depends(get_user)):
    conn.execute("""INSERT INTO patients(user_id,full_name,dob) VALUES(?,?,?)
        ON CONFLICT(user_id) DO UPDATE SET full_name=excluded.full_name,dob=excluded.dob""",
        (user,p.full_name,p.dob))
    conn.commit()
    return {"ok":True}
