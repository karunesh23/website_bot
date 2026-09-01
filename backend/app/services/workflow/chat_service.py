"""
ITC India Website Chatbot
Conversation Flow based on official requirements
"""

from app.services.crm.lead import LeadService
from app.repositories.lead_repository import LeadRepository
from app.repositories.ticket_repository import TicketRepository
from app.models.lead import Lead
from app.services.crm.ticket import TicketService
from app.services.rag.rag_service import RagService
from app.services.workflow.conversation import ConversationManager
from app.services.workflow.intent import IntentService
from app.utils.constants import (
    GREETING,
    KNOWLEDGE,
    NEW_ENQUIRY,
    EXISTING_ENQUIRY,
    FOLLOW_UP_TICKET,
    RAISE_NEW_TICKET,
    TICKET_CREATED,
    LEAD_CREATED,
    CALLBACK_SCHEDULED,
    SERVICE_OPTIONS,
    SERVICE_INFO,
    CALLBACK_OPTIONS,
    WELCOME_MSG,
    INTRO_MSG,
    GREETING_OPTIONS,
    SCHEDULE_CALL_MSG,
    POST_SUBMIT_OPTIONS,
    POST_CALL_SCHEDULED_OPTIONS,
)
from app.utils.helpers import (
    clean_text,
    validate_email,
    validate_contact_info,
    validate_phone,
    normalize_phone,
    EMAIL_SEARCH_REGEX,
)

import requests

conversation_manager = ConversationManager()


class ChatWorkflowService:

    def __init__(self):
        self.intent_service = IntentService()
        self.rag_service = RagService()
        self.lead_service = LeadService()
        self.ticket_service = TicketService()

    def process(self, db, session_id: str, message: str) -> dict:
        message = clean_text(message)
        state = conversation_manager.get(session_id)

        if state is None:
            return self._start_flow(db, session_id, message)

        flow = state["flow"]

        if flow == GREETING:
            return self._handle_greeting(db, session_id, message, state)

        if flow == KNOWLEDGE:
            return self._handle_fallback(db, session_id, message)

        if flow == NEW_ENQUIRY:
            return self._handle_new_enquiry(db, session_id, message, state)

        if flow == EXISTING_ENQUIRY:
            return self._handle_existing_enquiry(db, session_id, message, state)

        if flow == FOLLOW_UP_TICKET:
            return self._handle_follow_up_ticket(db, session_id, message, state)

        if flow == RAISE_NEW_TICKET:
            return self._handle_raise_new_ticket(db, session_id, message, state)

        if flow == CALLBACK_SCHEDULED:
            return self._handle_schedule_call(db, session_id, message, state)

        if flow == "SERVICE_INFO":
            service_sub_options = ["key standards", "key tests", "quality issues"]
            if any(opt in message.lower() for opt in service_sub_options):
                selected_service = state.get("data", {}).get("selected_service")
                if selected_service:
                    return self._service_detail_response(db, session_id, selected_service, message)
            return self._handle_fallback(db, session_id, message)

        if not message:
            conversation_manager.start(session_id, GREETING)
            return self._start_flow(db, session_id, "")

        service = self._match_service(message)
        if service:
            return self._service_response(db, session_id, service)

        return self._handle_fallback(db, session_id, message)

    # =========================================================
    # 1. ENTRY POINT - ONBOARDING + ROUTING
    # =========================================================
    def _start_flow(self, db, session_id: str, message: str = "") -> dict:
        lower = message.lower()

        # Post-submission follow-ups
        if "schedule a call" in lower or "schedule" in lower and "call" in lower:
            conversation_manager.start(session_id, CALLBACK_SCHEDULED)
            conversation_manager.set_step(session_id, "select_time")
            return {
                "answer": "When would you like our team to call you?",
                "intent": CALLBACK_SCHEDULED,
                "step": "select_time",
                "options": CALLBACK_OPTIONS,
            }

        if "that's all" in lower or "thank you" in lower or "no, that" in lower:
            conversation_manager.start(session_id, GREETING)
            return {
                "answer": (
                    "You're welcome! 😊 If you need anything else, feel free to ask.\n\n"
                    "You can explore our **services** below, raise a **new query** or "
                    "track an **existing query** anytime."
                ),
                "intent": GREETING,
                "options": POST_SUBMIT_OPTIONS,
            }

        if "connect me with the team" in lower or "connect with the team" in lower:
            from app.repositories.lead_repository import LeadRepository
            state = conversation_manager.get(session_id)
            matched_lead_id = state.get("data", {}).get("matched_lead_id") if state else None
            
            if matched_lead_id:
                lead = db.query(Lead).filter(Lead.id == matched_lead_id).first()
            else:
                lead = LeadRepository.get_by_session_id(db, session_id)
            
            if lead and lead.phone and lead.name and lead.name.lower() != "unknown":
                from app.services.crm.ticket import TicketRepository
                ticket = TicketRepository.get_latest_ticket_by_lead_id(db, lead.id)
                ticket_number = ticket.ticket_number if ticket else ""
                
                self._trigger_n8n_webhook(lead.phone, lead.name, lead.email or "", ticket_number)
                
                conversation_manager.to_knowledge(session_id)
                return {
                    "answer": f"**Got it, {lead.name}!**\n\nOur team has been notified and will call you on your registered number (**{lead.phone}**) shortly.\n\n**Meanwhile, feel free to explore our services below or type your query.**",
                    "intent": KNOWLEDGE,
                    "options": ["New Customer", "Existing Customer"],
                }
            else:
                conversation_manager.start(session_id, GREETING)
                conversation_manager.set_step(session_id, "gcontact")
                return {
                    "answer": "I'll connect you with our support team. Before we proceed, could you please share your **Full Name**?",
                    "intent": GREETING,
                    "step": "gcontact",
                }

        if (
            "new query" in lower
            or "new enquiry" in lower
            or "new enquir" in lower
            or "another enquiry" in lower
            or "another query" in lower
        ):
            conversation_manager.start(session_id, NEW_ENQUIRY)
            return self._handle_new_enquiry(
                db=db,
                session_id=session_id,
                message=message,
                state={"step": None, "data": {}},
            )

        is_knowledge_question = any(kw in lower for kw in ["what is", "what are", "how", "why", "explain", "tell me about"]) or "?" in message
        if is_knowledge_question and not any(kw in lower for kw in ["quote", "price", "cost", "new enquiry", "new query"]):
            conversation_manager.start(session_id, KNOWLEDGE)
            return self._handle_fallback(db, session_id, message)

        if "new issue" in lower or "raise a new issue" in lower or "new ticket" in lower or "raise a new ticket" in lower:
            conversation_manager.start(session_id, RAISE_NEW_TICKET)
            conversation_manager.set_step(session_id, "description")
            return {
                "answer": "Could you describe the issue or request in a few words?",
                "intent": RAISE_NEW_TICKET,
                "step": "description",
            }

        if "existing" in lower:
            conversation_manager.start(session_id, EXISTING_ENQUIRY)
            return self._handle_existing_enquiry(
                db=db,
                session_id=session_id,
                message=message,
                state={"step": None, "data": {}},
            )

        service_sub_options = ["key standards", "key tests", "quality issues"]
        if any(opt in lower for opt in service_sub_options):
            state = conversation_manager.get(session_id)
            selected_service = state.get("data", {}).get("selected_service") if state else None
            if selected_service:
                return self._service_detail_response(db, session_id, selected_service, message)

        service = self._match_service(message)
        if service:
            return self._service_response(db, session_id, service)

        # Default: friendly onboarding (ask name + email -> intro -> buttons)
        conversation_manager.start(session_id, GREETING)
        conversation_manager.set_step(session_id, "gcontact")

        if message.strip():
            state = conversation_manager.get(session_id)
            return self._handle_greeting(None, session_id, message, state)

        return {
            "answer": WELCOME_MSG,
            "intent": GREETING,
            "step": "gcontact",
        }

    # =========================================================
    # 1B. GREETING ONBOARDING
    # =========================================================
    def _handle_greeting(self, db, session_id: str, message: str, state: dict) -> dict:
        step = state.get("step")

        if step is None or step == "gcontact":
            data = state["data"]
            name = data.get("name", "")
            email = data.get("email", "")
            lower_msg = message.lower().strip()

            # If the user is asking a knowledge/service question, don't force onboarding now.
            is_knowledge_question = any(kw in lower_msg for kw in ["what is", "what are", "how", "why", "explain", "tell me about"]) or "?" in message
            if is_knowledge_question and not any(kw in lower_msg for kw in ["quote", "price", "cost", "new enquiry", "new query"]):
                conversation_manager.start(session_id, KNOWLEDGE)
                
                # Save query to CRM Lead
                if name and email:
                    from app.repositories.lead_repository import LeadRepository
                    lead = LeadRepository.get_by_session_id(db, session_id)
                    if not lead:
                        lead = LeadRepository.get_by_email(db, email)
                        if not lead:
                            lead = LeadRepository.create(
                                db=db,
                                name=name,
                                email=email,
                                phone="",
                                service="Chat Enquiry",
                                purpose=message,
                                session_id=session_id
                            )
                    if lead:
                        LeadRepository.update(
                            db=db,
                            lead_id=lead.id,
                            name=lead.name,
                            email=lead.email,
                            phone=lead.phone,
                            service=lead.service,
                            purpose=message,
                            session_id=session_id
                        )

                rag_response = self.rag_service.chat(db=db, session_id=session_id, question=message)
                rag_opts = rag_response.get("options", []) if isinstance(rag_response, dict) else []
                raw_answer = rag_response.get("answer", rag_response) if isinstance(rag_response, dict) else rag_response
                
                from app.repositories.lead_repository import LeadRepository
                lead = LeadRepository.get_by_session_id(db, session_id)
                user_name = lead.name if lead and lead.name and lead.name.lower() != "unknown" else ""
                if not user_name:
                    user_name = conversation_manager.get(session_id).get("data", {}).get("name", "")
                    
                name_str = f"**Got it, {user_name}!**\n\n" if user_name and user_name.lower() != "unknown" else "**Got it!**\n\n"
                
                footer_text = "\n\n**Feel free to click any of the questions below to explore further, or select 'Request a Callback' to speak directly with our team!**"
                return {
                    "answer": name_str + raw_answer + footer_text,
                    "intent": KNOWLEDGE,
                    "options": rag_opts + ["New Customer", "Existing Customer"],
                }

            service = self._match_service(message)
            if service:
                conversation_manager.start(session_id, KNOWLEDGE)
                # For explicit service name matches, prefer the service flow (may return service-specific options).
                return self._service_response(db, session_id, service)

            # Handle "connect me with the team" explicit bypass
            if "connect me with the team" in lower_msg or "connect with the team" in lower_msg:
                if not name:
                    return {
                        "answer": "I'll connect you with our support team. Before we proceed, could you please share your **Full Name**?",
                        "intent": GREETING,
                        "step": "gcontact",
                    }
                if not email:
                    return {
                        "answer": f"I'll connect you with our support team, **{name}**. Could you please share your **email address** so we can keep you updated?",
                        "intent": GREETING,
                        "step": "gcontact",
                        "onboarding": {"name": name}
                    }

            if not name:
                import re
                
                # Check for email in case they provided it early, we can save it for later
                email_match = EMAIL_SEARCH_REGEX.search(message)
                if email_match and validate_email(email_match.group(0).strip()):
                    conversation_manager.save(session_id, "email", email_match.group(0).strip())
                
                cleaned_name = message
                if email_match:
                    cleaned_name = cleaned_name.replace(email_match.group(0), " ")
                    
                if re.search(r"(?i)\b(my name\s*is|name\s*is|myself)\s+", cleaned_name):
                    cleaned_name = re.split(r"(?i)\b(?:my name\s*is|name\s*is|myself)\s+", cleaned_name)[-1]
                elif re.search(r"(?i)\b(i am|this is|i'm|im|call me)\s+", cleaned_name):
                    cleaned_name = re.split(r"(?i)\b(?:i am|this is|i'm|im|call me)\s+", cleaned_name)[-1]

                cleaned_name = re.sub(r"(?i)\s*(and\s+)?(my\s+)?(email|mail|gmail|phone|number|contact|mobile|ph)( is|'s)?\s*.*$", "", cleaned_name).strip(" ,;:_-")
                cleaned_name = re.sub(r"(?i)^(?:(?:\bhi\b|\bhello\b|\bhii\b|\bhey\b|\bgood\s+morning\b|\bgood\s+evening\b|\bgood\s+afternoon\b|\bgood\s+day\b)\s*,?\s*)+", "", cleaned_name)
                cleaned_name = re.sub(r"\s+", " ", cleaned_name).strip()

                # If the user separated name and email with a comma, take the first part as name
                provided_parts = [p.strip() for p in cleaned_name.split(",") if p.strip()]
                has_multiple_parts = len(provided_parts) > 1
                if has_multiple_parts:
                    cleaned_name = provided_parts[0]

                lower_name = cleaned_name.lower().strip()
                is_greeting = lower_name in ["hi", "hello", "hii", "hey", "good morning", "good evening", "thanks", "ok", "okay", "thank you", "bye"]

                # Heuristic: accept a name only when it looks like a short alpha name
                # (up to 4 words/parts, allowing spaces, dots, hyphens), does not contain common question/command words,
                # and is not a multi-word sentence or a question.
                name_candidate_re = re.compile(r"^[A-Za-z]+(?:[ .-]+[A-Za-z]+){0,3}$")
                forbidden_words = {"tell","about","services","service","help","how","what","where","who","when","price","cost","details","information","please","no","yes","nope","yeah","yep","sure"}
                contains_forbidden = any(w in re.findall(r'\b\w+\b', lower_name) for w in forbidden_words)
                is_valid_alpha = bool(name_candidate_re.match(cleaned_name)) and not contains_forbidden and "?" not in message and len(cleaned_name) >= 2

                if is_greeting or not message.strip():
                    from app.utils.constants import WELCOME_MSG
                    return {
                        "answer": WELCOME_MSG,
                        "intent": GREETING,
                        "step": "gcontact",
                    }
                
                if not is_valid_alpha:
                    saved_email = conversation_manager.get(session_id)["data"].get("email")
                    if saved_email:
                        return {
                            "answer": "Thank you for providing your **EMAIL**! Could you please share your **NAME**?",
                            "intent": GREETING,
                            "step": "gcontact",
                        }
                    else:
                        return {
                            "answer": "Please enter your **NAME** and **EMAIL** so that I can address you properly.",
                            "intent": GREETING,
                            "step": "gcontact",
                        }
                
                # Valid name provided
                name = cleaned_name
                conversation_manager.save(session_id, "name", name)
                
                # Re-fetch email from state in case it was just saved above
                email = conversation_manager.get(session_id)["data"].get("email", "")

                if not email:
                    error_msg = "It looks like the email address you provided isn't valid. Could you please share a valid email address?" if has_multiple_parts or "@" in message else "Could you please share your **email address** so we can keep you updated?"
                    return {
                        "answer": (
                            f"Nice to meet you, **{name}**! 😊\n\n"
                            f"{error_msg}"
                        ),
                        "intent": GREETING,
                        "step": "gcontact",
                        "onboarding": {"name": name}
                    }

            if not email:
                email_match = EMAIL_SEARCH_REGEX.search(message)
                email_from_msg = email_match.group(0).strip() if email_match else ""
                
                if email_from_msg and validate_email(email_from_msg):
                    email = email_from_msg
                    conversation_manager.save(session_id, "email", email)
                else:
                    return {
                        "answer": (
                            f"To ensure we can reach you with updates, "
                            "could you please provide a valid email address (e.g., name@example.com)?"
                        ) if "email" in message.lower() else (
                            f"Could you please share your **email address** so we can keep you updated?"
                        ),
                        "intent": GREETING,
                        "step": "gcontact",
                        "onboarding": {"name": name}
                    }

            conversation_manager.set_step(session_id, "new_or_existing")
            return {
                "answer": INTRO_MSG.format(name=name),
                "intent": GREETING,
                "step": "new_or_existing",
                "options": GREETING_OPTIONS,
                "onboarding": {"name": name, "email": email},
            }

        if step == "new_or_existing":
            lower = message.lower()
            if "new" in lower and "existing" not in lower:
                conversation_manager.start(session_id, NEW_ENQUIRY)
                return self._handle_new_enquiry(
                    db, session_id, message, {"step": None, "data": state["data"]}
                )
            if "existing" in lower:
                conversation_manager.start(session_id, EXISTING_ENQUIRY)
                return self._handle_existing_enquiry(
                    db, session_id, message, {"step": None, "data": state["data"]}
                )
            conversation_manager.to_knowledge(session_id)
            return self._handle_fallback(db, session_id, message)

        return self._handle_fallback(db, session_id, message)

    # =========================================================
    # 2. NEW ENQUIRY FLOW (Flow A)
    # =========================================================
    def _handle_new_enquiry(self, db, session_id: str, message: str, state: dict) -> dict:
        step = state.get("step")

        # Allow the user to cancel / reset the enquiry at any point
        lower_msg = message.lower().strip(".!?, \n\t")
        if (
            lower_msg in ("cancel", "cancel enquiry", "cancel form", "reset", "no, that's all", "that's all", "no that all", "bye", "goodbye", "no that's all", "thanks", "thank you")
            or "don't want" in lower_msg
            or "dont want" in lower_msg
            or "cancel" in lower_msg
        ):
            conversation_manager.to_knowledge(session_id)
            return self._handle_fallback(db, session_id, lower_msg)

        # Start of New Enquiry
        if step is None:
            state_data = conversation_manager.get(session_id).get("data", {})
            if not state_data.get("is_existing_customer"):
                conversation_manager.save(session_id, "is_new_customer", True)

            conversation_manager.set_step(session_id, "name")
            return {
                "answer": "Let's get started. Could you please provide your **Full Name**?",
                "intent": NEW_ENQUIRY,
                "step": "name",
            }

        if step == "name":
            import re
            cleaned_name = re.sub(r"^.*?(my name is|i am|this is|name is|i'm|im|call me)\s+", "", message, flags=re.IGNORECASE)
            cleaned_name = re.sub(r"(?i)\s*(and\s+)?(my\s+)?(email|mail|gmail|phone|number|contact|mobile|ph)( is|'s)?\s*.*$", "", cleaned_name).strip(" ,;:_-")

            # Similar strict name detection for new-enquiry flow: require short alpha-only names
            name_candidate_re = re.compile(r"^[A-Za-z]+(?: [A-Za-z]+){0,2}$")
            lower_clean = cleaned_name.lower().strip()
            forbidden_words = {"tell","about","services","service","help","how","what","where","who","when","price","cost","details","information","please","no","yes","nope","yeah","yep","sure"}
            contains_forbidden = any(w in re.findall(r'\b\w+\b', lower_clean) for w in forbidden_words)
            is_greeting = lower_clean in ["hello", "hi", "hey", "good morning", "good evening", "thanks", "ok", "okay", "thank you", "bye"]
            is_valid = bool(name_candidate_re.match(cleaned_name)) and not contains_forbidden and "?" not in cleaned_name

            if not is_valid or is_greeting:
                return {
                    "answer": "Please enter a valid **full name** (only alphabetic characters and spaces).",
                    "intent": NEW_ENQUIRY,
                    "step": "name",
                }

            conversation_manager.save(session_id, "name", cleaned_name)
            conversation_manager.set_step(session_id, "email")
            return {
                "answer": f"Thanks, **{cleaned_name}**!\n\nPlease share your **email address**.",
                "intent": NEW_ENQUIRY,
                "step": "email",
            }

        if step == "email":
            if not validate_email(message):
                return {
                    "answer": (
                        "That doesn't look like a valid email address.\n\n"
                        "Please enter a valid email like **user@gmail.com**."
                    ),
                    "intent": NEW_ENQUIRY,
                    "step": "email",
                }
            conversation_manager.save(session_id, "email", message.strip())
            conversation_manager.set_step(session_id, "phone")
            return {
                "answer": "Please share your **phone number**.",
                "intent": NEW_ENQUIRY,
                "step": "phone",
            }

        if step == "phone":
            if not validate_phone(message):
                return {
                    "answer": (
                        "Please enter a valid **phone number** (7-15 digits).\n"
                        "For international numbers include your country code "
                        "first, e.g., **+98 912 345 6789**."
                    ),
                    "intent": NEW_ENQUIRY,
                    "step": "phone",
                }
            conversation_manager.save(session_id, "phone", normalize_phone(message))
            conversation_manager.set_step(session_id, "category")
            return {
                "answer": "What can we help you with today?",
                "intent": NEW_ENQUIRY,
                "step": "category",
                "options": SERVICE_OPTIONS,
            }

        if step == "category":
            conversation_manager.save(session_id, "category", message)
            conversation_manager.set_step(session_id, "notes")
            return {
                "answer": "Please briefly describe your product or requirement (you can also skip this).",
                "intent": NEW_ENQUIRY,
                "step": "notes",
                "options": ["Skip"],
            }

        if step == "notes":
            if message.lower() != "skip":
                conversation_manager.save(session_id, "notes", message)
            else:
                conversation_manager.save(session_id, "notes", "")

            conversation_manager.set_step(session_id, "callback_time")
            return {
                "answer": "When would you like our team to call you?",
                "intent": NEW_ENQUIRY,
                "step": "callback_time",
                "options": CALLBACK_OPTIONS,
            }

        if step == "callback_time":
            conversation_manager.save(session_id, "callback_time", message)
            data = state["data"]
            conversation_manager.set_step(session_id, "confirm")
            return self._show_confirmation(data)

        # ========== CONFIRM / EDIT ==========
        if step == "confirm":
            lower = message.lower()

            if "yes" in lower or "arrange" in lower:
                data = state["data"]

                lead = self.lead_service.create_lead(
                    db=db,
                    name=data.get("name", "Unknown"),
                    email=data.get("email", ""),
                    phone=data.get("phone", ""),
                    service=data.get("category", "General"),
                    product_name=data.get("product_name", ""),
                    purpose=data.get("purpose", ""),
                    scope=data.get("scope", ""),
                    notes=data.get("notes", ""),
                    session_id=session_id
                )

                conversation_manager.to_knowledge(session_id)

                return {
                    "answer": (
                        f"All set! Our team will call you on **{data.get('phone')}** "
                        f"({data.get('callback_time')}).\n\n"
                        f"Your reference number is **{lead.get('lead_id', 'N/A')}**.\n\n"
                        "Thank you for choosing ITC India!"
                    ),
                    "intent": CALLBACK_SCHEDULED,
                    "options": ["I have another enquiry", "That's all, thank you"],
                }

            elif "edit" in lower:
                conversation_manager.set_step(session_id, "edit_choice")
                return {
                    "answer": "Which detail would you like to edit?",
                    "intent": NEW_ENQUIRY,
                    "step": "edit_choice",
                    "options": [
                        "Edit Name",
                        "Edit Email",
                        "Edit Phone",
                        "Edit Interest",
                        "Edit Preferred Time",
                        "Go back",
                    ],
                }

            else:
                conversation_manager.to_knowledge(session_id)
                return {
                    "answer": "Understood. Your details have not been submitted.\nFeel free to start again anytime.",
                    "intent": GREETING,
                    "options": [
                        "New Customer",
                        "Existing Customer",
                    ],
                }

        # ========== EDIT CHOICE ==========
        if step == "edit_choice":
            lower = message.lower()

            if "name" in lower:
                conversation_manager.set_step(session_id, "edit_name")
                return {
                    "answer": "Please enter the new **name**.",
                    "intent": NEW_ENQUIRY,
                    "step": "edit_name",
                }
            elif "email" in lower:
                conversation_manager.set_step(session_id, "edit_email")
                return {
                    "answer": "Please enter the new **email address**.",
                    "intent": NEW_ENQUIRY,
                    "step": "edit_email",
                }
            elif "phone" in lower:
                conversation_manager.set_step(session_id, "edit_phone")
                return {
                    "answer": "Please enter the new **phone number**.",
                    "intent": NEW_ENQUIRY,
                    "step": "edit_phone",
                }
            elif "interest" in lower or "category" in lower:
                conversation_manager.set_step(session_id, "edit_category")
                return {
                    "answer": "Please select the new interest area.",
                    "intent": NEW_ENQUIRY,
                    "step": "edit_category",
                    "options": SERVICE_OPTIONS,
                }
            elif "time" in lower or "preferred" in lower:
                conversation_manager.set_step(session_id, "edit_callback_time")
                return {
                    "answer": "Please select the new preferred time.",
                    "intent": NEW_ENQUIRY,
                    "step": "edit_callback_time",
                    "options": CALLBACK_OPTIONS,
                }
            else:
                data = state["data"]
                conversation_manager.set_step(session_id, "confirm")
                return self._show_confirmation(data)

        # ========== APPLY EDIT ==========
        if step == "edit_name":
            import re
            cleaned_name = re.sub(r"^.*?(my name is|i am|this is|name is|i'm|im|call me)\s+", "", message, flags=re.IGNORECASE)
            cleaned_name = re.sub(r"(?i)\s*(and\s+)?(my\s+)?(email|mail|gmail|phone|number|contact|mobile|ph)( is|'s)?\s*.*$", "", cleaned_name).strip(" ,;:_-")
            conversation_manager.save(session_id, "name", cleaned_name)
            conversation_manager.set_step(session_id, "confirm")
            data = conversation_manager.get(session_id)["data"]
            return self._show_confirmation(data)

        if step == "edit_email":
            if not validate_email(message):
                return {
                    "answer": (
                        "That doesn't look like a valid email address.\n\n"
                        "Please enter a valid email like **user@gmail.com**."
                    ),
                    "intent": NEW_ENQUIRY,
                    "step": "edit_email",
                }
            conversation_manager.save(session_id, "email", message.strip())
            conversation_manager.set_step(session_id, "confirm")
            data = conversation_manager.get(session_id)["data"]
            return self._show_confirmation(data)

        if step == "edit_phone":
            if not validate_phone(message):
                return {
                    "answer": (
                        "Please enter a valid **phone number** (7-15 digits).\n"
                        "For international numbers include your country code "
                        "first, e.g., **+98 912 345 6789**."
                    ),
                    "intent": NEW_ENQUIRY,
                    "step": "edit_phone",
                }
            conversation_manager.save(session_id, "phone", normalize_phone(message))
            conversation_manager.set_step(session_id, "confirm")
            data = conversation_manager.get(session_id)["data"]
            return self._show_confirmation(data)

        if step == "edit_category":
            conversation_manager.save(session_id, "category", message)
            conversation_manager.set_step(session_id, "confirm")
            data = conversation_manager.get(session_id)["data"]
            return self._show_confirmation(data)

        if step == "edit_callback_time":
            conversation_manager.save(session_id, "callback_time", message)
            conversation_manager.set_step(session_id, "confirm")
            data = conversation_manager.get(session_id)["data"]
            return self._show_confirmation(data)

        return self._handle_fallback(db, session_id, message)

    def _show_confirmation(self, data: dict) -> dict:
        return {
            "answer": (
                f"Please confirm your details:\n\n"
                f"• **Name**: {data.get('name')}\n"
                f"• **Email**: {data.get('email')}\n"
                f"• **Phone**: {data.get('phone')}\n"
                f"• **Interest**: {data.get('category')}\n"
                f"• **Preferred time**: {data.get('callback_time')}\n\n"
                f"Shall I arrange a callback from our team?"
            ),
            "intent": NEW_ENQUIRY,
            "step": "confirm",
            "options": [
                "Yes, arrange callback",
                "Cancel",
            ],
        }

    # =========================================================
    # 2B. NEW ENQUIRY VIA FORM (single submission)
    # =========================================================
    def _match_service(self, message: str):
        lower = (message or "").lower().strip()

        for name in SERVICE_OPTIONS:
            if lower == name.lower():
                return name

        return None

    def _service_response(self, db, session_id: str, service: str) -> dict:
        conversation_manager.start(session_id, "SERVICE_INFO")
        conversation_manager.save(session_id, "selected_service", service)
        from app.utils.constants import SERVICE_INFO
        service_data = SERVICE_INFO.get(service, "")
        
        description_prompt = (
            f"Provide a brief description of the {service} offered by ITC India. "
            f"Here is the accurate factual data to use:\n{service_data}\n\n"
            f"Format your response as exactly 3 very brief, 1-sentence paragraphs based ONLY on the data provided. Do not add any extra explanations or fluff. "
            f"Do not use bullet points or any leading symbols. ONLY bold specific testing standards (e.g., IEC 60335, ISO, etc.). Do not bold any other words. "
            f"Separate each paragraph with a blank line (\\n\\n). Do NOT write an introductory paragraph."
        )
        try:
            description = self.rag_service.llm.generate(description_prompt).strip()
        except Exception:
            description = (
                f"We offer comprehensive {service} to ensure your products meet all required safety standards.\n\n"
                f"Our expert team provides detailed testing and certification for international markets.\n\n"
                f"We guarantee reliable results to help you achieve full compliance."
            )
            
        from app.repositories.lead_repository import LeadRepository
        lead = LeadRepository.get_by_session_id(db, session_id)
        
        # Try to get name from lead first, then fallback to conversation manager state
        user_name = lead.name if lead and lead.name and lead.name.lower() != "unknown" else ""
        if not user_name:
            user_name = conversation_manager.get(session_id).get("data", {}).get("name", "")
            
        name_str = f", {user_name}" if user_name and user_name.lower() != "unknown" else ""
        prefix = f"**Got it{name_str}!**\n\n"
        suffix = f"\n\nWould you like to know more about **Key Standards, Key Tests, or Quality Issues** related to {service}?\n\n**Or else if you need further assistance, you can also request a callback from our ITC India team. Our team will be happy to understand your requirements and assist you further.**"
        
        final_answer = prefix + description + suffix
        
        return {
            "answer": final_answer,
            "intent": "SERVICE_INFO",
            "options": ["Key Standards", "Key Tests", "Quality Issues", "Request a Callback"]
        }

    def _service_detail_response(self, db, session_id: str, service: str, detail_type: str) -> dict:
        import json
        prompt = f"""
        You are an AI assistant for ITC India. A user has asked about "{detail_type}" for the service "{service}".
        Retrieve the relevant information from your knowledge base and format it as a JSON object.
        
        The JSON object must have the following structure:
        {{
            "title": "{detail_type}",
            "data": [
                {{"column1": "Value1", "column2": "Value2"}},
                {{"column1": "Value3", "column2": "Value4"}}
            ],
            "follow_up_questions": ["Question 1?", "Question 2?", "Question 3?"]
        }}
        
        Use up to 3 columns if needed (e.g., column1, column2, column3). Make sure the keys are column1, column2, etc.
        Generate 2-3 relevant follow-up questions a user might ask based on this information.
        Return ONLY valid JSON and nothing else. No markdown formatting like ```json.
        """
        try:
            response = self.rag_service.llm.generate(prompt).strip()
            # Remove markdown backticks if present
            if response.startswith("```json"):
                response = response[7:]
            if response.endswith("```"):
                response = response[:-3]
                
            data = json.loads(response.strip())
            options = data.get("follow_up_questions", []) + ["Request a Callback"]
            
            from app.repositories.lead_repository import LeadRepository
            lead = LeadRepository.get_by_session_id(db, session_id)
            user_name = lead.name if lead and lead.name and lead.name.lower() != "unknown" else ""
            if not user_name:
                user_name = conversation_manager.get(session_id).get("data", {}).get("name", "")
                
            name_str = f"**{user_name}!** " if user_name and user_name.lower() != "unknown" else ""
            
            return {
                "answer": f"{name_str}here is the information about {detail_type} for {service}:",
                "footer": "**Feel free to click any of the questions below to explore further, or select 'Request a Callback' to speak directly with our team!**",
                "intent": "SERVICE_DETAIL",
                "service_table": data,
                "options": options
            }
        except Exception as e:
            print(f"Error in _service_detail_response: {e}")
            print(f"LLM Response was: {response if 'response' in locals() else 'None'}")
            return self._handle_fallback(db, session_id, f"What are the {detail_type} for {service}?")

    def submit_enquiry(self, db, session_id: str, data: dict, background_tasks=None) -> dict:
        state = conversation_manager.get(session_id)
        if not state:
            from app.utils.constants import NEW_ENQUIRY
            conversation_manager.start(session_id, NEW_ENQUIRY)
            state = conversation_manager.get(session_id)

        from app.repositories.lead_repository import LeadRepository
        existing_lead = LeadRepository.get_by_session_id(db, session_id)

        is_edit = False
        if existing_lead:
            lead_result = self.lead_service.update_lead(
                db=db,
                lead_id=existing_lead.id,
                name=data.get("name", "Unknown"),
                email=data.get("email", ""),
                phone=data.get("phone", ""),
                service=data.get("service", "General"),
                product_name=data.get("product_name", ""),
                company_name=data.get("company_name", ""),
                purpose=data.get("purpose", ""),
                scope=data.get("scope", ""),
                notes=data.get("notes", ""),
                session_id=session_id
            )
            is_edit = lead_result.get("success", False)
            lead = lead_result

        if not is_edit:
            lead = self.lead_service.create_lead(
                db=db,
                name=data.get("name", "Unknown"),
                email=data.get("email", ""),
                phone=data.get("phone", ""),
                service=data.get("service", "General"),
                product_name=data.get("product_name", ""),
                company_name=data.get("company_name", ""),
                purpose=data.get("purpose", ""),
                scope=data.get("scope", ""),
                notes=data.get("notes", ""),
                session_id=session_id
            )

        # Create or Update Client
        from app.models.client import Client
        email = data.get("email", "")
        phone = data.get("phone", "")
        client = None
        if email:
            client = db.query(Client).filter(Client.email == email).first()
        elif phone:
            client = db.query(Client).filter(Client.phone == phone).first()
            
        client_type = "Existing Client" if state.get("data", {}).get("is_existing_customer") else "New Enquiry"
        
        if not client:
            client = Client(
                name=data.get("name", "Unknown"),
                email=email,
                phone=phone,
                company_name=data.get("company_name", ""),
                client_type=client_type
            )
            db.add(client)
            db.commit()
            db.refresh(client)
        else:
            client.name = data.get("name", "Unknown")
            client.client_type = client_type
            if data.get("company_name"):
                client.company_name = data.get("company_name")
            db.commit()

        conversation_manager.save(session_id, "last_lead_id", lead.get("lead_id"))

        # Apply client type based on flow history
        state_data = state.get("data", {})
        if state_data.get("is_existing_customer"):
            from app.repositories.lead_repository import LeadRepository
            LeadRepository.update_client_type_by_session(db, session_id, "Existing Client")
        elif state_data.get("is_new_customer"):
            from app.repositories.lead_repository import LeadRepository
            LeadRepository.update_client_type_by_session(db, session_id, "New Enquiry")

        conversation_manager.to_knowledge(session_id)

        name = data.get("name", "there")
        product_name = data.get("product_name") or "your product"
        notes = data.get("notes", "")

        if notes.startswith("Schedule a callback"):
            import datetime
            # Explicitly save Callback to DB
            from app.models.callback import Callback
            time_pref = data.get('callback_time', 'As soon as possible')
            new_cb = Callback(
                name=name,
                phone=data.get('phone', ''),
                email=data.get('email', ''),
                topic=data.get('service', 'General Callback'),
                requested_time=datetime.datetime.now(),
                status="Requested",
                lead_id=lead.get('lead_id') if str(lead.get('lead_id', '')).isdigit() else None,
                session_id=session_id
            )
            db.add(new_cb)
            db.commit()
            db.refresh(new_cb)
            ref_id = str(new_cb.id)
            
            # --- START N8N ESCALATION SIMULATION ---
            try:
                from app.models.call_log import CallLog
                from app.models.team_member import TeamMember
                import uuid
                
                team_members = db.query(TeamMember).order_by(TeamMember.id).limit(3).all()
                if len(team_members) >= 3:
                    tm1, tm2, tm3 = team_members[0], team_members[1], team_members[2]
                    base_time = datetime.datetime.now()
                    
                    cl1 = CallLog(
                        call_id=str(uuid.uuid4())[:8],
                        callback_id=new_cb.id,
                        member_id=tm1.id,
                        received_at=base_time,
                        picked=False,
                        escalated_to=tm2.id,
                        outcome="Escalated",
                        duration_seconds=0,
                        call_summary="No answer, escalated to Level 2"
                    )
                    
                    cl2 = CallLog(
                        call_id=str(uuid.uuid4())[:8],
                        callback_id=new_cb.id,
                        member_id=tm2.id,
                        received_at=base_time + datetime.timedelta(minutes=10),
                        picked=False,
                        escalated_to=tm3.id,
                        outcome="Escalated",
                        duration_seconds=0,
                        call_summary="No answer, escalated to Level 3"
                    )
                    
                    cl3 = CallLog(
                        call_id=str(uuid.uuid4())[:8],
                        callback_id=new_cb.id,
                        member_id=tm3.id,
                        received_at=base_time + datetime.timedelta(minutes=20),
                        picked=True,
                        picked_at=base_time + datetime.timedelta(minutes=21),
                        escalated_to=None,
                        outcome="Connected",
                        duration_seconds=180,
                        call_summary=f"Client requested a follow-up regarding {data.get('service', 'General Enquiry')}."
                    )
                    
                    db.add_all([cl1, cl2, cl3])
                    db.commit()
            except Exception as e:
                print(f"Error simulating n8n escalation: {e}")
            # --- END N8N ESCALATION SIMULATION ---
            
            if background_tasks:
                background_tasks.add_task(
                    self._trigger_n8n_webhook,
                    phone=data.get('phone', ''),
                    name=data.get('name', ''),
                    email=data.get('email', ''),
                    ticket_number=ref_id
                )
                
            answer = (
                f"Thank you, **{name}**! 🎉\n\n"
                f"Your callback request has been submitted successfully.\n"
                f"**Request Details**\n"
                f"• **Callback ID**: {ref_id}\n\n"
                f"Our technical team will review your request and contact you on your registered phone number or email at the earliest available time.\n\n"
                f"If you have any additional questions in the meantime, feel free to ask. 😊"
            )
            ticket_number = ref_id
            options = POST_CALL_SCHEDULED_OPTIONS
        else:
            lead_id = lead.get('lead_id') if str(lead.get('lead_id', '')).isdigit() else None
            
            if lead_id is not None:
                from app.repositories.ticket_repository import TicketRepository
                import random
                # Temporary number to satisfy unique constraint before flush
                temp_ticket_number = str(random.randint(100000, 999999))
                existing_ticket = TicketRepository.get_ticket(db, temp_ticket_number)
                if not existing_ticket:
                    issue_text = data.get('purpose') or f"{data.get('service')} Enquiry"
                    category = self._classify_category(issue_text)
                    ticket = TicketRepository.create(
                        db=db,
                        ticket_number=temp_ticket_number,
                        lead_id=lead_id,
                        issue=issue_text,
                        status="OPEN",
                        category=category
                    )
                    
                    # Update ticket_number to match its own ID (which starts at 10, so two digits)
                    ticket.ticket_number = str(ticket.id)
                    db.commit()
                    db.refresh(ticket)
                    ticket_number = ticket.ticket_number
                    
                    if background_tasks:
                        background_tasks.add_task(
                            self._trigger_n8n_webhook,
                            phone=data.get('phone', ''),
                            name=data.get('name', ''),
                            email=data.get('email', ''),
                            ticket_number=ticket_number
                        )
            else:
                ticket_number = "10" # Fallback

            action_word = "updated" if is_edit else "submitted"
            answer = (
                f"Perfect, **{name}**! 🎉 Your service request has been {action_word} successfully.\n\n"
                f"✅ **Ticket Number**: **{ticket_number}**\n\n"
                f"**Our team will contact you on your registered number shortly.**\n"
                f"You can got the **Ticket Number** while interacting with **ITC INDIA Compliance Team**\n\n"
                f"**Meanwhile, feel free to explore our services below or type your query.**"
            )
            options = POST_SUBMIT_OPTIONS

        return {
            "answer": answer,
            "intent": LEAD_CREATED,
            "ticket_number": ticket_number,
            "options": options,
        }

    def _trigger_n8n_webhook(self, phone: str, name: str, email: str = "", ticket_number: str = ""):
        if not phone:
            return
            
        # Ensure the phone number has a country code (+91) for Plivo
        phone_digits = ''.join(filter(str.isdigit, phone))
        if len(phone_digits) == 10:
            phone = f"+91{phone_digits}"
        elif phone_digits.startswith("91") and len(phone_digits) == 12:
            phone = f"+{phone_digits}"
        elif not phone.startswith("+"):
            phone = f"+91{phone_digits}"
            
        try:
            
            url = "https://damnart-ai-guladab.n8n-wsk.com/webhook/website_chatbot"
            payload = {
                "phone": phone,
                "name": name,
                "email": email,
                "ticket_number": ticket_number
            }
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            # Silently handle webhook failure to not disrupt the main flow
            print(f"Error triggering n8n webhook: {e}")

    # =========================================================
    # 3. EXISTING ENQUIRY FLOW (Flow B)
    # =========================================================
    def _handle_existing_enquiry(self, db, session_id: str, message: str, state: dict) -> dict:
        step = state.get("step")

        if step is None:
            conversation_manager.save(session_id, "is_existing_customer", True)
            
            conversation_manager.start(session_id, FOLLOW_UP_TICKET)
            conversation_manager.set_step(session_id, "lookup")
            return {
                "answer": "Welcome back! Could you please share your **company name**?",
                "intent": FOLLOW_UP_TICKET,
                "step": "lookup"
            }

        return self._handle_fallback(db, session_id, message)

    # =========================================================
    # 4. FOLLOW UP ON EXISTING TICKET
    # =========================================================
    def _handle_follow_up_ticket(self, db, session_id: str, message: str, state: dict) -> dict:
        step = state.get("step")

        if step == "lookup":
            lower = message.lower()
            
            # Intercept knowledge questions if user decides to ask something else instead of a ticket number
            is_knowledge_question = any(kw in lower for kw in ["what is", "what are", "how", "why", "explain", "tell me about", "tell me"]) or "?" in message
            if is_knowledge_question:
                conversation_manager.start(session_id, KNOWLEDGE)
                rag_response = self.rag_service.chat(db=db, session_id=session_id, question=message)
                rag_opts = rag_response.get("options", []) if isinstance(rag_response, dict) else []
                return {
                    "answer": rag_response.get("answer", rag_response) if isinstance(rag_response, dict) else rag_response,
                    "intent": KNOWLEDGE,
                    "options": rag_opts + ["Existing Customer"],
                }

            if "don't" in lower or "dont" in lower or "no company" in lower or "do not" in lower:
                conversation_manager.set_step(session_id, "lookup_by_email")
                return {
                    "answer": "No problem! Could you please share your **registered email address** or **phone number**?",
                    "intent": FOLLOW_UP_TICKET,
                    "step": "lookup_by_email",
                }

            company_name_input = message.strip()
            
            lead = db.query(Lead).filter(Lead.company_name.ilike(f"%{company_name_input}%")).order_by(Lead.id.desc()).first()

            conversation_manager.to_knowledge(session_id)

            if lead:
                conversation_manager.save(session_id, "matched_lead_id", lead.id)
            else:
                return {
                    "answer": (
                        "I couldn't find a record with that company name.\n\n"
                        "Would you like to raise it as a new ticket?"
                    ),
                    "intent": EXISTING_ENQUIRY,
                    "options": [
                        "Raise a new ticket",
                        "No, that's all",
                    ],
                }

            ticket = TicketRepository.get_latest_ticket_by_lead_id(db, lead.id)

            if ticket is None:
                return {
                    "answer": (
                        "I found your company, but there are no tickets associated with it.\n\n"
                        "Would you like to raise a new ticket?"
                    ),
                    "intent": EXISTING_ENQUIRY,
                    "options": [
                        "Raise a new ticket",
                        "No, that's all",
                    ],
                }

            return {
                "answer": (
                    f"Here's the latest on ticket **#{ticket.ticket_number}** for **{lead.company_name}**:\n\n"
                    f"• Status: **{ticket.status}**\n"
                    f"• Issue: {ticket.issue}\n\n"
                    "Would you like to speak with our team about this ticket?"
                ),
                "intent": FOLLOW_UP_TICKET,
                "options": [
                    "Connect me with the team",
                    "That's all, thanks",
                ],
            }

        if step == "lookup_by_email":
            identifier = message.strip()
            lead = None
            
            email_match = EMAIL_SEARCH_REGEX.search(identifier)
            if email_match and validate_email(email_match.group(0)):
                lead = LeadRepository.get_by_email(db, email_match.group(0))
            else:
                norm_phone = normalize_phone(identifier)
                if len(norm_phone) >= 7:
                    # Match trailing digits to catch phone numbers stored with country codes
                    lead = db.query(Lead).filter(Lead.phone.like(f"%{norm_phone[-10:]}%")).order_by(Lead.id.desc()).first()

            conversation_manager.to_knowledge(session_id)

            if lead:
                conversation_manager.save(session_id, "matched_lead_id", lead.id)
            else:
                return {
                    "answer": (
                        "I couldn't find any registered records for that email or phone number.\n\n"
                        "Would you like to raise a new ticket?"
                    ),
                    "intent": EXISTING_ENQUIRY,
                    "options": [
                        "Raise a new ticket",
                        "No, that's all",
                    ],
                }

            ticket = TicketRepository.get_latest_ticket_by_lead_id(db, lead.id)

            if ticket is None:
                return {
                    "answer": (
                        "I found your record, but there are no tickets associated with it.\n\n"
                        "Would you like to raise a new ticket?"
                    ),
                    "intent": EXISTING_ENQUIRY,
                    "options": [
                        "Raise a new ticket",
                        "No, that's all",
                    ],
                }

            return {
                "answer": (
                    f"I found a ticket for you! Here's the latest on ticket **#{ticket.ticket_number}**:\n\n"
                    f"• Status: **{ticket.status}**\n"
                    f"• Issue: {ticket.issue}\n\n"
                    "Would you like to speak with our team about this ticket?"
                ),
                "intent": FOLLOW_UP_TICKET,
                "options": [
                    "Connect me with the team",
                    "That's all, thanks",
                ],
            }

        return self._handle_fallback(db, session_id, message)

    # =========================================================
    # 5. RAISE A NEW TICKET
    # =========================================================
    def _handle_raise_new_ticket(self, db, session_id: str, message: str, state: dict) -> dict:
        step = state.get("step")

        if step == "description":
            conversation_manager.save(session_id, "description", message)
            
            category = self._classify_category(message)
            conversation_manager.save(session_id, "category", category)
            
            conversation_manager.set_step(session_id, "urgency")
            return {
                "answer": "How urgent is this?",
                "intent": RAISE_NEW_TICKET,
                "step": "urgency",
                "options": [
                    "Urgent – need help today",
                    "Normal",
                ],
            }

        if step == "urgency":
            conversation_manager.save(session_id, "urgency", message)
            data = state["data"]

            priority = "Urgent" if "urgent" in data.get("urgency", "").lower() else "Normal"
            
            from app.repositories.lead_repository import LeadRepository
            lead = LeadRepository.get_by_session_id(db, session_id)
            
            ticket = self.ticket_service.create_ticket(
                db=db,
                lead_id=lead.id if lead else 1,
                issue=data.get("description", "New issue"),
                category=data.get("category", "Support"),
                priority=priority
            )

            conversation_manager.to_knowledge(session_id)

            return {
                "answer": (
                    f"Thanks. I've logged this as ticket **#{ticket.ticket_number}**.\n\n"
                    "Would you like our team to call you about it?"
                ),
                "intent": TICKET_CREATED,
                "options": [
                    "Yes, please call me",
                    "No, that's all",
                ],
            }

        return self._handle_fallback(db, session_id, message)

    def _classify_category(self, description: str) -> str:
        prompt = f"""
        Classify the following issue description into EXACTLY ONE of these categories:
        - Test Report Query
        - Sample/Logistics
        - Billing
        - Certification Renewal
        - Technical Query
        - Other

        Issue Description: "{description}"

        Return ONLY the category name and nothing else.
        """
        try:
            category = self.rag_service.llm.generate(prompt).strip()
            valid_categories = ["Test Report Query", "Sample/Logistics", "Billing", "Certification Renewal", "Technical Query", "Other"]
            for valid in valid_categories:
                if valid.lower() in category.lower():
                    return valid
            return "Other"
        except Exception:
            return "Other"

    # =========================================================
    # 6. SCHEDULE A CALL
    # =========================================================
    def _handle_schedule_call(self, db, session_id: str, message: str, state: dict) -> dict:
        step = state.get("step")
        if step == "select_time":
            conversation_manager.to_knowledge(session_id)
            return {
                "answer": f"Great! 📞 We've scheduled a call for **{message}**.\n\nOur team will contact you on your registered number.",
                "intent": CALLBACK_SCHEDULED,
                "options": POST_CALL_SCHEDULED_OPTIONS,
            }
        return self._handle_fallback(db, session_id, message)

    # =========================================================
    # FALLBACK
    # =========================================================
    def _handle_fallback(self, db, session_id: str, message: str) -> dict:
        lower = message.lower()

        if "connect me with the team" in lower or "connect with the team" in lower:
            from app.repositories.lead_repository import LeadRepository
            state = conversation_manager.get(session_id)
            matched_lead_id = state.get("data", {}).get("matched_lead_id") if state else None
            
            if matched_lead_id:
                lead = db.query(Lead).filter(Lead.id == matched_lead_id).first()
            else:
                lead = LeadRepository.get_by_session_id(db, session_id)
            
            if lead and lead.phone and lead.name and lead.name.lower() != "unknown":
                from app.services.crm.ticket import TicketRepository
                ticket = TicketRepository.get_latest_ticket_by_lead_id(db, lead.id)
                ticket_number = ticket.ticket_number if ticket else ""
                
                self._trigger_n8n_webhook(lead.phone, lead.name, lead.email or "", ticket_number)
                
                conversation_manager.to_knowledge(session_id)
                return {
                    "answer": f"**Got it, {lead.name}!**\n\nOur team has been notified and will call you on your registered number (**{lead.phone}**) shortly.\n\n**Meanwhile, feel free to explore our services below or type your query.**",
                    "intent": KNOWLEDGE,
                    "options": ["New Customer", "Existing Customer"],
                }
            else:
                conversation_manager.start(session_id, GREETING)
                conversation_manager.set_step(session_id, "gcontact")
                return {
                    "answer": "I'll connect you with our support team. Before we proceed, could you please share your **Full Name**?",
                    "intent": GREETING,
                    "step": "gcontact",
                }

        service = self._match_service(message)
        if service:
            return self._service_response(db, session_id, service)

        service_sub_options = ["key standards", "key tests", "quality issues"]
        if any(opt in lower for opt in service_sub_options):
            state = conversation_manager.get(session_id)
            selected_service = state.get("data", {}).get("selected_service") if state else None
            if selected_service:
                return self._service_detail_response(db, session_id, selected_service, message)

        if "existing" in lower or "try again" in lower:
            conversation_manager.start(session_id, EXISTING_ENQUIRY)
            return self._handle_existing_enquiry(
                db, session_id, message, {"step": None, "data": {}}
            )

        if (
            any(trigger in lower for trigger in ["new enquiry", "new enquir", "new query", "another enquiry", "start over", "new issue", "raise a new issue", "new ticket", "raise a new ticket"])
            and not any(neg in lower for neg in ["don't", "dont", "do not"])
        ):
            conversation_manager.start(session_id, NEW_ENQUIRY)
            return self._handle_new_enquiry(
                db, session_id, message, {"step": None, "data": conversation_manager.get(session_id).get("data", {})}
            )

        stripped = lower.strip(".!?, \n\t")
        if (
            any(word in lower for word in ["that's all", "thank you", "thanks", "thanku", "thnku", "no, that", "bye", "goodbye"])
            or stripped in ["ok", "okay", "got it", "understood", "alright", "sure", "cool", "fine"]
        ):
            conversation_manager.to_knowledge(session_id)
            return {
                "answer": (
                    "Thank you for contacting ITC India. 👋 If you have any questions about our testing, certification, inspection, or compliance services in the future, feel free to return anytime."
                ),
                "intent": KNOWLEDGE,
                "options": [],
            }

        rag_response = self.rag_service.chat(db=db, session_id=session_id, question=message)
        rag_options = rag_response.get("options", [])
        if "Request a Callback" not in rag_options:
            rag_options.append("Request a Callback")
            
        raw_answer = rag_response.get("answer", rag_response) if isinstance(rag_response, dict) else rag_response
        
        from app.repositories.lead_repository import LeadRepository
        lead = LeadRepository.get_by_session_id(db, session_id)
        user_name = lead.name if lead and lead.name and lead.name.lower() != "unknown" else ""
        if not user_name:
            user_name = conversation_manager.get(session_id).get("data", {}).get("name", "")
            
        name_str = f"**Got it, {user_name}!**\n\n" if user_name and user_name.lower() != "unknown" else "**Got it!**\n\n"
            
        footer_text = "\n\n**Feel free to click any of the questions below to explore further, or select 'Request a Callback' to speak directly with our team!**"
        return {
            "answer": name_str + raw_answer + footer_text,
            "intent": KNOWLEDGE,
            "options": rag_options
        }
