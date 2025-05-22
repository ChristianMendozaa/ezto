import pytest
from httpx import AsyncClient
from datetime import date, timedelta

@pytest.mark.asyncio
async def test_create_usermembership_success(client):
    payload = {
        "user_id": "user001",
        "plan_id": "plan_mensual",
        "start_date": date.today().isoformat(),
        "end_date": (date.today() + timedelta(days=30)).isoformat(),
        "status": "active",
        "promotion_id": "promo10",
        "final_price": 90.0,
        "auto_renew": True
    }
    response = await client.post("/usermemberships/create", json=payload)
    assert response.status_code == 200
    assert response.json()["data"]["user_id"] == "user001"

@pytest.mark.asyncio
async def test_create_usermembership_invalid_dates(client):
    payload = {
        "user_id": "user002",
        "plan_id": "plan_mensual",
        "start_date": "2025-01-10",
        "end_date": "2025-01-05",  # ❌ Fecha inválida
        "status": "active",
        "final_price": 50.0,
        "auto_renew": False
    }
    response = await client.post("/usermemberships/create", json=payload)
    assert response.status_code == 422  # Validación Pydantic

@pytest.mark.asyncio
async def test_get_usermemberships(client):
    response = await client.get("/usermemberships/")
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)

@pytest.mark.asyncio
async def test_update_usermembership(client):
    # Primero crear
    payload = {
        "user_id": "user123",
        "plan_id": "plan_semestral",
        "start_date": date.today().isoformat(),
        "end_date": (date.today() + timedelta(days=180)).isoformat(),
        "status": "active",
        "final_price": 200.0,
        "auto_renew": False
    }
    create = await client.post("/usermemberships/create", json=payload)
    assert create.status_code == 200
    membership_id = create.json()["data"]["id"]

    # Ahora actualizar
    update_payload = {
        "final_price": 150.0,
        "auto_renew": True
    }
    update = await client.patch(f"/usermemberships/update/{membership_id}", json=update_payload)
    assert update.status_code == 200
    assert update.json()["data"]["final_price"] == 150.0

@pytest.mark.asyncio
async def test_delete_usermembership(client):
    # Crear
    payload = {
        "user_id": "user_delete",
        "plan_id": "plan_delete",
        "start_date": date.today().isoformat(),
        "end_date": (date.today() + timedelta(days=15)).isoformat(),
        "status": "active",
        "final_price": 49.99,
        "auto_renew": False
    }
    create = await client.post("/usermemberships/create", json=payload)
    assert create.status_code == 200
    membership_id = create.json()["data"]["id"]

    # Eliminar
    delete = await client.delete(f"/usermemberships/delete/{membership_id}")
    assert delete.status_code == 200
    assert delete.json()["message"] == "Membresía eliminada exitosamente"
