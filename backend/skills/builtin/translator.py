from __future__ import annotations

import os
from typing import Any

# Try to import for AI-powered translation
try:
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    EMERGENT_AVAILABLE = True
except ImportError:
    EMERGENT_AVAILABLE = False


LANGUAGE_CODES = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
    "ar": "Arabic",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "gu": "Gujarati",
    "pa": "Punjabi",
}


async def run(params: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    text = params.get("text", params.get("query", ""))
    target = params.get("target_language", params.get("target", "hi"))
    source = params.get("source_language", "auto")
    
    # Parse from query like "translate hello to hindi"
    if not text and "query" in params:
        query = params["query"].lower()
        if "translate" in query:
            parts = query.replace("translate", "").strip()
            if " to " in parts:
                text_part, lang_part = parts.rsplit(" to ", 1)
                text = text_part.strip()
                # Find language code
                lang_part = lang_part.strip().lower()
                for code, name in LANGUAGE_CODES.items():
                    if lang_part in name.lower() or lang_part == code:
                        target = code
                        break
    
    if not text:
        return {"text": "Please provide text to translate. Example: 'translate hello to Hindi'"}
    
    target_name = LANGUAGE_CODES.get(target, target)
    
    if not EMERGENT_AVAILABLE:
        return {
            "text": f"Translation to {target_name}: {text} (AI not available)",
            "data": {"original_text": text, "translated_text": text, "target_language": target_name}
        }
    
    api_key = os.getenv("EMERGENT_LLM_KEY", "")
    if not api_key:
        return {
            "text": f"Translation to {target_name}: {text} (API key not configured)",
            "data": {"original_text": text, "translated_text": text, "target_language": target_name}
        }
    
    try:
        chat = LlmChat(
            api_key=api_key,
            session_id=f"translate_{hash(text)}",
            system_message="You are a translator. Translate the given text accurately. Return ONLY the translated text, nothing else."
        )
        chat.with_model("gemini", "gemini-2.5-flash")
        
        message = UserMessage(
            text=f"Translate the following text to {target_name}:\n\n{text}"
        )
        translated = await chat.send_message(message)
        translated = translated.strip()
        
        return {
            "text": f"**{target_name} Translation:**\n{translated}",
            "data": {
                "original_text": text,
                "translated_text": translated,
                "source_language": source,
                "target_language": target_name
            }
        }
    except Exception as exc:
        return {
            "text": f"Translation failed: {str(exc)}",
            "error": str(exc),
            "data": {"original_text": text, "target_language": target_name}
        }
