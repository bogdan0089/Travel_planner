from core.enums import ProjectStatus
from core.exceptions import (
    ArtworkNotFoundError,
    PlaceAlreadyExistsError,
    PlaceLimitExceededError,
    PlaceNotFoundError,
    ProjectNotFoundError,
)
from database.unit_of_work import UnitOfWork
from models.models import ProjectPlace
from service.artwork_api import artwork_api


class PlaceService:
    async def add_place(self, project_id: int, user_id: int, external_id: int, notes: str | None) -> ProjectPlace:
        data = await artwork_api.get_artwork(external_id)
        if not data:
            raise ArtworkNotFoundError(external_id)

        async with UnitOfWork() as uow:
            project = await uow.project.get_project(project_id)
            if not project or project.user_id != user_id:
                raise ProjectNotFoundError()

            current_count = await uow.place.count_places(project_id)
            if current_count >= 10:
                raise PlaceLimitExceededError()

            existing = await uow.place.get_by_external_id(project_id, str(external_id))
            if existing:
                raise PlaceAlreadyExistsError()

            image_url = artwork_api.build_image_url(data.get("image_id"))
            place = await uow.place.add_place(
                project_id=project_id,
                external_id=str(data["id"]),
                title=data.get("title", ""),
                artist=data.get("artist_display"),
                image_url=image_url,
                notes=notes,
            )
        return place

    async def get_place(self, project_id: int, place_id: int, user_id: int) -> ProjectPlace:
        async with UnitOfWork() as uow:
            project = await uow.project.get_project(project_id)
            if not project or project.user_id != user_id:
                raise ProjectNotFoundError()
            place = await uow.place.get_place_in_project(project_id, place_id)
        if not place:
            raise PlaceNotFoundError()
        return place

    async def list_places(self, project_id: int, user_id: int, page: int, size: int):
        offset = (page - 1) * size
        async with UnitOfWork() as uow:
            project = await uow.project.get_project(project_id)
            if not project or project.user_id != user_id:
                raise ProjectNotFoundError()
            places = await uow.place.get_places_for_project(project_id, offset, size)
            total = await uow.place.count_places(project_id)
        pages = (total + size - 1) // size
        return places, total, pages

    async def update_place(self, project_id: int, place_id: int, user_id: int, notes: str | None, visited: bool | None) -> ProjectPlace:
        async with UnitOfWork() as uow:
            project = await uow.project.get_project_with_places(project_id)
            if not project or project.user_id != user_id:
                raise ProjectNotFoundError()
            place = await uow.place.get_place_in_project(project_id, place_id)
            if not place:
                raise PlaceNotFoundError()
            place = await uow.place.update_place(place, notes, visited)
            unvisited = await uow.place.count_unvisited(project_id)
            total = await uow.place.count_places(project_id)
            if total > 0 and unvisited == 0:
                await uow.project.update_status(project, ProjectStatus.completed)
            elif project.status == ProjectStatus.completed and unvisited > 0:
                await uow.project.update_status(project, ProjectStatus.active)
        return place
