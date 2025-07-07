# 💻 Remote Code Execution System 🧠✨
An advanced, secure and girly-themed RCE system that lets you run Python, Java, and C++ code via a web interface — built from scratch with Docker, FastAPI, Redis, and pure frontend tech.

![demo](https://user-images.githubusercontent.com/your-image-link.gif)

---

### ⚙️ Tech Stack

- 🐍 Backend: Python (FastAPI)
- 🧠 Redis for job queue
- 🌐 Frontend: HTML, CSS, JavaScript (Vanilla)


---

### 🚀 How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/navineha/rce-system.git
cd rce-system

# 2. Install requirements
cd api
source venv/bin/activate
pip install -r requirements.txt

# 3. Start the API server
uvicorn main:app --reload --port 8000

# 4. In another terminal, run the worker
cd worker
source venv/bin/activate
python3 worker.py

# 5. Open frontend/index.html in your browser
