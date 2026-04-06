from __future__ import annotations

from typing import Any


_NOTES: list[dict[str, Any]] = []


async def run(params: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    action = params.get("action", "add")
    if action == "add":
        text = params.get("text", "")
        if not text:
            return {"text": "Please provide note text."}
        _NOTES.append({"text": text, "user_id": (context or {}).get("user_id")})
        return {"text": "Note saved.", "data": {"count": len(_NOTES)}}
    if action == "list":
        user_id = (context or {}).get("user_id")
        notes = [n for n in _NOTES if not user_id or n.get("user_id") == user_id]
        return {"text": f"You have {len(notes)} notes.", "data": notes}
    return {"text": f"Unknown notes action: {action}"}
