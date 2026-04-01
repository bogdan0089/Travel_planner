from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.models import ProjectPlace


class PlaceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def add_place(self, project_id: int, external_id: str, title: str, artist: str | None, image_url: str | None, notes: str | None) -> ProjectPlace:
        place = ProjectPlace(
            project_id=project_id,
            external_id=external_id,
            title=title,
            artist=artist,
            image_url=image_url,
            notes=notes,
        )
        self.session.add(place)
        await self.session.flush()
        await self.session.refresh(place)
        return place

    async def get_place(self, place_id: int) -> ProjectPlace | None:
        return await self.session.get(ProjectPlace, place_id)

    async def get_place_in_project(self, project_id: int, place_id: int) -> ProjectPlace | None:
        result = await self.session.execute(
            select(ProjectPlace).where(ProjectPlace.project_id == project_id, ProjectPlace.id == place_id)
        )
        return result.scalar_one_or_none()

    async def get_by_external_id(self, project_id: int, external_id: str) -> ProjectPlace | None:
        result = await self.session.execute(
            select(ProjectPlace).where(ProjectPlace.project_id == project_id, ProjectPlace.external_id == external_id)
        )
        return result.scalar_one_or_none()

    async def get_places_for_project(self, project_id: int, offset: int, limit: int) -> list[ProjectPlace]:
        result = await self.session.execute(
            select(ProjectPlace)
            .where(ProjectPlace.project_id == project_id)
            .order_by(ProjectPlace.created_at.asc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def count_places(self, project_id: int) -> int:
        result = await self.session.execute(
            select(ProjectPlace).where(ProjectPlace.project_id == project_id)
        )
        return len(result.scalars().all())

    async def update_place(self, place: ProjectPlace, notes: str | None, visited: bool | None) -> ProjectPlace:
        if notes is not None:
            place.notes = notes
        if visited is not None:
            place.visited = visited
        await self.session.flush()
        await self.session.refresh(place)
        return place

    async def count_unvisited(self, project_id: int) -> int:
        result = await self.session.execute(
            select(ProjectPlace).where(ProjectPlace.project_id == project_id, ProjectPlace.visited == False)
        )
        return len(result.scalars().all())
