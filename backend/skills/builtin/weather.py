from __future__ import annotations

from typing import Any

import httpx

from utils.helpers import get_settings


async def run(params: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    location = params.get("location", "Mumbai")
    api_key = get_settings().weather_api_key
    if not api_key:
        return {
            "text": f"Weather in {location}: API key not configured. Set WEATHER_API_KEY.",
            "data": {"location": location},
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
        return {
            "text": f"Weather in {location}: {temp}C, {condition}",
            "data": {"temperature": temp, "condition": condition, "humidity": humidity},
        }
    except Exception as exc:
        return {"text": f"Could not fetch weather for {location}.", "error": str(exc)}
