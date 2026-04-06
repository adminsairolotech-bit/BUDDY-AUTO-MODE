from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException, Request

from database.models import SkillCreateRequest, SkillExecuteRequest
from database.repositories import SkillRepository
from utils.security import get_current_user


router = APIRouter(prefix="/api/skills", tags=["skills"])


@router.get("")
async def list_skills(request: Request, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    loader = request.app.state.skill_loader
    items = await loader.list_skills(user_id)
    skills = [
        {
            "id": s.get("skill_id"),
            "name": s.get("name"),
            "description": s.get("description"),
            "trigger_phrases": s.get("trigger_phrases", []),
            "type": s.get("type", "custom"),
        }
        for s in items
    ]
    return {"success": True, "skills": skills}


@router.post("", status_code=201)
async def create_skill(payload: SkillCreateRequest, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    repo = SkillRepository()
    skill_id = f"skill_{uuid.uuid4().hex[:8]}"
    await repo.create(
        user_id=user_id,
        data={
            "skill_id": skill_id,
            "name": payload.name,
            "description": payload.description,
            "type": "custom",
            "trigger_phrases": payload.trigger_phrases,
            "actions": [a.model_dump() for a in payload.actions],
            "response_template": payload.response_template,
            "enabled": True,
        },
    )
    return {"success": True, "skill_id": skill_id}


@router.post("/{skill_id}/execute")
async def execute_skill(skill_id: str, payload: SkillExecuteRequest, request: Request, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    executor = request.app.state.skill_executor
    result = await executor.execute(skill_id, payload.params, user_id=user_id)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Skill execution failed"))
    return {"success": True, "result": result.get("result")}
