from fastapi import APIRouter

router = APIRouter(
    tags=["Health"]
)


@router.get("/")
def health():

    return {
        "status": "Healthy",
        "service": "ITC RAG Chatbot",
        "version": "1.0.0"
    }