from __future__ import annotations

import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from utils.helpers import get_settings


_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None
logger = logging.getLogger(__name__)


async def init_database() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is not None:
        return _db

    settings = get_settings()
    if "@" not in settings.mongo_url:
        logger.warning("MongoDB URL appears to have no authentication credentials.")
    if "tls=true" not in settings.mongo_url.lower() and "ssl=true" not in settings.mongo_url.lower():
        logger.warning("MongoDB TLS/SSL is not enabled in connection string.")
    _client = AsyncIOMotorClient(settings.mongo_url)
    _db = _client[settings.db_name]
    await _db.command("ping")
    return _db


def get_database() -> AsyncIOMotorDatabase:
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_database() during startup.")
    return _db


async def close_database() -> None:
    global _client, _db
    if _client is not None:
        _client.close()
    _client = None
    _db = None
