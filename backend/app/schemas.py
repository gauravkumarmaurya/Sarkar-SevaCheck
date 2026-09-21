from pydantic import BaseModel, ConfigDict, Field, field_validator


class MobileIn(BaseModel):
    mobile: str = Field(min_length=10, max_length=10)
    name: str = Field(default="Citizen", max_length=120)

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: str) -> str:
        if not value.isdigit() or len(value) != 10 or value[0] not in "6789":
            raise ValueError("Enter a valid 10-digit Indian mobile number")
        return value


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    mobile: str
    is_admin: bool


class ServiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    state: str
    department: str
    name: str
    description: str
    government_fee: float
    authorized_service_charge: float
    other_allowed_charge: float
    processing_days: str
    documents: str
    official_portal: str
    source_url: str
    source_document: str
    fee_status: str
    verified_on: str
    latitude: float | None
    longitude: float | None
    office_name: str


class ServiceCreate(BaseModel):
    state: str = "Uttarakhand"
    department: str
    name: str
    description: str = ""
    government_fee: float = 0
    authorized_service_charge: float = 0
    other_allowed_charge: float = 0
    processing_days: str = "Verify from official source"
    documents: str = ""
    official_portal: str = "https://eservices.uk.gov.in/"
    source_url: str = "https://it.uk.gov.in/apuni-sarkar/"
    source_document: str = ""
    fee_status: str = "DEMO_DATA"
    verified_on: str = ""
    latitude: float | None = None
    longitude: float | None = None
    office_name: str = "Relevant Uttarakhand office"


class ReportCreate(BaseModel):
    service_id: int
    amount_paid: float = Field(ge=0)
    extracted_amount: float | None = Field(default=None, ge=0)
    extracted_text: str = ""
    notes: str = ""
