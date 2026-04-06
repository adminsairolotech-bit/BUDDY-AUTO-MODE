from __future__ import annotations

import re
from typing import Any


class IntentParser:
    def __init__(self) -> None:
        self.patterns: dict[str, dict[str, list[str]]] = {
            "email": {
                "keywords": ["email", "mail", "inbox", "compose"],
                "patterns": [
                    r"(send|write|compose|draft)\s*(an?\s*)?(email|mail)",
                    r"(check|read)\s*(my\s*)?(email|inbox)",
                    r"email\s+(to|about)",
                ],
            },
            "telegram": {
                "keywords": ["telegram", "message", "msg", "tg"],
                "patterns": [r"telegram", r"message\s+(to|on)"],
            },
            "calendar": {
                "keywords": ["calendar", "schedule", "meeting", "appointment", "event", "remind"],
                "patterns": [r"(schedule|create|add)\s+(a\s*)?(meeting|event|appointment)", r"calendar"],
            },
            "desktop": {
                "keywords": ["open", "launch", "start", "close", "screenshot", "click", "type"],
                "patterns": [
                    r"(open|launch|start|run)\s+\w+",
                    r"(take|capture)\s*(a\s*)?screenshot",
                    r"(click|type|press)\s+",
                ],
            },
            "weather": {"keywords": ["weather", "forecast", "temperature"], "patterns": [r"weather\s+(in|at|for)\s+\w+"]},
            "news": {"keywords": ["news", "headlines", "latest"], "patterns": [r"(latest|today's)\s+news", r"headlines"]},
            "memory": {"keywords": ["remember", "note", "save"], "patterns": [r"remember\s+that", r"(make|take)\s+a\s+note"]},
        }

    def parse(self, command: str) -> tuple[str, float]:
        text = command.lower().strip()
        scores: dict[str, int] = {}
        for intent, cfg in self.patterns.items():
            score = 0
            score += sum(1 for k in cfg["keywords"] if k in text)
            score += sum(2 for p in cfg["patterns"] if re.search(p, text))
            if score:
                scores[intent] = score

        if not scores:
            return "chat", 0.4
        best = max(scores, key=scores.get)
        return best, min(scores[best] / 6.0, 1.0)

    def extract_params(self, command: str, intent: str) -> dict[str, Any]:
        params: dict[str, Any] = {}
        lower = command.lower()
        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", command)
        if email_match:
            params["to"] = email_match.group(0)
        url_match = re.search(r"https?://\S+", command)
        if url_match:
            params["url"] = url_match.group(0)

        if intent == "email":
            about = re.search(r"about\s+(.+?)(?:$|[.?!])", lower)
            if about:
                params["subject"] = about.group(1).strip().title()
            to_name = re.search(r"to\s+([a-z0-9._-]+)", lower)
            if to_name and "to" not in params:
                params["to_name"] = to_name.group(1)

        if intent == "desktop":
            open_app = re.search(r"(open|launch|start|run)\s+([a-z0-9._-]+)", lower)
            if open_app:
                params["action"] = "open_app"
                params["app_name"] = open_app.group(2)
            if "screenshot" in lower:
                params["action"] = "screenshot"

        if intent == "weather":
            loc = re.search(r"(?:in|at|for)\s+([a-z\s]+)$", lower)
            if loc:
                params["location"] = loc.group(1).strip().title()

        if intent == "calendar":
            when = re.search(r"(today|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday)", lower)
            if when:
                params["date"] = when.group(1)
            at = re.search(r"at\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)", lower)
            if at:
                params["time"] = at.group(1)

        return params
