from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File

import shutil
from pathlib import Path

router = APIRouter(
    tags=["Knowledge Base"]
)


UPLOAD_FOLDER = Path("app/knowledge_base")

UPLOAD_FOLDER.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    destination = UPLOAD_FOLDER / file.filename

    with open(destination, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "Document uploaded successfully.",
        "file": file.filename
    }


@router.get("/")
def list_documents():

    files = []

    for file in UPLOAD_FOLDER.iterdir():

        if file.is_file():

            files.append(file.name)

    return files