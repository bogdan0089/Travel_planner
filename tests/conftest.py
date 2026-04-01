import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
import models.models  
from app.main import app
from database.database import Base, engine


@pytest_asyncio.fixture(autouse=True)
async def reset_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield

@pytest_asyncio.fixture
async def client(reset_db):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

@pytest_asyncio.fixture
async def auth_client(client):
    await client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123",
    })
    resp = await client.post("/auth/login", data={"username": "testuser", "password": "password123"})
    token = resp.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client
