# tests/test_class_service.py
import pytest
from httpx import AsyncClient
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
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/classes/", json=data)
        assert response.status_code == 400
        assert response.json()["success"] is False

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
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/classes/", json=data)
        assert response.status_code == 201
        assert response.json()["success"] is True
        assert "id" in response.json()["data"]

@pytest.mark.asyncio
async def test_get_class_not_found():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/classes/invalid_id")
        assert response.status_code == 404
        assert response.json()["success"] is False
        assert "no encontrada" in response.json()["error"]

@pytest.mark.asyncio
async def test_update_class():
    data = {
        "name": "Yoga Avanzado",
        "capacity": 15,
        "difficulty_level": "avanzado"
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.put("/classes/class123", json=data)
        assert response.status_code == 200
        assert response.json()["success"] is True

@pytest.mark.asyncio
async def test_delete_class():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.delete("/classes/class123")
        assert response.status_code == 200
        assert response.json()["success"] is True

@pytest.mark.asyncio
async def test_get_class_availability():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/classes/class123/availability")
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "available_spots" in response.json()["data"]

@pytest.mark.asyncio
async def test_get_class_with_invalid_token():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/classes/class123",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401
        assert response.json()["success"] is False

@pytest.mark.asyncio
async def test_get_classes_with_filters():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/classes/",
            params={
                "instructor": "inst123",
                "date": datetime.now().date().isoformat(),
                "available_only": "true"
            }
        )
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert isinstance(response.json()["data"], list)