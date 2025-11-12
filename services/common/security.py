from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
import jwt, time

bearer = HTTPBearer()
SECRET = "dev-secret"  # replace for production

def make_token(sub: str):
    return jwt.encode({"sub": sub, "exp": int(time.time()) + 3600}, SECRET, algorithm="HS256")

def get_user(token=Depends(bearer)):
    try:
        data = jwt.decode(token.credentials, SECRET, algorithms=["HS256"])
        return data["sub"]
    except Exception:
        raise HTTPException(401, "Invalid token")
