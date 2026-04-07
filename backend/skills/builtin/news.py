from __future__ import annotations

import os
from typing import Any

import httpx

from utils.helpers import get_settings

# Try to import for AI summaries
try:
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    EMERGENT_AVAILABLE = True
except ImportError:
    EMERGENT_AVAILABLE = False


MOCK_NEWS = [
    {"title": "AI Revolution: New Breakthroughs in Machine Learning", "source": "Tech Daily", "description": "Recent advances in AI are transforming industries worldwide."},
    {"title": "Climate Summit Reaches Historic Agreement", "source": "World News", "description": "World leaders commit to ambitious carbon reduction targets."},
    {"title": "Space Tourism Takes Off: First Commercial Flight Successful", "source": "Space Journal", "description": "Private space travel becomes a reality for civilians."},
    {"title": "Global Markets Show Strong Recovery", "source": "Finance Times", "description": "Stock markets worldwide report positive gains."},
    {"title": "New Medical Breakthrough in Cancer Treatment", "source": "Health News", "description": "Scientists discover promising new therapy approach."},
]


async def run(params: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    topic = params.get("topic", params.get("query", "technology"))
    
    # Clean up topic
    if isinstance(topic, str):
        topic = topic.lower().replace("news", "").replace("about", "").replace("latest", "").strip()
        if not topic:
            topic = "technology"
    
    api_key = get_settings().news_api_key
    
    if not api_key:
        # Return mock news with AI summary
        headlines = [n["title"] for n in MOCK_NEWS]
        text = f"📰 **Latest {topic.title()} News:**\n\n"
        for i, news in enumerate(MOCK_NEWS[:5], 1):
            text += f"{i}. **{news['title']}**\n   _{news['source']}_ - {news['description']}\n\n"
        
        # Add AI summary if available
        if EMERGENT_AVAILABLE:
            ai_key = os.getenv("EMERGENT_LLM_KEY", "")
            if ai_key:
                try:
                    chat = LlmChat(
                        api_key=ai_key,
                        session_id=f"news_{topic}",
                        system_message="You are a news summarizer. Provide a brief 2-sentence summary of the news topics."
                    )
                    chat.with_model("gemini", "gemini-2.5-flash")
                    
                    message = UserMessage(text=f"Summarize these headlines briefly: {', '.join(headlines)}")
                    summary = await chat.send_message(message)
                    text += f"\n**Summary:** {summary.strip()}"
                except Exception:
                    pass
        
        return {
            "text": text,
            "data": MOCK_NEWS[:5],
            "note": "Using sample news - NEWS_API_KEY not configured"
        }

    try:
        async with httpx.AsyncClient(timeout=12) as client:
            r = await client.get(
                "https://newsapi.org/v2/top-headlines",
                params={"q": topic, "language": "en", "apiKey": api_key, "pageSize": 5},
            )
        payload = r.json()
        articles = payload.get("articles", [])
        
        if not articles:
            return {"text": f"No news found for '{topic}'.", "data": []}
        
        text = f"📰 **Top {topic.title()} Headlines:**\n\n"
        headlines = []
        for i, article in enumerate(articles[:5], 1):
            title = article.get("title", "Untitled")
            source = article.get("source", {}).get("name", "Unknown")
            desc = article.get("description", "")[:100] + "..." if article.get("description") else ""
            text += f"{i}. **{title}**\n   _{source}_ - {desc}\n\n"
            headlines.append(title)
        
        # Add AI summary if available
        if EMERGENT_AVAILABLE:
            ai_key = os.getenv("EMERGENT_LLM_KEY", "")
            if ai_key:
                try:
                    chat = LlmChat(
                        api_key=ai_key,
                        session_id=f"news_{topic}",
                        system_message="You are a news summarizer. Provide a brief 2-sentence summary."
                    )
                    chat.with_model("gemini", "gemini-2.5-flash")
                    
                    message = UserMessage(text=f"Summarize these headlines: {', '.join(headlines)}")
                    summary = await chat.send_message(message)
                    text += f"\n**Summary:** {summary.strip()}"
                except Exception:
                    pass
        
        return {"text": text, "data": articles[:5]}
    except Exception as exc:
        return {"text": f"Failed to fetch news about {topic}.", "error": str(exc)}
