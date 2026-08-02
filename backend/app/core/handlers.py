import logging
from uuid import UUID, uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.core.exceptions import ApiError
from app.models.audit_event import AuditEvent

logger = logging.getLogger("app.error")


def _trace(request: Request) -> str:
    value = getattr(request.state, "request_id", str(uuid4()))
    try:
        return str(UUID(value))
    except ValueError:
        return str(uuid4())


def install_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApiError)
    async def api_error(request: Request, exc: ApiError) -> JSONResponse:
        if exc.status_code in {401, 403}:
            db = getattr(request.state, "db", None)
            if db is not None:
                try:
                    db.add(
                        AuditEvent(
                            event_type=(
                                "TOKEN_VALIDATION_FAILED"
                                if exc.status_code == 401
                                else "AUTHORIZATION_DENIED"
                            ),
                            actor_subject=getattr(request.state, "actor_subject", "unknown"),
                            actor_role=getattr(request.state, "actor_role", "unknown"),
                            resource_type="route",
                            resource_id=None,
                            result="denied",
                            request_id=getattr(request.state, "request_id", "unknown"),
                            source_ip=request.client.host if request.client else None,
                            event_metadata={"path": request.url.path},
                        )
                    )
                    db.commit()
                except Exception:
                    db.rollback()
                    logger.error(
                        "security_audit_write_failed",
                        extra={"request_id": _trace(request), "result": "failure"},
                    )
        return JSONResponse(
            status_code=exc.status_code,
            media_type="application/problem+json",
            content={
                "type": f"https://api.example.com/problems/{exc.problem_type}",
                "title": exc.title,
                "status": exc.status_code,
                "detail": exc.detail,
                "instance": request.url.path,
                "traceId": _trace(request),
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError) -> JSONResponse:
        errors = [
            {"field": ".".join(str(x) for x in item["loc"] if x != "body"), "message": item["msg"]}
            for item in exc.errors()
        ]
        return JSONResponse(
            status_code=422,
            media_type="application/problem+json",
            content={
                "type": "https://api.example.com/problems/validation",
                "title": "Validation failed",
                "status": 422,
                "detail": "One or more request fields are invalid.",
                "instance": request.url.path,
                "traceId": _trace(request),
                "errors": errors,
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def database_error(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        logger.exception(
            "database_error", extra={"request_id": _trace(request), "result": "failure"}
        )
        return JSONResponse(
            status_code=500,
            media_type="application/problem+json",
            content={
                "type": "https://api.example.com/problems/internal-error",
                "title": "Internal server error",
                "status": 500,
                "detail": "An unexpected error occurred.",
                "instance": request.url.path,
                "traceId": _trace(request),
            },
        )

    @app.exception_handler(Exception)
    async def unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            "unexpected_error", extra={"request_id": _trace(request), "result": "failure"}
        )
        return JSONResponse(
            status_code=500,
            media_type="application/problem+json",
            content={
                "type": "https://api.example.com/problems/internal-error",
                "title": "Internal server error",
                "status": 500,
                "detail": "An unexpected error occurred.",
                "instance": request.url.path,
                "traceId": _trace(request),
            },
        )
