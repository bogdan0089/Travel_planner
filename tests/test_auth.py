import pytest


@pytest.mark.asyncio
async def test_register(client):
    resp = await client.post("/auth/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "secret123",
    })
    assert resp.status_code == 201
    assert resp.json()["username"] == "alice"


@pytest.mark.asyncio
async def test_register_duplicate(client):
    payload = {"username": "alice", "email": "alice@example.com", "password": "secret123"}
    await client.post("/auth/register", json=payload)
    resp = await client.post("/auth/register", json=payload)
    assert resp.status_code == 409


@pytest.mark.asyncio
async def test_login(client):
    await client.post("/auth/register", json={"username": "bob", "email": "bob@example.com", "password": "pass123"})
    resp = await client.post("/auth/login", data={"username": "bob", "password": "pass123"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    await client.post("/auth/register", json={"username": "carl", "email": "carl@example.com", "password": "pass123"})
    resp = await client.post("/auth/login", data={"username": "carl", "password": "wrong"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_me(auth_client):
    resp = await auth_client.get("/auth/me")
    assert resp.status_code == 200
    assert resp.json()["username"] == "testuser"
