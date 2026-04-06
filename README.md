# BUDDY AUTO MODE (MVP)

OpenClaw-style assistant MVP with:
- FastAPI backend (`backend/`)
- React frontend (`frontend/`)
- Desktop agent skeleton (`desktop_agent/`)

## What Works In This MVP

- User register/login/logout + token refresh
- Authenticated command execution (`/api/command`)
- Skills/integrations/schedules/memory/privacy APIs wired
- WebSocket desktop bridge endpoint (`/ws/{user_id}`)
- Frontend login + command console connected to backend APIs

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

Backend prefers MongoDB:
- `MONGO_URL=mongodb://localhost:27017`
- `DB_NAME=openclaw_db`

Development fallback:
- If MongoDB is unavailable and `APP_ENV=development`, the backend now falls back to an in-memory database so local MVP flows can still boot and run.
- For persistent data and production-like behavior, run a real MongoDB instance.

Health check:
- `GET http://localhost:8001/api/health`

## 2) Frontend

```powershell
cd frontend
Copy-Item .env.example .env
npm install
npm start
```

Frontend opens on:
- `http://localhost:3000`

## 3) Desktop Agent (Optional)

```powershell
cd desktop_agent
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python agent.py
```

## Environment Notes

- Do not commit real secrets in `.env`.
- `frontend/.env` should point to backend URL:
  - `REACT_APP_BACKEND_URL=http://localhost:8001`

## One-Command Smoke Test

```powershell
cd "C:\Users\Sai Rolotech\Pictures\Screenshots\BUUDDI AUTO MODE"
python smoke_test.py
```

This starts the backend and frontend locally, runs auth + command API checks, probes the frontend, and prints a JSON summary.

## MVP Known Limits

- Gmail/Calendar/Telegram require real credentials/tokens.
- Voice STT endpoint is placeholder-based.
- Desktop agent confirmations and policy checks are basic safety, not full sandbox isolation.
