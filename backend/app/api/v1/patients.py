from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.dependencies.auth import require_scopes
from app.api.dependencies.database import DbSession
from app.api.v1.appointments import as_schema
from app.core.security import AuthenticatedUser
from app.schemas.appointment import AppointmentStatus, PaginatedAppointmentResponse
from app.services.appointment_service import AppointmentService

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.get(
    "/me/appointments",
    response_model=PaginatedAppointmentResponse,
    response_model_by_alias=True,
    operation_id="listMyAppointments",
)
def list_my_appointments(
    db: DbSession,
    actor: Annotated[AuthenticatedUser, Depends(require_scopes("appointment:read"))],
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: AppointmentStatus | None = None,
) -> PaginatedAppointmentResponse:
    items, total, pages = AppointmentService(db).list_mine(
        actor, page, size, status.value if status else None
    )
    return PaginatedAppointmentResponse(
        items=[as_schema(x) for x in items],
        page=page,
        size=size,
        total_items=total,
        total_pages=pages,
    )
