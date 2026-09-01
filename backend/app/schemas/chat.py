from typing import List

from pydantic import BaseModel, EmailStr, field_validator

from app.utils.helpers import validate_email, validate_phone_international


class ChatRequest(BaseModel):
    message: str
    session_id: str


class ChatResponse(BaseModel):
    answer: str
    session_id: str
    intent: str
    step: str | None = None
    options: List[str] | None = None
    ticket_number: str | None = None
    onboarding: dict | None = None
    audio: str | None = None
    alignment: dict | None = None
    service_table: dict | None = None
    footer: str | None = None


class EnquirySubmit(BaseModel):
    session_id: str
    name: str
    email: EmailStr
    phone: str
    service: str = "General"
    product_name: str = ""
    company_name: str = ""
    purpose: str = ""
    scope: str = ""
    notes: str = ""
    callback_time: str = "As soon as possible"

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        name = " ".join(v.split())
        if len(name) < 2:
            raise ValueError("Name must be at least 2 characters long.")
        return name

    @field_validator("company_name")
    @classmethod
    def validate_company_name(cls, v: str) -> str:
        name = " ".join(v.split())
        if len(name) < 2:
            raise ValueError("Company name must be at least 2 characters long.")
        return name

    @field_validator("product_name")
    @classmethod
    def validate_product_name(cls, v: str) -> str:
        product_name = " ".join(v.split())
        if len(product_name) < 2:
            raise ValueError(
                "Please enter the name of the product you'd like to get certified."
            )
        return product_name

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not validate_email(v):
            raise ValueError(
                "Please enter a valid email address (e.g., name@gmail.com)."
            )
        return v

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not validate_phone_international(v):
            raise ValueError(
                "Please enter a valid phone number with country code "
                "and the correct number of digits "
                "(e.g., +919876543210 or +989123456789)."
            )
        return v
