from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.database import Base


class ChatHistory(Base):

    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True)

    session_id = Column(
        String(255),
        index=True,
        nullable=False
    )

    question = Column(Text, nullable=False)

    answer = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )