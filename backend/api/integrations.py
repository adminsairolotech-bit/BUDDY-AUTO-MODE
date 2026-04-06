from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException

from database.models import IntegrationConnectRequest
from database.repositories import UserRepository
from utils.audit import AuditLogger
from utils.security import encrypt_api_key, get_current_user


router = APIRouter(prefix="/api/integrations", tags=["integrations"])


@router.get("")
async def list_integrations(current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    repo = UserRepository()
    user = await repo.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    integrations = user.get("integrations", {})
    result = []
    for integration_id in ["telegram", "gmail", "calendar", "notion", "github", "gemini"]:
        item = integrations.get(integration_id, {"connected": False})
        result.append(
            {
                "id": integration_id,
                "name": integration_id.capitalize(),
                "status": "connected" if item.get("connected") else "not_connected",
                **{k: v for k, v in item.items() if k not in {"connected"} and not k.endswith("_encrypted")},
            }
        )
    return {"success": True, "integrations": result}


@router.post("/{integration_id}/connect")
async def connect_integration(integration_id: str, payload: IntegrationConnectRequest, current_user: dict = Depends(get_current_user)):
    if integration_id not in {"telegram", "gmail", "calendar", "notion", "github", "gemini"}:
        raise HTTPException(status_code=404, detail="Unsupported integration")

    user_id = current_user.get("sub")
    repo = UserRepository()
    raw = payload.model_dump(exclude_none=True)
    data = {"connected": True, "connected_at": datetime.utcnow().isoformat(), **raw}
    if raw.get("bot_token"):
        data["bot_token_encrypted"] = encrypt_api_key(raw["bot_token"])
        data.pop("bot_token", None)
    if raw.get("refresh_token"):
        data["refresh_token_encrypted"] = encrypt_api_key(raw["refresh_token"])
        data.pop("refresh_token", None)
    if integration_id == "gemini":
        cfg = dict(raw.get("config") or {})
        if cfg.get("api_key"):
            cfg["api_key_encrypted"] = encrypt_api_key(str(cfg["api_key"]))
            cfg.pop("api_key", None)
        data["config"] = cfg
    await repo.update_integration(user_id, integration_id, data)
    await AuditLogger().log(user_id=user_id, action="integration.connect", status="success", source="api", details={"integration_id": integration_id})
    return {"success": True, "message": f"{integration_id.capitalize()} connected successfully", "bot_info": {"username": "@assistant_bot"} if integration_id == "telegram" else None}


@router.delete("/{integration_id}/disconnect")
async def disconnect_integration(integration_id: str, current_user: dict = Depends(get_current_user)):
    if integration_id not in {"telegram", "gmail", "calendar", "notion", "github", "gemini"}:
        raise HTTPException(status_code=404, detail="Unsupported integration")
    user_id = current_user.get("sub")
    repo = UserRepository()
    await repo.update_integration(user_id, integration_id, {"connected": False, "disconnected_at": datetime.utcnow().isoformat()})
    await AuditLogger().log(user_id=user_id, action="integration.disconnect", status="success", source="api", details={"integration_id": integration_id})
    return {"success": True, "message": "Integration disconnected"}
