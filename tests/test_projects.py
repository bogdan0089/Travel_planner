import pytest


@pytest.mark.asyncio
async def test_create_project_no_places(auth_client):
    resp = await auth_client.post("/projects", json={"name": "My Trip", "description": "Test"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "My Trip"
    assert data["status"] == "active"
    assert data["places"] == []


@pytest.mark.asyncio
async def test_list_projects_empty(auth_client):
    resp = await auth_client.get("/projects")
    assert resp.status_code == 200
    assert resp.json()["items"] == []
    assert resp.json()["total"] == 0


@pytest.mark.asyncio
async def test_get_project_not_found(auth_client):
    resp = await auth_client.get("/projects/999")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_project(auth_client):
    create = await auth_client.post("/projects", json={"name": "Original"})
    project_id = create.json()["id"]

    resp = await auth_client.patch(f"/projects/{project_id}", json={"name": "Updated"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated"


@pytest.mark.asyncio
async def test_delete_project(auth_client):
    create = await auth_client.post("/projects", json={"name": "To Delete"})
    project_id = create.json()["id"]

    resp = await auth_client.delete(f"/projects/{project_id}")
    assert resp.status_code == 204

    resp = await auth_client.get(f"/projects/{project_id}")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_unauthenticated_request(client):
    resp = await client.get("/projects")
    assert resp.status_code == 401
