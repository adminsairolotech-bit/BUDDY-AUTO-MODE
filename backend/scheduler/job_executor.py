from __future__ import annotations

from datetime import datetime
from typing import Any

from database.repositories import ScheduleRepository


class JobExecutor:
    def __init__(self, task_dispatcher: Any) -> None:
        self.task_dispatcher = task_dispatcher
        self.schedules = ScheduleRepository()

    async def execute_schedule(self, user_id: str, schedule_id: str, actions: list[dict[str, Any]]) -> dict[str, Any]:
        results = []
        for action in actions:
            result = await self.task_dispatcher(user_id=user_id, action=action)
            results.append(result)

        run_summary = {"run_at": datetime.utcnow(), "status": "success", "result": results}
        schedule = await self.schedules.get(user_id, schedule_id)
        if schedule:
            history = list(schedule.get("run_history", []))
            history.append(run_summary)
            history = history[-50:]
            await self.schedules.update(
                user_id,
                schedule_id,
                {"last_run": datetime.utcnow(), "run_history": history},
            )
        return {"success": True, "results": results}
