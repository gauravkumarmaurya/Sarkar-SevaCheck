from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..auth import get_current_user, require_admin
from ..database import get_db
from ..models import FeeReport, Service
from ..schemas import ReportCreate

router = APIRouter(prefix="/reports", tags=["Fee Reports"])


def classify(service: Service, amount: float) -> tuple[str, str, float | None]:
    total = (
        float(service.government_fee or 0)
        + float(service.authorized_service_charge or 0)
        + float(service.other_allowed_charge or 0)
    )
    if service.fee_status in {"VERIFIED", "VERIFIED_OFFICIAL"}:
        if amount > total:
            return "ABOVE_VERIFIED_TOTAL", f"Paid ₹{amount:.2f}; documented official total is ₹{total:.2f}. Verify the receipt and current order.", total
        return "WITHIN_VERIFIED_TOTAL", f"Paid amount is not above the documented official total of ₹{total:.2f}.", total
    if service.fee_status == "DEMO_DATA":
        if amount > total:
            return "ABOVE_DEMO_TOTAL", f"Demo check: paid ₹{amount:.2f}; synthetic demo amount is ₹{total:.2f}.", total
        return "WITHIN_DEMO_TOTAL", f"Demo check: paid amount is not above the synthetic demo amount of ₹{total:.2f}.", total
    return "NEEDS_OFFICIAL_FEE_VERIFICATION", "This service's fee record is not yet verified against a current official source.", None


@router.post("/fee")
def create_report(data: ReportCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    service = db.get(Service, data.service_id)
    if not service:
        raise HTTPException(404, "Service not found")

    status, notes, expected_total = classify(service, data.amount_paid)
    if data.notes.strip():
        notes += f" Citizen note: {data.notes.strip()}"

    report = FeeReport(
        user_id=user.id,
        service_id=service.id,
        amount_paid=data.amount_paid,
        extracted_text=data.extracted_text,
        extracted_amount=data.extracted_amount,
        status=status,
        notes=notes,
    )
    db.add(report)
    db.commit()
    db.refresh(report)

    return {
        "id": report.id,
        "status": status,
        "notes": notes,
        "expected_total": expected_total,
    }


@router.get("/mine")
def my_reports(db: Session = Depends(get_db), user=Depends(get_current_user)):
    rows = (
        db.query(FeeReport, Service.name)
        .outerjoin(Service, Service.id == FeeReport.service_id)
        .filter(FeeReport.user_id == user.id)
        .order_by(FeeReport.created_at.desc())
        .limit(50)
        .all()
    )
    return [
        {
            "id": r.id,
            "service_name": name or "Unknown service",
            "amount_paid": r.amount_paid,
            "extracted_amount": r.extracted_amount,
            "status": r.status,
            "notes": r.notes,
            "created_at": r.created_at.isoformat(),
        }
        for r, name in rows
    ]


@router.get("/summary")
def report_summary(db: Session = Depends(get_db), _=Depends(require_admin)):
    return {
        "total": db.query(func.count(FeeReport.id)).scalar() or 0,
        "above_verified_total": db.query(func.count(FeeReport.id)).filter(FeeReport.status == "ABOVE_VERIFIED_TOTAL").scalar() or 0,
        "above_demo_total": db.query(func.count(FeeReport.id)).filter(FeeReport.status == "ABOVE_DEMO_TOTAL").scalar() or 0,
        "within_verified_total": db.query(func.count(FeeReport.id)).filter(FeeReport.status == "WITHIN_VERIFIED_TOTAL").scalar() or 0,
        "needs_fee_verification": db.query(func.count(FeeReport.id)).filter(FeeReport.status == "NEEDS_OFFICIAL_FEE_VERIFICATION").scalar() or 0,
    }
