from pydantic import BaseModel, ConfigDict, Field


class ApiModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class StrictApiModel(ApiModel):
    model_config = ConfigDict(populate_by_name=True, from_attributes=True, extra="forbid")


class PaginationMetadata(ApiModel):
    page: int = Field(ge=1)
    size: int = Field(ge=1, le=100)
    total_items: int = Field(alias="totalItems", ge=0)
    total_pages: int = Field(alias="totalPages", ge=0)


class HealthResponse(StrictApiModel):
    status: str = "ok"
