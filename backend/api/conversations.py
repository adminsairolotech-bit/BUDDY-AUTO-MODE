from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from memory.memory_manager import MemoryManager
from utils.audit import AuditLogger
from utils.security import get_current_user


router = APIRouter(prefix="/api/conversations", tags=["conversations"])


@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    manager = MemoryManager(user_id)
    ok = await manager.delete_conversation(conversation_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Conversation not found")
    await AuditLogger().log(
        user_id=user_id,
        action="conversation.delete",
        status="success",
        source="api",
        details={"conversation_id": conversation_id},
    )
    return {"success": True, "message": "Conversation deleted"}
