"""
Knowledge Base Ingestion Pipeline

Pipeline

Knowledge Base
      │
      ▼
Loader
      │
      ▼
Chunker
      │
      ▼
Embedding
      │
      ▼
PostgreSQL (pgvector)
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app.database import SessionLocal

from app.services.rag.loader import DocumentLoader
from app.services.rag.chunker import DocumentChunker
from app.services.rag.embedder import EmbeddingService

from app.repositories.document_repository import DocumentRepository


def ingest_documents():

    db = SessionLocal()

    loader = DocumentLoader(
        "app/knowledge_base"
    )

    chunker = DocumentChunker()

    embedder = EmbeddingService()

    documents = loader.load_documents()

    for document in documents:

        db_document = DocumentRepository.create_document(

            db=db,

            title=document["title"],

            file_name=document["file_name"]

        )

        chunks = chunker.chunk_document(
            document
        )

        embedded_chunks = embedder.embed_chunks(
            chunks
        )

        for chunk in embedded_chunks:

            DocumentRepository.add_chunk(

                db=db,

                document_id=db_document.id,

                chunk_number=chunk["chunk_number"],

                chunk_text=chunk["chunk_text"],

                embedding=chunk["embedding"]

            )

        print(
            f"✅ Indexed {document['title']}"
        )

    db.close()

    print("🎉 Knowledge Base Ingestion Completed.")


if __name__ == "__main__":

    ingest_documents()