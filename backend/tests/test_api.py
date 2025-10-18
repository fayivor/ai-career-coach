import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "AI Career Coach API" in response.json()["message"]


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_chatbot_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/chatbot/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_roles():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/skills/roles")
    assert response.status_code == 200
    assert "roles" in response.json()
    assert len(response.json()["roles"]) > 0


@pytest.mark.asyncio
async def test_get_all_courses():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/recommendations/courses/all")
    assert response.status_code == 200
    assert "courses" in response.json()


@pytest.mark.asyncio
async def test_create_goal():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        goal_data = {
            "title": "Learn Python",
            "description": "Complete Python course",
            "target_date": "2025-12-31"
        }
        response = await ac.post("/api/tracker/goals", json=goal_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Learn Python"


@pytest.mark.asyncio
async def test_get_goals():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/tracker/goals")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_tracker_stats():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/tracker/stats")
    assert response.status_code == 200
    assert "total_goals" in response.json()
