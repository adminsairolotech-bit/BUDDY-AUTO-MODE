from __future__ import annotations

import webbrowser


class BrowserController:
    def open_url(self, url: str) -> dict:
        if not url:
            return {"success": False, "error": "Missing url"}
        try:
            webbrowser.open(url)
            return {"success": True, "message": f"Opened {url}"}
        except Exception as exc:
            return {"success": False, "error": str(exc)}
