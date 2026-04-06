from __future__ import annotations

import json
import threading
import time
from datetime import datetime
from typing import Any, Callable

import websocket


class DesktopWebSocketClient:
    def __init__(
        self,
        server_url: str,
        user_id: str,
        api_key: str,
        heartbeat_interval: int,
        reconnect_delay: int,
        on_task: Callable[[str, dict[str, Any]], dict[str, Any]],
        logger,
    ) -> None:
        self.server_url = server_url.rstrip("/")
        self.user_id = user_id
        self.api_key = api_key
        self.heartbeat_interval = heartbeat_interval
        self.reconnect_delay = reconnect_delay
        self.on_task = on_task
        self.logger = logger
        self.ws = None
        self.connected = False
        self.running = True

    def _build_url(self) -> str:
        # Supports server_url as ".../ws" or ".../ws/{user_id}".
        if self.server_url.endswith(f"/{self.user_id}"):
            base = self.server_url
        else:
            base = f"{self.server_url}/{self.user_id}"
        if self.api_key:
            return f"{base}?api_key={self.api_key}"
        return base

    def connect_forever(self) -> None:
        while self.running:
            try:
                self.ws = websocket.WebSocketApp(
                    self._build_url(),
                    on_open=self._on_open,
                    on_message=self._on_message,
                    on_error=self._on_error,
                    on_close=self._on_close,
                )
                self.ws.run_forever()
            except Exception as exc:
                self.logger.error("WebSocket connection failed: %s", exc)
            if self.running:
                time.sleep(self.reconnect_delay)

    def _on_open(self, ws) -> None:
        self.connected = True
        self.logger.info("Connected to server")
        self.send(
            {
                "type": "desktop_agent_register",
                "data": {
                    "os": "windows",
                    "hostname": "",
                    "python_version": "",
                },
            }
        )
        threading.Thread(target=self._heartbeat_loop, daemon=True).start()

    def _on_message(self, ws, message: str) -> None:
        try:
            data = json.loads(message)
            msg_type = data.get("type")
            if msg_type == "desktop_task":
                task_id = data.get("task_id")
                payload = data.get("data", {})
                result = self.on_task(task_id, payload)
                self.send({"type": "task_result", "task_id": task_id, "result": result})
            elif msg_type == "ping":
                self.send({"type": "pong"})
        except Exception as exc:
            self.logger.error("Message handling error: %s", exc)

    def _on_error(self, ws, error) -> None:
        self.logger.error("WebSocket error: %s", error)

    def _on_close(self, ws, close_code, close_msg) -> None:
        self.connected = False
        self.logger.warning("Connection closed: %s - %s", close_code, close_msg)

    def _heartbeat_loop(self) -> None:
        while self.running and self.connected:
            self.send({"type": "heartbeat", "timestamp": datetime.utcnow().isoformat()})
            time.sleep(self.heartbeat_interval)

    def send(self, data: dict[str, Any]) -> None:
        if self.ws and self.connected:
            self.ws.send(json.dumps(data))

    def stop(self) -> None:
        self.running = False
        if self.ws:
            self.ws.close()
