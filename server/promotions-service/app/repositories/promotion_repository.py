from firebase_admin import firestore
from app.models.dtos.promotion_dto import PromotionDTO
from app.utils.firebase_config import db
import asyncio
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class PromotionRepository:
    @staticmethod
    async def create_promotion(promotion: PromotionDTO):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("promotions").document()

            # 🔹 Convertir el objeto DTO en un diccionario si aún no lo es
            promotion_data = promotion if isinstance(promotion, dict) else promotion.model_dump()

            # Agregar el ID generado por Firestore
            promotion_data["id"] = ref.id
            
            # 🔹 Convertir fechas a formato ISO-8601 antes de enviarlas a Firestore
            promotion_data["start_date"] = promotion_data["start_date"].isoformat()
            promotion_data["end_date"] = promotion_data["end_date"].isoformat()

            # Ejecutar Firestore en un thread separado para evitar bloqueos
            await loop.run_in_executor(None, lambda: ref.set(promotion_data))

            return {"id": ref.id, **promotion_data}
        except Exception as e:
            raise Exception(f"Error registrando la promoción en Firestore: {str(e)}")

    @staticmethod
    async def get_all_promotions():
        try:
            logger.debug("🔹 Obteniendo promociones desde Firestore...")  
            loop = asyncio.get_running_loop()
            docs = await loop.run_in_executor(None, lambda: db.collection("promotions").stream())

            # 🔹 Convertir documentos Firestore a listas de diccionarios
            promotions = [{"id": doc.id, **doc.to_dict()} for doc in docs]

            logger.debug(f"✅ Promociones obtenidas: {promotions}")  
            return promotions
        except Exception as e:
            logger.error(f"❌ Error obteniendo promociones: {str(e)}")  
            raise Exception(f"Error obteniendo promociones: {str(e)}")

    @staticmethod
    async def update_promotion(promotion_id: str, promotion: PromotionDTO):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("promotions").document(promotion_id)

            # 🔹 Convertir objeto DTO a diccionario si no lo es
            promotion_data = promotion if isinstance(promotion, dict) else promotion.model_dump()

            # Convertir fechas a formato ISO-8601
            if "start_date" in promotion_data:
                promotion_data["start_date"] = promotion_data["start_date"].isoformat()
            if "end_date" in promotion_data:
                promotion_data["end_date"] = promotion_data["end_date"].isoformat()

            await loop.run_in_executor(None, lambda: ref.update(promotion_data))

            return {"message": "Promoción actualizada exitosamente", "id": promotion_id}
        except Exception as e:
            raise Exception(f"Error actualizando la promoción: {str(e)}")

    @staticmethod
    async def delete_promotion(promotion_id: str):
        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, lambda: db.collection("promotions").document(promotion_id).delete())

            return {"message": "Promoción eliminada exitosamente", "id": promotion_id}
        except Exception as e:
            raise Exception(f"Error eliminando la promoción: {str(e)}")
