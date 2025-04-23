# tests/test_reservation_service.py
import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta
from app.main import app

@pytest.mark.asyncio
async def test_reservation_class_full():
    data = {
        "class_id": "class123",
        "user_id": "user123",
        "date": datetime.now().isoformat()
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/reservations/class123", json=data)
        assert response.status_code == 400
        assert response.json()["error"] == "Clase sin cupos disponibles."

@pytest.mark.asyncio
async def test_reservation_invalid_class():
    data = {
        "class_id": "invalid_class",
        "user_id": "user123",
        "date": datetime.now().isoformat()
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/reservations/invalid_class", json=data)
        assert response.status_code == 404
        assert "Clase no encontrada" in response.json()["error"]

@pytest.mark.asyncio
async def test_reservation_past_date():
    past_date = datetime.now() - timedelta(days=1)
    data = {
        "class_id": "class123",
        "user_id": "user123",
        "date": past_date.isoformat()
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/reservations/class123", json=data)
        assert response.status_code == 400
        assert "fecha pasada" in response.json()["error"]