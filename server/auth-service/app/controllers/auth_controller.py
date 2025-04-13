from fastapi import APIRouter, Header, Request, HTTPException, Response
from pydantic import BaseModel, Field
from app.services.auth_service import AuthService
from app.utils.response_helper import StandardResponse, success_response, error_response
from app.models.responses_models import LoginSuccessResponse, UserResponse

router = APIRouter()

@router.get(
    "/me",
    summary="Obtener usuario autenticado",
    description="Obtiene la información del usuario autenticado extrayendo el token de la cookie `authToken`.",
    response_model=UserResponse  # La documentación sigue mostrando la estructura de usuario
)
async def get_current_user(request: Request):
    """
    Extrae la cookie y obtiene el usuario autenticado.
    Si la autenticación falla, devuelve un error con la razón específica.
    """
    try:
        user = await AuthService.get_current_user(request)
        return success_response(user)
    except HTTPException as e:
        return error_response(e.detail, e.status_code)

@router.post(
    "/login",
    summary="Autenticar usuario y establecer sesión",
    description="""
    Endpoint para autenticar a un usuario mediante un token JWT en el header `Authorization`.  
    Si el token es válido, se devuelve la información del usuario y se establece una cookie `authToken`.
    """,
    response_model=LoginSuccessResponse
)
async def login_user(response: Response, authorization: str = Header(None)):
    """
    Inicia sesión con un token de autorización y configura una cookie con el token de sesión.
    """
    if not authorization:
        return error_response("Token requerido", 401)
    
    try:
        token = authorization.split("Bearer ")[-1]  # Extraer el token correctamente
        user_data = await AuthService.verify_token(token)

        #   Establecer la cookie con el token de sesión
        response.set_cookie(
            key="authToken",
            value=token,
            httponly=True,  # Protege contra JavaScript (XSS)
            secure=False,   # ⚠ Para localhost debe ser False, en producción usa True
            samesite="Lax", # Permite envío seguro de cookies
            max_age=86400   # Expira en 24 horas
        )

        return {
            "user_id": user_data["user_id"],
            "email": user_data["email"],
            "role": user_data["role"],
            "token": token
        }
    except HTTPException as e:
        return error_response(e.detail, e.status_code)
    except Exception as e:
        return error_response("Error interno del servidor", 500)

@router.post(
    "/logout",
    summary="Cerrar sesión",
    description="Elimina la cookie de autenticación para cerrar sesión de manera segura.",
    response_model=StandardResponse
)
async def logout(response: Response):
    """
    Endpoint para cerrar sesión.  
    Elimina la cookie de autenticación `authToken` del usuario.
    """
    response.headers["Set-Cookie"] = "authToken=; Path=/; HttpOnly; Secure=False; SameSite=Lax; Max-Age=0"
    
    return success_response({"message": "Logout exitoso"})
