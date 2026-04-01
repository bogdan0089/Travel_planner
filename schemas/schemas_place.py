from datetime import datetime
from pydantic import BaseModel, Field


class PlaceAdd(BaseModel):
    external_id: int = Field(gt=0, description="Art Institute artwork ID")
    notes: str | None = None


class PlaceUpdate(BaseModel):
    notes: str | None = None
    visited: bool | None = None


class PlaceOut(BaseModel):
    id: int
    external_id: str
    title: str
    artist: str | None
    image_url: str | None
    notes: str | None
    visited: bool
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}


class PaginatedPlaces(BaseModel):
    items: list[PlaceOut]
    total: int
    page: int
    size: int
    pages: int
