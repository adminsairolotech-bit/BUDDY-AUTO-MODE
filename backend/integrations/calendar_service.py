from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

import os
import pickle

try:
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except Exception:  # pragma: no cover
    Request = None
    InstalledAppFlow = None
    build = None


SCOPES = ["https://www.googleapis.com/auth/calendar"]


class CalendarService:
    def __init__(self, token_file: str = "calendar_token.pickle") -> None:
        self.token_file = token_file
        self.service = None
        self.creds = None
        self.authenticate()

    def authenticate(self, credentials_file: str = "credentials.json") -> bool:
        if not (Request and InstalledAppFlow and build):
            return False

        if os.path.exists(self.token_file):
            with open(self.token_file, "rb") as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            elif os.path.exists(credentials_file):
                flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
                self.creds = flow.run_local_server(port=0)
            else:
                return False
            with open(self.token_file, "wb") as token:
                pickle.dump(self.creds, token)

        self.service = build("calendar", "v3", credentials=self.creds)
        return True

    def get_events(self, time_min: datetime | None = None, time_max: datetime | None = None, max_results: int = 10) -> list[dict[str, Any]]:
        if not self.service:
            return []
        time_min = time_min or datetime.utcnow()
        time_max = time_max or (time_min + timedelta(days=7))
        result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=time_min.isoformat() + "Z",
                timeMax=time_max.isoformat() + "Z",
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = result.get("items", [])
        return [
            {
                "id": e.get("id"),
                "summary": e.get("summary", "No Title"),
                "start": e.get("start", {}).get("dateTime", e.get("start", {}).get("date")),
                "end": e.get("end", {}).get("dateTime", e.get("end", {}).get("date")),
                "location": e.get("location", ""),
                "description": e.get("description", ""),
                "attendees": [a.get("email") for a in e.get("attendees", [])],
            }
            for e in events
        ]

    def create_event(
        self,
        summary: str,
        start: datetime,
        end: datetime | None = None,
        description: str | None = None,
        location: str | None = None,
        attendees: list[str] | None = None,
    ) -> dict[str, Any]:
        if not self.service:
            return {"success": False, "error": "Calendar not authenticated"}
        end = end or (start + timedelta(hours=1))
        event = {
            "summary": summary,
            "start": {"dateTime": start.isoformat(), "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": end.isoformat(), "timeZone": "Asia/Kolkata"},
        }
        if description:
            event["description"] = description
        if location:
            event["location"] = location
        if attendees:
            event["attendees"] = [{"email": e} for e in attendees]
        created = self.service.events().insert(calendarId="primary", body=event).execute()
        return {"success": True, "event_id": created.get("id"), "link": created.get("htmlLink", "")}

    def update_event(self, event_id: str, updates: dict[str, Any]) -> dict[str, Any]:
        if not self.service:
            return {"success": False, "error": "Calendar not authenticated"}
        event = self.service.events().get(calendarId="primary", eventId=event_id).execute()
        event.update(updates)
        updated = self.service.events().update(calendarId="primary", eventId=event_id, body=event).execute()
        return {"success": True, "event_id": updated.get("id")}

    def delete_event(self, event_id: str) -> bool:
        if not self.service:
            return False
        try:
            self.service.events().delete(calendarId="primary", eventId=event_id).execute()
            return True
        except Exception:
            return False

    def get_today_summary(self) -> str:
        start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        events = self.get_events(start, end, max_results=50)
        if not events:
            return "No events scheduled for today."
        lines = [f"You have {len(events)} event(s) today:"]
        for event in events:
            raw = event["start"]
            time_str = raw.split("T")[1][:5] if isinstance(raw, str) and "T" in raw else "All day"
            lines.append(f"- {time_str} {event['summary']}")
        return "\n".join(lines)
