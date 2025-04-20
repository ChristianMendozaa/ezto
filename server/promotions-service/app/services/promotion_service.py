from app.models.dtos.promotion_dto import PromotionDTO
from app.repositories.promotion_repository import PromotionRepository
from app.utils.response_standardization import SuccessResponse, ErrorResponse
from firebase_admin.exceptions import FirebaseError
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

class PromotionService:

    @staticmethod
    async def create_promotion(promotion: PromotionDTO):
        try:
            entity = promotion.to_entity()
            created = await PromotionRepository.create_promotion(entity)

            if created["status"] == "error":
                return ErrorResponse(
                    message="Error al crear la promoción",
                    errors=[created["message"]],
                    status_code=400
                )
            return SuccessResponse(message="Promoción creada exitosamente", data=created["data"])

        except ValidationError as ve:
            logger.error(f"❌ ValidationError en create_promotion: {ve.errors()}")
            return ErrorResponse(message="Error de validación", errors=[str(ve)], status_code=422)

        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en create_promotion: {str(fe)}")
            return ErrorResponse(message="Error en la base de datos", errors=[str(fe)], status_code=500)

        except Exception as e:
            logger.error(f"❌ Error inesperado en create_promotion: {str(e)}")
            return ErrorResponse(message="Error inesperado al crear promoción", errors=[str(e)], status_code=500)

    @staticmethod
    async def get_all_promotions():
        try:
            result = await PromotionRepository.get_all_promotions()
            if result["status"] == "error":
                return ErrorResponse(message="Error al obtener promociones", errors=[result["message"]], status_code=500)

            return SuccessResponse(data=result["data"])

        except Exception as e:
            logger.error(f"❌ Error inesperado en get_all_promotions: {str(e)}")
            return ErrorResponse(message="Error inesperado al obtener promociones", errors=[str(e)], status_code=500)

    @staticmethod
    async def get_promotion_by_id(promotion_id: str):
        try:
            result = await PromotionRepository.get_promotion_by_id(promotion_id)

            if result["status"] == "error":
                return ErrorResponse(message="Promoción no encontrada", errors=[result["message"]], status_code=404)

            return SuccessResponse(message="Promoción encontrada", data=result["data"])

        except Exception as e:
            logger.error(f"❌ Error inesperado en get_promotion_by_id: {str(e)}")
            return ErrorResponse(message="Error inesperado al obtener promoción", errors=[str(e)], status_code=500)

    @staticmethod
    async def delete_promotion(promotion_id: str):
        try:
            result = await PromotionRepository.delete_promotion(promotion_id)

            if result["status"] == "error":
                return ErrorResponse(message="Promoción no encontrada", errors=[result["message"]], status_code=404)

            return SuccessResponse(message="Promoción eliminada exitosamente")

        except Exception as e:
            logger.error(f"❌ Error inesperado en delete_promotion: {str(e)}")
            return ErrorResponse(message="Error inesperado al eliminar promoción", errors=[str(e)], status_code=500)

    @staticmethod
    async def update_promotion(promotion_id: str, promotion: PromotionDTO):
        try:
            entity = promotion.to_entity(promotion_id)
            result = await PromotionRepository.update_promotion(promotion_id, entity)

            if result["status"] == "error":
                return ErrorResponse(message="Error al actualizar promoción", errors=[result["message"]], status_code=400)

            return SuccessResponse(message="Promoción actualizada exitosamente", data=result["data"])

        except ValidationError as ve:
            logger.error(f"❌ ValidationError en update_promotion: {ve.errors()}")
            return ErrorResponse(message="Error de validación", errors=[str(ve)], status_code=422)

        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en update_promotion: {str(fe)}")
            return ErrorResponse(message="Error en la base de datos", errors=[str(fe)], status_code=500)

        except Exception as e:
            logger.error(f"❌ Error inesperado en update_promotion: {str(e)}")
            return ErrorResponse(message="Error inesperado al actualizar promoción", errors=[str(e)], status_code=500)

    @staticmethod
    async def update_promotion_partial(promotion_id: str, updates: dict):
        try:
            result = await PromotionRepository.update_promotion_partial(promotion_id, updates)

            if result["status"] == "error":
                return ErrorResponse(message="Error al actualizar promoción", errors=[result["message"]], status_code=400)

            return SuccessResponse(message="Promoción actualizada exitosamente", data=result["data"])

        except Exception as e:
            logger.error(f"❌ Error inesperado en update_promotion_partial: {str(e)}")
            return ErrorResponse(message="Error inesperado al actualizar promoción", errors=[str(e)], status_code=500)
