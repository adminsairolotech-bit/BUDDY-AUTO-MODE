from __future__ import annotations

import base64
import os
import pickle
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except Exception:  # pragma: no cover
    Request = None
    Credentials = None
    InstalledAppFlow = None
    build = None


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
]


class GmailService:
    def __init__(self, credentials_file: str = "credentials.json", token_file: str = "token.pickle") -> None:
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.creds = None
        self.authenticate()

    def authenticate(self) -> bool:
        if not (Request and InstalledAppFlow and build):
            return False

        if os.path.exists(self.token_file):
            with open(self.token_file, "rb") as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            elif os.path.exists(self.credentials_file):
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, SCOPES)
                self.creds = flow.run_local_server(port=0)
            else:
                return False

            with open(self.token_file, "wb") as token:
                pickle.dump(self.creds, token)

        self.service = build("gmail", "v1", credentials=self.creds)
        return True

    def send_email(self, to: str, subject: str, body: str, html: bool = False) -> dict[str, Any]:
        if not self.service:
            return {"success": False, "error": "Gmail not authenticated"}
        msg = MIMEMultipart("alternative")
        msg["to"] = to
        msg["subject"] = subject
        msg.attach(MIMEText(body, "html" if html else "plain"))

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        try:
            result = self.service.users().messages().send(userId="me", body={"raw": raw}).execute()
            return {"success": True, "message_id": result.get("id"), "thread_id": result.get("threadId")}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def get_emails(self, query: str = "is:unread", max_results: int = 10) -> list[dict[str, Any]]:
        if not self.service:
            return []
        try:
            results = self.service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
            emails = []
            for msg in results.get("messages", []):
                detail = self.get_email_details(msg["id"])
                if detail:
                    emails.append(detail)
            return emails
        except Exception:
            return []

    def search_emails(self, query: str, max_results: int = 10) -> list[dict[str, Any]]:
        return self.get_emails(query=query, max_results=max_results)

    def get_email_details(self, message_id: str) -> dict[str, Any] | None:
        if not self.service:
            return None
        try:
            msg = self.service.users().messages().get(userId="me", id=message_id, format="full").execute()
            headers = msg.get("payload", {}).get("headers", [])
            subject = next((h["value"] for h in headers if h["name"].lower() == "subject"), "No Subject")
            sender = next((h["value"] for h in headers if h["name"].lower() == "from"), "Unknown")
            date = next((h["value"] for h in headers if h["name"].lower() == "date"), "")
            return {
                "id": message_id,
                "thread_id": msg.get("threadId"),
                "subject": subject,
                "from": sender,
                "date": date,
                "snippet": msg.get("snippet", ""),
                "labels": msg.get("labelIds", []),
            }
        except Exception:
            return None

    def mark_as_read(self, message_id: str) -> bool:
        if not self.service:
            return False
        try:
            self.service.users().messages().modify(userId="me", id=message_id, body={"removeLabelIds": ["UNREAD"]}).execute()
            return True
        except Exception:
            return False

    def get_unread_count(self) -> int:
        if not self.service:
            return 0
        try:
            result = self.service.users().messages().list(userId="me", q="is:unread", maxResults=1).execute()
            return int(result.get("resultSizeEstimate", 0))
        except Exception:
            return 0
