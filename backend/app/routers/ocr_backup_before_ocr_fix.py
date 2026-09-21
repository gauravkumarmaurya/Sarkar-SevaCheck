import os
import re
from io import BytesIO
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from PIL import Image
import pytesseract
from sqlalchemy.orm import Session
from fastapi import Depends
from ..database import get_db
from ..models import Service

router = APIRouter(prefix="/ocr", tags=["Receipt OCR"])

cmd = os.getenv("TESSERACT_CMD", "")
if cmd:
    pytesseract.pytesseract.tesseract_cmd = cmd
elif os.name == "nt":
    default_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(default_cmd):
        pytesseract.pytesseract.tesseract_cmd = default_cmd


def extract_amount(text: str) -> float | None:
    clean = text.replace("=", " ").replace("₹", " Rs ")
    patterns = [
        r"(?:TOTAL\s*(?:AMOUNT|PAYMENT|PAID|DUE)?|GRAND\s*TOTAL|NET\s*TOTAL|AMOUNT\s*PAID)\s*[:\-]?\s*(?:RS\.?|INR)?\s*([0-9]{1,7}(?:[,.][0-9]{1,2})?)",
        r"(?:RS\.?|INR)\s*([0-9]{1,7}(?:[,.][0-9]{1,2})?)",
    ]
    candidates: list[float] = []
    for pattern in patterns:
        for match in re.findall(pattern, clean, flags=re.I):
            try:
                candidates.append(float(match.replace(",", "")))
            except ValueError:
                pass
        if candidates:
            return candidates[-1]
    return None


@router.post("/receipt")
async def receipt_ocr(
    file: UploadFile = File(...),
    service_id: int = Form(...),
    db: Session = Depends(get_db),
):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400, "Upload an image file")

    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(404, "Service not found")

    raw = await file.read()
    if len(raw) > 8 * 1024 * 1024:
        raise HTTPException(413, "Image is too large; maximum is 8 MB")

    try:
        image = Image.open(BytesIO(raw))
        text = pytesseract.image_to_string(image)
    except Exception as exc:
        raise HTTPException(
            503,
            "OCR is unavailable. Install Tesseract OCR and ensure it is configured.",
        ) from exc

    extracted = extract_amount(text)
    total = (
        float(service.government_fee or 0)
        + float(service.authorized_service_charge or 0)
        + float(service.other_allowed_charge or 0)
    )

    official = service.fee_status in {"VERIFIED", "VERIFIED_OFFICIAL"}
    demo = service.fee_status == "DEMO_DATA"
    comparison = "NEEDS_FEE_VERIFICATION"
    if extracted is not None and (official or demo):
        comparison = "ABOVE_DOCUMENTED_AMOUNT" if extracted > total else "WITHIN_DOCUMENTED_AMOUNT"

    return {
        "service_id": service.id,
        "service_name": service.name,
        "text": text,
        "extracted_amount": extracted,
        "documented_total": total if (official or demo) else None,
        "fee_status": service.fee_status,
        "is_official": official,
        "is_demo": demo,
        "comparison": comparison,
    }
