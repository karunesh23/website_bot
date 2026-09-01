"""
Document Loader Service

Supported Formats:
- .docx
- .pdf
- .txt

This service loads every supported document from
the knowledge_base folder and extracts plain text.
"""

from pathlib import Path
from typing import List, Dict

from docx import Document
from pypdf import PdfReader


class DocumentLoader:

    SUPPORTED_EXTENSIONS = {
        ".docx",
        ".pdf",
        ".txt"
    }

    def __init__(self, knowledge_base_path: str):
        self.knowledge_base_path = Path(knowledge_base_path)

    # --------------------------------------------------------
    # Load all documents
    # --------------------------------------------------------

    def load_documents(self) -> List[Dict]:

        documents = []

        if not self.knowledge_base_path.exists():
            raise FileNotFoundError(
                f"Knowledge base not found: {self.knowledge_base_path}"
            )

        files = sorted(self.knowledge_base_path.rglob("*"))

        for file in files:

            if not file.is_file():
                continue

            if file.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            content = self.extract_text(file)

            documents.append(
                {
                    "title": file.stem,
                    "file_name": file.name,
                    "extension": file.suffix.lower(),
                    "content": content
                }
            )

        return documents

    # --------------------------------------------------------
    # Detect file type
    # --------------------------------------------------------

    def extract_text(self, file_path: Path) -> str:

        extension = file_path.suffix.lower()

        if extension == ".docx":
            return self.load_docx(file_path)

        if extension == ".pdf":
            return self.load_pdf(file_path)

        if extension == ".txt":
            return self.load_txt(file_path)

        raise Exception(
            f"Unsupported document type: {extension}"
        )

    # --------------------------------------------------------
    # DOCX
    # --------------------------------------------------------

    @staticmethod
    def load_docx(file_path: Path) -> str:

        doc = Document(file_path)

        paragraphs = []

        for paragraph in doc.paragraphs:

            text = paragraph.text.strip()

            if text:
                paragraphs.append(text)

        return "\n".join(paragraphs)

    # --------------------------------------------------------
    # PDF
    # --------------------------------------------------------

    @staticmethod
    def load_pdf(file_path: Path) -> str:

        pdf = PdfReader(file_path)

        pages = []

        for page in pdf.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

        return "\n".join(pages)

    # --------------------------------------------------------
    # TXT
    # --------------------------------------------------------

    @staticmethod
    def load_txt(file_path: Path) -> str:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    # --------------------------------------------------------
    # Load a single document
    # --------------------------------------------------------

    def load_single_document(
        self,
        file_name: str
    ) -> Dict:

        file_path = self.knowledge_base_path / file_name

        if not file_path.exists():
            raise FileNotFoundError(file_name)

        return {
            "title": file_path.stem,
            "file_name": file_path.name,
            "extension": file_path.suffix.lower(),
            "content": self.extract_text(file_path)
        }