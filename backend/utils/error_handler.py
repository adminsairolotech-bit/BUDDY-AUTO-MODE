from __future__ import annotations

import logging
import traceback
from typing import Callable

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from memory.learning_engine import LearningEngine
from utils.sanitizers import mask_string, sanitize_for_log


logger = logging.getLogger(__name__)


def build_error_middleware() -> Callable:
    def _severity(status_code: int) -> str:
        if status_code >= 500:
            return "high"
        if status_code >= 400:
            return "medium"
        return "low"

    async def error_handler_middleware(request: Request, call_next):
        try:
            return await call_next(request)
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"success": False, "error": exc.detail, "severity": _severity(exc.status_code)},
            )
        except Exception as exc:
            message = mask_string(str(exc))
            tb = traceback.format_exc()
            logger.error("Unhandled error: %s\n%s", message, sanitize_for_log(tb))
            try:
                learning_engine = LearningEngine()
                await learning_engine.log_error(
                    error_type="unhandled_exception",
                    error_message=message,
                    context={"path": request.url.path, "method": request.method, "traceback": sanitize_for_log(tb), "severity": "high"},
                )
            except Exception:
                pass
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": "Internal server error", "severity": "high"},
            )

    return error_handler_middleware
