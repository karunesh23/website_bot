from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func

from app.database import Base


import uuid

class ChatTranscript(Base):

    __tablename__ = "chat_transcripts"

    transcript_id = Column(String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(255), nullable=False)
    related_id = Column(String(50), nullable=False)
    channel = Column(String(50), nullable=False, default="website")
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    transcript = Column(JSON, nullable=False)
    summary = Column(Text, nullable=True)
