from __future__ import annotations

from fastapi import APIRouter, Depends

from database.models import MemoryLearnRequest, MemoryWriteRequest
from memory.memory_manager import MemoryManager
from utils.audit import AuditLogger
from utils.security import get_current_user


router = APIRouter(prefix="/api/memory", tags=["memory"])


@router.get("")
async def get_memory(current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    manager = MemoryManager(user_id)
    context = await manager.get_user_context()
    return {"success": True, "memory": context}


@router.post("")
async def write_memory(payload: MemoryWriteRequest, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    manager = MemoryManager(user_id)
    await manager.store_memory(payload.type, payload.key, payload.value, payload.context, payload.confidence)
    await AuditLogger().log(user_id=user_id, action="memory.write", status="success", source="api", details={"key": payload.key, "type": payload.type})
    return {"success": True, "message": "Memory stored successfully"}


@router.post("/learn")
async def learn(payload: MemoryLearnRequest, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    manager = MemoryManager(user_id)
    await manager.learn_from_interaction(payload.input, payload.interpreted_as, payload.params_learned, payload.feedback)
    return {"success": True, "learning_id": f"learn_{payload.interpreted_as}"}


@router.delete("/all")
async def delete_all_memory(current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    manager = MemoryManager(user_id)
    deleted = await manager.delete_all_memory()
    await AuditLogger().log(user_id=user_id, action="memory.delete_all", status="success", source="api", details={"deleted": deleted})
    return {"success": True, "message": "All memory deleted", "deleted": deleted}
