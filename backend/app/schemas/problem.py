from uuid import UUID

from pydantic import Field

from app.schemas.common import StrictApiModel


class ProblemDetails(StrictApiModel):
    type: str
    title: str
    status: int
    detail: str
    instance: str | None = None
    trace_id: UUID = Field(alias="traceId")


class ValidationErrorItem(StrictApiModel):
    field: str
    message: str


class ValidationProblemDetails(ProblemDetails):
    errors: list[ValidationErrorItem]
