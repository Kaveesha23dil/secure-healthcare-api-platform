from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import Field

from app.schemas.common import ApiModel, PaginationMetadata, StrictApiModel


class AppointmentStatus(StrEnum):
    PROPOSED = "proposed"
    BOOKED = "booked"
    CHECKED_IN = "checked-in"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no-show"


class Appointment(ApiModel):
    id: UUID
    doctor_id: UUID = Field(alias="doctorId")
    slot_id: UUID = Field(alias="slotId")
    start_time: datetime = Field(alias="startAt")
    end_time: datetime = Field(alias="endAt")
    reason: str
    status: AppointmentStatus
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class CreateAppointmentRequest(StrictApiModel):
    doctor_id: UUID = Field(alias="doctorId")
    slot_id: UUID = Field(alias="slotId")
    reason: str = Field(min_length=1, max_length=500)


class UpdateAppointmentRequest(StrictApiModel):
    status: AppointmentStatus


class PaginatedAppointmentResponse(PaginationMetadata):
    items: list[Appointment]
