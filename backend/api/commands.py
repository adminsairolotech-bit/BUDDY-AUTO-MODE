from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile

from database.models import CommandRequest
from database.repositories import ConversationRepository, TaskRepository
from memory.context_builder import ContextBuilder
from memory.memory_manager import MemoryManager
from utils.audit import AuditLogger
from utils.security import get_current_user


router = APIRouter(prefix="/api", tags=["commands"])


HIGH_RISK_KEYWORDS = {"delete", "remove", "run command", "shell", "powershell", "screenshot", "clipboard", "format"}
CONFIRM_REQUIRED_DESKTOP_ACTIONS = {"run_command", "screenshot", "get_clipboard", "set_clipboard", "open_file"}


def _action_text(intent: str, action_result: dict[str, Any]) -> str:
    nested_text = action_result.get("result", {}).get("text") if isinstance(action_result.get("result"), dict) else None
    if nested_text:
        return nested_text
    if action_result.get("success"):
        if intent == "email":
            return "I sent that email."
        if intent == "desktop":
            return "Desktop action completed."
        if intent == "calendar":
            return "Calendar action completed."
        return "Done."
    return action_result.get("error", "Task failed.")


def _risk_score(command: str, intent: str, action: str) -> int:
    score = 1
    text = command.lower()
    if intent == "desktop":
        score += 2
    if action in {"run_command", "screenshot", "get_clipboard", "set_clipboard"}:
        score += 3
    if any(k in text for k in HIGH_RISK_KEYWORDS):
        score += 3
    return min(score, 10)


async def _process_command_inner(payload: CommandRequest, current_user: dict, request: Request):
    user_id = current_user.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid user token")

    app_state = request.app.state
    rate_limiter = app_state.rate_limiter
    if not rate_limiter.allow(f"command:user:{user_id}", limit=30, window_seconds=60):
        raise HTTPException(status_code=429, detail="Too many commands. Please slow down.")
    gemini = app_state.gemini_engine
    parser = app_state.intent_parser
    task_router = app_state.task_router

    conversation_id = (
        payload.context.conversation_id
        if payload.context and payload.context.conversation_id
        else f"conv_{uuid.uuid4().hex[:8]}"
    )
    conv_repo = ConversationRepository()
    task_repo = TaskRepository()
    memory = MemoryManager(user_id=user_id)

    await conv_repo.get_or_create(user_id, conversation_id)

    await conv_repo.append_message(
        user_id,
        conversation_id,
        {
            "id": f"msg_{uuid.uuid4().hex[:8]}",
            "role": "user",
            "content": payload.command,
            "timestamp": datetime.utcnow(),
            "type": payload.type,
        },
    )

    context = await ContextBuilder(user_id).build(conversation_id=conversation_id, command=payload.command)

    ai_parse = gemini.parse_command(payload.command, context=context) if gemini else {}
    intent, confidence = parser.parse(payload.command)
    params = parser.extract_params(payload.command, intent)
    action = params.get("action", intent)

    if ai_parse.get("understood"):
        intent = ai_parse.get("intent", intent)
        action = ai_parse.get("action", action)
        params = {**params, **ai_parse.get("params", {})}

    risk_score = _risk_score(payload.command, intent, action)
    needs_confirmation = intent == "desktop" and (action in CONFIRM_REQUIRED_DESKTOP_ACTIONS or risk_score >= 7)
    confirmed = bool(params.get("confirmed") or request.headers.get("x-confirm-action") == "true")
    if needs_confirmation and not confirmed:
        await AuditLogger().log(
            user_id=user_id,
            action="command.confirmation_required",
            status="blocked",
            source="api",
            ip=request.client.host if request.client else "unknown",
            details={"intent": intent, "action": action, "risk_score": risk_score},
        )
        return {
            "success": False,
            "response": {
                "text": f"Confirmation required for '{action}'. Re-send with confirmation.",
                "action_taken": {"type": intent, "status": "confirmation_required", "details": {"risk_score": risk_score}},
            },
            "conversation_id": conversation_id,
        }

    task_id = f"task_{uuid.uuid4().hex[:10]}"
    await task_repo.create(
        task_id=task_id,
        user_id=user_id,
        payload={
            "type": intent,
            "command": payload.command,
            "parsed_intent": {"action": action, "params": params, "confidence": confidence},
            "agent_used": f"{intent}_agent",
            "risk_score": risk_score,
        },
    )

    result = await task_router.route(intent=intent, action=action, params=params, context={"user_id": user_id})
    await task_repo.complete(task_id=task_id, result=result, success=result.get("success", False), error=result.get("error"))
    await memory.learn_from_interaction(command=payload.command, intent=intent, params=params)
    await AuditLogger().log(
        user_id=user_id,
        action="command.execute",
        status="success" if result.get("success") else "failed",
        source="api",
        ip=request.client.host if request.client else "unknown",
        details={"intent": intent, "action": action, "risk_score": risk_score},
    )

    assistant_text = ai_parse.get("response_text") if ai_parse.get("understood") else None
    assistant_text = assistant_text or _action_text(intent, result)
    await conv_repo.append_message(
        user_id,
        conversation_id,
        {
            "id": f"msg_{uuid.uuid4().hex[:8]}",
            "role": "assistant",
            "content": assistant_text,
            "timestamp": datetime.utcnow(),
            "type": "text",
            "action": {"type": intent, "details": result},
        },
    )

    # Update summary (short heuristic to avoid extra LLM call for every turn).
    latest_conv = await conv_repo.latest_for_user(user_id)
    messages = (latest_conv or {}).get("messages", [])[-8:]
    summary = " | ".join([f"{m.get('role')}:{m.get('content', '')[:40]}" for m in messages])
    await conv_repo.set_summary(user_id, conversation_id, summary=summary, entities=[])

    return {
        "success": True,
        "response": {"text": assistant_text, "action_taken": {"type": intent, "status": "completed" if result.get("success") else "failed", "details": result}},
        "conversation_id": conversation_id,
    }


@router.post("/command")
async def process_command(payload: CommandRequest, request: Request, current_user: dict = Depends(get_current_user)):
    return await _process_command_inner(payload, current_user, request)


@router.post("/command/voice")
async def process_voice_command(
    request: Request,
    audio: UploadFile = File(...),
    conversation_id: str | None = Form(default=None),
    current_user: dict = Depends(get_current_user),
):
    # Placeholder STT flow; wire Whisper/GCP Speech in production.
    transcription = audio.filename.replace("_", " ").replace(".wav", "").replace(".mp3", "") if audio.filename else "voice command"
    command_payload = CommandRequest(command=transcription, type="voice", context={"conversation_id": conversation_id})
    result = await _process_command_inner(command_payload, current_user, request)
    return {
        "success": True,
        "transcription": transcription,
        "response": {"text": result["response"]["text"], "audio_url": None},
    }
