"""
Rebuild embeddings after changing the embedding model.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from scripts.clear_database import clear_database
from scripts.ingest_documents import ingest_documents


if __name__ == "__main__":

    clear_database()

    ingest_documents()

    print("✅ Embeddings rebuilt successfully.")