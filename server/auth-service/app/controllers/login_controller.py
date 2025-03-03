from fastapi import APIRouter, HTTPException, Response, Header
from pydantic import BaseModel, Field
from app.services.auth_service import AuthService

router = APIRouter()

class LoginSuccessResponse(BaseModel):
    """
    Respuesta para un inicio de sesión exitoso.
    """
    user_id: str = Field(..., title="ID del Usuario", description="Identificador único del usuario autenticado.")
    email: str = Field(..., title="Correo Electrónico", description="Correo electrónico del usuario autenticado.")
    role: str = Field(..., title="Rol", description="Rol asignado al usuario en la plataforma.")
    token: str = Field(..., title="Token", description="Token de autenticación devuelto en la respuesta.")

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
        raise HTTPException(status_code=401, detail="Token requerido")
    
    token = authorization.split("Bearer ")[-1]  # Extraer el token correctamente
    user_data = await AuthService.verify_token(token)

    # 🔥 Establecer la cookie con el token de sesión
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
