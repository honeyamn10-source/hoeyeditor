from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse

app = FastAPI(title="Document Digital Twin - Orchestrator")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # Placeholder: save file to /tmp and respond with stubbed analysis id
    contents = await file.read()
    # TODO: forward to OCR and layout agents for processing
    return JSONResponse({"filename": file.filename, "size": len(contents), "analysis_id": "stub-0001"})
