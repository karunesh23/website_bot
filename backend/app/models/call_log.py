from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

import uuid

class CallLog(Base):
    __tablename__ = "call_logs"

    call_id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    callback_id = Column(String(50), ForeignKey("callbacks.id"), nullable=True)
    member_id = Column(Integer, ForeignKey("team_members.id"), nullable=True)
    received_at = Column(DateTime(timezone=True), server_default=func.now())
    picked = Column(Boolean, default=False)
    picked_at = Column(DateTime(timezone=True), nullable=True)
    escalated_to = Column(Integer, ForeignKey("team_members.id"), nullable=True)
    outcome = Column(String(50)) # Connected, Missed, Escalated
    duration_seconds = Column(Integer, nullable=True)
    recording_url = Column(String(500), nullable=True)
    call_summary = Column(Text, nullable=True)
    
    callback = relationship("Callback")
    team_member = relationship("TeamMember", foreign_keys=[member_id])
    escalated_to_member = relationship("TeamMember", foreign_keys=[escalated_to])
