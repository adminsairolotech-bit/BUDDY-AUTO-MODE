from __future__ import annotations

import asyncio
import hashlib
import hmac
import uuid
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from utils.audit import AuditLogger
from utils.helpers import get_settings


router = APIRouter(tags=["websocket"])


class DesktopWebSocketManager:
    def __init__(self) -> None:
        self.desktop_connections: dict[str, WebSocket] = {}
        self.desktop_info: dict[str, dict[str, Any]] = {}
        self.pending_tasks: dict[str, asyncio.Future] = {}

    async def connect(self, user_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        await websocket.send_json({"type": "connected", "message": "WebSocket connected", "user_id": user_id})

    def register_desktop(self, user_id: str, websocket: WebSocket, info: dict[str, Any]) -> None:
        self.desktop_connections[user_id] = websocket
        self.desktop_info[user_id] = {
            **info,
            "connected_since": datetime.now(timezone.utc).isoformat(),
            "last_heartbeat": datetime.now(timezone.utc).isoformat(),
        }

    def touch_heartbeat(self, user_id: str) -> None:
        if user_id in self.desktop_info:
            self.desktop_info[user_id]["last_heartbeat"] = datetime.now(timezone.utc).isoformat()

    def disconnect(self, user_id: str, websocket: WebSocket) -> None:
        if self.desktop_connections.get(user_id) is websocket:
            self.desktop_connections.pop(user_id, None)
        if user_id in self.desktop_info:
            self.desktop_info[user_id]["last_seen"] = datetime.now(timezone.utc).isoformat()

    def is_connected(self, user_id: str) -> bool:
        return user_id in self.desktop_connections

    def get_info(self, user_id: str) -> dict[str, Any] | None:
        return self.desktop_info.get(user_id)

    async def send_task(self, user_id: str, action: str, params: dict[str, Any]) -> dict[str, Any]:
        ws = self.desktop_connections.get(user_id)
        if not ws:
            return {"success": False, "error": "Desktop agent not connected"}

        task_id = f"task_{uuid.uuid4().hex[:10]}"
        loop = asyncio.get_event_loop()
        fut: asyncio.Future = loop.create_future()
        self.pending_tasks[task_id] = fut
        issued_at = datetime.now(timezone.utc).isoformat()
        task_nonce = uuid.uuid4().hex
        signature = self._sign_task(task_id, action, params, issued_at, task_nonce)
        try:
            await ws.send_json(
                {
                    "type": "desktop_task",
                    "task_id": task_id,
                    "data": {
                        "action": action,
                        "params": params,
                        "issued_at": issued_at,
                        "task_nonce": task_nonce,
                        "signature": signature,
                    },
                }
            )
            result = await asyncio.wait_for(fut, timeout=45)
            return result
        except asyncio.TimeoutError:
            return {"success": False, "error": "Desktop task timeout"}
        finally:
            self.pending_tasks.pop(task_id, None)

    def resolve_task(self, task_id: str, result: dict[str, Any]) -> None:
        fut = self.pending_tasks.get(task_id)
        if fut and not fut.done():
            fut.set_result(result)

    @staticmethod
    def _sign_task(task_id: str, action: str, params: dict[str, Any], issued_at: str, task_nonce: str) -> str:
        secret = get_settings().desktop_signing_secret
        if not secret:
            return ""
        raw = f"{task_id}|{action}|{params}|{issued_at}|{task_nonce}"
        return hmac.new(secret.encode("utf-8"), raw.encode("utf-8"), hashlib.sha256).hexdigest()


@router.websocket("/ws/{user_id}")
async def ws_endpoint(websocket: WebSocket, user_id: str):
    manager: DesktopWebSocketManager = websocket.app.state.desktop_ws_manager
    settings = get_settings()
    ws_scheme = (websocket.url.scheme or "").lower()
    host = websocket.client.host if websocket.client else ""
    if settings.require_secure_transport and ws_scheme != "wss":
        if not (settings.allow_insecure_localhost and host in {"127.0.0.1", "localhost", "::1"}):
            await websocket.close(code=1008, reason="WSS required")
            return
    await manager.connect(user_id, websocket)

    try:
        while True:
            message = await websocket.receive_json()
            msg_type = message.get("type")
            if msg_type == "desktop_agent_register":
                limiter = websocket.app.state.rate_limiter
                if not limiter.allow(f"ws-register:{user_id}", limit=10, window_seconds=60):
                    await websocket.send_json({"type": "error", "error": "Rate limit exceeded"})
                    continue
                manager.register_desktop(user_id, websocket, message.get("data", {}))
                await AuditLogger().log(
                    user_id=user_id,
                    action="websocket.desktop_register",
                    status="success",
                    source="ws",
                    ip=host,
                    details=message.get("data", {}),
                )
            elif msg_type == "heartbeat":
                manager.touch_heartbeat(user_id)
                await websocket.send_json({"type": "pong"})
            elif msg_type == "task_result":
                manager.resolve_task(message.get("task_id", ""), message.get("result", {"success": False}))
            elif msg_type == "command":
                # Placeholder real-time command path from frontend.
                await websocket.send_json({"type": "response", "data": {"text": "Command received", "action_status": "queued"}})
            elif msg_type == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
