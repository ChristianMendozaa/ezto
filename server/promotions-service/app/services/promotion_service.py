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
            # 🔹 Validar los datos antes de enviarlos al repositorio
            if not isinstance(promotion, PromotionDTO):
                raise ValidationError("Los datos enviados no son válidos", PromotionDTO)

            created_promotion = await PromotionRepository.create_promotion(promotion)
            if created_promotion["status"] == "error":
                return ErrorResponse(message="Error al crear la promoción", errors=[created_promotion["message"]], status_code=400)

            return SuccessResponse(message="Promoción creada exitosamente", data=created_promotion)
        
        except ValidationError as ve:
            logger.error(f"❌ ValidationError en create_promotion: {ve.errors()}")
            return ErrorResponse(message="Error de validación", errors=[str(ve)], status_code=422)
        
        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en create_promotion: {str(fe)}")
            return ErrorResponse(message="Error en la base de datos", errors=[str(fe)], status_code=500)
        
        except Exception as e:
            logger.error(f"❌ Error inesperado en create_promotion: {str(e)}")
            return ErrorResponse(message="Error inesperado al registrar la promoción", errors=[str(e)], status_code=500)

    @staticmethod
    async def get_all_promotions():
        try:
            promotions = await PromotionRepository.get_all_promotions()
            if promotions["status"] == "error":
                return ErrorResponse(message="Error al obtener promociones", errors=[promotions["message"]], status_code=500)

            return SuccessResponse(data=promotions)
        
        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en get_all_promotions: {str(fe)}")
            return ErrorResponse(message="Error en la base de datos", errors=[str(fe)], status_code=500)
        
        except Exception as e:
            logger.error(f"❌ Error inesperado en get_all_promotions: {str(e)}")
            return ErrorResponse(message="Error inesperado al obtener promociones", errors=[str(e)], status_code=500)

    @staticmethod
    async def update_promotion(promotion_id: str, promotion: PromotionDTO):
        try:
            # 🔹 Validar los datos antes de actualizar
            if not isinstance(promotion, PromotionDTO):
                raise ValidationError("Los datos enviados no son válidos", PromotionDTO)

            updated_promotion = await PromotionRepository.update_promotion(promotion_id, promotion)

            if updated_promotion["status"] == "error":
                return ErrorResponse(message="Error al actualizar la promoción", errors=[updated_promotion["message"]], status_code=400)

            return SuccessResponse(message="Promoción actualizada exitosamente", data=updated_promotion)

        except ValidationError as ve:
            logger.error(f"❌ ValidationError en update_promotion: {ve.errors()}")
            return ErrorResponse(message="Error de validación", errors=[str(ve)], status_code=422)

        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en update_promotion: {str(fe)}")
            return ErrorResponse(message="Error en la base de datos", errors=[str(fe)], status_code=500)

        except Exception as e:
            logger.error(f"❌ Error inesperado en update_promotion: {str(e)}")
            return ErrorResponse(message="Error inesperado al actualizar la promoción", errors=[str(e)], status_code=500)

    @staticmethod
    async def delete_promotion(promotion_id: str):
        try:
            response = await PromotionRepository.delete_promotion(promotion_id)
            
            if response["status"] == "error":
                return ErrorResponse(message="Promoción no encontrada", errors=["ID inválido"], status_code=404)

            return SuccessResponse(message="Promoción eliminada exitosamente")

        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en delete_promotion: {str(fe)}")
            return ErrorResponse(message="Error en la base de datos", errors=[str(fe)], status_code=500)

        except Exception as e:
            logger.error(f"❌ Error inesperado en delete_promotion: {str(e)}")
            return ErrorResponse(message="Error inesperado al eliminar la promoción", errors=[str(e)], status_code=500)

    @staticmethod
    async def get_promotion_by_id(promotion_id: str):
        try:
            promotion = await PromotionRepository.get_promotion_by_id(promotion_id)

            if promotion["status"] == "error":
                return ErrorResponse(
                    message="Promoción no encontrada",
                    errors=[promotion["message"]],
                    status_code=404
                )

            return SuccessResponse(
                message="Promoción encontrada",
            )

        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en get_promotion_by_id: {str(fe)}")
            return ErrorResponse(
                message="Error en la base de datos",
                errors=[str(fe)],
                status_code=500
            )

        except Exception as e:
            logger.error(f"❌ Error inesperado en get_promotion_by_id: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al obtener la promoción",
                errors=[str(e)],
                status_code=500
            )
