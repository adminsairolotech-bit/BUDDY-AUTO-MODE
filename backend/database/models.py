from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class UserRegisterRequest(StrictModel):
    email: str
    password: str = Field(min_length=12)
    name: str = Field(min_length=1, max_length=120)


class UserLoginRequest(StrictModel):
    email: str
    password: str


class CommandContext(StrictModel):
    conversation_id: str | None = None
    previous_messages: list[dict[str, Any]] = Field(default_factory=list)


class CommandRequest(StrictModel):
    command: str = Field(min_length=1, max_length=5000)
    type: Literal["text", "voice"] = "text"
    context: CommandContext | None = None


class AgentExecuteRequest(StrictModel):
    task: str
    params: dict[str, Any] = Field(default_factory=dict)


class MemoryWriteRequest(StrictModel):
    type: str
    key: str
    value: Any
    context: str | None = None
    confidence: float = 1.0


class MemoryLearnRequest(StrictModel):
    interaction_type: str
    input: str
    interpreted_as: str
    params_learned: dict[str, Any] = Field(default_factory=dict)
    feedback: str = "correct"


class SkillAction(StrictModel):
    type: str
    config: dict[str, Any] | None = None
    url: str | None = None
    method: str | None = None


class SkillCreateRequest(StrictModel):
    name: str
    description: str
    trigger_phrases: list[str] = Field(default_factory=list)
    actions: list[SkillAction] = Field(default_factory=list)
    response_template: str = ""


class SkillExecuteRequest(StrictModel):
    params: dict[str, Any] = Field(default_factory=dict)


class ScheduleNotification(StrictModel):
    type: str | None = None
    chat_id: str | None = None


class ScheduleCreateRequest(StrictModel):
    name: str
    cron: str
    description: str | None = None
    timezone: str = "UTC"
    actions: list[dict[str, Any]] = Field(default_factory=list)
    notification: ScheduleNotification | None = None


class ScheduleUpdateRequest(StrictModel):
    name: str | None = None
    cron: str | None = None
    description: str | None = None
    timezone: str | None = None
    enabled: bool | None = None
    actions: list[dict[str, Any]] | None = None
    notification: ScheduleNotification | None = None


class IntegrationConnectRequest(StrictModel):
    bot_token: str | None = None
    refresh_token: str | None = None
    config: dict[str, Any] = Field(default_factory=dict)


class DesktopCommandRequest(StrictModel):
    action: str
    params: dict[str, Any] = Field(default_factory=dict)


class ConversationMessage(StrictModel):
    id: str
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    type: str = "text"
    action: dict[str, Any] | None = None


class TokenRefreshRequest(StrictModel):
    refresh_token: str = Field(min_length=20)


class EmailVerificationRequest(StrictModel):
    email: str
    code: str = Field(min_length=4, max_length=12)
