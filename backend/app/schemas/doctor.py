from uuid import UUID

from pydantic import Field

from app.schemas.common import ApiModel, PaginationMetadata, StrictApiModel


class DoctorSummary(ApiModel):
    id: UUID
    display_name: str = Field(alias="displayName")
    specialization: str
    clinic_name: str = Field(alias="clinicName")


class Doctor(DoctorSummary):
    active: bool


class DoctorCreateRequest(StrictApiModel):
    display_name: str = Field(alias="displayName", min_length=1, max_length=120)
    specialization: str = Field(min_length=1, max_length=100)
    clinic_name: str = Field(alias="clinicName", min_length=1, max_length=160)


class DoctorUpdateRequest(StrictApiModel):
    display_name: str | None = Field(None, alias="displayName", min_length=1, max_length=120)
    specialization: str | None = Field(None, min_length=1, max_length=100)
    clinic_name: str | None = Field(None, alias="clinicName", min_length=1, max_length=160)
    active: bool | None = None


class PaginatedDoctorResponse(PaginationMetadata):
    items: list[DoctorSummary]
