from __future__ import annotations

from typing import Any, Awaitable, Callable

from database.repositories import SkillRepository
from skills.builtin.calculator import run as calculator_run
from skills.builtin.news import run as news_run
from skills.builtin.notes import run as notes_run
from skills.builtin.translator import run as translator_run
from skills.builtin.weather import run as weather_run


BuiltinFn = Callable[[dict[str, Any], dict[str, Any] | None], Awaitable[dict[str, Any]]]


class SkillLoader:
    def __init__(self) -> None:
        self.repo = SkillRepository()
        self.builtin: dict[str, BuiltinFn] = {
            "weather": weather_run,
            "news": news_run,
            "calculator": calculator_run,
            "translator": translator_run,
            "notes": notes_run,
        }

    async def list_skills(self, user_id: str) -> list[dict[str, Any]]:
        db_items = await self.repo.list(user_id)
        builtins = [
            {
                "skill_id": k,
                "name": k.capitalize(),
                "description": f"Built-in {k} skill",
                "trigger_phrases": [k],
                "type": "builtin",
            }
            for k in self.builtin
        ]
        # Merge and dedupe by skill_id.
        merged: dict[str, dict[str, Any]] = {s["skill_id"]: s for s in builtins}
        for item in db_items:
            sid = item.get("skill_id")
            if sid:
                merged[sid] = item
        return list(merged.values())

    def get_builtin(self, skill_id: str) -> BuiltinFn | None:
        return self.builtin.get(skill_id)
