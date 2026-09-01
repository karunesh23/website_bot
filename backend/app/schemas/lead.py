from pydantic import BaseModel, EmailStr


class LeadCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None
    service: str | None = "General"
    notes: str | None = None
    company_name: str | None = None
