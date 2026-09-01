from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.lead import LeadCreate

from app.repositories.lead_repository import LeadRepository

router = APIRouter(
    tags=["Lead"]
)


@router.post("/")
def create_lead(
    request: LeadCreate,
    db: Session = Depends(get_db)
):

    lead = LeadRepository.create(
        db=db,
        name=request.name,
        email=request.email,
        phone=request.phone,
        service=request.service,
        notes=request.notes,
        company_name=request.company_name
    )

    return lead