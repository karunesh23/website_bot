from openai import OpenAI

from app.config import settings


class LLMService:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )

    def generate(
        self,
        prompt: str
    ) -> str:

        response = self.client.chat.completions.create(

            model=settings.LLM_MODEL,

            messages=[
                {
                    "role": "system",
                    "content": "You are an enterprise ITC assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=settings.TEMPERATURE,

            max_tokens=settings.MAX_OUTPUT_TOKENS
        )

        return response.choices[0].message.content