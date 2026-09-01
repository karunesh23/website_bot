from sqlalchemy.orm import Session

from app.models.chat_history import ChatHistory


class ConversationRepository:

    @staticmethod
    def get_history(
        db: Session,
        session_id: str,
        limit: int = 5
    ):

        history = (
            db.query(ChatHistory)
            .filter(ChatHistory.session_id == session_id)
            .order_by(ChatHistory.id.desc())
            .limit(limit)
            .all()
        )

        history.reverse()

        conversation = ""

        for chat in history:

            conversation += f"User: {chat.question}\n"

            conversation += f"Assistant: {chat.answer}\n\n"

        return conversation