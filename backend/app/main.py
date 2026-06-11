from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from app import digital_twin
from app import ocr_agent
from app import layout_agent


app = FastAPI(title="Document Digital Twin - Orchestrator")


@app.get("/health")
async def health():
    return {"status": "ok"}


# include routers
app.include_router(ocr_agent.router)
app.include_router(layout_agent.router)


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    contents = await file.read()
    return JSONResponse({"filename": file.filename, "size": len(contents), "analysis_id": "stub-0001"})


@app.post("/digital_twin")
async def build_digital_twin(file: UploadFile = File(...)):
    """Simple digital twin builder: runs OCR then a lightweight layout pass and
    returns a structured Digital Twin model. This is a prototype/stub for the
    full engine.
    """
    contents = await file.read()
    # reuse pytesseract OCR logic similar to ocr_agent
    try:
        from PIL import Image
        import io
        img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        return JSONResponse({"error": f"Unable to open image: {str(e)}"}, status_code=400)

    try:
        import pytesseract
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        blocks = []
        n = len(data.get('level', []))
        for i in range(n):
            text = data.get('text', [])[i].strip()
            if not text:
                continue
            left = data.get('left', [])[i]
            top = data.get('top', [])[i]
            width = data.get('width', [])[i]
            height = data.get('height', [])[i]
            conf = data.get('conf', [])[i]
            blocks.append({
                "text": text,
                "bbox": [int(left), int(top), int(width), int(height)],
                "conf": int(conf) if conf.isdigit() else conf,
            })

        # run a simple layout grouping
        layout = layout_agent.group_blocks_into_paragraphs(blocks)
        twin = digital_twin.DigitalTwin.from_layout_and_ocr(layout, blocks)
        return twin.dict()
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
