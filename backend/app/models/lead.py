from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Lead(Base):

    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_number = Column(String(50), nullable=True)

    name = Column(String(100), nullable=False)

    email = Column(String(150), nullable=False)

    phone = Column(String(20), nullable=False)

    service = Column(String(150), nullable=False)

    product_name = Column(String(200))

    purpose = Column(Text)

    scope = Column(Text)

    notes = Column(Text)
    
    # CRM Fields
    company_name = Column(String(200))
    client_type = Column(String(50), default="New Enquiry")
    last_contacted_at = Column(DateTime(timezone=True))
    session_id = Column(String(100))
    call_recording = Column(String(500))

    status = Column(
        String(30),
        default="NEW"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )