from __future__ import annotations

from datetime import datetime
from typing import Any

from database.connection import get_database
from utils.sanitizers import sanitize_for_log


class AuditLogger:
    def __init__(self) -> None:
        self.collection = get_database().audit_logs

    async def log(
        self,
        *,
        user_id: str | None,
        action: str,
        status: str,
        source: str,
        ip: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        await self.collection.insert_one(
            {
                "user_id": user_id,
                "action": action,
                "status": status,
                "source": source,
                "ip": ip,
                "details": sanitize_for_log(details or {}),
                "created_at": datetime.utcnow(),
            }
        )
