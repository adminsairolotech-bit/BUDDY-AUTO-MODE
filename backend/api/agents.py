from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request

from database.models import AgentExecuteRequest
from utils.security import get_current_user


router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.get("")
async def list_agents(request: Request, current_user: dict = Depends(get_current_user)):
    app_state = request.app.state
    desktop_connected = app_state.desktop_ws_manager.is_connected(current_user.get("sub", ""))
    agents = [
        app_state.email_agent.metadata("active"),
        app_state.telegram_agent.metadata("active"),
        app_state.calendar_agent.metadata("active"),
        app_state.desktop_agent.metadata("connected" if desktop_connected else "offline"),
        app_state.skill_agent.metadata("active"),
    ]
    return {"success": True, "agents": agents}


@router.post("/{agent_id}/execute")
async def execute_agent(agent_id: str, payload: AgentExecuteRequest, request: Request, current_user: dict = Depends(get_current_user)):
    app_state = request.app.state
    agents = {
        "email_agent": app_state.email_agent,
        "telegram_agent": app_state.telegram_agent,
        "calendar_agent": app_state.calendar_agent,
        "desktop_agent": app_state.desktop_agent,
        "skill_agent": app_state.skill_agent,
        "search_agent": app_state.search_agent,
    }
    agent = agents.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    result = await agent.execute(payload.task, payload.params, context={"user_id": current_user.get("sub")})
    return {"success": True, "result": {"task_id": payload.task, "status": "completed" if result.get("success") else "failed", "output": result}}
