from sqlalchemy.orm import Session

from app.models.ticket import Ticket


class TicketRepository:


    @staticmethod
    def create(
        db: Session,
        ticket_number: str,
        lead_id: str,
        issue: str,
        status: str = "OPEN",
        category: str = "Support",
        priority: str = "Normal"
    ):

        ticket = Ticket(
            ticket_number=ticket_number,
            lead_id=lead_id,
            issue=issue,
            status=status,
            category=category,
            priority=priority
        )

        db.add(ticket)

        db.commit()

        db.refresh(ticket)

        return ticket



    @staticmethod
    def get_ticket(
        db: Session,
        ticket_number: str
    ):

        return db.query(Ticket).filter(
            Ticket.ticket_number == ticket_number
        ).first()



    @staticmethod
    def update_status(
        db: Session,
        ticket_number: str,
        status: str
    ):

        ticket = db.query(Ticket).filter(
            Ticket.ticket_number == ticket_number
        ).first()


        if ticket:

            ticket.status = status

            db.commit()

            db.refresh(ticket)


        return ticket



    # ADD THIS METHOD

    @staticmethod
    def get_latest_ticket_by_lead_id(
        db: Session,
        lead_id: str
    ):

        return (
            db.query(Ticket)
            .filter(
                Ticket.lead_id == lead_id
            )
            .order_by(
                Ticket.id.desc()
            )
            .first()
        )