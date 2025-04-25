"""
Controlador para endpoints de gestión de movimientos de inventario.

Incluye:
- Registrar un nuevo movimiento.
- Listar todos los movimientos.
- Obtener un movimiento por ID.
- Actualizar un movimiento existente.
- Eliminar un movimiento.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel, Field
from app.services.inventory_service import InventoryService
from app.services.auth_service import AuthService
from app.models.inventory_model import InventoryMovement

router = APIRouter()


class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Mensaje de error")


class InventoryMovementUpdate(BaseModel):
    quantity:        int | None = Field(None, description="Cantidad de unidades afectadas")
    reason:          str | None = Field(None, max_length=200, description="Justificación del movimiento")
    reference_id:    str | None = Field(None, description="ID de la transacción relacionada")
    # No permitimos cambiar tipo ni fechas ni producto ni responsable
    class Config:
        schema_extra = {
            "example": {
                "quantity":  20,
                "reason":    "Ajuste manual",
                "reference_id": "nuevo-ref-1234"
            }
        }


@router.post(
    "/",
    summary="Registrar un movimiento de inventario",
    description="Registra un nuevo movimiento (entrada, salida, ajuste o devolución). Requiere rol 'gym_owner'.",
    response_model=InventoryMovement,
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}}
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
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}}
)
async def list_movements(
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Retorna el historial completo de movimientos.
    Solo el 'gym_owner' puede acceder.
    """
    return await InventoryService.get_all_movements()


@router.get(
    "/{movement_id}",
    summary="Obtener movimiento por ID",
    description="Retorna los datos de un movimiento específico. Requiere rol 'gym_owner'.",
    response_model=InventoryMovement,
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}}
)
async def get_movement(
    movement_id: str,
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Obtiene la información de un movimiento a partir de su ID.
    """
    mv = await InventoryService.get_movement_by_id(movement_id)
    if not mv:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado.")
    return mv


@router.put(
    "/{movement_id}",
    summary="Actualizar movimiento de inventario",
    description="Actualiza campos específicos de un movimiento. Requiere rol 'gym_owner'.",
    response_model=InventoryMovement,
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}}
)
async def update_movement(
    movement_id: str,
    update_data: InventoryMovementUpdate,
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Aplica actualizaciones parciales a un movimiento existente.
    """
    return await InventoryService.update_movement(movement_id, update_data.model_dump(), user)


@router.delete(
    "/{movement_id}",
    summary="Eliminar movimiento de inventario",
    description="Elimina un movimiento por ID. Requiere rol 'gym_owner'.",
    response_model=dict,
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}, 404: {"model": ErrorResponse}}
)
async def delete_movement(
    movement_id: str,
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Borra completamente un movimiento de inventario.
    """
    return await InventoryService.delete_movement(movement_id, user)
