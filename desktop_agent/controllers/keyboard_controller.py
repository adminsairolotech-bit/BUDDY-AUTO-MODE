from __future__ import annotations

from typing import Any

import pyautogui


class KeyboardController:
    def type_text(self, text: str, interval: float = 0.05) -> dict[str, Any]:
        try:
            pyautogui.typewrite(text or "", interval=interval)
            return {"success": True, "message": f"Typed {len(text or '')} characters"}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def press_key(self, key: str) -> dict[str, Any]:
        try:
            pyautogui.press(key)
            return {"success": True, "message": f"Pressed {key}"}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def hotkey(self, keys: list[str]) -> dict[str, Any]:
        try:
            pyautogui.hotkey(*keys)
            return {"success": True, "message": f"Pressed {'+'.join(keys)}"}
        except Exception as exc:
            return {"success": False, "error": str(exc)}
