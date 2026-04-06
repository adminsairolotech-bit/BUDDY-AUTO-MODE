from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, status

from database.models import EmailVerificationRequest, TokenRefreshRequest, UserLoginRequest, UserRegisterRequest
from database.repositories import UserRepository
from utils.audit import AuditLogger
from utils.helpers import get_settings
from utils.security import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    hash_password,
    revoke_token,
    is_token_revoked,
    validate_password_strength,
    verify_password,
    verify_refresh_token,
)
from utils.validators import is_valid_email, password_policy_errors


router = APIRouter(prefix="/api/auth", tags=["auth"])
LOGIN_FAIL_LIMIT = 5
LOGIN_LOCK_MINUTES = 15


def _hash_code(code: str) -> str:
    return hashlib.sha256(code.encode("utf-8")).hexdigest()


def _generate_code() -> str:
    return "".join(secrets.choice("0123456789") for _ in range(6))


def _client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


@router.post("/register", status_code=201)
async def register(payload: UserRegisterRequest, request: Request):
    if not is_valid_email(payload.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    if not validate_password_strength(payload.password):
        raise HTTPException(status_code=400, detail=" ".join(password_policy_errors(payload.password)))

    repo = UserRepository()
    existing = await repo.find_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = await repo.create(payload.email, hash_password(payload.password), payload.name)
    access_token = create_access_token({"sub": user["_id"], "email": user["email"]})
    refresh_token = create_refresh_token({"sub": user["_id"], "email": user["email"]})
    verification_code = _generate_code()
    await repo.collection.update_one(
        {"email": payload.email},
        {
            "$set": {
                "email_verified": False,
                "email_verification_code_hash": _hash_code(verification_code),
                "email_verification_expires_at": datetime.utcnow() + timedelta(minutes=30),
                "failed_login_attempts": 0,
                "login_locked_until": None,
                "updated_at": datetime.utcnow(),
            }
        },
    )
    audit = AuditLogger()
    await audit.log(user_id=user["_id"], action="auth.register", status="success", source="api", ip=_client_ip(request), details={"email": payload.email})
    response = {
        "success": True,
        "message": "User registered successfully",
        "user": {"id": user["_id"], "email": user["email"], "name": user["name"]},
        "token": access_token,
        "refresh_token": refresh_token,
    }
    if get_settings().app_env != "production":
        response["verification_code_dev_only"] = verification_code
    return response


@router.post("/login")
async def login(payload: UserLoginRequest, request: Request):
    rate_limiter = request.app.state.rate_limiter
    ip = _client_ip(request)
    if not rate_limiter.allow(f"login:ip:{ip}", limit=10, window_seconds=60):
        raise HTTPException(status_code=429, detail="Too many login attempts. Try again later.")

    repo = UserRepository()
    user = await repo.find_by_email(payload.email)
    audit = AuditLogger()
    if not user:
        await audit.log(user_id=None, action="auth.login", status="failed", source="api", ip=ip, details={"reason": "user_not_found", "email": payload.email})
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    locked_until = user.get("login_locked_until")
    if isinstance(locked_until, datetime) and locked_until > datetime.utcnow():
        raise HTTPException(status_code=423, detail="Account temporarily locked due to failed login attempts")

    if not verify_password(payload.password, user["password_hash"]):
        failed = int(user.get("failed_login_attempts", 0)) + 1
        lock_until = None
        if failed >= LOGIN_FAIL_LIMIT:
            lock_until = datetime.utcnow() + timedelta(minutes=LOGIN_LOCK_MINUTES)
        await repo.collection.update_one(
            {"email": payload.email},
            {"$set": {"failed_login_attempts": failed, "login_locked_until": lock_until, "updated_at": datetime.utcnow()}},
        )
        await audit.log(user_id=user["_id"], action="auth.login", status="failed", source="api", ip=ip, details={"reason": "bad_password", "attempts": failed})
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    await repo.collection.update_one(
        {"email": payload.email},
        {"$set": {"failed_login_attempts": 0, "login_locked_until": None, "updated_at": datetime.utcnow()}},
    )

    access_token = create_access_token({"sub": user["_id"], "email": user["email"]})
    refresh_token = create_refresh_token({"sub": user["_id"], "email": user["email"]})
    await audit.log(user_id=user["_id"], action="auth.login", status="success", source="api", ip=ip, details={"email_verified": bool(user.get("email_verified", False))})
    return {
        "success": True,
        "token": access_token,
        "refresh_token": refresh_token,
        "email_verified": bool(user.get("email_verified", False)),
        "user": {"id": user["_id"], "email": user["email"], "name": user["name"]},
    }


@router.get("/me")
async def me(current_user: dict = Depends(get_current_user)):
    user_id = current_user.get("sub")
    repo = UserRepository()
    user = await repo.find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "success": True,
        "user": {
            "id": user["_id"],
            "email": user["email"],
            "name": user["name"],
            "email_verified": bool(user.get("email_verified", False)),
            "preferences": user.get("preferences", {}),
        },
    }


@router.post("/refresh")
async def refresh_token(payload: TokenRefreshRequest, request: Request):
    rate_limiter = request.app.state.rate_limiter
    ip = _client_ip(request)
    if not rate_limiter.allow(f"refresh:ip:{ip}", limit=20, window_seconds=60):
        raise HTTPException(status_code=429, detail="Too many token refresh requests")
    token = payload.refresh_token
    if not token:
        raise HTTPException(status_code=400, detail="refresh_token is required")
    data = verify_refresh_token(token)
    if not data:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    if await is_token_revoked(token, data):
        raise HTTPException(status_code=401, detail="Refresh token revoked")

    access = create_access_token({"sub": data.get("sub"), "email": data.get("email")})
    new_refresh = create_refresh_token({"sub": data.get("sub"), "email": data.get("email")})
    await AuditLogger().log(
        user_id=data.get("sub"),
        action="auth.refresh",
        status="success",
        source="api",
        ip=_client_ip(request),
        details={},
    )
    return {"success": True, "token": access, "refresh_token": new_refresh}


@router.post("/logout")
async def logout(request: Request, current_user: dict = Depends(get_current_user)):
    auth_header = request.headers.get("authorization", "")
    token = auth_header.replace("Bearer ", "").strip() if auth_header.lower().startswith("bearer ") else ""
    refresh_token = request.headers.get("x-refresh-token", "").strip()
    if token:
        await revoke_token(token, reason="logout")
    if refresh_token:
        await revoke_token(refresh_token, reason="logout")
    await AuditLogger().log(user_id=current_user.get("sub"), action="auth.logout", status="success", source="api", ip=_client_ip(request), details={})
    return {"success": True, "message": "Logged out successfully"}


@router.post("/verify-email")
async def verify_email(payload: EmailVerificationRequest, request: Request):
    repo = UserRepository()
    user = await repo.find_by_email(payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    code_hash = user.get("email_verification_code_hash")
    expires = user.get("email_verification_expires_at")
    if not code_hash or not isinstance(expires, datetime):
        raise HTTPException(status_code=400, detail="No active verification code")
    if datetime.utcnow() > expires:
        raise HTTPException(status_code=400, detail="Verification code expired")
    if _hash_code(payload.code) != code_hash:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    await repo.collection.update_one(
        {"email": payload.email},
        {
            "$set": {"email_verified": True, "updated_at": datetime.utcnow()},
            "$unset": {"email_verification_code_hash": "", "email_verification_expires_at": ""},
        },
    )
    await AuditLogger().log(
        user_id=user["_id"],
        action="auth.verify_email",
        status="success",
        source="api",
        ip=_client_ip(request),
        details={},
    )
    return {"success": True, "message": "Email verified successfully"}
