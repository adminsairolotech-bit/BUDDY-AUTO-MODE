from __future__ import annotations

import json
import os
import asyncio
from typing import Any
from dotenv import load_dotenv

load_dotenv()

# Try to import emergent integrations
try:
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    EMERGENT_AVAILABLE = True
except ImportError:
    EMERGENT_AVAILABLE = False

SYSTEM_PROMPT = """You are BUDDY, an AI personal assistant. You are helpful, friendly, and efficient.
You can help with:
- Weather information
- News updates
- Mathematical calculations
- Language translation
- Taking notes
- General questions and conversations

Always be concise but helpful. If asked to perform a specific action, acknowledge it clearly.
For calculations, show your work. For translations, provide the translated text clearly.
"""

PARSE_PROMPT = """You are a command parser for an AI assistant. 
Analyze the user's command and return a JSON response with these keys:
- understood: boolean (true if you understand the command)
- intent: string (weather, news, calculator, translator, notes, chat, desktop, schedule)
- action: string (specific action to take)
- params: object (relevant parameters extracted)
- response_text: string (natural language response to user)
- needs_confirmation: boolean (true if action needs user confirmation)
- follow_up_question: string or null (if you need more info)

Return ONLY valid JSON, no markdown or extra text.
"""


class GeminiEngine:
    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("EMERGENT_LLM_KEY", "")
        self.model_ready = False
        
        if EMERGENT_AVAILABLE and self.api_key:
            self.model_ready = True

    def is_enabled(self) -> bool:
        return self.model_ready

    def _get_chat(self, session_id: str, system_message: str = SYSTEM_PROMPT) -> LlmChat:
        """Create a new chat instance"""
        chat = LlmChat(
            api_key=self.api_key,
            session_id=session_id,
            system_message=system_message
        )
        # Use Gemini model
        chat.with_model("gemini", "gemini-2.5-flash")
        return chat

    def parse_command(self, command: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Parse a command and return structured response"""
        if not self.model_ready:
            return self._fallback_parse(command)
        
        try:
            # Run async in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self._async_parse_command(command, context))
            loop.close()
            return result
        except Exception as exc:
            print(f"Parse error: {exc}")
            return self._fallback_parse(command)

    async def _async_parse_command(self, command: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Async parse command"""
        chat = self._get_chat(f"parse_{hash(command)}", PARSE_PROMPT)
        
        prompt = f"Context: {json.dumps(context or {})}\nUser command: {command}\n\nReturn JSON:"
        message = UserMessage(text=prompt)
        
        response = await chat.send_message(message)
        text = response.strip()
        
        # Clean up response
        if "```json" in text:
            text = text.split("```json", 1)[1].split("```", 1)[0].strip()
        elif "```" in text:
            text = text.split("```", 1)[1].split("```", 1)[0].strip()
        
        return json.loads(text)

    def generate_response(self, prompt: str, context: dict[str, Any] | None = None) -> str:
        """Generate a natural language response"""
        if not self.model_ready:
            return self._fallback_response(prompt)
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self._async_generate_response(prompt, context))
            loop.close()
            return result
        except Exception as exc:
            print(f"Generate error: {exc}")
            return self._fallback_response(prompt)

    async def _async_generate_response(self, prompt: str, context: dict[str, Any] | None = None) -> str:
        """Async generate response"""
        chat = self._get_chat(f"response_{hash(prompt)}")
        
        full_prompt = prompt
        if context:
            full_prompt = f"Context: {json.dumps(context)}\n\nUser: {prompt}"
        
        message = UserMessage(text=full_prompt)
        response = await chat.send_message(message)
        return response.strip()

    def summarize_conversation(self, messages: list[dict[str, Any]]) -> str:
        """Summarize a conversation"""
        if not messages:
            return ""
        
        if not self.model_ready:
            latest = messages[-6:]
            return " | ".join(f"{m.get('role')}: {m.get('content', '')[:80]}" for m in latest)
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self._async_summarize(messages))
            loop.close()
            return result
        except Exception:
            return "Conversation summary unavailable."

    async def _async_summarize(self, messages: list[dict[str, Any]]) -> str:
        """Async summarize"""
        chat = self._get_chat("summarize", "You are a conversation summarizer. Be concise.")
        
        conv_text = "\n".join(f"{m.get('role')}: {m.get('content', '')}" for m in messages[-20:])
        prompt = f"Summarize this conversation in 2-3 sentences:\n{conv_text}"
        
        message = UserMessage(text=prompt)
        return await chat.send_message(message)

    def extract_entities(self, text: str) -> dict[str, list[str]]:
        """Extract entities from text"""
        default = {"names": [], "emails": [], "phones": [], "dates": [], "locations": [], "organizations": [], "other": []}
        
        if not self.model_ready:
            return default
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(self._async_extract_entities(text))
            loop.close()
            return result
        except Exception:
            return default

    async def _async_extract_entities(self, text: str) -> dict[str, list[str]]:
        """Async extract entities"""
        chat = self._get_chat("entities", "You are an entity extractor. Return only JSON.")
        
        prompt = f"Extract entities from this text and return JSON with keys: names, emails, phones, dates, locations, organizations, other.\n\nText: {text}\n\nJSON:"
        message = UserMessage(text=prompt)
        
        response = await chat.send_message(message)
        text = response.strip()
        
        if "```" in text:
            text = text.split("```", 1)[1].split("```", 1)[0].replace("json", "", 1).strip()
        
        return json.loads(text)

    def _fallback_parse(self, command: str) -> dict[str, Any]:
        """Fallback when AI is not available"""
        command_lower = command.lower()
        
        # Simple intent detection
        if any(w in command_lower for w in ['weather', 'temperature', 'forecast']):
            intent = 'weather'
        elif any(w in command_lower for w in ['news', 'headline', 'update']):
            intent = 'news'
        elif any(w in command_lower for w in ['calculate', 'math', '+', '-', '*', '/', '=']):
            intent = 'calculator'
        elif any(w in command_lower for w in ['translate', 'translation']):
            intent = 'translator'
        elif any(w in command_lower for w in ['note', 'remember', 'save']):
            intent = 'notes'
        else:
            intent = 'chat'
        
        return {
            "understood": True,
            "intent": intent,
            "action": intent,
            "params": {"query": command},
            "response_text": f"I understand you want help with {intent}. Processing your request...",
            "needs_confirmation": False,
            "follow_up_question": None,
        }

    def _fallback_response(self, prompt: str) -> str:
        """Fallback response when AI is not available"""
        return f"I can help you with that! Your request about '{prompt[:50]}...' has been noted."
