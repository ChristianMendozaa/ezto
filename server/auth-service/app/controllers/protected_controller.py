from fastapi import APIRouter, Depends
from app.services.auth_service import AuthService
from app.utils.response_helper import success_response
from app.models.responses_models import DashboardResponse, ClientResponse, StandardResponse

router = APIRouter()

@router.get(
    "/dashboard",
    summary="Panel de Administración",
    description="Acceso al panel de administración para dueños de gimnasios. Se requiere el rol 'gym_owner'.",
    response_model=StandardResponse
)
async def dashboard(user: dict = Depends(AuthService.require_role("gym_owner"))):
    """
    Endpoint para acceder al panel de administración de gimnasios.
    """
    return DashboardResponse(message="Bienvenido al Dashboard", user=user)


@router.get(
    "/client",
    summary="Panel de Cliente",
    description="Acceso al panel de cliente para miembros del gimnasio. Se requiere el rol 'gym_member'.",
    response_model=StandardResponse
)
async def client(user: dict = Depends(AuthService.require_role("gym_member"))):
    """
    Endpoint para acceder al panel de clientes del gimnasio.
    """
    return ClientResponse(message="Bienvenido al Panel de Cliente", user=user)

