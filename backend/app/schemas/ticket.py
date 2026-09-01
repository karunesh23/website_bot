from pydantic import BaseModel


class TicketCreate(BaseModel):
    subject: str
    description: str
    status: str = "open"
