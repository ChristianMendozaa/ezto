from fastapi import APIRouter, Request, Depends, HTTPException
from pydantic import BaseModel, Field
from app.services.auth_service import AuthService

router = APIRouter()

class UserResponse(BaseModel):
    """
    Respuesta para la obtención del usuario autenticado.
    """
    user_id: str = Field(..., title="ID del Usuario", description="Identificador único del usuario autenticado.")
    email: str = Field(..., title="Correo Electrónico", description="Correo electrónico del usuario autenticado.")
    role: str = Field(..., title="Rol", description="Rol asignado al usuario en la plataforma.")

class ErrorResponse(BaseModel):
    """
    Respuesta en caso de error de autenticación.
    """
    error: str = Field(..., title="Error", description="Descripción del error ocurrido.")

@router.get(
    "/me",
    summary="Obtener usuario autenticado",
    description="""
    Obtiene la información del usuario autenticado extrayendo el token de la cookie `authToken`.
    """,
    response_model=UserResponse,
    responses={401: {"model": ErrorResponse, "description": "Error de autenticación"}}
)
async def get_current_user(request: Request):
    """
    Extrae la cookie y obtiene el usuario autenticado.
    Si la autenticación falla, devuelve un error con la razón específica.
    """
    try:
        user = await AuthService.get_current_user(request)
        return user
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
