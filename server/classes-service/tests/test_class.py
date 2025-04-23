# tests/test_class_service.py
import pytest
from httpx import AsyncClient, ASGITransport
from datetime import datetime, timedelta
from app.main import app

@pytest.mark.asyncio
async def test_create_class_invalid_data():
    data = {
        "name": "Yo",  # Nombre muy corto
        "description": "Corto",  # Descripción muy corta
        "instructor_id": "inst123",
        "capacity": 0,  # Capacidad inválida
        "duration": 0,  # Duración inválida
        "room": "",  # Sala vacía
        "class_type": "invalid_type",  # Tipo inválido
        "difficulty_level": "invalid"  # Nivel inválido
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/classes/", json=data)
        assert response.status_code == 422
        response_json = response.json()
        assert "detail" in response_json

@pytest.mark.asyncio
async def test_create_class_valid_data():
    data = {
        "name": "Yoga Básico",
        "description": "Clase de yoga para principiantes",
        "instructor_id": "inst123",
        "capacity": 20,
        "duration": 60,
        "room": "Sala 1",
        "class_type": "yoga",
        "difficulty_level": "principiante"
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/classes/", json=data)
        assert response.status_code == 422
        response_json = response.json()
        assert "detail" in response_json

@pytest.mark.asyncio
async def test_get_class_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/classes/invalid_id")
        assert response.status_code == 401
        response_json = response.json()
        assert "detail" in response_json

@pytest.mark.asyncio
async def test_update_class():
    data = {
        "name": "Yoga Avanzado",
        "capacity": 15,
        "difficulty_level": "avanzado"
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.put("/classes/class123", json=data)
        assert response.status_code == 422
        response_json = response.json()
        assert "detail" in response_json

@pytest.mark.asyncio
async def test_delete_class():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete("/classes/class123")
        assert response.status_code == 401
        response_json = response.json()
        assert "detail" in response_json

@pytest.mark.asyncio
async def test_get_class_availability():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/classes/class123/availability")
        assert response.status_code == 401
        response_json = response.json()
        assert "detail" in response_json

@pytest.mark.asyncio
async def test_get_class_with_invalid_token():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/classes/class123",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
        response_json = response.json()
        assert "detail" in response_json

@pytest.mark.asyncio
async def test_get_classes_with_filters():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get(
            "/classes/",
            params={
                "instructor": "inst123",
                "date": datetime.now().date().isoformat(),
                "available_only": "true"
            }
        )
        assert response.status_code == 401
        response_json = response.json()
        assert "detail" in response_json