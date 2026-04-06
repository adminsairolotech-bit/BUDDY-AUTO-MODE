# OpenClaw Clone (Spec-Based Scaffold)

Generated from your complete January 2025 specification as a runnable full-stack scaffold.

## What Is Included

- FastAPI backend with routes:
  - `/api/auth/*`
  - `/api/command`, `/api/command/voice`
  - `/api/agents`
  - `/api/memory`
  - `/api/skills`
  - `/api/schedules`
  - `/api/integrations`
  - `/api/desktop/*`
  - `/ws/{user_id}` WebSocket
- Core systems:
  - Gemini wrapper + fallback intent parser
  - Task router and agent abstraction
  - Persistent memory + learning/error logs
  - Cron scheduling via APScheduler
- Desktop agent:
  - WebSocket client
  - Modular action controllers
  - Command execution + heartbeat + task results

## Quick Start

## 1) Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

Required services:
- MongoDB running on `MONGO_URL`

Optional APIs:
- Gemini (`GEMINI_API_KEY`)
- Telegram (`TELEGRAM_BOT_TOKEN`)
- Gmail/Calendar OAuth (`credentials.json`)
- Weather/News keys

## 2) Desktop Agent

```powershell
cd desktop_agent
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
python agent.py
```

Set `USER_ID` and `SERVER_URL` in `.env` or `config.json`.

Recommended local server URL:
- `ws://localhost:8001/ws`

## Notes

- This is production-structured scaffolding with real endpoint wiring and core orchestration.
- Some integrations include safe placeholders when credentials are missing.
- All generated Python files compile successfully (`python -m compileall backend desktop_agent`).

## Security Hardening Included

- JWT access + refresh token flow with token revocation list.
- Password policy enforcement (12+ chars, upper, lower, number, special).
- Login/command/websocket registration rate limiting.
- Failed-login account lockout.
- Integration secret encryption (`bot_token`, `refresh_token`, Gemini key in config).
- Confirmation gate for risky desktop actions.
- Desktop command/path blocker policy.
- Secure transport enforcement option (`REQUIRE_SECURE_TRANSPORT`).
- Audit logging for auth, commands, desktop, integrations, and privacy actions.
- Privacy APIs:
  - `DELETE /api/memory/all`
  - `DELETE /api/conversations/{id}`
  - `POST /api/privacy/export`
  - `POST /api/privacy/forget-me`

## ULTIMATE v5 File + Runner

- Added project copy of your file at:
  - `docs/ULTIMATE_AI_SYSTEM_v5_LEARNING.md`
- Implemented v5 execution loop runner with parameters:
  - `MAX_CYCLES`
  - `ERROR_REPEAT_LIMIT`
  - `MAX_PIPELINE_RUN`
  - learning logs in `.ai_memory/errors.log` and `.ai_memory/solutions.log`

Run manually:

```powershell
cd backend
python run_ultimate_v5.py --project-root ..
```
