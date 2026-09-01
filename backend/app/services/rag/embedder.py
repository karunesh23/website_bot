from typing import Dict, List

from openai import OpenAI

from app.config import settings


class EmbeddingService:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

        self.model = settings.EMBEDDING_MODEL

    # ----------------------------------------
    # Document Embedding
    # ----------------------------------------

    def generate_embedding(
        self,
        text: str
    ) -> List[float]:

        response = self.client.embeddings.create(
            model=self.model,
            input=text
        )

        return response.data[0].embedding

    # ----------------------------------------
    # Embed Chunks
    # ----------------------------------------

    def embed_chunks(
        self,
        chunks: List[Dict]
    ) -> List[Dict]:

        embedded_chunks = []

        for chunk in chunks:

            embedding = self.generate_embedding(
                chunk["chunk_text"]
            )

            embedded_chunks.append(
                {
                    "title": chunk["title"],
                    "file_name": chunk["file_name"],
                    "chunk_number": chunk["chunk_number"],
                    "chunk_text": chunk["chunk_text"],
                    "embedding": embedding,
                }
            )

        return embedded_chunks

    # ----------------------------------------
    # Query Embedding
    # ----------------------------------------

    def embed_query(
        self,
        question: str
    ) -> List[float]:

        response = self.client.embeddings.create(
            model=self.model,
            input=question
        )

        return response.data[0].embedding