"""
CRM Ticket Service
"""

import uuid

from sqlalchemy.orm import Session

from app.repositories.ticket_repository import TicketRepository


class TicketService:

    @staticmethod
    def generate_ticket():
        import random
        return str(random.randint(1000, 9999))


    @classmethod
    def create_ticket(
        cls,
        db: Session,
        lead_id: int,
        issue: str,
        category: str = "Support",
        priority: str = "Normal"
    ):

        ticket = TicketRepository.create(
            db=db,
            ticket_number=cls.generate_ticket(),
            lead_id=lead_id,
            issue=issue,
            status="OPEN",
            category=category,
            priority=priority
        )

        return ticket



    @staticmethod
    def get_status(
        db: Session,
        ticket_number: str
    ):

        ticket = TicketRepository.get_ticket(
            db,
            ticket_number
        )


        if ticket is None:

            return {
                "success": False,
                "message": "Ticket not found."
            }


        return {
            "success": True,
            "ticket": ticket.ticket_number,
            "status": ticket.status,
            "issue": ticket.issue
        }



    @staticmethod
    def close_ticket(
        db: Session,
        ticket_number: str
    ):

        ticket = TicketRepository.update_status(
            db,
            ticket_number,
            "CLOSED"
        )

        return ticket



    # ADD THIS METHOD HERE

    @staticmethod
    def get_latest_ticket(
        db: Session,
        lead_id: int
    ):

        return TicketRepository.get_latest_ticket_by_lead_id(
            db,
            lead_id
        )