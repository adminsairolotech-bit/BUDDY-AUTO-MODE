from __future__ import annotations

from fastapi import APIRouter


router = APIRouter(prefix="/api", tags=["system"])


@router.get("")
async def api_root():
    return {
        "success": True,
        "service": "OpenClaw Clone API",
        "status": "online",
        "docs": "/docs",
        "health": "/api/health",
    }
