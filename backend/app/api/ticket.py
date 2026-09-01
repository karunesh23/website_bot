from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.repositories.ticket_repository import TicketRepository

router = APIRouter(
    tags=["Ticket"]
)


@router.get("/{ticket_number}")
def get_ticket(
    ticket_number: str,
    db: Session = Depends(get_db)
):

    ticket = TicketRepository.get_ticket(
        db=db,
        ticket_number=ticket_number
    )

    if ticket is None:

        return {
            "message": "Ticket not found."
        }

    return ticket