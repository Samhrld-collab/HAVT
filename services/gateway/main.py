from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(title="HAVT API Gateway")

# CORS: allow your Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] during dev
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, OPTIONS, etc.
    allow_headers=["*"],
)

SERVICES = {
    "auth": "http://localhost:8001",
    "patients": "http://localhost:8002",
    "appointments": "http://localhost:8003",
    "vitals": "http://localhost:8004",
}

@app.api_route("/api/{service}/{path:path}",
               methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def gateway(service: str, path: str, request: Request):
    # Let CORSMiddleware handle preflight automatically
    if request.method == "OPTIONS":
        return Response(status_code=200)

    if service not in SERVICES:
        return Response(f"Unknown service '{service}'", status_code=404)

    target_url = f"{SERVICES[service]}/{path}"
    async with httpx.AsyncClient() as client:
        resp = await client.request(
            method=request.method,
            url=target_url,
            headers={k: v for k, v in request.headers.items() if k.lower() != "host"},
            content=await request.body(),
        )
    return Response(
        content=resp.content,
        status_code=resp.status_code,
        headers={"content-type": resp.headers.get("content-type", "application/json")},
    )

@app.get("/")
def root():
    return {"gateway": "HAVT API Gateway", "routes": list(SERVICES.keys())}
