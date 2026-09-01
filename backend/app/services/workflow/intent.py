"""
Intent Detection Service
Updated for ITC India Website Chatbot
"""

from app.utils.constants import (
    GREETING,
    KNOWLEDGE,
    NEW_ENQUIRY,
    EXISTING_ENQUIRY,
)


class IntentService:

    GREETINGS = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening",
    ]

    NEW_ENQUIRY_KEYWORDS = [
        "new enquiry",
        "new query",
        "i'm a new",
        "i am a new",
        "first time",
        "quotation",
        "quote",
        "price",
        "testing",
        "test my product",
        "contact",
        "sales",
        "buy",
        "purchase",
    ]

    EXISTING_ENQUIRY_KEYWORDS = [
        "existing enquiry",
        "existing ticket",
        "existing query",
        "i have an existing",
        "already have",
        "follow up",
        "follow-up",
        "ticket status",
        "check ticket",
        "my ticket",
        "old query",
        "ongoing",
        "previous",
    ]

    def detect(self, message: str):

        message = message.lower().strip()

        # Greeting
        if any(word in message for word in self.GREETINGS):
            return GREETING

        # New Enquiry
        if any(word in message for word in self.NEW_ENQUIRY_KEYWORDS):
            return NEW_ENQUIRY

        # Existing Enquiry
        if any(word in message for word in self.EXISTING_ENQUIRY_KEYWORDS):
            return EXISTING_ENQUIRY

        # Default → Knowledge Base
        return KNOWLEDGE