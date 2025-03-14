from fastapi import APIRouter, HTTPException
from app.models.dtos.promotion_dto import PromotionDTO
from app.services.promotion_service import PromotionService
from app.utils.response_standardization import SuccessResponse, ErrorResponse
import logging

router = APIRouter()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@router.get("/", tags=["Promociones"], response_model=SuccessResponse)
async def list_promotions():
    """Obtiene la lista de todas las promociones disponibles."""
    logger.debug("Recibida petición GET /promotions/")
    response = await PromotionService.get_all_promotions()
    if response.status == "error":
        raise HTTPException(status_code=500, detail=response.dict())
    return response

@router.post("/create", tags=["Promociones"], response_model=SuccessResponse)
async def create_promotion(promotion: PromotionDTO):
    """Crea una nueva promoción en la plataforma."""
    response = await PromotionService.create_promotion(promotion)
    if response.status == "error":
        raise HTTPException(status_code=400, detail=response.dict())
    return response

@router.put("/update/{promotion_id}", tags=["Promociones"], response_model=SuccessResponse)
async def update_promotion(promotion_id: str, promotion: PromotionDTO):
    """Actualiza una promoción en la plataforma."""
    response = await PromotionService.update_promotion(promotion_id, promotion)
    if response.status == "error":
        raise HTTPException(status_code=400, detail=response.dict())
    return response

@router.delete("/delete/{promotion_id}", tags=["Promociones"], response_model=SuccessResponse)
async def delete_promotion(promotion_id: str):
    """Elimina una promoción por su ID."""
    response = await PromotionService.delete_promotion(promotion_id)
    if response.status == "error":
        raise HTTPException(status_code=400, detail=response.dict())
    return response
