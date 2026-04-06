"""
Desktop Agent for OpenClaw Clone
Connects to backend WebSocket and executes desktop automation tasks.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import pyautogui
from dotenv import load_dotenv

from communication.command_handler import CommandHandler
from communication.websocket_client import DesktopWebSocketClient
from utils.logger import build_logger
from utils.system_info import get_system_info


DEFAULT_CONFIG: dict[str, Any] = {
    "server_url": "ws://localhost:8001/ws",
    "user_id": "",
    "api_key": "",
    "heartbeat_interval": 30,
    "reconnect_delay": 5,
    "log_file": "agent.log",
    "allowed_commands": [
        "open_app",
        "open_file",
        "open_url",
        "type_text",
        "press_key",
        "hotkey",
        "click",
        "move_mouse",
        "screenshot",
        "get_clipboard",
        "set_clipboard",
        "run_command",
        "get_windows",
        "focus_window",
        "close_window",
        "get_system_info",
    ],
    "blocked_commands": ["format", "delete", "rm -rf", "del /f /s /q", "powershell -enc", "reg add", "reg delete"],
    "allowed_paths": ["C:/Users"],
    "blocked_paths": ["C:/Windows", "C:/Program Files", "C:/Program Files (x86)", "C:/Windows/System32"],
    "require_confirmation_for": ["run_command", "screenshot", "get_clipboard", "set_clipboard", "open_file"],
    "verify_command_signature": False,
    "command_signature_secret": "",
    "require_secure_ws": False,
    "max_action_timeout": 45,
}


def load_config() -> dict[str, Any]:
    load_dotenv()
    config = dict(DEFAULT_CONFIG)
    config_path = Path(__file__).with_name("config.json")
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            file_cfg = json.load(f)
        config.update(file_cfg)

    config["server_url"] = os.getenv("SERVER_URL", os.getenv("AGENT_SERVER_URL", config["server_url"]))
    config["user_id"] = os.getenv("USER_ID", os.getenv("AGENT_USER_ID", config["user_id"]))
    config["api_key"] = os.getenv("API_KEY", os.getenv("AGENT_API_KEY", config["api_key"]))
    config["heartbeat_interval"] = int(os.getenv("HEARTBEAT_INTERVAL", config["heartbeat_interval"]))
    config["reconnect_delay"] = int(os.getenv("RECONNECT_DELAY", config["reconnect_delay"]))
    config["log_file"] = os.getenv("LOG_FILE", config["log_file"])
    config["verify_command_signature"] = str(os.getenv("VERIFY_COMMAND_SIGNATURE", config.get("verify_command_signature", False))).lower() in {"1", "true", "yes"}
    config["command_signature_secret"] = os.getenv("COMMAND_SIGNATURE_SECRET", config.get("command_signature_secret", ""))
    config["require_secure_ws"] = str(os.getenv("REQUIRE_SECURE_WS", config.get("require_secure_ws", False))).lower() in {"1", "true", "yes"}
    config["max_action_timeout"] = int(os.getenv("MAX_ACTION_TIMEOUT", config.get("max_action_timeout", 45)))
    return config


def _is_ws_transport_allowed(config: dict[str, Any]) -> bool:
    url = config.get("server_url", "")
    parsed = urlparse(url)
    if not config.get("require_secure_ws"):
        return True
    if parsed.scheme.lower() == "wss":
        return True
    return parsed.hostname in {"localhost", "127.0.0.1", "::1"}


def _verify_signature(task_id: str, payload: dict[str, Any], config: dict[str, Any]) -> bool:
    if not config.get("verify_command_signature"):
        return True
    secret = str(config.get("command_signature_secret", ""))
    signature = str(payload.get("signature", "") or "")
    if not secret or not signature:
        return False
    action = payload.get("action", "")
    params = payload.get("params", {})
    issued_at = payload.get("issued_at", "")
    task_nonce = payload.get("task_nonce", "")
    raw = f"{task_id}|{action}|{params}|{issued_at}|{task_nonce}"
    expected = hmac.new(secret.encode("utf-8"), raw.encode("utf-8"), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def main() -> None:
    config = load_config()
    logger = build_logger(config["log_file"])

    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.3

    if not config.get("user_id"):
        logger.error("Missing USER_ID in config.json or environment.")
        return
    if not _is_ws_transport_allowed(config):
        logger.error("Insecure WebSocket URL blocked by policy. Use wss:// or localhost for local dev.")
        return

    handler = CommandHandler(config=config)
    executor = ThreadPoolExecutor(max_workers=1)

    def on_task(task_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        if not _verify_signature(task_id, payload, config):
            logger.warning("Rejected unsigned/invalid-signed command for task %s", task_id)
            return {"success": False, "error": "Invalid command signature"}
        action = payload.get("action", "")
        params = payload.get("params", {})
        logger.info("Executing task %s: %s", task_id, action)
        timeout = int(config.get("max_action_timeout", 45))
        fut = executor.submit(handler.execute, action, params)
        try:
            result = fut.result(timeout=timeout)
        except FutureTimeout:
            result = {"success": False, "error": f"Action timeout after {timeout}s"}
        logger.info("Task %s result: success=%s", task_id, bool(result.get("success")))
        return result

    ws_client = DesktopWebSocketClient(
        server_url=config["server_url"],
        user_id=config["user_id"],
        api_key=config["api_key"],
        heartbeat_interval=config["heartbeat_interval"],
        reconnect_delay=config["reconnect_delay"],
        on_task=on_task,
        logger=logger,
    )

    logger.info("Desktop agent starting")
    logger.info("System info: %s", get_system_info())
    try:
        ws_client.connect_forever()
    except KeyboardInterrupt:
        logger.info("Stopping desktop agent")
        ws_client.stop()
    finally:
        executor.shutdown(wait=False)


if __name__ == "__main__":
    main()
