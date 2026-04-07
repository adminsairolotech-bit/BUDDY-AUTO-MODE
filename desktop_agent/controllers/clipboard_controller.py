from __future__ import annotations

from typing import Any

import pyperclip


class ClipboardController:
    def get_clipboard(self) -> dict[str, Any]:
        try:
            content = pyperclip.paste()
            return {"success": True, "data": content}
        except Exception as exc:
            return {"success": False, "error": str(exc)}

    def set_clipboard(self, text: str) -> dict[str, Any]:
        try:
            pyperclip.copy(text or "")
            return {"success": True, "message": "Clipboard updated"}
        except Exception as exc:
            return {"success": False, "error": str(exc)}
