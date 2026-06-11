from pydantic import BaseModel, Field
from typing import List, Optional, Any


class TextElement(BaseModel):
    id: str
    text: str
    bbox: List[int]
    confidence: Optional[float]
    font: Optional[str] = None


class ImageElement(BaseModel):
    id: str
    bbox: List[int]
    metadata: Optional[Any]


class TableElement(BaseModel):
    id: str
    bbox: List[int]
    rows: int = 0
    cols: int = 0


class Layer(BaseModel):
    id: str
    name: str
    elements: List[Any] = Field(default_factory=list)


class DigitalTwin(BaseModel):
    id: str
    pages: int = 1
    layers: List[Layer] = Field(default_factory=list)

    @classmethod
    def from_layout_and_ocr(cls, layout, ocr_blocks):
        # very small prototype: create one layer with text elements from OCR
        texts = []
        for i, b in enumerate(ocr_blocks):
            texts.append(TextElement(id=f"t{i}", text=b.get('text',''), bbox=b.get('bbox',[]), confidence=b.get('conf', None)).dict())

        layer = Layer(id="layer1", name="text", elements=texts)
        return cls(id="twin-0001", pages=1, layers=[layer])
