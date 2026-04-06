# Secure OpenClaw Patch QA Template (Pass/Fail)

Use this sheet for validating the 27-file security patch.

## 0) Test Metadata

- Build/Commit:
- Tester:
- Date:
- Environment (dev/stage/prod):
- API Base URL:
- Desktop Agent Version:

## 1) Auth & Token Security

### 1.1 Password Policy (12+, upper/lower/number/special)
- Steps:
1. Try weak password on `/api/auth/register`.
2. Try strong password on `/api/auth/register`.
- Expected:
1. Weak password rejected (400).
2. Strong password accepted.
- Result: PASS / FAIL
- Evidence:

### 1.2 Login Rate Limit + Lockout
- Steps:
1. Send 10 invalid logins quickly.
2. Continue login attempts.
- Expected:
1. 401 on bad creds initially.
2. 429 rate-limit and/or 423 lockout after threshold.
- Result: PASS / FAIL
- Evidence:

### 1.3 Refresh + Revoke + Logout
- Steps:
1. Login and get access+refresh tokens.
2. Call `/api/auth/refresh`.
3. Logout and retry old tokens.
- Expected:
1. Refresh works before logout.
2. Revoked token rejected after logout.
- Result: PASS / FAIL
- Evidence:

### 1.4 Secret Leak Check in Auth Responses
- Steps:
1. Register/login/me calls.
- Expected:
1. No password hash/secret keys/tokens (other than intended auth tokens) leaked.
- Result: PASS / FAIL
- Evidence:

## 2) Commands & Risk Control

### 2.1 Command Rate Limit
- Steps:
1. Burst `/api/command` with >30 req/min for one user.
- Expected:
1. 429 returned after threshold.
- Result: PASS / FAIL
- Evidence:

### 2.2 High-Risk Confirmation Gate
- Steps:
1. Send risky desktop intent (run_command/screenshot/get_clipboard) without confirmation.
2. Repeat with `confirmed=true` or `x-confirm-action: true`.
- Expected:
1. Blocked or confirmation-required response without execution.
2. Allowed only after confirmation.
- Result: PASS / FAIL
- Evidence:

### 2.3 Fake Success Guard
- Steps:
1. Send deliberately broken desktop action.
- Expected:
1. Response shows failure, not success.
2. Audit log contains failed event.
- Result: PASS / FAIL
- Evidence:

## 3) Desktop API Safety

### 3.1 Dangerous Command Blocking
- Test inputs:
1. `rm -rf`
2. `del /f /s /q`
3. `powershell -enc ...`
4. `reg add ...`
- Expected:
1. Hard reject (403/blocked policy).
- Result: PASS / FAIL
- Evidence:

### 3.2 Dangerous Path Blocking
- Test paths:
1. `C:\Windows\System32\...`
2. `C:\Program Files\...`
- Expected:
1. Rejected by backend desktop policy.
- Result: PASS / FAIL
- Evidence:

### 3.3 Unknown EXE Confirmation
- Steps:
1. `open_app` with unknown app name without confirmation.
- Expected:
1. Confirmation required.
- Result: PASS / FAIL
- Evidence:

## 4) Desktop Agent Enforcement

### 4.1 Allowlist Enforcement
- Steps:
1. Send unsupported action.
- Expected:
1. Blocked by `allowed_commands`.
- Result: PASS / FAIL
- Evidence:

### 4.2 Confirmation-Required Actions
- Steps:
1. Trigger `run_command`, `screenshot`, `get_clipboard`, `open_file` without `confirmed`.
- Expected:
1. Agent blocks with confirmation-required error.
- Result: PASS / FAIL
- Evidence:

### 4.3 Action Timeout
- Steps:
1. Run long command exceeding timeout.
- Expected:
1. Timeout failure returned.
- Result: PASS / FAIL
- Evidence:

### 4.4 Signature Verification (if enabled)
- Steps:
1. Enable signature verification.
2. Send unsigned/invalid signed task.
- Expected:
1. Task rejected.
- Result: PASS / FAIL
- Evidence:

## 5) Privacy & Memory Controls

### 5.1 Sensitive Memory Redaction
- Steps:
1. Store memory containing token/password-like text.
2. Read/export memory.
- Expected:
1. Raw sensitive value not stored; redacted token present.
- Result: PASS / FAIL
- Evidence:

### 5.2 Delete Memory All
- Endpoint:
1. `DELETE /api/memory/all`
- Expected:
1. User memory removed.
- Result: PASS / FAIL
- Evidence:

### 5.3 Delete Conversation
- Endpoints:
1. `DELETE /api/conversations/{id}` and/or `DELETE /api/privacy/conversations/{id}`
- Expected:
1. Conversation removed only for current user scope.
- Result: PASS / FAIL
- Evidence:

### 5.4 Privacy Export + Forget-Me
- Endpoints:
1. `POST /api/privacy/export`
2. `POST /api/privacy/forget-me`
- Expected:
1. Export returns scoped user data (sanitized).
2. Forget-me deletes user memory/conversation footprint.
- Result: PASS / FAIL
- Evidence:

## 6) WebSocket Security

### 6.1 Unauthenticated/Invalid WS Register
- Steps:
1. Attempt register spam / malformed WS messages.
- Expected:
1. Rate limit applies; invalid flow blocked.
- Result: PASS / FAIL
- Evidence:

### 6.2 User Isolation
- Steps:
1. Try cross-user task/result injection.
- Expected:
1. No cross-user execution.
- Result: PASS / FAIL
- Evidence:

### 6.3 HTTPS/WSS Policy
- Steps:
1. Enable strict secure transport flags.
2. Call over insecure remote transport.
- Expected:
1. Insecure transport rejected (except allowed localhost).
- Result: PASS / FAIL
- Evidence:

## 7) Logging, Audit, Error Handling

### 7.1 Audit Completeness
- Check fields:
1. actor/user_id
2. action
3. status
4. source
5. timestamp
- Expected:
1. Present for auth, commands, desktop, integrations, privacy.
- Result: PASS / FAIL
- Evidence:

### 7.2 Secret Redaction in Logs
- Steps:
1. Trigger known errors with token-like values.
- Expected:
1. Masked/redacted logs, no raw secret exposure.
- Result: PASS / FAIL
- Evidence:

### 7.3 Error Response Hygiene
- Steps:
1. Trigger 500 intentionally.
- Expected:
1. Client gets sanitized error (no raw stack trace).
2. Internal logs keep useful sanitized diagnostics.
- Result: PASS / FAIL
- Evidence:

## 8) Final Sign-off

- Critical tests passed: YES / NO
- High severity issues open: YES / NO
- Patch readiness:
1. Dev Ready
2. Stage Ready
3. Production Ready
- Sign-off by:

