from __future__ import annotations

import os


class FileController:
    def open_file(self, path: str) -> dict:
        if not path:
            return {"success": False, "error": "Missing path"}
        if not os.path.exists(path):
            return {"success": False, "error": f"File not found: {path}"}
        try:
            os.startfile(path)  # type: ignore[attr-defined]
            return {"success": True, "message": f"Opened {path}"}
        except Exception as exc:
            return {"success": False, "error": str(exc)}
