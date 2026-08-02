from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.api.dependencies.auth import require_scopes
from app.api.dependencies.database import DbSession
from app.api.v1.appointments import as_schema
from app.core.security import AuthenticatedUser
from app.repositories.patient_repository import PatientRepository
from app.schemas.appointment import AppointmentStatus, PaginatedAppointmentResponse
from app.schemas.patient import PaginatedPatientResponse, PatientSummary
from app.services.appointment_service import AppointmentService

router = APIRouter(prefix="/admin", tags=["Administration"])


def mask_email(value: str | None) -> str:
    if not value or "@" not in value:
        return "***"
    local, domain = value.split("@", 1)
    return f"{local[:1]}***@{domain}"


@router.get(
    "/appointments",
    response_model=PaginatedAppointmentResponse,
    response_model_by_alias=True,
    operation_id="listAllAppointments",
)
def list_all_appointments(
    db: DbSession,
    actor: Annotated[
        AuthenticatedUser, Depends(require_scopes("appointment:read:all", "admin:manage"))
    ],
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: AppointmentStatus | None = None,
    doctor_id: UUID | None = Query(None, alias="doctorId"),
) -> PaginatedAppointmentResponse:
    items, total, pages = AppointmentService(db).list_all(
        actor, page, size, status.value if status else None, doctor_id
    )
    return PaginatedAppointmentResponse(
        items=[as_schema(x) for x in items],
        page=page,
        size=size,
        total_items=total,
        total_pages=pages,
    )


@router.get(
    "/patients",
    response_model=PaginatedPatientResponse,
    response_model_by_alias=True,
    operation_id="listPatients",
)
def list_patients(
    db: DbSession,
    actor: Annotated[AuthenticatedUser, Depends(require_scopes("patient:read", "admin:manage"))],
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> PaginatedPatientResponse:
    from app.services.authorization_service import AuthorizationService

    AuthorizationService.require_role(actor, "administrator")
    items, total = PatientRepository(db).list(page, size)
    pages = (total + size - 1) // size
    result = [
        PatientSummary(
            id=x.id,
            display_name=x.user.display_name,
            masked_email=mask_email(x.user.email),
            status="active" if x.user.active else "disabled",
        )
        for x in items
    ]
    return PaginatedPatientResponse(
        items=result, page=page, size=size, total_items=total, total_pages=pages
    )
