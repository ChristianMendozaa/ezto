from fastapi import APIRouter, Request, HTTPException, Depends
from app.services.auth_service import AuthService
from app.utils.response_helper import success_response
from app.models.reservation_model import (
    ReservationCreate, 
    ReservationResponse,
    DashboardResponse,  
    ClientResponse      
)
from app.services.reservation_service import ReservationService
from typing import List
from datetime import datetime

router = APIRouter()

@router.post(
    "/{class_id}",
    summary="Crear reserva",
    description="Crea una nueva reserva para una clase.",
    response_model=ReservationResponse
)
async def create_reservation(
    class_id: str,
    request: Request,
    user: dict = Depends(lambda request: AuthService.require_role(request, "gym_member"))
):
    """
    Crea una nueva reserva para una clase específica.
    """
    reservation = await ReservationService.create_reservation(class_id, user["id"])
    return success_response(reservation)

@router.get(
    "/my-reservations",
    summary="Mis reservas",
    description="Obtiene todas las reservas del usuario actual.",
    response_model=List[ReservationResponse]
)
async def get_my_reservations(
    user: dict = Depends(lambda request: AuthService.require_role(request, "gym_member"))
):
    """
    Obtiene todas las reservas del usuario actual.
    """
    reservations = await ReservationService.get_user_reservations(user["id"])
    return success_response(reservations)

@router.delete(
    "/{reservation_id}",
    summary="Cancelar reserva",
    description="Cancela una reserva existente."
)
async def cancel_reservation(
    reservation_id: str,
    request: Request,
    user: dict = Depends(lambda request: AuthService.require_role(request, "gym_member"))
):
    """
    Cancela una reserva específica.
    """
    await ReservationService.cancel_reservation(reservation_id, user["id"])
    return success_response({"message": "Reserva cancelada exitosamente"})

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
    return success_response({"message": "Bienvenido al Dashboard", "user": user})

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
    return success_response({"message": "Bienvenido al Panel de Cliente", "user": user})

@router.post(
    "/{class_id}/waitlist",
    summary="Unirse a lista de espera",
    description="Permite a un usuario unirse a la lista de espera de una clase llena.",
)
async def join_waitlist(
    class_id: str,
    request: Request,
    user: dict = Depends(lambda request: AuthService.require_role(request, "gym_member"))
):
    """
    Añade al usuario a la lista de espera de una clase.
    """
    waitlist_position = await ReservationService.add_to_waitlist(class_id, user["id"])
    return success_response({
        "message": "Añadido a la lista de espera",
        "position": waitlist_position
    })
