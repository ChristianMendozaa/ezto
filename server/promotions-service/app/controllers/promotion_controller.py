from fastapi import APIRouter, HTTPException
from app.services.promotion_service import PromotionService
from app.models.dtos.promotion_dto import PromotionDTO
import logging
from datetime import datetime

router = APIRouter()

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@router.get("/", tags=["Promociones"])
async def list_promotions():
    """Obtiene la lista de todas las promociones disponibles."""
    logger.debug("Recibida petición GET /promotions/list")  
    try:
        promotions = await PromotionService.get_all_promotions() 
        logger.debug(f"Promociones obtenidas: {promotions}")
        return [{"id": promo["id"], **promo} for promo in promotions]
    except Exception as e:
        logger.error(f"Error en GET /promotions/list: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create", tags=["Promociones"])
async def create_promotion(promotion: PromotionDTO):
    """Crea una nueva promoción en la plataforma."""
    try:
        # 🔹 Convertir fechas a `datetime.datetime` para Firestore
        promotion_data = promotion.dict()
        promotion_data["start_date"] = datetime.strptime(promotion.start_date, "%Y-%m-%d")
        promotion_data["end_date"] = datetime.strptime(promotion.end_date, "%Y-%m-%d")

        return await PromotionService.create_promotion(promotion_data)
    except Exception as e:
        logger.error(f"Error en POST /promotions/create: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/update/{promotion_id}", tags=["Promociones"])
async def update_promotion(promotion_id: str, promotion: PromotionDTO):
    """Actualiza una promoción en la plataforma."""
    try:
        # 🔹 Convertir fechas antes de actualizar
        promotion_data = promotion.dict()
        promotion_data["start_date"] = datetime.strptime(promotion.start_date, "%Y-%m-%d")
        promotion_data["end_date"] = datetime.strptime(promotion.end_date, "%Y-%m-%d")

        return await PromotionService.update_promotion(promotion_id, promotion_data)
    except Exception as e:
        logger.error(f"Error en PUT /promotions/update/{promotion_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/delete/{promotion_id}", tags=["Promociones"])
async def delete_promotion(promotion_id: str):
    """Elimina una promoción por su ID."""
    try:
        return await PromotionService.delete_promotion(promotion_id)
    except Exception as e:
        logger.error(f"Error en DELETE /promotions/delete/{promotion_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
