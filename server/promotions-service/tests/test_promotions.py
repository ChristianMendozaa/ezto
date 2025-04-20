import pytest
from httpx import AsyncClient
from datetime import date, timedelta

@pytest.mark.asyncio
async def test_create_promotion_success(client):
    payload = {
        "name": "Black Friday",
        "description": "50% en todos los planes",
        "start_date": date.today().isoformat(),
        "end_date": (date.today() + timedelta(days=5)).isoformat(),
        "discount_type": "percentage",
        "discount_value": 50,
        "applicable_to": "all_users",
        "auto_apply": True,
        "status": True,
        "promo_code": "BLACK2025" 
    }

    response = await client.post("/promotions/create", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "Promoción creada exitosamente" in response.json()["message"]

@pytest.mark.asyncio
async def test_create_promotion_invalid_dates(client):
    payload = {
        "name": "Black Friday",
        "description": "50% en todos los planes",
        "start_date": date.today().isoformat(),
        "end_date": (date.today() + timedelta(days=5)).isoformat(),
        "discount_type": "percentage",
        "discount_value": 50,
        "applicable_to": "all",  # 🔁 Cambiado
        "auto_apply": True,
        "status": True,
    }
    response = await client.post("/promotions/create", json=payload)
    assert response.status_code == 400 or response.status_code == 422
    assert "fecha" in response.json()["message"].lower() or "validación" in response.json()["message"].lower()

@pytest.mark.asyncio
async def test_get_all_promotions(client):
    response = await client.get("/promotions/")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert isinstance(response.json()["data"], list)

@pytest.mark.asyncio
async def test_update_promotion_partial(client):
    # Crear primero una promoción
    payload = {
        "name": "Cyber Week",
        "description": "Descuento para test parcial",
        "start_date": date.today().isoformat(),
        "end_date": (date.today() + timedelta(days=7)).isoformat(),
        "discount_type": "fixed",          
        "discount_value": 100,
        "applicable_to": "all_users",       
        "auto_apply": False,
        "status": True,
        "promo_code": "CYBER2025"       
    }
    create_response = await client.post("/promotions/create", json=payload)
    assert create_response.status_code == 200
    promotion_id = create_response.json()["data"]["id"]

    # Ahora actualizamos parcialmente
    partial_update = {
        "description": "Descripción actualizada",
        "auto_apply": True
    }
    patch_response = await client.patch(f"/promotions/update/{promotion_id}", json=partial_update)
    assert patch_response.status_code == 200
    assert patch_response.json()["message"] == "Promoción actualizada exitosamente"

@pytest.mark.asyncio
async def test_delete_promotion(client):
    # Crear una promoción para eliminarla
    payload = {
        "name": "Eliminar",
        "description": "Esta será eliminada",
        "start_date": date.today().isoformat(),
        "end_date": (date.today() + timedelta(days=1)).isoformat(),
        "discount_type": "percentage",   
        "discount_value": 10,
        "applicable_to": "all_users",    
        "auto_apply": False,
        "promo_code": "DEL2025",         
        "status": True
    }

    create_response = await client.post("/promotions/create", json=payload)
    assert create_response.status_code == 200, create_response.text
    promotion_id = create_response.json()["data"]["id"]

    delete_response = await client.delete(f"/promotions/delete/{promotion_id}")
    assert delete_response.status_code == 200
    assert "eliminada exitosamente" in delete_response.json()["message"]
