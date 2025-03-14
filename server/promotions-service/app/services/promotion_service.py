from app.models.dtos.promotion_dto import PromotionDTO
from app.repositories.promotion_repository import PromotionRepository

class PromotionService:
    
    @staticmethod
    async def create_promotion(promotion: PromotionDTO):
        return await PromotionRepository.create_promotion(promotion)

    @staticmethod
    async def get_all_promotions():
        return await PromotionRepository.get_all_promotions()
    
    @staticmethod
    async def update_promotion(promotion_id: str, promotion: PromotionDTO):
        return await PromotionRepository.update_promotion(promotion_id, promotion)
    
    @staticmethod
    async def delete_promotion(promotion_id: str):
        return await PromotionRepository.delete_promotion(promotion_id)
