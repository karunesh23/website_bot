from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Ticket(Base):

    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, autoincrement=True)

    ticket_number = Column(
        String(50),
        unique=True,
        nullable=False
    )

    lead_id = Column(
        Integer,
        ForeignKey("leads.id")
    )
    
    session_id = Column(String(255))

    issue = Column(Text)

    category = Column(String(100))
    
    priority = Column(String(50), default="Normal")

    status = Column(
        String(30),
        default="OPEN"
    )
    
    last_updated = Column(
        DateTime(timezone=True),
        onupdate=func.now()
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    lead = relationship("Lead")