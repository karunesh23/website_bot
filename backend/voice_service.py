"""Text-to-Speech (TTS) service using ElevenLabs.

This module converts the chatbot's response into clear, professional
English speech with precise character-level timestamps for UI highlighting.
"""

import re
from typing import Tuple
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
from elevenlabs.core.api_error import ApiError

from app.config import get_settings


# -------------------------------------------------------------------
# Pronunciation corrections
# -------------------------------------------------------------------
PRONUNCIATION_MAP = {
    # ITC / company terms
    r"\bITC India\b": "I T C India",
    r"\bITC\b": "I T C",
    # Accreditation / testing terms
    r"\bNABL\b": "N A B L",
    r"\bEMC\b": "E M C",
    r"\bTCF\b": "T C F",
    # IP ratings
    r"\bIP67\b": "I P sixty-seven",
    r"\bIP66\b": "I P sixty-six",
    r"\bIP65\b": "I P sixty-five",
    r"\bIP54\b": "I P fifty-four",
    r"\bIP44\b": "I P forty-four",
    # Common abbreviations
    r"\bAC\b": "A C",
    r"\bDC\b": "D C",
    r"\bIEC\b": "I E C",
    r"\bISO\b": "I S O",
    r"\bUL\b": "U L",
    r"\bCE\b": "C E",
    r"\bPCB\b": "P C B",
    r"\bLED\b": "L E D",
    r"\bEMI\b": "E M I",
    r"\bESD\b": "E S D",
    r"\bRF\b": "R F",
    r"\bDUT\b": "D U T",
    r"\bRCD\b": "R C D",
    # Common test names
    r"\bHipot\b": "High Pot",
    r"\bHIPOT\b": "High Pot",
    # Units
    r"\bkV\b": "kilovolts",
    r"\bKV\b": "kilovolts",
    r"\bV\b": "volts",
    r"\bmV\b": "millivolts",
    r"\bA\b": "amps",
    r"\bmA\b": "milliamps",
    r"\bHz\b": "hertz",
    r"\bkHz\b": "kilohertz",
    r"\bMHz\b": "megahertz",
    r"\bGHz\b": "gigahertz",
    r"\bW\b": "watts",
    r"\bkW\b": "kilowatts",
    r"Ω": "ohms",
    # Symbols
    r"&": " and ",
    r"/": " or ",
    r"→": " to ",
    r"↔": " and ",
    r"\bHi!\b": "Hi,",
    r"\bKanu\b": "Kaanu",
    r"\bkanu\b": "Kaanu"
}

def prepare_speech_and_mapping(original_text: str) -> Tuple[str, list[int]]:
    """
    Cleans text for TTS and returns a mapping from the TTS string index
    back to the original text string index. This ensures UI highlighting
    remains perfectly aligned despite text changes.
    """
    tts_chars = []
    tts_to_orig = []
    
    i = 0
    while i < len(original_text):
        if original_text.startswith("**", i):
            i += 2
            continue
        if original_text.startswith("*", i):
            i += 1
            continue
        if original_text.startswith("`", i):
            i += 1
            continue
        tts_chars.append(original_text[i])
        tts_to_orig.append(i)
        i += 1
        
    text1 = "".join(tts_chars)
    
    # Add periods to the end of lines missing punctuation to prevent the bot from
    # speaking too fast when reading lists or bullet points.
    # Remove bullet points entirely so the bot doesn't pronounce them as "dash".
    replacements = [
        (r"(?<=[^.,:;!?>\s])\s*\n", ".\n"),
        (r"^\s*[-•]\s*", "")
    ] + list(PRONUNCIATION_MAP.items())
    
    for pattern, repl in replacements:
        while True:
            match = re.search(pattern, text1, flags=re.MULTILINE)
            if not match:
                break
            start, end = match.span()
            orig_idx = tts_to_orig[start] if start < len(tts_to_orig) else 0
            text1 = text1[:start] + repl + text1[end:]
            tts_to_orig = tts_to_orig[:start] + [orig_idx]*len(repl) + tts_to_orig[end:]
            
    # Add a final period if the text doesn't end with punctuation
    if text1 and text1[-1] not in ".,:;!?>":
        text1 += "."
        tts_to_orig.append(tts_to_orig[-1] if tts_to_orig else 0)

    # Insert <break time="0.5s" /> after sentence terminators to enforce a clear but natural pause
    break_tag = '<break time="0.5s" />'
    i = len(text1) - 1
    while i >= 0:
        if text1[i] in ".?!":
            # Check if it's the end of a sentence
            if i == len(text1) - 1 or text1[i+1] in " \n":
                # Exclude decimal numbers like 1.0
                if not (text1[i] == '.' and i > 0 and i < len(text1)-1 and text1[i-1].isdigit() and text1[i+1].isdigit()):
                    # Avoid inserting multiple breaks for ellipsis "..."
                    if not (i > 0 and text1[i-1] in ".?!"):
                        text1 = text1[:i+1] + break_tag + text1[i+1:]
                        orig_idx = tts_to_orig[i]
                        tts_to_orig = tts_to_orig[:i+1] + [orig_idx]*len(break_tag) + tts_to_orig[i+1:]
        i -= 1
            
    return text1, tts_to_orig


# -------------------------------------------------------------------
# ElevenLabs error handling
# -------------------------------------------------------------------

def _elevenlabs_error_message(exc: ApiError) -> str:
    """Return a human-readable message from an ElevenLabs ApiError."""

    body = getattr(exc, "body", None)

    if isinstance(body, dict):
        detail = body.get("detail")

        if isinstance(detail, dict):
            return (
                detail.get("message")
                or detail.get("type")
                or str(exc)
            )

    return str(exc)


# -------------------------------------------------------------------
# Main TTS function
# -------------------------------------------------------------------

def synthesize_speech_to_mp3(text: str) -> Tuple[str, dict]:
    """
    Convert the chatbot response into clear English MP3 speech with timestamps.

    Parameters
    ----------
    text : str
        Exact text generated by the chatbot.

    Returns
    -------
    Tuple[str, dict]
        A tuple containing:
        - base64 encoded MP3 audio string
        - alignment dictionary with character timestamps mapped to the original text
    """

    settings = get_settings()

    api_key = (settings.ELEVENLABS_API_KEY or "").strip()
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY is not set")

    voice_id = (settings.ELEVENLABS_VOICE_ID or "").strip()
    if not voice_id:
        raise ValueError("ELEVENLABS_VOICE_ID is not set")

    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    client = ElevenLabs(api_key=api_key)

    # Clean text for speech and track character index mapping
    speech_text, tts_to_orig = prepare_speech_and_mapping(text)

    res = client.text_to_speech.convert_with_timestamps(
        text=speech_text,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        voice_settings=VoiceSettings(
            stability=0.65,
            similarity_boost=0.4,
            style=0.0,
            use_speaker_boost=True
        )
    )

    # Rebuild alignment dictionary for the frontend
    final_starts = [None] * len(text)
    final_ends = [None] * len(text)
    
    tts_starts = res.alignment.character_start_times_seconds
    tts_ends = res.alignment.character_end_times_seconds
    
    for tts_i, orig_i in enumerate(tts_to_orig):
        if tts_i < len(tts_starts):
            st = tts_starts[tts_i]
            en = tts_ends[tts_i]
            
            if final_starts[orig_i] is None or st < final_starts[orig_i]:
                final_starts[orig_i] = st
            if final_ends[orig_i] is None or en > final_ends[orig_i]:
                final_ends[orig_i] = en

    # Forward-fill any missing characters (e.g. stripped markdown asterisks)
    last_st, last_en = 0.0, 0.0
    for i in range(len(text)):
        if final_starts[i] is not None:
            last_st = final_starts[i]
            last_en = final_ends[i]
        else:
            final_starts[i] = last_st
            final_ends[i] = last_en
            
    # Create the final alignment dictionary
    alignment_dict = {
        "characters": list(text),
        "character_start_times_seconds": final_starts,
        "character_end_times_seconds": final_ends
    }

    return res.audio_base_64, alignment_dict


# -------------------------------------------------------------------
# Safe API error message
# -------------------------------------------------------------------

def api_error_user_message(exc: ApiError) -> str:
    """
    Return a safe error message for API clients.

    Stack traces and internal implementation details are not exposed.
    """
    return _elevenlabs_error_message(exc)