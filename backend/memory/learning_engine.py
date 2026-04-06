from __future__ import annotations

import json
import os
import re
from datetime import datetime
from typing import Any

from database.connection import get_database


class LearningEngine:
    def __init__(self, memory_dir: str = "ai_memory") -> None:
        self.db = get_database()
        self.errors_collection = self.db.errors
        self.solutions_collection = self.db.solutions

        self.memory_dir = memory_dir
        os.makedirs(self.memory_dir, exist_ok=True)
        self.errors_log = os.path.join(self.memory_dir, "errors.log")
        self.solutions_log = os.path.join(self.memory_dir, "solutions.log")

    def normalize_error(self, error: str) -> str:
        value = error
        value = re.sub(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}", "[TIMESTAMP]", value)
        value = re.sub(r"[a-f0-9]{24,}", "[ID]", value)
        value = re.sub(r"[a-f0-9]{8}-[a-f0-9-]{27}", "[UUID]", value)
        value = re.sub(r"line \d+", "line [N]", value)
        value = re.sub(r"([a-zA-Z]:)?[\\/][\w .\\/:-]+\.\w+", "[PATH]", value)
        return value.strip()

    async def log_error(self, error_type: str, error_message: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        normalized = self.normalize_error(error_message)
        now = datetime.utcnow()

        existing = await self.errors_collection.find_one({"normalized_error": normalized})
        if existing:
            await self.errors_collection.update_one(
                {"_id": existing["_id"]},
                {"$inc": {"occurrence_count": 1}, "$set": {"last_seen": now}},
            )
            result = {"error_id": str(existing["_id"]), "is_known": True}
        else:
            ins = await self.errors_collection.insert_one(
                {
                    "error_type": error_type,
                    "error_message": error_message,
                    "normalized_error": normalized,
                    "context": context or {},
                    "occurrence_count": 1,
                    "first_seen": now,
                    "last_seen": now,
                    "resolved": False,
                }
            )
            result = {"error_id": str(ins.inserted_id), "is_known": False}

        solution = await self.get_solution(normalized)
        result["solution"] = solution
        self._write_log(
            self.errors_log,
            {
                "error_id": result["error_id"],
                "type": error_type,
                "message": error_message,
                "normalized": normalized,
                "timestamp": now.isoformat(),
            },
        )
        return result

    async def get_solution(self, normalized_error: str) -> dict[str, Any] | None:
        doc = await self.solutions_collection.find_one({"error_pattern": normalized_error, "success_rate": {"$gte": 0.5}})
        if not doc:
            return None
        await self.solutions_collection.update_one(
            {"_id": doc["_id"]},
            {"$inc": {"times_applied": 1}, "$set": {"last_used": datetime.utcnow()}},
        )
        return {"solution_id": str(doc["_id"]), "solution": doc.get("solution"), "success_rate": doc.get("success_rate", 0.0)}

    async def record_solution(self, error_pattern: str, solution: dict[str, Any], worked: bool) -> None:
        now = datetime.utcnow()
        existing = await self.solutions_collection.find_one({"error_pattern": error_pattern})
        if existing:
            times_applied = int(existing.get("times_applied", 0)) + 1
            times_worked = int(existing.get("times_worked", 0)) + (1 if worked else 0)
            success_rate = times_worked / max(1, times_applied)
            await self.solutions_collection.update_one(
                {"_id": existing["_id"]},
                {
                    "$set": {
                        "solution": solution if worked else existing.get("solution"),
                        "success_rate": success_rate,
                        "times_applied": times_applied,
                        "times_worked": times_worked,
                        "last_used": now,
                    }
                },
            )
        else:
            await self.solutions_collection.insert_one(
                {
                    "error_pattern": error_pattern,
                    "solution": solution,
                    "success_rate": 1.0 if worked else 0.0,
                    "times_applied": 1,
                    "times_worked": 1 if worked else 0,
                    "created_at": now,
                    "last_used": now,
                }
            )

        if worked:
            await self.errors_collection.update_many({"normalized_error": error_pattern}, {"$set": {"resolved": True}})

        self._write_log(
            self.solutions_log,
            {"error_pattern": error_pattern, "solution": solution, "worked": worked, "timestamp": now.isoformat()},
        )

    def get_recent_errors(self, limit: int = 20) -> list[dict[str, Any]]:
        if not os.path.exists(self.errors_log):
            return []
        rows: list[dict[str, Any]] = []
        with open(self.errors_log, "r", encoding="utf-8") as f:
            for line in f.readlines()[-limit:]:
                try:
                    rows.append(json.loads(line.strip()))
                except Exception:
                    continue
        return rows

    def _write_log(self, path: str, data: dict[str, Any]) -> None:
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, default=str) + "\n")
