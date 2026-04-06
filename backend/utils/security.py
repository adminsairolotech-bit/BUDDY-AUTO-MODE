from __future__ import annotations

import base64
import hashlib
import os
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from cryptography.fernet import Fernet
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from database.connection import get_database
from .helpers import get_settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security_scheme = HTTPBearer()

ALGORITHM = "HS256"


def _resolve_fernet_key() -> bytes:
    key = get_settings().encryption_key.strip()
    if not key:
        return Fernet.generate_key()

    try:
        decoded = key.encode("utf-8")
        base64.urlsafe_b64decode(decoded)
        return decoded
    except Exception:
        return Fernet.generate_key()


fernet = Fernet(_resolve_fernet_key())


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    settings = get_settings()
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire, "iat": now, "jti": str(uuid.uuid4()), "typ": "access"})
    return jwt.encode(to_encode, settings.jwt_secret_key, algorithm=ALGORITHM)


def create_refresh_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    settings = get_settings()
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + (expires_delta or timedelta(days=settings.refresh_token_expire_days))
    to_encode.update({"exp": expire, "iat": now, "jti": str(uuid.uuid4()), "typ": "refresh"})
    return jwt.encode(to_encode, settings.jwt_refresh_secret_key, algorithm=ALGORITHM)


def _decode_with_rotation(token: str, *, refresh: bool = False) -> dict[str, Any]:
    settings = get_settings()
    primary = settings.jwt_refresh_secret_key if refresh else settings.jwt_secret_key
    try:
        return jwt.decode(token, primary, algorithms=[ALGORITHM])
    except JWTError:
        if settings.jwt_prev_secret_key:
            return jwt.decode(token, settings.jwt_prev_secret_key, algorithms=[ALGORITHM])
        raise


def verify_token(token: str) -> dict[str, Any] | None:
    try:
        payload = _decode_with_rotation(token, refresh=False)
        if payload.get("typ") != "access":
            return None
        return payload
    except JWTError:
        return None


def verify_refresh_token(token: str) -> dict[str, Any] | None:
    try:
        payload = _decode_with_rotation(token, refresh=True)
        if payload.get("typ") != "refresh":
            return None
        return payload
    except JWTError:
        return None


def encrypt_api_key(api_key: str) -> str:
    return fernet.encrypt(api_key.encode("utf-8")).decode("utf-8")


def decrypt_api_key(encrypted_key: str) -> str:
    return fernet.decrypt(encrypted_key.encode("utf-8")).decode("utf-8")


def validate_password_strength(password: str) -> bool:
    if len(password) < 12:
        return False
    has_upper = any(ch.isupper() for ch in password)
    has_lower = any(ch.islower() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    has_special = any(not ch.isalnum() for ch in password)
    return has_upper and has_lower and has_digit and has_special


def generate_csrf_token() -> str:
    return secrets.token_urlsafe(32)


def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


async def revoke_token(token: str, reason: str = "logout") -> None:
    payload = verify_token(token) or verify_refresh_token(token)
    if not payload:
        return
    await get_database().revoked_tokens.insert_one(
        {
            "jti": payload.get("jti"),
            "token_hash": _token_hash(token),
            "sub": payload.get("sub"),
            "typ": payload.get("typ"),
            "reason": reason,
            "revoked_at": datetime.now(timezone.utc),
            "exp": datetime.fromtimestamp(payload["exp"], tz=timezone.utc) if isinstance(payload.get("exp"), (int, float)) else payload.get("exp"),
        }
    )


async def is_token_revoked(token: str, payload: dict[str, Any] | None = None) -> bool:
    data = payload or (verify_token(token) or verify_refresh_token(token))
    if not data:
        return True
    jti = data.get("jti")
    token_hash = _token_hash(token)
    doc = await get_database().revoked_tokens.find_one({"$or": [{"jti": jti}, {"token_hash": token_hash}]})
    return doc is not None


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> dict[str, Any]:
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if await is_token_revoked(token, payload):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload
