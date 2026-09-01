from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    role = Column(String(100))
    service_desk = Column(String(100), default="IT Support")
    escalation_level = Column(String(50))
    call_performance = Column(String(50))
    is_active = Column(Boolean, default=True)


    created_at = Column(DateTime(timezone=True), server_default=func.now())
