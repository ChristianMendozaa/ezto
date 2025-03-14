from app.models.dtos.promotion_dto import PromotionDTO
from app.repositories.promotion_repository import PromotionRepository
from app.utils.response_standardization import SuccessResponse, ErrorResponse

class PromotionService:
    
    @staticmethod
    async def create_promotion(promotion: PromotionDTO):
        try:
            created_promotion = await PromotionRepository.create_promotion(promotion)
            return SuccessResponse(message="Promoción creada exitosamente", data=created_promotion)
        except Exception as e:
            return ErrorResponse(message="Error registrando la promoción", errors=[str(e)])

    @staticmethod
    async def get_all_promotions():
        try:
            promotions = await PromotionRepository.get_all_promotions()
            return SuccessResponse(data=promotions)
        except Exception as e:
            return ErrorResponse(message="Error obteniendo promociones", errors=[str(e)])
    
    @staticmethod
    async def update_promotion(promotion_id: str, promotion: PromotionDTO):
        try:
            updated_promotion = await PromotionRepository.update_promotion(promotion_id, promotion)
            return SuccessResponse(message="Promoción actualizada exitosamente", data=updated_promotion)
        except Exception as e:
            return ErrorResponse(message="Error actualizando la promoción", errors=[str(e)])
    
    @staticmethod
    async def delete_promotion(promotion_id: str):
        try:
            await PromotionRepository.delete_promotion(promotion_id)
            return SuccessResponse(message="Promoción eliminada exitosamente")
        except Exception as e:
            return ErrorResponse(message="Error eliminando la promoción", errors=[str(e)])
