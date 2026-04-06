# OpenClaw Clone - AI Personal Assistant Backend

## Original Problem Statement
User shared GitHub repository `BUDDY-AUTO-MODE` (OpenClaw Clone). Task was to set up and build the backend/app logic only - UI will be made separately in Lovable.

## Architecture
- **Backend**: FastAPI (Python)
- **Database**: MongoDB
- **Auth**: JWT (access + refresh tokens with revocation)
- **Scheduler**: APScheduler for cron jobs
- **AI**: Gemini integration for command parsing (optional)

## Core Features Implemented

### Authentication (`/api/auth/*`)
- User registration with password policy (12+ chars, mixed case, number, special)
- Login with rate limiting and account lockout
- JWT access/refresh token flow
- Token revocation and rotation
- Email verification (dev mode shows code)

### Commands (`/api/command`)
- Text/voice command processing
- Intent parsing (local + Gemini AI)
- Task routing to agents
- Conversation history
- Risk scoring for desktop actions

### Skills (`/api/skills`)
- 5 built-in skills: Weather, News, Calculator, Translator, Notes
- Custom skill creation support

### Schedules (`/api/schedules`)
- Cron-based job scheduling
- Action execution on schedule

### Integrations (`/api/integrations`)
- Telegram, Gmail, Calendar, Notion, GitHub, Gemini
- Connect/disconnect flow with encrypted secrets

### Desktop Agent (`/api/desktop/*` + WebSocket)
- WebSocket connection for desktop client
- Remote command execution
- Status monitoring
- Confirmation gate for risky actions

### Privacy (`/api/privacy`)
- Export user data
- Forget-me (delete all data)

### Memory (`/api/memory`)
- Store/retrieve user memory
- Learning from interactions
- Context building for AI

## User Personas
- Individual users wanting AI-powered personal assistant
- Developers integrating with desktop automation

## What's Been Implemented (April 6, 2026)
- [x] Complete backend from GitHub repo setup
- [x] All API endpoints working
- [x] MongoDB integration
- [x] JWT authentication with security features
- [x] 5 built-in skills seeded
- [x] 6 integration placeholders

## Test Credentials
- Email: test@example.com
- Password: Password@12345!

## Backlog / Future Features
- P0: Gemini API key integration for AI parsing
- P1: Telegram bot actual connection
- P1: Gmail/Calendar OAuth setup
- P2: Desktop agent Windows client
- P2: Voice transcription (Whisper)

## API Base URL
- Production: https://buddy-automation.preview.emergentagent.com
- Health: /api/health
