# app/controllers/purchase_controller.py

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel, Field
from app.services.sale_service import SaleService
from app.services.auth_service import AuthService
from app.models.purchase_model import SaleCreate, SaleResponse

router = APIRouter()

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Mensaje de error.")

@router.post(
    "/",
    summary="Registrar nueva venta",
    description="Registra una nueva transacción de venta. Requiere rol `gym_owner` o `gym_employee`.",
    response_model=SaleResponse,
    responses={403: {"model": ErrorResponse}, 401: {"model": ErrorResponse}}
)
async def create_sale(
    sale_data: SaleCreate,
    user: dict = Depends(AuthService.get_current_user)
):
    return await SaleService.create_sale(sale_data, user)

@router.get(
    "/",
    summary="Listar todas las ventas",
    description="Devuelve un histórico de todas las ventas. Requiere rol `gym_owner`.",
    response_model=List[SaleResponse],
    responses={401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}}
)
async def list_sales(
    user: dict = Depends(AuthService.get_current_user)
):
    if user.get("role") != "gym_owner":
        raise HTTPException(status_code=403, detail="No tienes permiso para listar ventas.")
    return await SaleService.get_all_sales()

@router.get(
    "/{sale_id}",
    summary="Obtener venta por ID",
    description="Consulta la información de una venta específica. Requiere rol `gym_owner`.",
    response_model=SaleResponse,
    responses={404: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 403: {"model": ErrorResponse}}
)
async def get_sale(
    sale_id: str,
    user: dict = Depends(AuthService.get_current_user)
):
    if user.get("role") != "gym_owner":
        raise HTTPException(status_code=403, detail="No tienes permiso para consultar ventas.")
    sale = await SaleService.get_sale_by_id(sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Venta no encontrada.")
    return sale

@router.delete(
    "/{sale_id}",
    summary="Eliminar una venta",
    description="Elimina una venta por completo. Requiere rol `gym_owner`.",
    response_model=dict,
    responses={404: {"model": ErrorResponse}, 403: {"model": ErrorResponse}, 401: {"model": ErrorResponse}}
)
async def delete_sale(
    sale_id: str,
    user: dict = Depends(AuthService.get_current_user)
):
    if user.get("role") != "gym_owner":
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar ventas.")
    success = await SaleService.delete_sale(sale_id)
    if not success:
        raise HTTPException(status_code=404, detail="Venta no encontrada.")
    return {"message": "Venta eliminada exitosamente"}
