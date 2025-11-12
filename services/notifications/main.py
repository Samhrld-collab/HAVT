from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI(title="Notifications Service")
class Event(BaseModel):
    type:str
    appointmentId:int

@app.post("/events")
def ingest(e:Event):
    # In real life publish to queue/SMTP/SMS. For demo, just log.
    print(f"[NOTIFY] {e.type} for appointment #{e.appointmentId}")
    return {"accepted":True}
