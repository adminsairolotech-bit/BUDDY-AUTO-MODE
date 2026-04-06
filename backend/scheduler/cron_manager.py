from __future__ import annotations

import logging
from typing import Any, Awaitable, Callable

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


logger = logging.getLogger(__name__)


class CronManager:
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler(job_defaults={"coalesce": True, "max_instances": 1, "misfire_grace_time": 60})

    def start(self) -> None:
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Cron scheduler started")

    def stop(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            logger.info("Cron scheduler stopped")

    def add_job(
        self,
        job_id: str,
        cron_expression: str,
        handler: Callable[..., Awaitable[Any]],
        user_id: str,
        job_data: dict[str, Any] | None = None,
    ) -> bool:
        try:
            minute, hour, day, month, day_of_week = cron_expression.strip().split()
            trigger = CronTrigger(minute=minute, hour=hour, day=day, month=month, day_of_week=day_of_week)
            self.scheduler.add_job(
                handler,
                trigger=trigger,
                id=job_id,
                kwargs={"user_id": user_id, "job_id": job_id, "job_data": job_data or {}},
                replace_existing=True,
            )
            return True
        except Exception as exc:
            logger.error("Failed to add cron job %s: %s", job_id, exc)
            return False

    def remove_job(self, job_id: str) -> bool:
        try:
            self.scheduler.remove_job(job_id)
            return True
        except Exception:
            return False

    def pause_job(self, job_id: str) -> bool:
        try:
            self.scheduler.pause_job(job_id)
            return True
        except Exception:
            return False

    def resume_job(self, job_id: str) -> bool:
        try:
            self.scheduler.resume_job(job_id)
            return True
        except Exception:
            return False

    def get_job(self, job_id: str) -> dict[str, Any] | None:
        job = self.scheduler.get_job(job_id)
        if not job:
            return None
        return {"id": job.id, "next_run": job.next_run_time, "pending": job.pending}

    def get_all_jobs(self) -> list[dict[str, Any]]:
        return [{"id": j.id, "next_run": j.next_run_time, "pending": j.pending} for j in self.scheduler.get_jobs()]
