from __future__ import annotations

from typing import Any

from PIL import ImageGrab


class ScreenshotController:
    def screenshot(self, save_path: str = "screenshot.png", region: tuple[int, int, int, int] | None = None) -> dict[str, Any]:
        try:
            if region:
                img = ImageGrab.grab(bbox=region)
            else:
                img = ImageGrab.grab()
            img.save(save_path)
            return {"success": True, "message": f"Screenshot saved to {save_path}", "path": save_path}
        except Exception as exc:
            return {"success": False, "error": str(exc)}
