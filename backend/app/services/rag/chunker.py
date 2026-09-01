"""
Document Chunking Service

Splits extracted documents into overlapping chunks
ready for embedding and storage.
"""

from typing import List, Dict

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings


class DocumentChunker:

    def __init__(self):

        self.text_splitter = RecursiveCharacterTextSplitter(

            chunk_size=settings.CHUNK_SIZE,

            chunk_overlap=settings.CHUNK_OVERLAP,

            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    # -------------------------------------------------------
    # Chunk one document
    # -------------------------------------------------------

    def chunk_document(
        self,
        document: Dict
    ) -> List[Dict]:

        chunks = self.text_splitter.split_text(
            document["content"]
        )

        output = []

        for index, chunk in enumerate(chunks):

            output.append(
                {
                    "title": document["title"],

                    "file_name": document["file_name"],

                    "chunk_number": index + 1,

                    "chunk_text": chunk
                }
            )

        return output

    # -------------------------------------------------------
    # Chunk multiple documents
    # -------------------------------------------------------

    def chunk_documents(
        self,
        documents: List[Dict]
    ) -> List[Dict]:

        all_chunks = []

        for document in documents:

            chunks = self.chunk_document(document)

            all_chunks.extend(chunks)

        return all_chunks