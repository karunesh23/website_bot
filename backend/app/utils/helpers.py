import re
import uuid

from app.utils.constants import COUNTRY_DIAL_CODES

EMAIL_REGEX = re.compile(r"^[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}$")
EMAIL_SEARCH_REGEX = re.compile(r"[\w.+-]+@[\w-]+\.[a-zA-Z]{2,}")
PHONE_REGEX = re.compile(r"^\+[1-9]\d{6,14}$")


def generate_session_id():

    return str(uuid.uuid4())


def clean_text(text: str):

    return " ".join(text.split())


def validate_email(email: str) -> bool:
    """
    Validate an email address. The local part (before @) must contain
    at least one letter, so obviously bogus addresses like 23324@gmail.com
    are rejected.
    """

    email = (email or "").strip()
    if not EMAIL_REGEX.match(email):
        return False
    local = email.split("@")[0]
    return any(c.isalpha() for c in local)


def validate_contact_info(message: str) -> bool:
    """
    Validate the "existing enquiry" contact prompt, which asks for a name
    together with an email or phone number. Accepts any message that
    contains a valid email address or a valid phone number.
    """

    message = (message or "").strip()
    if not message:
        return False

    email = EMAIL_SEARCH_REGEX.search(message)
    if email and validate_email(email.group(0)):
        return True

    digits = re.sub(r"\D", "", message)
    return 7 <= len(digits) <= 15


def _local_digits(phone: str):
    """
    Given a full international phone number starting with '+', return the
    matching dial code and the local digits after it (or None, phone).
    """

    if not (phone or "").startswith("+"):
        return None, phone or ""
    for code in sorted(COUNTRY_DIAL_CODES, key=len, reverse=True):
        if phone.startswith(code):
            return code, phone[len(code):]
    return None, phone[1:]


def validate_phone(phone: str) -> bool:
    """
    Validate a phone number. If it starts with a known '+cc' country code,
    enforce that country's local-digit count; otherwise accept a plain
    7-15 digit number (chat flow).
    """

    phone = (phone or "").strip()
    if phone.startswith("+"):
        return validate_phone_international(phone)
    digits = re.sub(r"\D", "", phone)
    return 7 <= len(digits) <= 15


def validate_phone_international(phone: str) -> bool:
    """
    Validate a full international phone number with a leading '+'
    country code (e.g. +919876543210, +989123456789). Enforces each
    country's expected number of local digits.
    """

    phone = (phone or "").strip()
    if not PHONE_REGEX.match(phone):
        return False

    code, local = _local_digits(phone)
    if code:
        info = COUNTRY_DIAL_CODES[code]
        return info["min_digits"] <= len(local) <= info["max_digits"]

    digits = phone[1:]
    return 7 <= len(digits) <= 15


def normalize_phone(phone: str) -> str:

    return re.sub(r"\D", "", phone or "")


def success_response(message, data=None):

    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(message):

    return {
        "success": False,
        "message": message
    }