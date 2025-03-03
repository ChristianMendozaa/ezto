from fastapi import APIRouter, Depends, Request
from app.services.auth_service import AuthService
from pydantic import BaseModel, Field

router = APIRouter()

class DashboardResponse(BaseModel):
    """
    Respuesta para el Panel de Administración.
    """
    message: str = Field(..., title="Mensaje", description="Mensaje de bienvenida al Dashboard.")
    user: dict = Field(..., title="Usuario", description="Información del usuario autenticado.")

class ClientResponse(BaseModel):
    """
    Respuesta para el Panel de Cliente.
    """
    message: str = Field(..., title="Mensaje", description="Mensaje de bienvenida al Panel de Cliente.")
    user: dict = Field(..., title="Usuario", description="Información del usuario autenticado.")

@router.get(
    "/dashboard",
    summary="Panel de Administración",
    description="Acceso al panel de administración para dueños de gimnasios. Se requiere el rol 'gym_owner'.",
    response_model=DashboardResponse
)
async def dashboard(user: dict = Depends(lambda request: AuthService.require_role(request, "gym_owner"))):
    """
    Endpoint para acceder al panel de administración de gimnasios.
    """
    return {"message": "Bienvenido al Dashboard", "user": user}

@router.get(
    "/client",
    summary="Panel de Cliente",
    description="Acceso al panel de cliente para miembros del gimnasio. Se requiere el rol 'gym_member'.",
    response_model=ClientResponse
)
async def client(user: dict = Depends(lambda request: AuthService.require_role(request, "gym_member"))):
    """
    Endpoint para acceder al panel de clientes del gimnasio.
    """
    return {"message": "Bienvenido al Panel de Cliente", "user": user}
