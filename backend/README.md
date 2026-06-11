# Backend - Skeleton Services

This folder will host FastAPI services for orchestration and light-weight AI prototypes. Heavy inference engines (Rust/CUDA) will be placed under `services/` or separate repos.

Run dev server:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
