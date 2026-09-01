"""
Prompt Builder Service

Builds the final prompt sent to the LLM.
"""

from app.prompts.system_prompt import SYSTEM_PROMPT
from app.prompts.rag_prompt import RAG_PROMPT


class PromptBuilder:

    def build_prompt(
        self,
        question: str,
        context: str,
        history: str = ""
    ) -> str:

        prompt = f"""
{SYSTEM_PROMPT}

=========================
Conversation History
=========================

{history}

=========================
Retrieved Knowledge
=========================

{context}

=========================
User Question
=========================

{question}

=========================
Instructions
=========================

{RAG_PROMPT}
"""

        return prompt

    # -----------------------------------------
    # Build prompt without history
    # -----------------------------------------

    def build_simple_prompt(
        self,
        question: str,
        context: str
    ) -> str:

        prompt = f"""
{SYSTEM_PROMPT}

Context:

{context}

Question:

{question}

Answer:
"""

        return prompt