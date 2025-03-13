from firebase_admin import firestore
from app.models.promotion_model import Promotion
from app.utils.firebase_config import db
import asyncio
from datetime import date
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class PromotionRepository:
    @staticmethod
    async def create_promotion(promotion: Promotion):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("promotions").document()
            promotion_data = promotion.dict()
            promotion_data["id"] = ref.id  # 🔹 Asigna el ID generado por Firestore
            
            # Ejecutar Firestore en un thread separado para evitar bloqueos
            await loop.run_in_executor(None, lambda: ref.set(promotion_data))
            
            return {"id": ref.id, **promotion_data}  # 🔹 Devuelve el ID
        except Exception as e:
            raise Exception(f"Error registrando la promoción en Firestore: {str(e)}")

    @staticmethod
    async def get_all_promotions():
        try:
            print("🔹 Obteniendo promociones desde Firestore...")  
            loop = asyncio.get_running_loop()
            docs = await loop.run_in_executor(None, lambda: db.collection("promotions").stream())  # ✅ Aquí usamos `await`
            promotions = [{"id": doc.id, **doc.to_dict()} for doc in docs]
            print(f"✅ Promociones obtenidas: {promotions}")  
            return promotions
        except Exception as e:
            print(f"❌ Error obteniendo promociones: {str(e)}")  
            raise Exception(f"Error obteniendo promociones: {str(e)}")


    
    @staticmethod
    async def update_promotion(promotion_id: str, promotion: Promotion):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("promotions").document(promotion_id)
            promotion_data = promotion.dict()
            
            # Convertir fechas a formato ISO-8601
            if isinstance(promotion.start_date, date):
                promotion_data["start_date"] = promotion.start_date.isoformat()
            if isinstance(promotion.end_date, date):
                promotion_data["end_date"] = promotion.end_date.isoformat()
            
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
