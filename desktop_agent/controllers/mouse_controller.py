from __future__ import annotations

from typing import Any

import pyautogui


class MouseController:
    def click(self, x: int | None = None, y: int | None = None, button: str = "left", clicks: int = 1) -> dict[str, Any]:
        try:
            if x is not None and y is not None:
                pyautogui.click(x, y, button=button, clicks=clicks)
            else:
                pyautogui.click(button=button, clicks=clicks)
            return {"success": True, "message": f"Clicked at ({x}, {y})"}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def move_mouse(self, x: int, y: int, duration: float = 0.5) -> dict[str, Any]:
        try:
            pyautogui.moveTo(x, y, duration=duration)
            return {"success": True, "message": f"Moved to ({x}, {y})"}
        except Exception as exc:
            return {"success": False, "error": str(exc)}
