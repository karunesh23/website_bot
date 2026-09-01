"""
Enterprise RAG Service

Pipeline

User Question
      │
      ▼
Conversation Memory
      │
      ▼
Retriever
      │
      ▼
Prompt Builder
      │
      ▼
Gemini LLM
      │
      ▼
Return Answer
"""

from sqlalchemy.orm import Session

from app.services.rag.retriever import RetrieverService
from app.services.rag.prompt_builder import PromptBuilder
from app.services.rag.llm import LLMService

from app.repositories.conversation_repository import ConversationRepository
from app.repositories.chat_repository import ChatRepository


class RagService:

    def __init__(self):

        self.retriever = RetrieverService()

        self.prompt_builder = PromptBuilder()

        self.llm = LLMService()

    # ---------------------------------------------------
    # Main Chat Function
    # ---------------------------------------------------

    def chat(
        self,
        db: Session,
        session_id: str,
        question: str
    ):

        # ---------------------------------------------
        # Load Previous Conversation
        # ---------------------------------------------

        history = ConversationRepository.get_history(
            db=db,
            session_id=session_id
        )

        # ---------------------------------------------
        # Retrieve Relevant Knowledge
        # ---------------------------------------------

        context = self.retriever.retrieve_context(
            db=db,
            question=question
        )

        # ---------------------------------------------
        # Build Prompt
        # ---------------------------------------------

        prompt = self.prompt_builder.build_prompt(
            question=question,
            context=context,
            history=history
        )

        # ---------------------------------------------
        # Generate Answer
        # ---------------------------------------------

        raw_answer = self.llm.generate(
            prompt=prompt
        )
        
        import re, json, ast
        options = []
        match = re.search(r'FOLLOWUP_OPTIONS:\s*(\[[^\]]+\])', raw_answer)
        if match:
            try:
                options = json.loads(match.group(1))
                raw_answer = raw_answer.replace(match.group(0), "").strip()
            except:
                try:
                    options = ast.literal_eval(match.group(1))
                    raw_answer = raw_answer.replace(match.group(0), "").strip()
                except:
                    pass

        # ---------------------------------------------
        # Save Chat History
        # ---------------------------------------------

        ChatRepository.save_chat(
            db=db,
            session_id=session_id,
            question=question,
            answer=raw_answer
        )

        return {"answer": raw_answer, "options": options}

    # ---------------------------------------------------
    # Ask Without History
    # ---------------------------------------------------

    def ask(
        self,
        db: Session,
        question: str
    ):

        context = self.retriever.retrieve_context(
            db=db,
            question=question
        )

        prompt = self.prompt_builder.build_simple_prompt(
            question=question,
            context=context
        )

        return self.llm.generate(prompt)

    # ---------------------------------------------------
    # Retrieve Context Only
    # ---------------------------------------------------

    def retrieve_context(
        self,
        db: Session,
        question: str
    ):

        return self.retriever.retrieve_context(
            db=db,
            question=question
        )