import pytest
from httpx import AsyncClient
from datetime import date, timedelta
from app.main import app  # asegúrate de que `PYTHONPATH=.` esté configurado o usa rutas relativas si estás fuera del proyecto

# 1. Contraseñas no coinciden
@pytest.mark.asyncio
async def test_register_passwords_dont_match():
    data = {
        "full_name": "Pedro Gym",
        "email": "pedro@example.com",
        "password": "Abc123!@#",
        "confirm_password": "Wrong123!",
        "phone": "+59170000000",
        "user_type": "gym_owner",
        "gym_name": "FitZone",
        "gym_address": "Calle Falsa 123",
        "gym_phone": "+59170000001",
        "opening_hours": "7:00-21:00",
        "services_offered": "pesas,cardio",
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("auth/register", data=data)
    assert response.status_code == 400
    assert response.json()["error"] == "Las contraseñas no coinciden."

# 2. Contraseña demasiado corta
@pytest.mark.asyncio
async def test_register_short_password():
    data = {
        "full_name": "Test User",
        "email": "shortpass@test.com",
        "password": "A1!",
        "confirm_password": "A1!",
        "phone": "+59170000000",
        "user_type": "gym_owner",
        "gym_name": "MiniGym",
        "gym_address": "Avenida 1",
        "gym_phone": "+59170000001",
        "opening_hours": "8:00-20:00",
        "services_offered": "cardio",
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("auth/register", data=data)
    assert response.status_code == 400
    assert "al menos 8 caracteres" in response.json()["error"]

# 3. Contraseña sin número
@pytest.mark.asyncio
async def test_register_password_missing_number():
    data = {
        "full_name": "Test User",
        "email": "nonumber@test.com",
        "password": "Abcdefg!",
        "confirm_password": "Abcdefg!",
        "phone": "+59170000000",
        "user_type": "gym_owner",
        "gym_name": "GymPro",
        "gym_address": "Zona Sur",
        "gym_phone": "+59170000001",
        "opening_hours": "9:00-21:00",
        "services_offered": "pesas",
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("auth/register", data=data)
    assert response.status_code == 400
    assert "al menos un número" in response.json()["error"]

# 4. Tipo de usuario inválido
@pytest.mark.asyncio
async def test_register_invalid_user_type():
    data = {
        "full_name": "Invalid Type",
        "email": "invalidtype@test.com",
        "password": "Valid123!",
        "confirm_password": "Valid123!",
        "phone": "+59170000000",
        "user_type": "admin",  # inválido
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("auth/register", data=data)
    assert response.status_code == 400
    assert "debe ser 'gym_owner' o 'gym_member'" in response.json()["error"]

# 5. Menor de edad (menos de 14 años)
@pytest.mark.asyncio
async def test_register_underage_member():
    thirteen_years_ago = date.today() - timedelta(days=13 * 365)
    data = {
        "full_name": "Young User",
        "email": "young@test.com",
        "password": "Valid123!",
        "confirm_password": "Valid123!",
        "phone": "+59170000000",
        "user_type": "gym_member",
        "gym_id": "gym001",
        "membership_number": "12345",
        "birth_date": thirteen_years_ago.isoformat(),
        "gender": "Masculino"
    }
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("auth/register", data=data)
    assert response.status_code == 400
    assert "al menos 14 años" in response.json()["error"]
