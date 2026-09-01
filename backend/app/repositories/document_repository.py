from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk


class DocumentRepository:

    @staticmethod
    def create_document(
        db: Session,
        title: str,
        file_name: str
    ):

        document = Document(
            title=title,
            file_name=file_name
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    @staticmethod
    def add_chunk(
        db: Session,
        document_id: int,
        chunk_number: int,
        chunk_text: str,
        embedding
    ):

        chunk = DocumentChunk(
            document_id=document_id,
            chunk_number=chunk_number,
            chunk_text=chunk_text,
            embedding=embedding
        )

        db.add(chunk)
        db.commit()

        return chunk

    @staticmethod
    def get_all_documents(db: Session):

        return db.query(Document).all()

    @staticmethod
    def delete_document(
        db: Session,
        document_id: int
    ):

        document = db.query(Document).filter(
            Document.id == document_id
        ).first()

        if document:

            db.delete(document)

            db.commit()

        return document