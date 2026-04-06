from __future__ import annotations

from datetime import datetime
from typing import Any

from bson import ObjectId
from pymongo import ReturnDocument

from .connection import get_database


def _to_str_id(doc: dict[str, Any] | None) -> dict[str, Any] | None:
    if not doc:
        return doc
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc


class UserRepository:
    def __init__(self) -> None:
        self.collection = get_database().users

    async def create(self, email: str, password_hash: str, name: str) -> dict[str, Any]:
        now = datetime.utcnow()
        doc = {
            "email": email,
            "password_hash": password_hash,
            "name": name,
            "created_at": now,
            "updated_at": now,
            "preferences": {
                "language": "en",
                "timezone": "Asia/Kolkata",
                "notification_enabled": True,
                "voice_enabled": True,
                "personality": "friendly",
            },
            "integrations": {},
            "desktop_agent": {"connected": False, "last_seen": None, "device_info": None},
        }
        result = await self.collection.insert_one(doc)
        doc["_id"] = result.inserted_id
        return _to_str_id(doc) or {}

    async def find_by_email(self, email: str) -> dict[str, Any] | None:
        return _to_str_id(await self.collection.find_one({"email": email}))

    async def find_by_id(self, user_id: str) -> dict[str, Any] | None:
        try:
            oid = ObjectId(user_id)
        except Exception:
            return None
        return _to_str_id(await self.collection.find_one({"_id": oid}))

    async def update_desktop_status(self, user_id: str, connected: bool, device_info: dict[str, Any] | None = None) -> None:
        try:
            oid = ObjectId(user_id)
        except Exception:
            return
        await self.collection.update_one(
            {"_id": oid},
            {
                "$set": {
                    "desktop_agent.connected": connected,
                    "desktop_agent.last_seen": datetime.utcnow(),
                    "desktop_agent.device_info": device_info,
                    "updated_at": datetime.utcnow(),
                }
            },
        )

    async def update_integration(self, user_id: str, integration_id: str, data: dict[str, Any]) -> None:
        try:
            oid = ObjectId(user_id)
        except Exception:
            return
        await self.collection.update_one(
            {"_id": oid},
            {"$set": {f"integrations.{integration_id}": data, "updated_at": datetime.utcnow()}},
        )


class ConversationRepository:
    def __init__(self) -> None:
        self.collection = get_database().conversations

    async def get_or_create(self, user_id: str, conversation_id: str) -> dict[str, Any]:
        now = datetime.utcnow()
        doc = await self.collection.find_one_and_update(
            {"user_id": user_id, "conversation_id": conversation_id},
            {
                "$setOnInsert": {
                    "user_id": user_id,
                    "conversation_id": conversation_id,
                    "created_at": now,
                    "messages": [],
                    "summary": "",
                    "entities_extracted": [],
                },
                "$set": {"updated_at": now},
            },
            upsert=True,
            return_document=ReturnDocument.AFTER,
        )
        return _to_str_id(doc) or {}

    async def append_message(self, user_id: str, conversation_id: str, message: dict[str, Any]) -> None:
        await self.collection.update_one(
            {"user_id": user_id, "conversation_id": conversation_id},
            {"$push": {"messages": message}, "$set": {"updated_at": datetime.utcnow()}},
            upsert=True,
        )

    async def set_summary(self, user_id: str, conversation_id: str, summary: str, entities: list[str]) -> None:
        await self.collection.update_one(
            {"user_id": user_id, "conversation_id": conversation_id},
            {"$set": {"summary": summary, "entities_extracted": entities, "updated_at": datetime.utcnow()}},
        )

    async def latest_for_user(self, user_id: str) -> dict[str, Any] | None:
        doc = await self.collection.find_one({"user_id": user_id}, sort=[("updated_at", -1)])
        return _to_str_id(doc)

    async def delete_conversation(self, user_id: str, conversation_id: str) -> bool:
        result = await self.collection.delete_one({"user_id": user_id, "conversation_id": conversation_id})
        return result.deleted_count > 0

    async def delete_all_for_user(self, user_id: str) -> int:
        result = await self.collection.delete_many({"user_id": user_id})
        return result.deleted_count


class MemoryRepository:
    def __init__(self) -> None:
        self.collection = get_database().memory

    async def upsert(self, user_id: str, memory_type: str, key: str, value: Any, context: str | None, confidence: float) -> str:
        now = datetime.utcnow()
        existing = await self.collection.find_one({"user_id": user_id, "key": key})
        if existing:
            doc = await self.collection.find_one_and_update(
                {"user_id": user_id, "key": key},
                {
                    "$set": {
                        "type": memory_type,
                        "value": value,
                        "context": context,
                        "confidence": confidence,
                        "updated_at": now,
                        "last_accessed": now,
                    },
                    "$inc": {"access_count": 1},
                },
                return_document=ReturnDocument.AFTER,
            )
        else:
            doc = await self.collection.find_one_and_update(
                {"user_id": user_id, "key": key},
                {
                    "$set": {
                        "type": memory_type,
                        "value": value,
                        "context": context,
                        "confidence": confidence,
                        "updated_at": now,
                        "last_accessed": now,
                        "created_at": now,
                        "access_count": 1,
                        "source": "conversation",
                    },
                },
                upsert=True,
                return_document=ReturnDocument.AFTER,
            )
        return str(doc["_id"])

    async def get(self, user_id: str, key: str) -> dict[str, Any] | None:
        doc = await self.collection.find_one_and_update(
            {"user_id": user_id, "key": key},
            {"$set": {"last_accessed": datetime.utcnow()}, "$inc": {"access_count": 1}},
            return_document=ReturnDocument.AFTER,
        )
        return _to_str_id(doc)

    async def search(self, user_id: str, query: str, limit: int = 10) -> list[dict[str, Any]]:
        cursor = self.collection.find(
            {
                "user_id": user_id,
                "$or": [
                    {"key": {"$regex": query, "$options": "i"}},
                    {"context": {"$regex": query, "$options": "i"}},
                    {"value": {"$regex": query, "$options": "i"}},
                ],
            }
        ).sort("access_count", -1).limit(limit)
        docs = await cursor.to_list(length=limit)
        return [_to_str_id(d) or {} for d in docs]

    async def by_type(self, user_id: str, memory_type: str, limit: int = 100) -> list[dict[str, Any]]:
        docs = await self.collection.find({"user_id": user_id, "type": memory_type}).limit(limit).to_list(length=limit)
        return [_to_str_id(d) or {} for d in docs]

    async def delete(self, user_id: str, key: str) -> bool:
        result = await self.collection.delete_one({"user_id": user_id, "key": key})
        return result.deleted_count > 0

    async def delete_all(self, user_id: str) -> int:
        result = await self.collection.delete_many({"user_id": user_id})
        return result.deleted_count


class TaskRepository:
    def __init__(self) -> None:
        self.collection = get_database().tasks

    async def create(self, task_id: str, user_id: str, payload: dict[str, Any]) -> None:
        now = datetime.utcnow()
        await self.collection.insert_one(
            {
                "task_id": task_id,
                "user_id": user_id,
                "status": "pending",
                "created_at": now,
                "updated_at": now,
                **payload,
            }
        )

    async def complete(self, task_id: str, result: dict[str, Any], success: bool = True, error: str | None = None) -> None:
        now = datetime.utcnow()
        await self.collection.update_one(
            {"task_id": task_id},
            {
                "$set": {
                    "status": "completed" if success else "failed",
                    "result": result,
                    "error": error,
                    "completed_at": now,
                    "updated_at": now,
                }
            },
        )


class SkillRepository:
    def __init__(self) -> None:
        self.collection = get_database().skills

    async def list(self, user_id: str) -> list[dict[str, Any]]:
        docs = await self.collection.find({"$or": [{"user_id": None}, {"user_id": user_id}]}).to_list(length=200)
        return [_to_str_id(d) or {} for d in docs]

    async def create(self, user_id: str, data: dict[str, Any]) -> str:
        doc = {"user_id": user_id, "created_at": datetime.utcnow(), "usage_count": 0, **data}
        result = await self.collection.insert_one(doc)
        return str(result.inserted_id)

    async def get(self, user_id: str, skill_id: str) -> dict[str, Any] | None:
        doc = await self.collection.find_one({"$or": [{"skill_id": skill_id, "user_id": None}, {"skill_id": skill_id, "user_id": user_id}]})
        return _to_str_id(doc)


class ScheduleRepository:
    def __init__(self) -> None:
        self.collection = get_database().schedules

    async def list(self, user_id: str) -> list[dict[str, Any]]:
        docs = await self.collection.find({"user_id": user_id}).sort("created_at", -1).to_list(length=500)
        return [_to_str_id(d) or {} for d in docs]

    async def create(self, user_id: str, data: dict[str, Any]) -> str:
        doc = {
            "user_id": user_id,
            "enabled": True,
            "created_at": datetime.utcnow(),
            "run_history": [],
            **data,
        }
        result = await self.collection.insert_one(doc)
        return str(result.inserted_id)

    async def update(self, user_id: str, schedule_id: str, data: dict[str, Any]) -> bool:
        result = await self.collection.update_one({"user_id": user_id, "schedule_id": schedule_id}, {"$set": data})
        return result.matched_count > 0

    async def delete(self, user_id: str, schedule_id: str) -> bool:
        result = await self.collection.delete_one({"user_id": user_id, "schedule_id": schedule_id})
        return result.deleted_count > 0

    async def get(self, user_id: str, schedule_id: str) -> dict[str, Any] | None:
        doc = await self.collection.find_one({"user_id": user_id, "schedule_id": schedule_id})
        return _to_str_id(doc)


class ErrorRepository:
    def __init__(self) -> None:
        self.errors = get_database().errors
        self.solutions = get_database().solutions
