from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Path, Request

from app.api.dependencies.auth import require_any_scope, require_scopes
from app.api.dependencies.database import DbSession
from app.core.security import AuthenticatedUser
from app.models.appointment import Appointment as AppointmentModel
from app.schemas.appointment import Appointment as AppointmentSchema
from app.schemas.appointment import CreateAppointmentRequest, UpdateAppointmentRequest
from app.services.appointment_service import AppointmentService

router = APIRouter(prefix="/appointments", tags=["Appointments"])


def as_schema(item: AppointmentModel) -> AppointmentSchema:
    return AppointmentSchema(
        id=item.id,
        doctor_id=item.doctor_id,
        slot_id=item.slot_id,
        start_time=item.slot.start_time,
        end_time=item.slot.end_time,
        reason=item.reason,
        status=item.status,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


@router.post(
    "",
    response_model=AppointmentSchema,
    response_model_by_alias=True,
    status_code=201,
    operation_id="createAppointment",
)
def create_appointment(
    data: CreateAppointmentRequest,
    request: Request,
    db: DbSession,
    actor: Annotated[AuthenticatedUser, Depends(require_scopes("appointment:create"))],
) -> AppointmentSchema:
    return as_schema(
        AppointmentService(db).create(
            data, actor, request.state.request_id, request.client.host if request.client else None
        )
    )


@router.get(
    "/{appointmentId}",
    response_model=AppointmentSchema,
    response_model_by_alias=True,
    operation_id="getAppointment",
)
def get_appointment(
    appointment_id: Annotated[UUID, Path(alias="appointmentId")],
    request: Request,
    db: DbSession,
    actor: Annotated[
        AuthenticatedUser, Depends(require_any_scope("appointment:read", "appointment:read:all"))
    ],
) -> AppointmentSchema:
    return as_schema(
        AppointmentService(db).get_authorized(
            appointment_id,
            actor,
            request.state.request_id,
            request.client.host if request.client else None,
        )
    )


@router.patch(
    "/{appointmentId}",
    response_model=AppointmentSchema,
    response_model_by_alias=True,
    operation_id="updateAppointment",
)
def update_appointment(
    appointment_id: Annotated[UUID, Path(alias="appointmentId")],
    data: UpdateAppointmentRequest,
    request: Request,
    db: DbSession,
    actor: Annotated[
        AuthenticatedUser, Depends(require_any_scope("appointment:update", "appointment:cancel"))
    ],
) -> AppointmentSchema:
    if (
        data.status.value == "cancelled"
        and "appointment:cancel" not in actor.scopes
        and "appointment:update" not in actor.scopes
    ):
        from app.core.exceptions import AuthorizationError

        raise AuthorizationError()
    return as_schema(
        AppointmentService(db).update(
            appointment_id,
            data.status.value,
            actor,
            request.state.request_id,
            request.client.host if request.client else None,
        )
    )
