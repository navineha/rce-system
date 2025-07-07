import json, tempfile
from redis import Redis
import docker

# ── Redis & Docker ─────────────────────────────────────────────
redis  = Redis(host="localhost", port=6379, db=0)
client = docker.from_env()

print("🚀 Worker started. Listening on 'code_queue' …")

while True:
    # wait up to 10 s for a job
    result = redis.blpop("code_queue", timeout=10)
    if result is None:
        continue                     # queue empty → keep waiting

    _, job_data = result
    print(f"📨 Raw job_data: {job_data}")

    job = json.loads(job_data)
    print(f"🧾 Code received:\n{job['code']}")

    job_id   = job["id"]
    code     = job["code"]
    language = job["language"]

    if language != "python":
        redis.set(job_id, f"Error: unsupported language '{language}'")
        continue

    # write code into a temp file inside /tmp
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", dir="/tmp") as tmp:
        tmp.write(code.encode("utf-8"))
        tmp_file_path = tmp.name

    try:
        container = client.containers.run(
            image="python:3.10",
            command=f"python -u {tmp_file_path}",
            volumes={"/tmp": {"bind": "/tmp", "mode": "ro"}},
            network_disabled=True,
            mem_limit="128m",
            stderr=True,
            stdout=True,
            detach=True
            
        )
        exit_code = container.wait(timeout=10)["StatusCode"]
        logs = container.logs(stdout=True, stderr=True).decode("utf-8")

        print(f"📦 Output for {job_id}:\n{logs}")

        if exit_code == 0:
            redis.set(job_id, logs or "[no output]")
            container.remove(force=True)
        else:
            redis.set(job_id, f"[Error] Exit Code {exit_code}\n{logs or '[no logs]'}")
            container.remove(force=True)


    except Exception as e:
        err = f"Runtime error: {e}"
        redis.set(job_id, err)
        print(f"💥 {job_id}: {err}")
