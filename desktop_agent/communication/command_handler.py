from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from controllers.app_controller import AppController
from controllers.browser_controller import BrowserController
from controllers.clipboard_controller import ClipboardController
from controllers.file_controller import FileController
from controllers.keyboard_controller import KeyboardController
from controllers.mouse_controller import MouseController
from controllers.screenshot_controller import ScreenshotController
from controllers.window_controller import WindowController
from utils.system_info import get_system_info


class CommandHandler:
    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        self.app = AppController()
        self.browser = BrowserController()
        self.file = FileController()
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.window = WindowController()
        self.clipboard = ClipboardController()
        self.screenshot_ctrl = ScreenshotController()

    def execute(self, action: str, params: dict[str, Any]) -> dict[str, Any]:
        if not self._is_allowed(action, params):
            return {"success": False, "error": f"Blocked action: {action}"}
        if self._needs_confirmation(action, params):
            return {"success": False, "error": f"Confirmation required for action: {action}"}
        if not self._path_allowed(params.get("path")):
            return {"success": False, "error": "Blocked restricted file path"}
        if not self._path_allowed(params.get("save_path")):
            return {"success": False, "error": "Blocked restricted save path"}

        try:
            if action == "open_app":
                return self.app.open_app(params.get("app_name", ""))
            if action == "open_file":
                return self.file.open_file(params.get("path", ""))
            if action == "open_url":
                return self.browser.open_url(params.get("url", ""))
            if action == "type_text":
                return self.keyboard.type_text(params.get("text", ""), float(params.get("interval", 0.05)))
            if action == "press_key":
                return self.keyboard.press_key(params.get("key", ""))
            if action == "hotkey":
                return self.keyboard.hotkey(params.get("keys", []))
            if action == "click":
                return self.mouse.click(params.get("x"), params.get("y"), params.get("button", "left"), int(params.get("clicks", 1)))
            if action == "move_mouse":
                return self.mouse.move_mouse(int(params.get("x", 0)), int(params.get("y", 0)), float(params.get("duration", 0.5)))
            if action == "screenshot":
                return self.screenshot_ctrl.screenshot(params.get("save_path", "screenshot.png"), params.get("region"))
            if action == "get_clipboard":
                return self.clipboard.get_clipboard()
            if action == "set_clipboard":
                return self.clipboard.set_clipboard(params.get("text", ""))
            if action == "run_command":
                return self._run_command(params.get("command", ""), int(params.get("timeout", 30)))
            if action == "get_windows":
                return self.window.get_windows()
            if action == "focus_window":
                return self.window.focus_window(params.get("title", ""))
            if action == "close_window":
                return self.window.close_window(params.get("title", ""))
            if action == "get_system_info":
                return {"success": True, "data": get_system_info()}

            return {"success": False, "error": f"Unknown action: {action}"}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def _is_allowed(self, action: str, params: dict[str, Any]) -> bool:
        allowed = self.config.get("allowed_commands", [])
        blocked = [b.lower() for b in self.config.get("blocked_commands", [])]
        if action not in allowed:
            return False
        cmd = str(params.get("command", "")).lower()
        for token in blocked:
            if token in cmd:
                return False
        return True

    def _needs_confirmation(self, action: str, params: dict[str, Any]) -> bool:
        required = set(self.config.get("require_confirmation_for", []))
        if action not in required:
            return False
        return not bool(params.get("confirmed"))

    def _path_allowed(self, path_value: Any) -> bool:
        if not isinstance(path_value, str) or not path_value.strip():
            return True
        try:
            p = Path(path_value).resolve()
        except Exception:
            return False
        normalized = str(p).lower().replace("\\", "/")

        blocked_paths = [str(x).lower().replace("\\", "/") for x in self.config.get("blocked_paths", [])]
        if any(normalized.startswith(bp.rstrip("/")) for bp in blocked_paths):
            return False

        allowed_paths = [str(x).lower().replace("\\", "/") for x in self.config.get("allowed_paths", [])]
        if not allowed_paths:
            return True
        return any(normalized.startswith(ap.rstrip("/")) for ap in allowed_paths)

    def _run_command(self, command: str, timeout: int) -> dict[str, Any]:
        if not command.strip():
            return {"success": False, "error": "Missing command"}
        blocked = [b.lower() for b in self.config.get("blocked_commands", [])]
        lowered = command.lower()
        if any(token in lowered for token in blocked):
            return {"success": False, "error": "Dangerous command blocked by policy"}
        try:
            max_timeout = int(self.config.get("max_action_timeout", 45))
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=min(timeout, max_timeout))
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
            }
        except Exception as exc:
            return {"success": False, "error": str(exc)}
