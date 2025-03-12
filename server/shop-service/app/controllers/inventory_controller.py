"""
Controlador para endpoints de gestión de movimientos de inventario.

Incluye:
- Registrar un nuevo movimiento.
- Listar todos los movimientos.
- Obtener un movimiento por ID.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel, Field

from app.services.inventory_service import InventoryService
from app.services.auth_service import AuthService
from app.models.inventory_model import InventoryMovement

router = APIRouter()

class ErrorResponse(BaseModel):
    """
    Modelo de error estándar.
    """
    detail: str = Field(..., description="Mensaje de error.")


@router.post(
    "/",
    summary="Registrar un movimiento de inventario",
    description="Registra un nuevo movimiento (entrada, salida, ajuste o devolución). Requiere rol 'gym_owner'.",
    response_model=InventoryMovement,
    responses={403: {"model": ErrorResponse}, 401: {"model": ErrorResponse}}
)
async def register_movement(
    movement_data: InventoryMovement,
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Crea un nuevo movimiento de inventario.
    Solo el 'gym_owner' puede registrar movimientos.
    """
    return await InventoryService.create_movement(movement_data, user)


@router.get(
    "/",
    summary="Listar movimientos de inventario",
    description="Devuelve todos los movimientos registrados. Requiere rol 'gym_owner'.",
    response_model=List[InventoryMovement],
    responses={403: {"model": ErrorResponse}, 401: {"model": ErrorResponse}}
)
async def list_movements(
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Retorna el historial completo de movimientos.  
    Solo 'gym_owner' puede acceder para evitar fugas de datos.
    """
    if user.get("role") != "gym_owner":
        raise HTTPException(status_code=403, detail="No tienes permiso para listar movimientos de inventario.")
    return await InventoryService.get_all_movements()


@router.get(
    "/{movement_id}",
    summary="Obtener movimiento de inventario por ID",
    description="Retorna los datos de un movimiento específico. Requiere rol 'gym_owner'.",
    response_model=InventoryMovement,
    responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}}
)
async def get_movement(
    movement_id: str,
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Obtiene la información de un movimiento a partir de su ID.
    """
    if user.get("role") != "gym_owner":
        raise HTTPException(status_code=403, detail="No tienes permiso para consultar movimientos.")

    movement = await InventoryService.get_movement_by_id(movement_id)
    if not movement:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado.")
    return movement
