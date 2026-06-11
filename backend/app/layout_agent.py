from fastapi import APIRouter, HTTPException
from typing import List, Dict

router = APIRouter(prefix="/agents/layout", tags=["layout_agent"])


def group_blocks_into_paragraphs(blocks: List[Dict]) -> List[Dict]:
    """Very small heuristic: group OCR blocks into paragraphs by proximity on Y axis.
    Returns list of paragraphs with bbox and contained texts."""
    if not blocks:
        return []
    # sort by top coordinate
    sorted_blocks = sorted(blocks, key=lambda b: b['bbox'][1])
    paragraphs = []
    current = {"texts": [], "bbox": None}
    prev_bottom = None
    for b in sorted_blocks:
        top = b['bbox'][1]
        height = b['bbox'][3]
        bottom = top + height
        if prev_bottom is None or top - prev_bottom <= max(10, int(height * 0.5)):
            # continue paragraph
            current['texts'].append(b['text'])
            # update bbox
            if current['bbox'] is None:
                current['bbox'] = b['bbox'].copy()
            else:
                lx, ly, lw, lh = current['bbox']
                rx = max(lx + lw, b['bbox'][0] + b['bbox'][2])
                by = max(ly + lh, b['bbox'][1] + b['bbox'][3])
                nx = min(lx, b['bbox'][0])
                ny = min(ly, b['bbox'][1])
                current['bbox'] = [nx, ny, rx - nx, by - ny]
            prev_bottom = max(prev_bottom or 0, bottom)
        else:
            # flush
            paragraphs.append({"text": " ".join(current['texts']), "bbox": current['bbox']})
            current = {"texts": [b['text']], "bbox": b['bbox'].copy()}
            prev_bottom = b['bbox'][1] + b['bbox'][3]

    if current and current.get('texts'):
        paragraphs.append({"text": " ".join(current['texts']), "bbox": current['bbox']})

    return paragraphs


@router.post("/analyze")
async def analyze_layout(blocks: List[Dict]):
    try:
        paras = group_blocks_into_paragraphs(blocks)
        return {"paragraphs": paras}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
