from __future__ import annotations

from typing import Any

import pygetwindow as gw


class WindowController:
    def get_windows(self) -> dict[str, Any]:
        try:
            windows = []
            for window in gw.getAllWindows():
                if window.title:
                    windows.append(
                        {
                            "title": window.title,
                            "position": {"x": window.left, "y": window.top},
                            "size": {"width": window.width, "height": window.height},
                            "visible": window.visible,
                            "minimized": window.isMinimized,
                        }
                    )
            return {"success": True, "data": windows}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def focus_window(self, title: str) -> dict[str, Any]:
        try:
            windows = gw.getWindowsWithTitle(title)
            if not windows:
                return {"success": False, "error": f"Window not found: {title}"}
            windows[0].activate()
            return {"success": True, "message": f"Focused {title}"}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def close_window(self, title: str) -> dict[str, Any]:
        try:
            windows = gw.getWindowsWithTitle(title)
            if not windows:
                return {"success": False, "error": f"Window not found: {title}"}
            windows[0].close()
            return {"success": True, "message": f"Closed {title}"}
        except Exception as exc:
            return {"success": False, "error": str(exc)}
