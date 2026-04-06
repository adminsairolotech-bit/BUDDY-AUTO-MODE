from __future__ import annotations

from datetime import datetime
from typing import Any


async def run(user_id: str, job_id: str, job_data: dict[str, Any]) -> dict[str, Any]:
    return {
        "success": True,
        "title": "Evening Summary",
        "user_id": user_id,
        "job_id": job_id,
        "generated_at": datetime.utcnow().isoformat(),
        "message": "Daily wrap-up job placeholder.",
        "job_data": job_data,
    }
