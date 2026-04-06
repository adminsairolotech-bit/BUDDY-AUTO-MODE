from __future__ import annotations

import json
import os
from typing import Any

try:
    import google.generativeai as genai
except Exception:  # pragma: no cover - optional dependency at runtime
    genai = None


SYSTEM_PROMPT = """You are an AI personal assistant.
Return strict JSON for command parsing with keys:
understood, intent, action, params, response_text, needs_confirmation, follow_up_question.
"""


class GeminiEngine:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model = None
        if genai and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config={"temperature": 0.4, "top_p": 0.95, "top_k": 40, "max_output_tokens": 2048},
            )

    def is_enabled(self) -> bool:
        return self.model is not None

    def parse_command(self, command: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self.model:
            return {
                "understood": False,
                "intent": "chat",
                "action": "fallback",
                "params": {},
                "response_text": "I can help with that. Let me route it using local intent parsing.",
                "needs_confirmation": False,
                "follow_up_question": None,
            }

        prompt = f"{SYSTEM_PROMPT}\nContext: {json.dumps(context or {})}\nCommand: {command}\nJSON:"
        try:
            response = self.model.generate_content(prompt)
            text = (response.text or "").strip()
            if "```json" in text:
                text = text.split("```json", 1)[1].split("```", 1)[0].strip()
            elif "```" in text:
                text = text.split("```", 1)[1].split("```", 1)[0].strip()
            return json.loads(text)
        except Exception as exc:
            return {
                "understood": False,
                "intent": "chat",
                "action": "fallback",
                "params": {},
                "response_text": "I hit a parsing issue, using fallback parser.",
                "needs_confirmation": False,
                "follow_up_question": None,
                "error": str(exc),
            }

    def generate_response(self, prompt: str, context: dict[str, Any] | None = None) -> str:
        if not self.model:
            return "I can help with that."
        try:
            response = self.model.generate_content(
                f"{SYSTEM_PROMPT}\nContext: {json.dumps(context or {})}\nUser: {prompt}\nAssistant:"
            )
            return (response.text or "").strip()
        except Exception:
            return "I can help with that."

    def summarize_conversation(self, messages: list[dict[str, Any]]) -> str:
        if not messages:
            return ""
        if not self.model:
            latest = messages[-6:]
            return " | ".join(f"{m.get('role')}: {m.get('content', '')[:80]}" for m in latest)
        prompt = (
            "Summarize this conversation in 2-3 sentences. Focus on user goals and completed actions.\n"
            + "\n".join(f"{m.get('role')}: {m.get('content', '')}" for m in messages[-20:])
        )
        try:
            return (self.model.generate_content(prompt).text or "").strip()
        except Exception:
            return "Conversation summary unavailable."

    def extract_entities(self, text: str) -> dict[str, list[str]]:
        if not self.model:
            return {"names": [], "emails": [], "phones": [], "dates": [], "locations": [], "organizations": [], "other": []}
        prompt = (
            "Extract entities and return JSON with names,emails,phones,dates,locations,organizations,other.\n"
            f"Text: {text}\nJSON:"
        )
        try:
            raw = (self.model.generate_content(prompt).text or "").strip()
            if "```" in raw:
                raw = raw.split("```", 1)[1].split("```", 1)[0].replace("json", "", 1).strip()
            return json.loads(raw)
        except Exception:
            return {"names": [], "emails": [], "phones": [], "dates": [], "locations": [], "organizations": [], "other": []}
