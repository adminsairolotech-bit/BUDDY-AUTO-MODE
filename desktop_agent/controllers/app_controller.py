from __future__ import annotations

import os


class AppController:
    APP_PATHS = {
        "chrome": "chrome",
        "firefox": "firefox",
        "edge": "msedge",
        "notepad": "notepad",
        "calculator": "calc",
        "explorer": "explorer",
        "cmd": "cmd",
        "powershell": "powershell",
        "word": "winword",
        "excel": "excel",
        "outlook": "outlook",
        "vscode": "code",
        "spotify": "spotify",
    }

    def open_app(self, app_name: str) -> dict:
        name = (app_name or "").lower().strip()
        target = self.APP_PATHS.get(name, name)
        if not target:
            return {"success": False, "error": "Missing app_name"}
        try:
            os.startfile(target)  # type: ignore[attr-defined]
            return {"success": True, "message": f"Opened {name or target}"}
        except Exception as exc:
            return {"success": False, "error": str(exc)}
