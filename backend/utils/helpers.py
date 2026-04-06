from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()


class Settings(BaseModel):
    app_env: str = os.getenv("APP_ENV", "development")
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8001"))
    mongo_url: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    db_name: str = os.getenv("DB_NAME", "openclaw_db")
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "change-this-secret-in-production")
    jwt_refresh_secret_key: str = os.getenv("JWT_REFRESH_SECRET_KEY", os.getenv("JWT_SECRET_KEY", "change-this-secret-in-production"))
    jwt_prev_secret_key: str = os.getenv("JWT_PREV_SECRET_KEY", "")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
    refresh_token_expire_days: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "14"))
    encryption_key: str = os.getenv("ENCRYPTION_KEY", "")
    desktop_signing_secret: str = os.getenv("DESKTOP_SIGNING_SECRET", "")
    require_secure_transport: bool = os.getenv("REQUIRE_SECURE_TRANSPORT", "false").lower() in {"1", "true", "yes"}
    allow_insecure_localhost: bool = os.getenv("ALLOW_INSECURE_LOCALHOST", "true").lower() in {"1", "true", "yes"}
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    telegram_bot_token: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID", "")
    google_client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    weather_api_key: str = os.getenv("WEATHER_API_KEY", "")
    news_api_key: str = os.getenv("NEWS_API_KEY", "")


@lru_cache
def get_settings() -> Settings:
    return Settings()


def utc_now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()


def ok(data: Any = None, message: str | None = None) -> dict[str, Any]:
    return {"success": True, "data": data, "error": None, "message": message}


def fail(error: str, message: str | None = None, data: Any = None) -> dict[str, Any]:
    return {"success": False, "data": data, "error": error, "message": message}
