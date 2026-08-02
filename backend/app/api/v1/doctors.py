from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, Request, Response, status

from app.api.dependencies.auth import require_scopes
from app.api.dependencies.database import DbSession
from app.core.security import AuthenticatedUser
from app.schemas.doctor import (
    Doctor,
    DoctorCreateRequest,
    DoctorSummary,
    DoctorUpdateRequest,
    PaginatedDoctorResponse,
)
from app.services.doctor_service import DoctorService

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.get(
    "",
    response_model=PaginatedDoctorResponse,
    response_model_by_alias=True,
    operation_id="listDoctors",
)
def list_doctors(
    db: DbSession,
    actor: Annotated[AuthenticatedUser, Depends(require_scopes("doctor:read"))],
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    specialization: str | None = None,
) -> PaginatedDoctorResponse:
    items, total, pages = DoctorService(db).list(page, size, specialization)
    return PaginatedDoctorResponse(
        items=[DoctorSummary.model_validate(x) for x in items],
        page=page,
        size=size,
        total_items=total,
        total_pages=pages,
    )


@router.get(
    "/{doctorId}", response_model=Doctor, response_model_by_alias=True, operation_id="getDoctor"
)
def get_doctor(
    doctor_id: Annotated[UUID, Path(alias="doctorId")],
    db: DbSession,
    actor: Annotated[AuthenticatedUser, Depends(require_scopes("doctor:read"))],
) -> Doctor:
    return Doctor.model_validate(DoctorService(db).get(doctor_id))


@router.post(
    "",
    response_model=Doctor,
    response_model_by_alias=True,
    status_code=201,
    operation_id="createDoctor",
)
def create_doctor(
    data: DoctorCreateRequest,
    request: Request,
    db: DbSession,
    actor: Annotated[AuthenticatedUser, Depends(require_scopes("doctor:write", "admin:manage"))],
) -> Doctor:
    return Doctor.model_validate(
        DoctorService(db).create(
            data, actor, request.state.request_id, request.client.host if request.client else None
        )
    )


@router.patch(
    "/{doctorId}", response_model=Doctor, response_model_by_alias=True, operation_id="updateDoctor"
)
def update_doctor(
    doctor_id: Annotated[UUID, Path(alias="doctorId")],
    data: DoctorUpdateRequest,
    request: Request,
    db: DbSession,
    actor: Annotated[AuthenticatedUser, Depends(require_scopes("doctor:write", "admin:manage"))],
) -> Doctor:
    return Doctor.model_validate(
        DoctorService(db).update(
            doctor_id,
            data,
            actor,
            request.state.request_id,
            request.client.host if request.client else None,
        )
    )


@router.delete("/{doctorId}", status_code=status.HTTP_204_NO_CONTENT, operation_id="deleteDoctor")
def delete_doctor(
    doctor_id: Annotated[UUID, Path(alias="doctorId")],
    request: Request,
    db: DbSession,
    actor: Annotated[AuthenticatedUser, Depends(require_scopes("doctor:write", "admin:manage"))],
) -> Response:
    DoctorService(db).deactivate(
        doctor_id, actor, request.state.request_id, request.client.host if request.client else None
    )
    return Response(status_code=204)
