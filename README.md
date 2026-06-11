# Document Digital Twin Editor (Prototype)

High-level scaffold for an AI-powered Document Digital Twin Editor.

Goal: transform uploaded files into editable, structured "Digital Twins" preserving visual fidelity.

Tech stack (initial):
- Frontend: Next.js, TypeScript, Tailwind CSS, Konva/Fabric.js
- Backend: FastAPI (Python) for orchestration; Rust for performance-critical modules
- AI: Vision-Language models, OCR agents, SAM, LayoutLM, ONNX
- Storage: PostgreSQL, Redis

This workspace contains minimal skeletons to iterate on architecture and integration.

Developer quickstart

1. Backend dev server

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

2. Frontend dev server

```bash
cd frontend
npm install
npm run dev
```
