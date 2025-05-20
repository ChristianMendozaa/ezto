# promotions-service/app/controllers/promotion_controller.py
from fastapi import APIRouter, HTTPException, Body, Depends
from typing import Dict, Any
from app.models.dtos.promotion_dto import PromotionDTO
from app.services.promotion_service import PromotionService
from app.utils.response_standardization import SuccessResponse, ErrorResponse, StandardResponse
from app.services.auth_service import AuthService
import logging

router = APIRouter()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@router.get("/", tags=["Promociones"], response_model=SuccessResponse)
async def list_promotions(user: dict = Depends(AuthService.get_current_user)):
    """Obtiene la lista de todas las promociones disponibles."""
    logger.debug("Recibida petición GET /promotions/")
    response = await PromotionService.get_all_promotions()
    if response.status == "error":
        raise HTTPException(status_code=500, detail=response.dict())
    return response

@router.post("/create", response_model=StandardResponse)
async def create_promotion(promotion: PromotionDTO,user: dict = Depends(AuthService.get_current_user)):
    """Crea una nueva promoción en la plataforma."""
    try:
        return await PromotionService.create_promotion(promotion)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/update/{promotion_id}", tags=["Promociones"], response_model=SuccessResponse)
async def update_promotion_partial(promotion_id: str, updates: Dict[str, Any] = Body(...), user: dict = Depends(AuthService.get_current_user)):
    """
    Actualiza parcialmente una promoción por su ID (por ejemplo, solo el estado, descripción o fecha de fin).
    """
    logger.debug(f"Recibida petición PATCH /promotions/update/{promotion_id} con cambios: {updates}")
    response = await PromotionService.update_promotion_partial(promotion_id, updates)
    if response.status == "error":
        raise HTTPException(status_code=400, detail=response.dict())
    return response

@router.delete("/delete/{promotion_id}", tags=["Promociones"], response_model=SuccessResponse)
async def delete_promotion(promotion_id: str,user: dict = Depends(AuthService.get_current_user)):
    """Elimina una promoción por su ID."""
    response = await PromotionService.delete_promotion(promotion_id)
    if response.status == "error":
        raise HTTPException(status_code=400, detail=response.dict())
    return response

@router.get("/{promotion_id}", tags=["Promociones"], response_model=SuccessResponse)
async def get_promotion_by_id(promotion_id: str,user: dict = Depends(AuthService.get_current_user)):
    """Obtiene los detalles de una promoción por su ID."""
    logger.debug(f"Recibida petición GET /promotions/{promotion_id}")
    response = await PromotionService.get_promotion_by_id(promotion_id)
    if response.status == "error":
        raise HTTPException(status_code=404, detail=response.dict())
    return response
