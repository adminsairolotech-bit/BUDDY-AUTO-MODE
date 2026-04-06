from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request

from database.models import DesktopCommandRequest
from utils.audit import AuditLogger
from utils.security import get_current_user


router = APIRouter(prefix="/api/desktop", tags=["desktop"])
ALLOWED_DESKTOP_ACTIONS = {
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
}
HIGH_RISK_ACTIONS = {"run_command", "screenshot", "get_clipboard", "set_clipboard", "open_file"}
BLOCKED_COMMAND_TOKENS = ["rm -rf", "del /f /s /q", "format", "powershell -enc", "reg add", "reg delete", "shutdown", "bcdedit"]
BLOCKED_PATH_PREFIXES = [r"c:\windows", r"c:\program files", r"c:\program files (x86)", r"c:\windows\system32"]


@router.get("/status")
async def desktop_status(request: Request, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    manager = request.app.state.desktop_ws_manager
    info = manager.get_info(user_id)
    return {"success": True, "status": "connected" if info else "offline", "agent_info": info}


@router.post("/command")
async def send_desktop_command(payload: DesktopCommandRequest, request: Request, current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    rate_limiter = request.app.state.rate_limiter
    if not rate_limiter.allow(f"desktop:user:{user_id}", limit=20, window_seconds=60):
        raise HTTPException(status_code=429, detail="Too many desktop commands. Try later.")

    action = payload.action
    params = payload.params or {}
    if action not in ALLOWED_DESKTOP_ACTIONS:
        raise HTTPException(status_code=400, detail=f"Action not allowed: {action}")

    if action == "run_command":
        raw = str(params.get("command", "")).lower()
        if any(token in raw for token in BLOCKED_COMMAND_TOKENS):
            raise HTTPException(status_code=403, detail="Blocked dangerous shell command")

    path_value = params.get("path") or params.get("save_path")
    if isinstance(path_value, str) and path_value.strip():
        normalized = str(Path(path_value).resolve()).lower()
        if any(normalized.startswith(prefix) for prefix in BLOCKED_PATH_PREFIXES):
            raise HTTPException(status_code=403, detail="Blocked restricted path")

    if action in HIGH_RISK_ACTIONS and not bool(params.get("confirmed") or request.headers.get("x-confirm-action") == "true"):
        raise HTTPException(status_code=409, detail=f"Confirmation required for desktop action '{action}'")
    if action == "open_app":
        app_name = str(params.get("app_name", "")).lower()
        known_apps = {"chrome", "firefox", "edge", "notepad", "calculator", "explorer", "cmd", "powershell", "word", "excel", "outlook", "vscode", "spotify"}
        if app_name and app_name not in known_apps and not bool(params.get("confirmed") or request.headers.get("x-confirm-action") == "true"):
            raise HTTPException(status_code=409, detail="Confirmation required to open unknown executable")

    manager = request.app.state.desktop_ws_manager
    if not manager.is_connected(user_id):
        raise HTTPException(status_code=409, detail="Desktop agent is not connected")
    result = await manager.send_task(user_id=user_id, action=action, params=params)
    await AuditLogger().log(
        user_id=user_id,
        action="desktop.command",
        status="success" if result.get("success") else "failed",
        source="api",
        ip=request.client.host if request.client else "unknown",
        details={"desktop_action": action},
    )
    return {"success": True, "result": {"status": "completed" if result.get("success") else "failed", "message": result.get("message", ""), "data": result}}
