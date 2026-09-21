import os
import re
from io import BytesIO

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, Depends
from PIL import Image, ImageOps, ImageEnhance
import pytesseract
from sqlalchemy.orm import Session

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
    clean = (
        text.replace("₹", " Rs ")
        .replace("â‚¹", " Rs ")
        .replace("®", " ")
        .replace("%", " ")
        .replace("=", " ")
        .replace("—", "-")
    )

    # TOTAL AMOUNT patterns
    patterns = [
        r"TOTAL\s+AMOUNT\s+PAID[^\d]{0,50}([0-9]{1,7}(?:[,.][0-9]{1,2})?)",
        r"TOTAL\s+PAYMENT[^\d]{0,50}([0-9]{1,7}(?:[,.][0-9]{1,2})?)",
        r"TOTAL\s+PAID[^\d]{0,50}([0-9]{1,7}(?:[,.][0-9]{1,2})?)",
        r"GRAND\s+TOTAL[^\d]{0,50}([0-9]{1,7}(?:[,.][0-9]{1,2})?)",
        r"NET\s+TOTAL[^\d]{0,50}([0-9]{1,7}(?:[,.][0-9]{1,2})?)",
        r"AMOUNT\s+PAID[^\d]{0,50}([0-9]{1,7}(?:[,.][0-9]{1,2})?)",
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            clean,
            flags=re.IGNORECASE | re.DOTALL
        )

        if match:
            try:
                return float(match.group(1).replace(",", ""))
            except ValueError:
                pass

    # Currency fallback
    currency_pattern = (
        r"(?:RS\.?|INR|RUPEES)\s*"
        r"([0-9]{1,7}(?:[,.][0-9]{1,2})?)"
    )

    matches = re.findall(
        currency_pattern,
        clean,
        flags=re.IGNORECASE
    )

    if matches:
        try:
            return float(matches[-1].replace(",", ""))
        except ValueError:
            pass

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
        raise HTTPException(413, "Image is too large; maximum is 8 MB.")

    try:
        image = Image.open(BytesIO(raw)).convert("RGB")

        # First try normal OCR
        text = pytesseract.image_to_string(
            image,
            config="--psm 6"
        )

        # If OCR text is too short, use enhanced image
        if len(text.strip()) < 20:
            gray = ImageOps.grayscale(image)
            gray = ImageEnhance.Contrast(gray).enhance(2.0)

            width, height = gray.size

            if width < 1200:
                scale = 1200 / width
                gray = gray.resize(
                    (1200, int(height * scale))
                )

            enhanced_text = pytesseract.image_to_string(
                gray,
                config="--psm 6"
            )

            if len(enhanced_text.strip()) > len(text.strip()):
                text = enhanced_text

        # Final fallback OCR mode
        if len(text.strip()) < 20:
            extra_text = pytesseract.image_to_string(
                image,
                config="--psm 11"
            )

            if len(extra_text.strip()) > len(text.strip()):
                text = extra_text

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

    official = service.fee_status in {
        "VERIFIED",
        "VERIFIED_OFFICIAL"
    }

    demo = service.fee_status == "DEMO_DATA"

    comparison = "NEEDS_FEE_VERIFICATION"

    if extracted is not None and (official or demo):
        if extracted > total:
            comparison = "ABOVE_DOCUMENTED_AMOUNT"
        else:
            comparison = "WITHIN_DOCUMENTED_AMOUNT"

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