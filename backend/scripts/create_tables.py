"""
Create all database tables.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.database import Base, engine

# Import all models
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.lead import Lead
from app.models.ticket import Ticket
from app.models.conversation import Conversation
from app.models.chat_history import ChatHistory


def create_tables():

    Base.metadata.create_all(bind=engine)

    print("✅ Database tables created successfully.")


if __name__ == "__main__":

    create_tables()