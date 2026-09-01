from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.api.documents import router as document_router
from app.api.health import router as health_router
from app.api.lead import router as lead_router
from app.api.ticket import router as ticket_router
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../crm_design/backend')))
from api import router as crm_router
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    health_router,
    prefix="/health",
    tags=["Health"]
)

app.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"]
)

app.include_router(
    document_router,
    prefix="/documents",
    tags=["Documents"]
)

app.include_router(
    lead_router,
    prefix="/lead",
    tags=["Lead"]
)

app.include_router(
    ticket_router,
    prefix="/ticket",
    tags=["Ticket"]
)

app.include_router(crm_router)


@app.get("/")
# trigger reload 4
def root():

    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "Running"
    }