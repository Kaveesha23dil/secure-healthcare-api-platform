from uuid import UUID

from pydantic import Field

from app.schemas.common import ApiModel, PaginationMetadata


class PatientSummary(ApiModel):
    id: UUID
    display_name: str = Field(alias="displayName")
    masked_email: str = Field(alias="maskedEmail")
    status: str


class PaginatedPatientResponse(PaginationMetadata):
    items: list[PatientSummary]
