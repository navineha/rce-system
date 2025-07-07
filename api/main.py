from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from redis import Redis
import uuid, json

app = FastAPI()
redis = Redis(host="localhost", port=6379, db=0)

# 🛡️ CORS fix
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "RCE API is alive!"}

@app.post("/run")
async def run_code(request: Request):
    body = await request.json()
    code = body["code"]
    lang = body["language"]

    job_id = str(uuid.uuid4())
    job_data = {
        "id": job_id,
        "code": code,
        "language": lang
    }

    redis.rpush("code_queue", json.dumps(job_data))
    return {"job_id": job_id, "status": "queued"}

@app.get("/result/{job_id}")
def get_result(job_id: str):
    output = redis.get(job_id)
    if output:
        return {"job_id": job_id, "output": output.decode("utf-8")}
    else:
        return {"job_id": job_id, "status": "pending"}
