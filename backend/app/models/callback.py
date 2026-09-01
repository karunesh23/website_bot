from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Callback(Base):
    __tablename__ = "callbacks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150))
    phone = Column(String(20))
    email = Column(String(150))
    topic = Column(String(255))
    requested_time = Column(DateTime(timezone=True))
    status = Column(String(50), default="Requested") # Requested, Sent to Evoke, Connected, Missed
    session_id = Column(String(255), nullable=True)
    
    lead_id = Column(Integer, ForeignKey("leads.id"), nullable=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    lead = relationship("Lead")
    ticket = relationship("Ticket")
