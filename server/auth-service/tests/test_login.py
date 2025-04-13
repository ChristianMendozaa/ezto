from fastapi import HTTPException
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from unittest.mock import patch

@pytest.mark.asyncio
@patch("app.services.auth_service.AuthService.verify_token")
async def test_login_success(mock_verify):
    mock_verify.return_value = {
        "user_id": "123456",
        "email": "user@example.com",
        "role": "gym_owner"
    }

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "auth/login",
            headers={"Authorization": "Bearer dummy_token"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == "123456"
        assert data["email"] == "user@example.com"
        assert data["role"] == "gym_owner"
        assert data["token"] == "dummy_token"

@pytest.mark.asyncio
async def test_login_missing_token():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("auth/login")
        assert response.status_code == 401
        assert "Token requerido" in response.text

@pytest.mark.asyncio
@patch("app.services.auth_service.AuthService.verify_token")
async def test_login_invalid_token(mock_verify):
    mock_verify.side_effect = Exception("Token inválido")

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "auth/login",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 500
        assert "Error interno del servidor" in response.text

@pytest.mark.asyncio
@patch("app.services.auth_service.AuthService.verify_token", return_value={
    "user_id": "user123",
    "email": "test@example.com",
    "role": "gym_member"
})
async def test_login_malformed_header(mock_verify):


    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "auth/login",
            headers={"Authorization": "malformed_header_without_bearer"}
        )
        assert response.status_code == 200  # El controlador aún extrae el token con .split()
        # Puedes ajustar esto si deseas validar más estrictamente el formato
        
@patch("app.services.auth_service.AuthService.verify_token", side_effect=HTTPException(status_code=401, detail="Token caducado"))
@pytest.mark.asyncio
async def test_login_expired_token(mock_verify):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("auth/login", headers={"Authorization": "Bearer expiredtoken"})
        assert response.status_code == 401
        assert response.json()["error"] == "Token caducado"

@patch("app.services.auth_service.AuthService.verify_token", return_value={
    "user_id": "user123", "email": "test@example.com", "role": "gym_member"
})
@pytest.mark.asyncio
async def test_login_authorization_without_bearer(mock_verify):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("auth/login", headers={"Authorization": "noBearerJustToken"})
        assert response.status_code == 200  # Porque aún así extrae el token con `.split("Bearer ")[-1]`
        assert response.json()["user_id"] == "user123"

@patch("app.services.auth_service.AuthService.verify_token", return_value={
    "user_id": "user123", "email": "test@example.com", "role": "gym_member"
})
@pytest.mark.asyncio
async def test_login_sets_cookie(mock_verify):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "auth/login",
            headers={"Authorization": "Bearer validtoken123"}
        )
        assert response.status_code == 200
        cookies = response.cookies
        assert "authToken" in cookies
        assert cookies.get("authToken") == "validtoken123"
