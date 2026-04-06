from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Request

from database.models import ScheduleCreateRequest, ScheduleUpdateRequest
from database.repositories import ScheduleRepository
from utils.security import get_current_user
from utils.validators import is_safe_cron


router = APIRouter(prefix="/api/schedules", tags=["schedules"])


@router.get("")
async def list_schedules(current_user: dict = Depends(get_current_user)):
    repo = ScheduleRepository()
    user_id = current_user.get("sub")
    schedules = await repo.list(user_id)
    return {"success": True, "schedules": schedules}


@router.post("", status_code=201)
async def create_schedule(payload: ScheduleCreateRequest, request: Request, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    if not is_safe_cron(payload.cron):
        raise HTTPException(status_code=400, detail="Invalid cron expression")

    schedule_id = f"schedule_{uuid.uuid4().hex[:8]}"
    repo = ScheduleRepository()
    await repo.create(
        user_id,
        {
            "schedule_id": schedule_id,
            "name": payload.name,
            "description": payload.description,
            "cron": payload.cron,
            "timezone": payload.timezone,
            "actions": payload.actions,
            "notification": payload.notification.model_dump() if payload.notification else None,
        },
    )

    added = request.app.state.cron_manager.add_job(
        job_id=schedule_id,
        cron_expression=payload.cron,
        handler=request.app.state.run_scheduled_job,
        user_id=user_id,
        job_data={"schedule_id": schedule_id},
    )
    if not added:
        raise HTTPException(status_code=400, detail="Failed to schedule cron job")

    return {"success": True, "schedule_id": schedule_id}


@router.put("/{schedule_id}")
async def update_schedule(schedule_id: str, payload: ScheduleUpdateRequest, request: Request, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    repo = ScheduleRepository()
    existing = await repo.get(user_id, schedule_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Schedule not found")

    updates = payload.model_dump(exclude_none=True)
    if "cron" in updates:
        if not is_safe_cron(updates["cron"]):
            raise HTTPException(status_code=400, detail="Invalid cron expression")
        request.app.state.cron_manager.remove_job(schedule_id)
        request.app.state.cron_manager.add_job(
            job_id=schedule_id,
            cron_expression=updates["cron"],
            handler=request.app.state.run_scheduled_job,
            user_id=user_id,
            job_data={"schedule_id": schedule_id},
        )
    if "enabled" in updates:
        if updates["enabled"]:
            request.app.state.cron_manager.resume_job(schedule_id)
        else:
            request.app.state.cron_manager.pause_job(schedule_id)

    ok = await repo.update(user_id, schedule_id, updates)
    if not ok:
        raise HTTPException(status_code=500, detail="Failed to update schedule")
    return {"success": True, "message": "Schedule updated"}


@router.delete("/{schedule_id}")
async def delete_schedule(schedule_id: str, request: Request, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    repo = ScheduleRepository()
    request.app.state.cron_manager.remove_job(schedule_id)
    deleted = await repo.delete(user_id, schedule_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"success": True, "message": "Schedule deleted"}
