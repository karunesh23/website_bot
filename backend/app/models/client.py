from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(255), nullable=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), nullable=True)
    phone = Column(String(50), nullable=True)
    company_name = Column(String(150), nullable=True)
    client_type = Column(String(50), default="New Enquiry")
    status = Column(String(50), default="Active")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_contacted_at = Column(DateTime(timezone=True), nullable=True)
