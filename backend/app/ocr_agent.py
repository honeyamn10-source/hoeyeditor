from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import io

router = APIRouter(prefix="/agents/ocr", tags=["ocr_agent"])


@router.post("/extract")
async def extract_text(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        img = Image.open(io.BytesIO(contents)).convert("RGB")
    except Exception as e:
        return JSONResponse({"error": f"Unable to open image: {str(e)}"}, status_code=400)

    # Try to perform OCR using pytesseract if available
    try:
        import pytesseract
        # Use pytesseract to get box-level data
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        # Simplify results into text blocks with bounding boxes
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

        return {"engine": "pytesseract", "blocks": blocks}
    except Exception as e:
        # Provide helpful guidance if pytesseract or tesseract binary missing
        msg = (
            "pytesseract OCR not available or failed. "
            "Install Tesseract OCR and the Python package pytesseract to enable OCR: "
            "https://github.com/tesseract-ocr/tesseract\n"
            "On Debian/Ubuntu: `sudo apt-get install tesseract-ocr`\n"
            "Then `pip install pytesseract`"
        )
        return JSONResponse({"error": str(e), "message": msg}, status_code=500)
