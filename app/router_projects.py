from fastapi import APIRouter, Depends, Query
from core.enums import ProjectStatus
from models.models import User
from schemas.schemas_project import (
    PaginatedProjects,
    ProjectCreate,
    ProjectOut,
    ProjectUpdate,
    ProjectWithPlacesOut,
)
from service.project_service import ProjectService
from utils.dependencies import get_current_user


router = APIRouter(prefix="/projects")


@router.post("", response_model=ProjectWithPlacesOut, status_code=201)
async def create_project(data: ProjectCreate, current_user: User = Depends(get_current_user)):
    service = ProjectService()
    project = await service.create_project(
        user_id=current_user.id,
        name=data.name,
        description=data.description,
        start_date=data.start_date,
        place_ids=data.place_ids,
    )
    return project


@router.get("", response_model=PaginatedProjects)
async def list_projects(
    status: ProjectStatus | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
):
    service = ProjectService()
    projects, total, pages = await service.list_projects(current_user.id, status, page, size)
    return PaginatedProjects(items=projects, total=total, page=page, size=size, pages=pages)

@router.get("/{project_id}", response_model=ProjectWithPlacesOut)
async def get_project(project_id: int, current_user: User = Depends(get_current_user)):
    service = ProjectService()
    return await service.get_project(project_id, current_user.id)

@router.patch("/{project_id}", response_model=ProjectOut)
async def update_project(project_id: int, data: ProjectUpdate, current_user: User = Depends(get_current_user)):
    service = ProjectService()
    return await service.update_project(project_id, current_user.id, data.name, data.description, data.start_date)

@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: int, current_user: User = Depends(get_current_user)):
    service = ProjectService()
    await service.delete_project(project_id, current_user.id)
