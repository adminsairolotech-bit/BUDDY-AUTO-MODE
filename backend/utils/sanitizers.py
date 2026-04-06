from __future__ import annotations

import re
from typing import Any


SENSITIVE_KEYWORDS = {
    "password",
    "passwd",
    "otp",
    "token",
    "secret",
    "api_key",
    "authorization",
    "refresh_token",
    "access_token",
    "card",
    "cvv",
    "bank",
}

SECRET_VALUE_PATTERNS = [
    re.compile(r"bearer\s+[a-z0-9\-._~+/]+=*", re.IGNORECASE),
    re.compile(r"[a-z0-9_\-]{20,}\.[a-z0-9_\-]{20,}\.[a-z0-9_\-]{20,}", re.IGNORECASE),
]


def mask_string(value: str) -> str:
    if not value:
        return value
    result = value
    for pattern in SECRET_VALUE_PATTERNS:
        result = pattern.sub("[REDACTED]", result)
    return result


def sanitize_for_log(data: Any) -> Any:
    if isinstance(data, dict):
        sanitized: dict[str, Any] = {}
        for key, value in data.items():
            if any(k in key.lower() for k in SENSITIVE_KEYWORDS):
                sanitized[key] = "[REDACTED]"
            else:
                sanitized[key] = sanitize_for_log(value)
        return sanitized
    if isinstance(data, list):
        return [sanitize_for_log(v) for v in data]
    if isinstance(data, str):
        return mask_string(data)
    if isinstance(data, (int, float, bool)) or data is None:
        return data
    # Handles ObjectId, datetime, and custom types for safe JSON serialization.
    return str(data)
    return data


def contains_sensitive_content(key: str, value: Any) -> bool:
    key_lower = (key or "").lower()
    if any(k in key_lower for k in {"password", "otp", "secret", "token", "api_key", "bank", "cvv", "pin"}):
        return True

    if isinstance(value, str):
        lowered = value.lower()
        if any(marker in lowered for marker in ["password=", "otp", "cvv", "account number", "bank account"]):
            return True
        for pattern in SECRET_VALUE_PATTERNS:
            if pattern.search(value):
                return True
    return False


def sanitize_memory_value(key: str, value: Any) -> tuple[Any, bool]:
    if contains_sensitive_content(key, value):
        return "[REDACTED_SENSITIVE]", True
    if isinstance(value, str):
        return mask_string(value), False
    return value, False
