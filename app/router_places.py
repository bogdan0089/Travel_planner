from fastapi import APIRouter, Depends, Query
from models.models import User
from schemas.schemas_place import PaginatedPlaces, PlaceAdd, PlaceOut, PlaceUpdate
from service.place_service import PlaceService
from utils.dependencies import get_current_user


router = APIRouter(prefix="/projects/{project_id}/places")


@router.post("", response_model=PlaceOut, status_code=201)
async def add_place(project_id: int, data: PlaceAdd, current_user: User = Depends(get_current_user)):
    service = PlaceService()
    return await service.add_place(project_id, current_user.id, data.external_id, data.notes)

@router.get("", response_model=PaginatedPlaces)
async def list_places(
    project_id: int,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
):
    service = PlaceService()
    places, total, pages = await service.list_places(project_id, current_user.id, page, size)
    return PaginatedPlaces(items=places, total=total, page=page, size=size, pages=pages)

@router.get("/{place_id}", response_model=PlaceOut)
async def get_place(project_id: int, place_id: int, current_user: User = Depends(get_current_user)):
    service = PlaceService()
    return await service.get_place(project_id, place_id, current_user.id)

@router.patch("/{place_id}", response_model=PlaceOut)
async def update_place(project_id: int, place_id: int, data: PlaceUpdate, current_user: User = Depends(get_current_user)):
    service = PlaceService()
    return await service.update_place(project_id, place_id, current_user.id, data.notes, data.visited)
