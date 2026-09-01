"""
CRM Lead Service
"""

from sqlalchemy.orm import Session

from app.repositories.lead_repository import LeadRepository


class LeadService:

    @staticmethod
    def create_lead(
        db: Session,
        name: str,
        email: str,
        phone: str,
        service: str,
        product_name: str = None,
        company_name: str = None,
        purpose: str = None,
        scope: str = None,
        notes: str = None,
        session_id: str = None
    ):

        lead = LeadRepository.create(
            db=db,
            name=name,
            email=email,
            phone=phone,
            service=service,
            product_name=product_name,
            company_name=company_name,
            purpose=purpose,
            scope=scope,
            notes=notes,
            session_id=session_id
        )

        return {
            "success": True,
            "message": "Lead created successfully.",
            "lead_id": lead.id
        }

    @staticmethod
    def update_lead(
        db: Session,
        lead_id: int,
        name: str,
        email: str,
        phone: str,
        service: str,
        product_name: str = None,
        company_name: str = None,
        purpose: str = None,
        scope: str = None,
        notes: str = None,
        session_id: str = None
    ):

        lead = LeadRepository.update(
            db=db,
            lead_id=lead_id,
            name=name,
            email=email,
            phone=phone,
            service=service,
            product_name=product_name,
            company_name=company_name,
            purpose=purpose,
            scope=scope,
            notes=notes,
            session_id=session_id
        )

        if lead:
            return {
                "success": True,
                "message": "Lead updated successfully.",
                "lead_id": lead.id
            }
        return {
            "success": False,
            "message": "Lead not found.",
            "lead_id": None
        }

    @staticmethod
    def get_customer(
        db: Session,
        email=None,
        phone=None
    ):

        if email:

            customer = LeadRepository.get_by_email(
                db,
                email
            )

            if customer:
                return customer

        if phone:
            customer = LeadRepository.get_by_phone(db, phone)
            if customer:
                return customer

        return None

    @staticmethod
    def get_customer_by_session(
        db: Session,
        session_id: str
    ):
        return LeadRepository.get_by_session_id(db, session_id)