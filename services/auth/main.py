from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import sqlite3
from services.common.security import make_token

app = FastAPI(title="Auth Service")
DB = "auth.db"
conn = sqlite3.connect(DB, check_same_thread=False)
conn.execute("""CREATE TABLE IF NOT EXISTS users(
                                                    id INTEGER PRIMARY KEY, email TEXT UNIQUE, password TEXT)""")

class Creds(BaseModel):
    email: EmailStr
    password: str

@app.post("/register")
def register(c: Creds):
    try:
        conn.execute("INSERT INTO users(email,password) VALUES(?,?)", (c.email, c.password))
        conn.commit()
        return {"ok": True}
    except sqlite3.IntegrityError:
        raise HTTPException(409, "Email exists")

@app.post("/login")
def login(c: Creds):
    cur = conn.execute("SELECT id FROM users WHERE email=? AND password=?", (c.email, c.password))
    row = cur.fetchone()
    if not row:
        raise HTTPException(401, "Bad credentials")
    return {"access_token": make_token(str(row[0]))}
