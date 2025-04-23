import pytest
from httpx import AsyncClient
from fastapi import status
from unittest.mock import patch, AsyncMock
from app.main import app


# Verifica que se rechace un token inválido en la ruta protegida /auth/me
@pytest.mark.asyncio
@patch("app.utils.keycloak_config.keycloak_openid.introspect")
async def test_get_current_user_invalid_token(mock_introspect):
    mock_introspect.return_value = {"active": False}

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/auth/me", cookies={"authToken": "invalid-token"})
        assert response.status_code == 401


# Prueba exitosa de login: usuario válido, token válido, respuesta esperada
@pytest.mark.asyncio
@patch("app.utils.keycloak_config.keycloak_openid.token")
@patch("app.services.auth_service.AuthService.verify_token", new_callable=AsyncMock)        
async def test_login_success(mock_verify_token, mock_token):
    mock_token.return_value = {"access_token": "fake-token"}
    mock_verify_token.return_value = {
        "user_id": "abc123",
        "email": "test@ezto.com",
        "role": "admin"
    }

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/auth/login", json={
            "email": "test@ezto.com",
            "password": "Abc12345!"  # ✅ válida
        })

        data = response.json()
        assert response.status_code == 200
        assert data["user_id"] == "abc123"
        assert data["email"] == "test@ezto.com"
        assert data["role"] == "admin"


# Prueba de login con credenciales incorrectas: debería lanzar excepción y retornar 401
@pytest.mark.asyncio
@patch("app.utils.keycloak_config.keycloak_openid.token")
async def test_login_failure(mock_token):
    mock_token.side_effect = Exception("Invalid credentials")

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/auth/login", json={
            "email": "bad@user.com",
            "password": "wrongpass"
        })
        assert response.status_code == 401
        assert response.json()["detail"] == "Credenciales inválidas"


# Verifica que al hacer logout se elimine la cookie authToken
@pytest.mark.asyncio
async def test_logout():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/auth/logout")
        assert response.status_code == 200
        assert response.cookies.get("authToken") is None
        assert response.json()["success"] is True
        assert response.json()["data"]["message"] == "Logout exitoso"


# Test negativo: contraseña demasiado corta, espera error 422 de validación
@pytest.mark.asyncio
async def test_login_invalid_password_format():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/auth/login", json={
            "email": "test@ezto.com",
            "password": "123"  # ❌ inválida: menos de 8 caracteres
        })
        assert response.status_code == 422
