from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Service
from ..schemas import ServiceOut

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("", response_model=list[ServiceOut])
def list_services(q: str = Query("", max_length=100), db: Session = Depends(get_db)):
    query = db.query(Service)
    if q.strip():
        like = f"%{q.strip()}%"
        query = query.filter(or_(
            Service.name.ilike(like),
            Service.department.ilike(like),
            Service.description.ilike(like),
        ))
    return query.order_by(Service.id).all()


@router.get("/{service_id}", response_model=ServiceOut)
def get_service(service_id: int, db: Session = Depends(get_db)):
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(404, "Service not found")
    return service
