from __future__ import annotations

from typing import Any


def build_action_response(
    text: str,
    action_type: str | None = None,
    status: str = "completed",
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = {"text": text}
    if action_type:
        payload["action_taken"] = {"type": action_type, "status": status, "details": details or {}}
    return payload


def build_error_response(message: str, error: str) -> dict[str, Any]:
    return {"success": False, "response": {"text": message}, "error": error}
