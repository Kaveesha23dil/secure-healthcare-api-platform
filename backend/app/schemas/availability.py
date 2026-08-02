from datetime import datetime
from uuid import UUID

from pydantic import Field, model_validator

from app.schemas.common import ApiModel, PaginationMetadata, StrictApiModel


class AvailabilitySlot(ApiModel):
    id: UUID
    doctor_id: UUID = Field(alias="doctorId")
    start_time: datetime = Field(alias="startAt")
    end_time: datetime = Field(alias="endAt")
    available: bool


class AvailabilitySlotCreateRequest(StrictApiModel):
    start_time: datetime = Field(alias="startAt")
    end_time: datetime = Field(alias="endAt")

    @model_validator(mode="after")
    def validate_range(self) -> "AvailabilitySlotCreateRequest":
        if self.start_time.tzinfo is None or self.end_time.tzinfo is None:
            raise ValueError("Date-time values require timezone offsets")
        if self.start_time >= self.end_time:
            raise ValueError("startAt must be before endAt")
        return self


class PaginatedAvailabilityResponse(PaginationMetadata):
    items: list[AvailabilitySlot]
