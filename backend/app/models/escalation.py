from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Escalation(Base):
    __tablename__ = "escalations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=False)
    
    reason = Column(Text, nullable=False)
    
    status = Column(String(30), default="Pending")
    
    raised_on = Column(DateTime(timezone=True), server_default=func.now())

    lead = relationship("Lead")
