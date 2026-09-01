from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func

from app.database import Base


class Conversation(Base):

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)

    session_id = Column(
        String(255),
        unique=True,
        nullable=False
    )

    current_flow = Column(String(100))

    current_step = Column(String(100))

    state_data = Column(JSON)

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )