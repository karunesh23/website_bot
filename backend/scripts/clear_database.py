"""
Delete all records from database.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.database import SessionLocal

from app.models.document_chunk import DocumentChunk
from app.models.document import Document
from app.models.chat_history import ChatHistory
from app.models.conversation import Conversation
from app.models.ticket import Ticket
from app.models.lead import Lead


def clear_database():

    db = SessionLocal()

    db.query(DocumentChunk).delete()
    db.query(Document).delete()

    db.query(ChatHistory).delete()
    db.query(Conversation).delete()

    db.query(Ticket).delete()
    db.query(Lead).delete()

    db.commit()

    db.close()

    print("✅ Database cleared.")


if __name__ == "__main__":

    clear_database()