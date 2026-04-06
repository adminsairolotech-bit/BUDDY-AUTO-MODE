from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from agents.calendar_agent import CalendarAgent
from agents.desktop_agent import DesktopControlAgent
from agents.email_agent import EmailAgent
from agents.search_agent import SearchAgent
from agents.skill_agent import SkillAgent
from agents.telegram_agent import TelegramAgent
from api import ALL_ROUTERS
from api.websocket import DesktopWebSocketManager
from core.gemini_engine import GeminiEngine
from core.intent_parser import IntentParser
from core.task_router import TaskRouter
from database.connection import close_database, init_database
from database.repositories import ScheduleRepository
from scheduler.cron_manager import CronManager
from skills.skill_executor import SkillExecutor
from skills.skill_loader import SkillLoader
from utils.error_handler import build_error_middleware
from utils.helpers import get_settings
from utils.rate_limiter import RateLimiter


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
logger = logging.getLogger("openclaw")


async def _telegram_command_handler(**kwargs):
    return {"response_text": "Telegram command handler is available via backend /api/command flow."}


async def _seed_builtin_skills(app: FastAPI) -> None:
    db = app.state.db
    collection = db.skills
    for skill_id, name in [
        ("weather", "Weather"),
        ("news", "News"),
        ("calculator", "Calculator"),
        ("translator", "Translator"),
        ("notes", "Notes"),
    ]:
        exists = await collection.find_one({"skill_id": skill_id, "user_id": None})
        if exists:
            continue
        await collection.insert_one(
            {
                "skill_id": skill_id,
                "user_id": None,
                "name": name,
                "description": f"Built-in {name.lower()} skill",
                "type": "builtin",
                "trigger_phrases": [name.lower()],
                "actions": [],
                "response_template": "",
                "enabled": True,
                "usage_count": 0,
                "created_at": datetime.utcnow(),
            }
        )


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.settings = settings
    app.state.db = await init_database()
    app.state.rate_limiter = RateLimiter()
    await app.state.db.revoked_tokens.create_index("exp", expireAfterSeconds=0)
    await app.state.db.audit_logs.create_index("created_at")

    # Core engines and managers
    app.state.gemini_engine = GeminiEngine(settings.gemini_api_key)
    app.state.intent_parser = IntentParser()
    app.state.desktop_ws_manager = DesktopWebSocketManager()
    app.state.skill_loader = SkillLoader()
    app.state.skill_executor = SkillExecutor(app.state.skill_loader)
    app.state.cron_manager = CronManager()

    # Agents
    app.state.email_agent = EmailAgent()
    app.state.telegram_agent = TelegramAgent(settings.telegram_bot_token, command_handler=_telegram_command_handler)
    app.state.calendar_agent = CalendarAgent()
    app.state.desktop_agent = DesktopControlAgent(app.state.desktop_ws_manager)
    app.state.search_agent = SearchAgent()
    app.state.skill_agent = SkillAgent(app.state.skill_executor)

    app.state.task_router = TaskRouter(
        email_agent=app.state.email_agent,
        telegram_agent=app.state.telegram_agent,
        calendar_agent=app.state.calendar_agent,
        desktop_agent=app.state.desktop_agent,
        search_agent=app.state.search_agent,
        skill_agent=app.state.skill_agent,
    )

    async def run_scheduled_job(user_id: str, job_id: str, job_data: dict[str, Any]):
        schedule_id = job_data.get("schedule_id", job_id)
        repo = ScheduleRepository()
        schedule = await repo.get(user_id, schedule_id)
        if not schedule or not schedule.get("enabled", True):
            return
        for action in schedule.get("actions", []):
            action_type = action.get("type")
            if action_type == "skill":
                await app.state.skill_executor.execute(
                    skill_id=action.get("skill_id", ""),
                    params=action.get("params", {}),
                    user_id=user_id,
                )
            elif action_type == "agent":
                await app.state.task_router.route(
                    intent=action.get("agent_id", "").replace("_agent", ""),
                    action=action.get("action", ""),
                    params=action.get("params", {}),
                    context={"user_id": user_id},
                )
            else:
                await app.state.task_router.route(
                    intent=action_type or "chat",
                    action=action.get("action", ""),
                    params=action.get("params", {}),
                    context={"user_id": user_id},
                )

    app.state.run_scheduled_job = run_scheduled_job
    app.state.cron_manager.start()

    await _seed_builtin_skills(app)
    logger.info("OpenClaw backend started on %s:%s", settings.host, settings.port)
    try:
        yield
    finally:
        app.state.cron_manager.stop()
        await close_database()
        logger.info("OpenClaw backend stopped")


app = FastAPI(
    title="OpenClaw Clone API",
    version="1.0.0",
    description="OpenClaw-like AI Personal Assistant backend",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(build_error_middleware())


@app.middleware("http")
async def enforce_secure_transport(request: Request, call_next):
    settings = get_settings()
    if settings.require_secure_transport:
        scheme = request.url.scheme.lower()
        host = request.client.host if request.client else ""
        is_local = settings.allow_insecure_localhost and host in {"127.0.0.1", "::1", "localhost"}
        if scheme != "https" and not is_local:
            return JSONResponse(status_code=426, content={"success": False, "error": "HTTPS is required"})
    return await call_next(request)

for r in ALL_ROUTERS:
    app.include_router(r)


@app.get("/")
async def root():
    return {"success": True, "message": "OpenClaw Clone backend is running"}


@app.get("/api/health")
async def health():
    return {"success": True, "status": "ok"}
