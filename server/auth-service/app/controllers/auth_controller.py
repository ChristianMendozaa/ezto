from fastapi import APIRouter, Header, Request, HTTPException, Response
from pydantic import BaseModel, Field
from app.services.auth_service import AuthService
from app.utils.response_helper import StandardResponse, success_response, error_response
from app.models.responses_models import LoginSuccessResponse, UserResponse
from app.models.request_models import LoginData
from app.utils.keycloak_config import keycloak_openid

router = APIRouter()

@router.get(
    "/me",
    summary="Obtener usuario autenticado",
    description="Obtiene la información del usuario autenticado extrayendo el token de la cookie `authToken`.",
    response_model=UserResponse,
    status_code=200,
    tags=["Autenticación"]
)
async def get_current_user(request: Request):
    try:
        user = await AuthService.get_current_user(request)
        return user
    except HTTPException as e:
        raise e

@router.post(
    "/login",
    summary="Iniciar sesión",
    description="Inicia sesión con email y contraseña. Solicita el token a Keycloak y lo guarda como cookie `authToken`.",
    response_model=LoginSuccessResponse,
    status_code=200,
    tags=["Autenticación"]
)
async def login_user(data: LoginData, response: Response):
    try:
        token = keycloak_openid.token(
            username=data.email,
            password=data.password,
            grant_type="password"
        )["access_token"]

        user_data = await AuthService.verify_token(token)

        response.set_cookie(
            key="authToken",
            value=token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=86400
        )

        return {
            "user_id": user_data["user_id"],
            "email": user_data["email"],
            "role": user_data["role"],
            "token": token
        }

    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

@router.post(
    "/logout",
    summary="Cerrar sesión",
    description="Elimina la cookie de autenticación `authToken` para cerrar sesión de manera segura.",
    response_model=StandardResponse,
    status_code=200,
    tags=["Logout"]
)
async def logout(response: Response):
    response.headers["Set-Cookie"] = "authToken=; Path=/; HttpOnly; Secure=False; SameSite=Lax; Max-Age=0"
    return success_response({"message": "Logout exitoso"})
