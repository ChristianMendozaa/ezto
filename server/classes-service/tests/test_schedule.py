# tests/test_schedule_service.py
import pytest
from httpx import AsyncClient, ASGITransport
from datetime import datetime, time
from app.main import app

@pytest.mark.asyncio
async def test_create_schedule_invalid_time():
    data = {
        "class_id": "class123",
        "start_time": "10:00",
        "end_time": "09:00",  # Hora fin antes que inicio
        "days_of_week": [1, 3, 5],
        "room": "Sala 1",
        "instructor_id": "inst123"
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/schedules/", json=data)
        assert response.status_code == 422
        response_json = response.json()
        assert "detail" in response_json

@pytest.mark.asyncio
async def test_create_schedule_invalid_days():
    data = {
        "class_id": "class123",
        "start_time": "10:00",
        "end_time": "11:00",
        "days_of_week": [7, 8],  # Días inválidos
        "room": "Sala 1",
        "instructor_id": "inst123"
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/schedules/", json=data)
        assert response.status_code == 422
        response_json = response.json()
        assert "detail" in response_json

@pytest.mark.asyncio
async def test_schedule_room_conflict():
    data = {
        "class_id": "class123",
        "start_time": "10:00",
        "end_time": "11:00",
        "days_of_week": [1, 3],
        "room": "Sala Ocupada",
        "instructor_id": "inst123"
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/schedules/", json=data)
        assert response.status_code == 422
        response_json = response.json()
        assert "detail" in response_json