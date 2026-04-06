from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from database.connection import get_database
from memory.memory_manager import MemoryManager
from utils.audit import AuditLogger
from utils.security import get_current_user
from utils.sanitizers import sanitize_for_log


router = APIRouter(prefix="/api/privacy", tags=["privacy"])


@router.post("/export")
async def export_data(current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    db = get_database()
    memories = await db.memory.find({"user_id": user_id}).to_list(length=5000)
    conversations = await db.conversations.find({"user_id": user_id}).to_list(length=5000)
    tasks = await db.tasks.find({"user_id": user_id}).sort("created_at", -1).limit(1000).to_list(length=1000)
    schedules = await db.schedules.find({"user_id": user_id}).to_list(length=1000)
    data = {
        "user_id": user_id,
        "memory": sanitize_for_log(memories),
        "conversations": sanitize_for_log(conversations),
        "tasks": sanitize_for_log(tasks),
        "schedules": sanitize_for_log(schedules),
    }
    await AuditLogger().log(user_id=user_id, action="privacy.export", status="success", source="api", details={"items": len(memories) + len(conversations)})
    return {"success": True, "data": data}


@router.post("/forget-me")
async def forget_me(current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    manager = MemoryManager(user_id)
    result = await manager.forget_me()
    await AuditLogger().log(user_id=user_id, action="privacy.forget_me", status="success", source="api", details=result)
    return {"success": True, "message": "User memory and conversations deleted", "data": result}


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    manager = MemoryManager(user_id)
    ok = await manager.delete_conversation(conversation_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Conversation not found")
    await AuditLogger().log(user_id=user_id, action="privacy.delete_conversation", status="success", source="api", details={"conversation_id": conversation_id})
    return {"success": True, "message": "Conversation deleted"}
