from sqlalchemy.orm import Session

from app.models.chat_history import ChatHistory


class ChatRepository:

    @staticmethod
    def save_chat(
        db: Session,
        session_id: str,
        question: str,
        answer: str
    ):

        chat = ChatHistory(
            session_id=session_id,
            question=question,
            answer=answer
        )

        db.add(chat)

        db.commit()

        db.refresh(chat)

        try:
            ChatRepository._update_transcript(db, session_id)
        except Exception as e:
            print(f"Error updating chat transcript: {e}")

        return chat

    @staticmethod
    def _update_transcript(db: Session, session_id: str):
        from app.models.chat_transcript import ChatTranscript
        from app.models.lead import Lead
        from app.models.ticket import Ticket
        
        chats = db.query(ChatHistory).filter(ChatHistory.session_id == session_id).order_by(ChatHistory.id).all()
        if not chats:
            return
            
        transcript_data = []
        for c in chats:
            transcript_data.append({"role": "user", "content": c.question, "time": c.created_at.isoformat() if c.created_at else None})
            transcript_data.append({"role": "assistant", "content": c.answer, "time": c.created_at.isoformat() if c.created_at else None})
            
        started_at = chats[0].created_at
        ended_at = chats[-1].created_at
        
        related_id = "Anonymous"
        lead = db.query(Lead).filter(Lead.session_id == session_id).first()
        if lead:
            ticket = db.query(Ticket).filter(Ticket.lead_id == lead.id).first()
            if ticket and ticket.ticket_number:
                related_id = str(ticket.ticket_number)
            else:
                related_id = f"REF-{lead.id}"
                
        transcript = db.query(ChatTranscript).filter(ChatTranscript.session_id == session_id).first()
        if not transcript:
            transcript = ChatTranscript(
                session_id=session_id,
                related_id=related_id,
                channel="website",
                started_at=started_at,
                ended_at=ended_at,
                transcript=transcript_data,
                summary="Chat interaction in progress."
            )
            db.add(transcript)
        else:
            transcript.related_id = related_id
            transcript.ended_at = ended_at
            transcript.transcript = transcript_data
            
        db.commit()

    @staticmethod
    def get_chats(
        db: Session,
        session_id: str
    ):

        return (
            db.query(ChatHistory)
            .filter(ChatHistory.session_id == session_id)
            .all()
        )

    @staticmethod
    def delete_history(
        db: Session,
        session_id: str
    ):

        chats = (
            db.query(ChatHistory)
            .filter(ChatHistory.session_id == session_id)
            .all()
        )

        for chat in chats:
            db.delete(chat)

        db.commit()