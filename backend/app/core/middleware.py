import logging
import re
import time
from uuid import UUID, uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response

from app.core.config import get_settings

logger = logging.getLogger("app.request")
REQUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9._-]{1,64}$")


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        incoming = request.headers.get("X-Request-ID", "")
        request_id = incoming if REQUEST_ID_PATTERN.fullmatch(incoming) else str(uuid4())
        request.state.request_id = request_id
        started = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        logger.info(
            "http_request",
            extra={
                "request_id": request_id,
                "method": request.method,
                "route": request.url.path,
                "status_code": response.status_code,
                "duration_ms": round((time.perf_counter() - started) * 1000, 2),
                "actor_subject": getattr(request.state, "actor_subject", None),
                "result": "success" if response.status_code < 400 else "failure",
            },
        )
        return response


class RequestBodyLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        maximum = get_settings().max_request_body_bytes
        raw_length = request.headers.get("content-length")
        if raw_length and raw_length.isdigit() and int(raw_length) > maximum:
            request_id = getattr(request.state, "request_id", str(uuid4()))
            return JSONResponse(
                status_code=413,
                media_type="application/problem+json",
                content={
                    "type": "https://api.example.com/problems/payload-too-large",
                    "title": "Payload too large",
                    "status": 413,
                    "detail": "The request body exceeds the permitted size.",
                    "traceId": str(UUID(request_id)) if _is_uuid(request_id) else str(uuid4()),
                },
            )
        return await call_next(request)


def _is_uuid(value: str) -> bool:
    try:
        UUID(value)
    except ValueError:
        return False
    return True
