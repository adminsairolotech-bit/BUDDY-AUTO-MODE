from __future__ import annotations

from typing import Any

import httpx

from utils.helpers import get_settings


async def run(params: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    topic = params.get("topic", "technology")
    api_key = get_settings().news_api_key
    if not api_key:
        return {"text": f"News skill is ready, but NEWS_API_KEY is missing for live headlines about {topic}.", "data": []}

    try:
        async with httpx.AsyncClient(timeout=12) as client:
            r = await client.get(
                "https://newsapi.org/v2/top-headlines",
                params={"q": topic, "language": "en", "apiKey": api_key, "pageSize": 5},
            )
        payload = r.json()
        articles = payload.get("articles", [])
        headlines = [a.get("title", "Untitled") for a in articles[:5]]
        text = "Top headlines:\n" + "\n".join(f"- {h}" for h in headlines) if headlines else "No headlines found."
        return {"text": text, "data": articles[:5]}
    except Exception as exc:
        return {"text": "Failed to fetch news.", "error": str(exc)}
