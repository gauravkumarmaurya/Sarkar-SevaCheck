from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..auth import require_admin
from ..database import get_db
from ..models import Service
from ..schemas import ServiceCreate, ServiceOut

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats")
def stats(db: Session = Depends(get_db), _=Depends(require_admin)):
    services = db.query(Service).all()
    return {
        "total_services": len(services),
        "official_verified": sum(s.fee_status in {"VERIFIED", "VERIFIED_OFFICIAL"} for s in services),
        "demo_data": sum(s.fee_status == "DEMO_DATA" for s in services),
        "needs_verification": sum(s.fee_status == "VERIFY_FROM_OFFICIAL_ORDER" for s in services),
    }


@router.post("/services", response_model=ServiceOut)
def create_service(data: ServiceCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    if db.query(Service).filter(Service.name == data.name.strip()).first():
        raise HTTPException(409, "A service with this name already exists")
    service = Service(**data.model_dump())
    service.name = service.name.strip()
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


@router.put("/services/{service_id}", response_model=ServiceOut)
def update_service(service_id: int, data: ServiceCreate, db: Session = Depends(get_db), _=Depends(require_admin)):
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(404, "Service not found")
    for key, value in data.model_dump().items():
        setattr(service, key, value)
    service.name = service.name.strip()
    db.commit()
    db.refresh(service)
    return service


@router.delete("/services/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db), _=Depends(require_admin)):
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(404, "Service not found")
    db.delete(service)
    db.commit()
    return {"ok": True}
