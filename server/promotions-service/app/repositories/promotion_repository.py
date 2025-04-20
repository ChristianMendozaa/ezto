from firebase_admin import firestore
from app.models.promotion_model import PromotionEntity
from datetime import datetime
from app.utils.firebase_config import db
import asyncio
import logging

logger = logging.getLogger(__name__)

class PromotionRepository:

    @staticmethod
    async def create_promotion(entity: PromotionEntity):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("promotions").document()

            entity.id = ref.id
            data = entity.to_dict()

            await loop.run_in_executor(None, lambda: ref.set(data))
            return {
                "status": "success",
                "data": data
            }

        except Exception as e:
            logger.error(f"❌ Error creando promoción: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    async def get_all_promotions():
        try:
            loop = asyncio.get_running_loop()
            docs = await loop.run_in_executor(None, lambda: list(db.collection("promotions").stream()))
            promotions = [doc.to_dict() for doc in docs]

            return {"status": "success", "data": promotions}

        except Exception as e:
            logger.error(f"❌ Error obteniendo promociones: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def get_promotion_by_id(promotion_id: str):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("promotions").document(promotion_id)

            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Promoción no encontrada"}

            data = doc.to_dict()
            return {"status": "success", "data": data}

        except Exception as e:
            logger.error(f"❌ Error obteniendo promoción: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def delete_promotion(promotion_id: str):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("promotions").document(promotion_id)

            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Promoción no encontrada"}

            await loop.run_in_executor(None, lambda: ref.delete())
            return {"status": "success"}

        except Exception as e:
            logger.error(f"❌ Error eliminando promoción: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def update_promotion(promotion_id: str, entity: PromotionEntity):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("promotions").document(promotion_id)

            data = entity.to_dict()
            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Promoción no encontrada"}

            await loop.run_in_executor(None, lambda: ref.update(data))

            updated = await loop.run_in_executor(None, lambda: ref.get())
            return {
                "status": "success",
                "data": updated.to_dict()
            }

        except Exception as e:
            logger.error(f"❌ Error actualizando promoción: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def update_promotion_partial(promotion_id: str, updates: dict):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("promotions").document(promotion_id)

            # 🔍 Obtener documento actual
            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Promoción no encontrada"}

            current_data = doc.to_dict()

            # 🔁 Preparar fechas
            start_date = updates.get("start_date")
            end_date = updates.get("end_date")

            if start_date:
                if isinstance(start_date, str):
                    start_date = datetime.fromisoformat(start_date).date()
                elif isinstance(start_date, datetime):
                    start_date = start_date.date()
                updates["start_date"] = start_date.isoformat()
            else:
                start_date = datetime.fromisoformat(current_data.get("start_date")).date()

            if end_date:
                if isinstance(end_date, str):
                    end_date = datetime.fromisoformat(end_date).date()
                elif isinstance(end_date, datetime):
                    end_date = end_date.date()
                updates["end_date"] = end_date.isoformat()
            else:
                end_date = datetime.fromisoformat(current_data.get("end_date")).date()

            # ✅ Validar orden de fechas
            if end_date <= start_date:
                return {
                    "status": "error",
                    "message": "La fecha de finalización debe ser posterior a la fecha de inicio"
                }

            # 🔄 Aplicar actualización
            await loop.run_in_executor(None, lambda: ref.update(updates))

            updated = await loop.run_in_executor(None, lambda: ref.get())
            return {
                "status": "success",
                "data": updated.to_dict()
            }

        except Exception as e:
            logger.error(f"❌ Error actualizando promoción: {e}")
            return {"status": "error", "message": str(e)}
