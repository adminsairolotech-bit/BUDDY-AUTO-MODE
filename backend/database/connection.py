from __future__ import annotations

import copy
import logging
import re
from dataclasses import dataclass
from typing import Any, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from utils.helpers import get_settings


_client: Optional[AsyncIOMotorClient] = None
_db: Any = None
logger = logging.getLogger(__name__)


@dataclass
class _InsertOneResult:
    inserted_id: Any


@dataclass
class _UpdateResult:
    matched_count: int
    modified_count: int
    upserted_id: Any = None


@dataclass
class _DeleteResult:
    deleted_count: int


def _is_operator_dict(value: Any) -> bool:
    return isinstance(value, dict) and any(str(k).startswith("$") for k in value)


def _get_nested(document: dict[str, Any], path: str) -> Any:
    current: Any = document
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


def _set_nested(document: dict[str, Any], path: str, value: Any) -> None:
    current = document
    parts = path.split(".")
    for part in parts[:-1]:
        next_value = current.get(part)
        if not isinstance(next_value, dict):
            next_value = {}
            current[part] = next_value
        current = next_value
    current[parts[-1]] = value


def _unset_nested(document: dict[str, Any], path: str) -> None:
    current = document
    parts = path.split(".")
    for part in parts[:-1]:
        next_value = current.get(part)
        if not isinstance(next_value, dict):
            return
        current = next_value
    current.pop(parts[-1], None)


def _match_condition(field_value: Any, condition: Any) -> bool:
    if isinstance(condition, dict):
        regex = condition.get("$regex")
        options = str(condition.get("$options", ""))
        if regex is not None:
            flags = re.IGNORECASE if "i" in options.lower() else 0
            return re.search(str(regex), "" if field_value is None else str(field_value), flags) is not None
        if "$gte" in condition:
            try:
                return field_value >= condition["$gte"]
            except TypeError:
                return False
        plain_items = {k: v for k, v in condition.items() if not str(k).startswith("$")}
        if plain_items:
            return field_value == plain_items
        return field_value == condition
    return field_value == condition


def _matches(document: dict[str, Any], query: dict[str, Any] | None) -> bool:
    if not query:
        return True
    for key, value in query.items():
        if key == "$or":
            if not any(_matches(document, subquery) for subquery in value):
                return False
            continue
        if key == "$and":
            if not all(_matches(document, subquery) for subquery in value):
                return False
            continue
        if not _match_condition(_get_nested(document, key), value):
            return False
    return True


def _apply_sort(documents: list[dict[str, Any]], sort_spec: Any) -> list[dict[str, Any]]:
    items = list(documents)
    if not sort_spec:
        return items

    if isinstance(sort_spec, tuple):
        sort_fields = [sort_spec]
    elif isinstance(sort_spec, list):
        sort_fields = sort_spec
    else:
        sort_fields = [(sort_spec, 1)]

    for field, direction in reversed(sort_fields):
        reverse = int(direction) < 0
        items.sort(key=lambda doc: _get_nested(doc, field), reverse=reverse)
    return items


def _extract_upsert_seed(query: dict[str, Any] | None) -> dict[str, Any]:
    seed: dict[str, Any] = {}
    for key, value in (query or {}).items():
        if str(key).startswith("$") or _is_operator_dict(value):
            continue
        _set_nested(seed, key, copy.deepcopy(value))
    return seed


class AsyncInMemoryCursor:
    def __init__(self, documents: list[dict[str, Any]]) -> None:
        self._documents = [copy.deepcopy(doc) for doc in documents]
        self._index = 0

    def sort(self, field: str, direction: int) -> "AsyncInMemoryCursor":
        self._documents = _apply_sort(self._documents, [(field, direction)])
        return self

    def limit(self, count: int) -> "AsyncInMemoryCursor":
        self._documents = self._documents[:count]
        return self

    async def to_list(self, length: int | None = None) -> list[dict[str, Any]]:
        if length is None:
            return [copy.deepcopy(doc) for doc in self._documents]
        return [copy.deepcopy(doc) for doc in self._documents[:length]]

    def __aiter__(self) -> "AsyncInMemoryCursor":
        self._index = 0
        return self

    async def __anext__(self) -> dict[str, Any]:
        if self._index >= len(self._documents):
            raise StopAsyncIteration
        item = copy.deepcopy(self._documents[self._index])
        self._index += 1
        return item


class AsyncInMemoryCollection:
    def __init__(self, name: str) -> None:
        self.name = name
        self._documents: list[dict[str, Any]] = []

    async def create_index(self, *args: Any, **kwargs: Any) -> str:
        return "in_memory_index"

    async def insert_one(self, document: dict[str, Any]) -> _InsertOneResult:
        doc = copy.deepcopy(document)
        doc.setdefault("_id", ObjectId())
        self._documents.append(doc)
        return _InsertOneResult(inserted_id=doc["_id"])

    async def find_one(self, query: dict[str, Any] | None = None, sort: Any = None) -> dict[str, Any] | None:
        documents = [doc for doc in self._documents if _matches(doc, query)]
        documents = _apply_sort(documents, sort)
        if not documents:
            return None
        return copy.deepcopy(documents[0])

    def find(self, query: dict[str, Any] | None = None) -> AsyncInMemoryCursor:
        documents = [doc for doc in self._documents if _matches(doc, query)]
        return AsyncInMemoryCursor(documents)

    async def find_one_and_update(
        self,
        query: dict[str, Any],
        update: dict[str, Any],
        upsert: bool = False,
        return_document: Any = None,
    ) -> dict[str, Any] | None:
        original: dict[str, Any] | None = None
        target: dict[str, Any] | None = None
        for document in self._documents:
            if _matches(document, query):
                target = document
                original = copy.deepcopy(document)
                break

        inserted = False
        if target is None:
            if not upsert:
                return None
            target = _extract_upsert_seed(query)
            target["_id"] = ObjectId()
            self._documents.append(target)
            original = None
            inserted = True

        self._apply_update(target, update, inserted=inserted)
        return copy.deepcopy(target if return_document is not None else (original or target))

    async def update_one(self, query: dict[str, Any], update: dict[str, Any], upsert: bool = False) -> _UpdateResult:
        target: dict[str, Any] | None = None
        for document in self._documents:
            if _matches(document, query):
                target = document
                break

        inserted_id = None
        if target is None:
            if not upsert:
                return _UpdateResult(matched_count=0, modified_count=0)
            target = _extract_upsert_seed(query)
            target["_id"] = ObjectId()
            self._documents.append(target)
            inserted_id = target["_id"]
            self._apply_update(target, update, inserted=True)
            return _UpdateResult(matched_count=1, modified_count=1, upserted_id=inserted_id)

        self._apply_update(target, update, inserted=False)
        return _UpdateResult(matched_count=1, modified_count=1)

    async def delete_one(self, query: dict[str, Any]) -> _DeleteResult:
        for index, document in enumerate(self._documents):
            if _matches(document, query):
                del self._documents[index]
                return _DeleteResult(deleted_count=1)
        return _DeleteResult(deleted_count=0)

    async def delete_many(self, query: dict[str, Any]) -> _DeleteResult:
        keep = [doc for doc in self._documents if not _matches(doc, query)]
        deleted = len(self._documents) - len(keep)
        self._documents = keep
        return _DeleteResult(deleted_count=deleted)

    def _apply_update(self, document: dict[str, Any], update: dict[str, Any], *, inserted: bool) -> None:
        for path, value in update.get("$setOnInsert", {}).items():
            if inserted and _get_nested(document, path) is None:
                _set_nested(document, path, copy.deepcopy(value))

        for path, value in update.get("$set", {}).items():
            _set_nested(document, path, copy.deepcopy(value))

        for path, increment in update.get("$inc", {}).items():
            current = _get_nested(document, path) or 0
            _set_nested(document, path, current + increment)

        for path, value in update.get("$push", {}).items():
            current = _get_nested(document, path)
            if not isinstance(current, list):
                current = []
                _set_nested(document, path, current)
            current.append(copy.deepcopy(value))

        for path in update.get("$unset", {}).keys():
            _unset_nested(document, path)


class AsyncInMemoryDatabase:
    def __init__(self) -> None:
        self._collections: dict[str, AsyncInMemoryCollection] = {}

    def __getattr__(self, name: str) -> AsyncInMemoryCollection:
        if name.startswith("_"):
            raise AttributeError(name)
        if name not in self._collections:
            self._collections[name] = AsyncInMemoryCollection(name)
        return self._collections[name]

    def __getitem__(self, name: str) -> AsyncInMemoryCollection:
        return getattr(self, name)

    async def command(self, name: str) -> dict[str, int]:
        if name == "ping":
            return {"ok": 1}
        return {"ok": 1}


async def init_database() -> Any:
    global _client, _db
    if _db is not None:
        return _db

    settings = get_settings()
    if "@" not in settings.mongo_url:
        logger.warning("MongoDB URL appears to have no authentication credentials.")
    if "tls=true" not in settings.mongo_url.lower() and "ssl=true" not in settings.mongo_url.lower():
        logger.warning("MongoDB TLS/SSL is not enabled in connection string.")

    try:
        _client = AsyncIOMotorClient(settings.mongo_url)
        _db = _client[settings.db_name]
        await _db.command("ping")
        logger.info("Connected to MongoDB database '%s'.", settings.db_name)
        return _db
    except Exception as exc:
        if settings.app_env == "production":
            raise
        logger.warning("MongoDB unavailable, using in-memory development fallback: %s", exc)
        _client = None
        _db = AsyncInMemoryDatabase()
        return _db


def get_database() -> Any:
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_database() during startup.")
    return _db


async def close_database() -> None:
    global _client, _db
    if _client is not None:
        _client.close()
    _client = None
    _db = None
