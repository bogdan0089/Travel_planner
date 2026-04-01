from core.enums import ProjectStatus
from core.exceptions import (
    ArtworkNotFoundError,
    PlaceAlreadyExistsError,
    PlaceLimitExceededError,
    ProjectDeleteForbiddenError,
    ProjectNotFoundError,
)
from database.unit_of_work import UnitOfWork
from models.models import Project
from service.artwork_api import artwork_api


class ProjectService:
    async def create_project(
        self,
        user_id: int,
        name: str,
        description: str | None,
        start_date,
        place_ids: list[int],
    ) -> Project:
        if len(place_ids) > 10:
            raise PlaceLimitExceededError()
        artworks = []
        for ext_id in place_ids:
            data = await artwork_api.get_artwork(ext_id)
            if not data:
                raise ArtworkNotFoundError(ext_id)
            artworks.append(data)
        async with UnitOfWork() as uow:
            project = await uow.project.create_project(name, user_id, description, start_date)
            for data in artworks:
                image_url = artwork_api.build_image_url(data.get("image_id"))
                await uow.place.add_place(
                    project_id=project.id,
                    external_id=str(data["id"]),
                    title=data.get("title", ""),
                    artist=data.get("artist_display"),
                    image_url=image_url,
                    notes=None,
                )

        async with UnitOfWork() as uow:
            return await uow.project.get_project_with_places(project.id)

    async def get_project(self, project_id: int, user_id: int) -> Project:
        async with UnitOfWork() as uow:
            project = await uow.project.get_project_with_places(project_id)
        if not project or project.user_id != user_id:
            raise ProjectNotFoundError()
        return project

    async def list_projects(self, user_id: int, status: ProjectStatus | None, page: int, size: int):
        offset = (page - 1) * size
        async with UnitOfWork() as uow:
            projects = await uow.project.get_all_projects(user_id, status, offset, size)
            total = await uow.project.count_projects(user_id, status)
        pages = (total + size - 1) // size
        return projects, total, pages

    async def update_project(self, project_id: int, user_id: int, name: str | None, description: str | None, start_date) -> Project:
        async with UnitOfWork() as uow:
            project = await uow.project.get_project(project_id)
            if not project or project.user_id != user_id:
                raise ProjectNotFoundError()
            project = await uow.project.update_project(project, name, description, start_date)
        return project

    async def delete_project(self, project_id: int, user_id: int) -> None:
        async with UnitOfWork() as uow:
            project = await uow.project.get_project_with_places(project_id)
            if not project or project.user_id != user_id:
                raise ProjectNotFoundError()
            if any(p.visited for p in project.places):
                raise ProjectDeleteForbiddenError()
            await uow.project.delete_project(project)
