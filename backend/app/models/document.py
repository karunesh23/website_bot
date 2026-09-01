from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    file_name = Column(String(255), unique=True, nullable=False)

    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan"
    )