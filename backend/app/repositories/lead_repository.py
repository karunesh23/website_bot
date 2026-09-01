from sqlalchemy.orm import Session

from app.models.lead import Lead


class LeadRepository:

    @staticmethod
    def create(
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

        lead = Lead(
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

        db.add(lead)
        db.commit()
        db.refresh(lead)

        return lead

    @staticmethod
    def update(
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
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if lead:
            lead.name = name
            lead.email = email
            lead.phone = phone
            lead.service = service
            lead.product_name = product_name
            if company_name is not None:
                lead.company_name = company_name
            lead.purpose = purpose
            lead.scope = scope
            lead.notes = notes
            if session_id:
                lead.session_id = session_id
            db.commit()
            db.refresh(lead)
        return lead

    @staticmethod
    def get_by_email(
        db: Session,
        email: str
    ):

        return db.query(Lead).filter(
            Lead.email == email
        ).first()

    @staticmethod
    def get_by_phone(
        db: Session,
        phone: str
    ):

        return db.query(Lead).filter(
            Lead.phone == phone
        ).first()

    @staticmethod
    def get_by_session_id(
        db: Session,
        session_id: str
    ):
        return db.query(Lead).filter(
            Lead.session_id == session_id
        ).first()

    @staticmethod
    def update_client_type_by_session(
        db: Session,
        session_id: str,
        client_type: str
    ):
        lead = db.query(Lead).filter(Lead.session_id == session_id).first()
        if lead:
            lead.client_type = client_type
            db.commit()
            db.refresh(lead)
        return lead