from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, Request

from app.api.dependencies.auth import require_scopes
from app.api.dependencies.database import DbSession
from app.core.security import AuthenticatedUser
from app.models.availability import AvailabilitySlot as AvailabilitySlotModel
from app.schemas.availability import AvailabilitySlot as SlotSchema
from app.schemas.availability import AvailabilitySlotCreateRequest, PaginatedAvailabilityResponse
from app.services.availability_service import AvailabilityService

router = APIRouter(prefix="/doctors/{doctorId}/availability", tags=["Availability"])


def as_schema(slot: AvailabilitySlotModel) -> SlotSchema:
    return SlotSchema(
        id=slot.id,
        doctor_id=slot.doctor_id,
        start_time=slot.start_time,
        end_time=slot.end_time,
        available=slot.status == "available",
    )


@router.get(
    "",
    response_model=PaginatedAvailabilityResponse,
    response_model_by_alias=True,
    operation_id="listDoctorAvailability",
)
def list_availability(
    doctor_id: Annotated[UUID, Path(alias="doctorId")],
    db: DbSession,
    actor: Annotated[AuthenticatedUser, Depends(require_scopes("availability:read"))],
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    start: datetime | None = Query(None, alias="from"),
    end: datetime | None = Query(None, alias="to"),
) -> PaginatedAvailabilityResponse:
    items, total, pages = AvailabilityService(db).list(doctor_id, page, size, start, end)
    return PaginatedAvailabilityResponse(
        items=[as_schema(x) for x in items],
        page=page,
        size=size,
        total_items=total,
        total_pages=pages,
    )


@router.post(
    "",
    response_model=SlotSchema,
    response_model_by_alias=True,
    status_code=201,
    operation_id="createDoctorAvailability",
)
def create_availability(
    doctor_id: Annotated[UUID, Path(alias="doctorId")],
    data: AvailabilitySlotCreateRequest,
    request: Request,
    db: DbSession,
    actor: Annotated[AuthenticatedUser, Depends(require_scopes("availability:write"))],
) -> SlotSchema:
    return as_schema(
        AvailabilityService(db).create(
            doctor_id,
            data,
            actor,
            request.state.request_id,
            request.client.host if request.client else None,
        )
    )
