from fastapi import APIRouter, HTTPException
from app.models.promotion_model import Promotion
from app.services.promotion_service import PromotionService
from typing import List
import logging

router = APIRouter()

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@router.get("/", tags=["Promociones"])
async def list_promotions():
    """Obtiene la lista de todas las promociones disponibles."""
    logger.debug("Recibida petición GET /promotions/list")  # 🚀 Ver si la petición llega
    try:
        promotions = await PromotionService.get_all_promotions()  # ✅ CORRECTO
        logger.debug(f"Promociones obtenidas: {promotions}")  # 🚀 Ver si Firestore devuelve datos
        return [{"id": promo["id"], **promo} for promo in promotions]
    except Exception as e:
        logger.error(f"Error en GET /promotions/list: {str(e)}")  # ❌ Si algo falla
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/create",
    summary="Crear una nueva promoción",
    description="Registra una nueva promoción en la plataforma.",
    response_description="La promoción ha sido registrada exitosamente.",
    responses={
        200: {"description": "Promoción creada exitosamente"},
        400: {"description": "Error en los datos proporcionados"},
    },
    tags=["Promociones"]
)
async def create_promotion(promotion: Promotion):
    """Crea una nueva promoción en la plataforma."""
    try:
        return await PromotionService.create_promotion(promotion)
    except Exception as e:
        logger.error(f"Error en POST /promotions/create: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.put(
    "/update/{promotion_id}",
    summary="Actualizar una promoción",
    description="Actualiza los datos de una promoción existente.",
    tags=["Promociones"]
)
async def update_promotion(promotion_id: str, promotion: Promotion):
    """Actualiza una promoción en la plataforma."""
    try:
        return await PromotionService.update_promotion(promotion_id, promotion)
    except Exception as e:
        logger.error(f"Error en PUT /promotions/update/{promotion_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete(
    "/delete/{promotion_id}",
    summary="Eliminar una promoción",
    description="Elimina una promoción de la plataforma.",
    tags=["Promociones"]
)
async def delete_promotion(promotion_id: str):
    """Elimina una promoción por su ID."""
    try:
        return await PromotionService.delete_promotion(promotion_id)
    except Exception as e:
        logger.error(f"Error en DELETE /promotions/delete/{promotion_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
