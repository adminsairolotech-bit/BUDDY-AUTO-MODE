from __future__ import annotations

from typing import Any

from integrations.gmail_service import GmailService

from .base_agent import BaseAgent


class EmailAgent(BaseAgent):
    id = "email_agent"
    name = "Email Agent"
    description = "Handles Gmail operations"
    capabilities = ["send", "read", "search", "draft", "unread_count"]

    def __init__(self, gmail_service: GmailService | None = None) -> None:
        self.gmail = gmail_service or GmailService()

    async def execute(self, task: str, params: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
        if task == "send_email":
            return self.gmail.send_email(
                to=params.get("to", ""),
                subject=params.get("subject", "No Subject"),
                body=params.get("body", ""),
                html=bool(params.get("html", False)),
            )
        if task == "read_email":
            return {"success": True, "emails": self.gmail.get_emails(query=params.get("query", "is:unread"), max_results=10)}
        if task == "search_email":
            return {"success": True, "emails": self.gmail.search_emails(query=params.get("query", ""), max_results=10)}
        if task == "unread_count":
            return {"success": True, "count": self.gmail.get_unread_count()}
        return {"success": False, "error": f"Unknown email task: {task}"}
