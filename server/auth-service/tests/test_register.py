import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app  # asegúrate que esto apunta correctamente a tu instancia de FastAPI

transport = ASGITransport(app=app)

@pytest.mark.asyncio
async def test_register_gym_owner_success():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("auth/register", data={
            "full_name": "Test Owner",
            "email": "owner@test.com",
            "password": "TestPass123!",
            "confirm_password": "TestPass123!",
            "phone": "+59171234567",
            "user_type": "gym_owner",
            "gym_name": "Test Gym",
            "gym_address": "Calle Falsa 123",
            "gym_phone": "+59176543210",
            "opening_hours": "6:00-22:00",
            "services_offered": "weights,cardio",
            "capacity": 50,
            "social_media": "https://instagram.com/testgym"
        }, files={})
        assert response.status_code == 200
        assert "registrado exitosamente" in response.text

@pytest.mark.asyncio
async def test_register_owner_invalid_social_media():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("auth/register", data={
            "full_name": "Owner Bad Link",
            "email": "bad@owner.com",
            "password": "OwnerBad123!",
            "confirm_password": "OwnerBad123!",
            "phone": "+59176543211",
            "user_type": "gym_owner",
            "gym_name": "Bad Gym",
            "gym_address": "NoLink Street",
            "gym_phone": "+59176543212",
            "opening_hours": "5:00-23:00",
            "services_offered": "weights",
            "capacity": 30,
            "social_media": "instagram.com/badgym"  # no https
        }, files={})
        assert response.status_code == 400
        assert "url válida" in response.text.lower()

@pytest.mark.asyncio
async def test_register_member_success():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("auth/register", data={
            "full_name": "Test Member",
            "email": "member@test.com",
            "password": "TestPass123!",
            "confirm_password": "TestPass123!",
            "phone": "+59175555555",
            "user_type": "gym_member",
            "gym_id": "gym123",
            "membership_number": "M123",
            "birth_date": "2000-01-01",
            "gender": "Masculino",
            "training_goals": "loseWeight",
            "activity_preferences": "yoga"
        }, files={})
        assert response.status_code == 200
        assert "registrado exitosamente" in response.text.lower()

@pytest.mark.asyncio
async def test_register_member_invalid_age():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("auth/register", data={
            "full_name": "Young Member",
            "email": "young@member.com",
            "password": "TestPass123!",
            "confirm_password": "TestPass123!",
            "phone": "+59175550000",
            "user_type": "gym_member",
            "gym_id": "gym123",
            "membership_number": "M124",
            "birth_date": "2015-01-01",
            "gender": "Femenino",
            "training_goals": "gainMuscle",
            "activity_preferences": "cardio"
        }, files={})
        assert response.status_code == 400
        assert "al menos 14 años" in response.text.lower()

@pytest.mark.asyncio
async def test_register_owner_passwords_do_not_match():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("auth/register", data={
            "full_name": "Mismatch Owner",
            "email": "mismatch@owner.com",
            "password": "Mismatch123!",
            "confirm_password": "Other123!",
            "phone": "+59176666666",
            "user_type": "gym_owner",
            "gym_name": "Mismatch Gym",
            "gym_address": "Fail Street",
            "gym_phone": "+59176660000",
            "opening_hours": "8:00-20:00",
            "services_offered": "groupClasses",
            "capacity": 40,
            "social_media": "https://facebook.com/mismatchgym"
        }, files={})
        assert response.status_code == 400
        assert "no coinciden" in response.text.lower()
