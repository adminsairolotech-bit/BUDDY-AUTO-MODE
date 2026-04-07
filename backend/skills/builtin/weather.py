from __future__ import annotations

import os
from typing import Any

import httpx

from utils.helpers import get_settings

# Try to import Gemini for AI-powered weather descriptions
try:
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    EMERGENT_AVAILABLE = True
except ImportError:
    EMERGENT_AVAILABLE = False


async def _get_ai_weather_description(location: str, temp: float, condition: str, humidity: int) -> str:
    """Generate AI-powered weather description"""
    if not EMERGENT_AVAILABLE:
        return f"Weather in {location}: {temp}°C, {condition}, Humidity: {humidity}%"
    
    api_key = os.getenv("EMERGENT_LLM_KEY", "")
    if not api_key:
        return f"Weather in {location}: {temp}°C, {condition}, Humidity: {humidity}%"
    
    try:
        chat = LlmChat(
            api_key=api_key,
            session_id=f"weather_{location}",
            system_message="You are a weather assistant. Provide brief, helpful weather summaries with clothing/activity suggestions. Keep responses under 50 words."
        )
        chat.with_model("gemini", "gemini-2.5-flash")
        
        message = UserMessage(
            text=f"Weather in {location}: Temperature {temp}°C, Condition: {condition}, Humidity: {humidity}%. Give a brief summary with suggestions."
        )
        response = await chat.send_message(message)
        return response.strip()
    except Exception:
        return f"Weather in {location}: {temp}°C, {condition}, Humidity: {humidity}%"


async def run(params: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    location = params.get("location", params.get("query", "Mumbai"))
    
    # Extract location from query if present
    if isinstance(location, str) and "weather" in location.lower():
        parts = location.lower().replace("weather", "").replace("in", "").replace("for", "").strip()
        if parts:
            location = parts.title()
    
    api_key = get_settings().weather_api_key
    if not api_key:
        # Return mock data with AI description
        mock_data = {
            "temperature": 28,
            "condition": "Partly Cloudy",
            "humidity": 65,
            "location": location
        }
        text = await _get_ai_weather_description(location, 28, "Partly Cloudy", 65)
        return {
            "text": text,
            "data": mock_data,
            "note": "Using simulated data - weather API key not configured"
        }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"q": location, "appid": api_key, "units": "metric"},
            )
        data = r.json()
        temp = data["main"]["temp"]
        condition = data["weather"][0]["main"]
        humidity = data["main"]["humidity"]
        
        # Get AI-powered description
        text = await _get_ai_weather_description(location, temp, condition, humidity)
        
        return {
            "text": text,
            "data": {"temperature": temp, "condition": condition, "humidity": humidity, "location": location},
        }
    except Exception as exc:
        return {"text": f"Could not fetch weather for {location}.", "error": str(exc)}
