"""
Retriever Service

Performs semantic search using PostgreSQL + pgvector.
"""

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.rag.embedder import EmbeddingService
from app.config import settings


class RetrieverService:

    def __init__(self):

        self.embedder = EmbeddingService()

        self.top_k = settings.TOP_K

    # -------------------------------------------------------
    # Search similar chunks
    # -------------------------------------------------------

    def retrieve(
        self,
        db: Session,
        question: str
    ):

        query_embedding = self.embedder.embed_query(question)

        sql = text("""

        SELECT
            id,
            document_id,
            chunk_number,
            chunk_text,
            embedding <=> CAST(:embedding AS vector) AS distance

        FROM document_chunks

        ORDER BY embedding <=> CAST(:embedding AS vector)

        LIMIT :top_k

        """)

        result = db.execute(

            sql,

            {
                "embedding": query_embedding,
                "top_k": self.top_k
            }

        )

        rows = result.fetchall()

        documents = []

        for row in rows:

            documents.append(

                {
                    "id": row.id,

                    "document_id": row.document_id,

                    "chunk_number": row.chunk_number,

                    "chunk_text": row.chunk_text,

                    "score": float(row.distance)
                }

            )

        return documents

    # -------------------------------------------------------
    # Retrieve only context text
    # -------------------------------------------------------

    def retrieve_context(
        self,
        db: Session,
        question: str
    ) -> str:

        chunks = self.retrieve(
            db,
            question
        )

        context = "\n\n".join(

            chunk["chunk_text"]

            for chunk in chunks

        )

        return context