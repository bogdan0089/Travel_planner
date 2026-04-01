from database.database import AsyncSessionFactory
from repository.user_repository import UserRepository
from repository.project_repository import ProjectRepository
from repository.place_repository import PlaceRepository


class UnitOfWork:
    async def __aenter__(self):
        self.session = AsyncSessionFactory()
        self.user = UserRepository(self.session)
        self.project = ProjectRepository(self.session)
        self.place = PlaceRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
