from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from core.enums import ProjectStatus
from models.models import Project


class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create_project(self, name: str, user_id: int, description: str | None, start_date) -> Project:
        project = Project(name=name, user_id=user_id, description=description, start_date=start_date)
        self.session.add(project)
        await self.session.flush()
        await self.session.refresh(project)
        return project

    async def get_project(self, project_id: int) -> Project | None:
        return await self.session.get(Project, project_id)

    async def get_project_with_places(self, project_id: int) -> Project | None:
        result = await self.session.execute(
            select(Project).options(selectinload(Project.places)).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def get_all_projects(self, user_id: int, status: ProjectStatus | None, offset: int, limit: int) -> list[Project]:
        stmt = select(Project).where(Project.user_id == user_id)
        if status:
            stmt = stmt.where(Project.status == status)
        stmt = stmt.order_by(Project.created_at.desc()).offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def count_projects(self, user_id: int, status: ProjectStatus | None) -> int:
        stmt = select(Project).where(Project.user_id == user_id)
        if status:
            stmt = stmt.where(Project.status == status)
        result = await self.session.execute(stmt)
        return len(result.scalars().all())

    async def update_project(self, project: Project, name: str | None, description: str | None, start_date) -> Project:
        if name is not None:
            project.name = name
        if description is not None:
            project.description = description
        if start_date is not None:
            project.start_date = start_date
        await self.session.flush()
        await self.session.refresh(project)
        return project

    async def update_status(self, project: Project, status: ProjectStatus) -> None:
        project.status = status
        await self.session.flush()

    async def delete_project(self, project: Project) -> None:
        await self.session.delete(project)
        await self.session.flush()
