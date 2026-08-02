from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from sqlalchemy import text

from app.api.v1.router import router
from app.core.config import get_settings
from app.core.handlers import install_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware import RequestBodyLimitMiddleware, RequestContextMiddleware
from app.db.session import SessionLocal
from app.schemas.common import HealthResponse

settings = get_settings()
configure_logging(settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    get_settings()  # force validated startup configuration
    yield


app = FastAPI(
    title="Secure Healthcare API Platform",
    description="Contract-first fictional healthcare appointment API",
    version=settings.app_version,
    debug=settings.app_debug,
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "Idempotency-Key", "X-Request-ID"],
)
app.add_middleware(RequestBodyLimitMiddleware)
app.add_middleware(RequestContextMiddleware)
install_exception_handlers(app)
app.include_router(router)

SECURITY_BY_OPERATION = {
    "listDoctors": ["doctor:read"],
    "getDoctor": ["doctor:read"],
    "createDoctor": ["doctor:write", "admin:manage"],
    "updateDoctor": ["doctor:write", "admin:manage"],
    "deleteDoctor": ["doctor:write", "admin:manage"],
    "listDoctorAvailability": ["availability:read"],
    "createDoctorAvailability": ["availability:write"],
    "createAppointment": ["appointment:create"],
    "getAppointment": ["appointment:read"],
    "updateAppointment": ["appointment:update"],
    "listMyAppointments": ["appointment:read"],
    "listAllAppointments": ["appointment:read:all", "admin:manage"],
    "listPatients": ["patient:read", "admin:manage"],
}


def contract_openapi() -> dict[str, object]:
    if app.openapi_schema is not None:
        return app.openapi_schema
    schema = get_openapi(
        title=app.title, version=app.version, description=app.description, routes=app.routes
    )
    for path_item in schema["paths"].values():
        for operation in path_item.values():
            operation_id = operation.get("operationId")
            if operation_id in SECURITY_BY_OPERATION:
                operation["security"] = [{"oauth2": SECURITY_BY_OPERATION[operation_id]}]
    app.openapi_schema = schema
    return schema


app.openapi = contract_openapi  # type: ignore[method-assign]


@app.get(
    "/health",
    response_model=HealthResponse,
    response_model_by_alias=True,
    operation_id="getHealth",
    tags=["System"],
)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/ready", include_in_schema=True, tags=["System"])
def ready() -> dict[str, str]:
    with SessionLocal() as session:
        session.execute(text("SELECT 1"))
    return {"status": "ready"}
