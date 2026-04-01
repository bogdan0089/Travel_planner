from datetime import date, datetime
from pydantic import BaseModel, Field
from core.enums import ProjectStatus
from schemas.schemas_place import PlaceOut


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    start_date: date | None = None
    place_ids: list[int] = Field(default_factory=list, max_length=10, description="Art Institute artwork IDs")


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    start_date: date | None = None


class ProjectOut(BaseModel):
    id: int
    name: str
    description: str | None
    start_date: date | None
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class ProjectWithPlacesOut(ProjectOut):
    places: list[PlaceOut] = []


class PaginatedProjects(BaseModel):
    items: list[ProjectOut]
    total: int
    page: int
    size: int
    pages: int
