from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), default="Citizen")
    mobile: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Service(Base):
    __tablename__ = "services"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    state: Mapped[str] = mapped_column(String(80), default="Uttarakhand")
    department: Mapped[str] = mapped_column(String(160))
    name: Mapped[str] = mapped_column(String(220), index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    government_fee: Mapped[float] = mapped_column(Float, default=0)
    authorized_service_charge: Mapped[float] = mapped_column(Float, default=0)
    other_allowed_charge: Mapped[float] = mapped_column(Float, default=0)
    processing_days: Mapped[str] = mapped_column(String(120), default="Verify from official source")
    documents: Mapped[str] = mapped_column(Text, default="")
    official_portal: Mapped[str] = mapped_column(String(500), default="https://eservices.uk.gov.in/")
    source_url: Mapped[str] = mapped_column(String(500), default="https://it.uk.gov.in/apuni-sarkar/")
    source_document: Mapped[str] = mapped_column(String(300), default="")
    fee_status: Mapped[str] = mapped_column(String(40), default="VERIFY_FROM_OFFICIAL_ORDER")
    verified_on: Mapped[str] = mapped_column(String(40), default="")
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    office_name: Mapped[str] = mapped_column(String(220), default="")


class FeeReport(Base):
    __tablename__ = "fee_reports"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    amount_paid: Mapped[float] = mapped_column(Float)
    extracted_text: Mapped[str] = mapped_column(Text, default="")
    extracted_amount: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[str] = mapped_column(String(80), default="NEEDS_VERIFICATION")
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
