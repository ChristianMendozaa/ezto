from firebase_admin import firestore
from app.models.dtos.promotion_dto import PromotionDTO
from app.utils.firebase_config import db
from app.utils.responses import StandardResponse, PromotionsResponse
import asyncio
import logging
from datetime import datetime
from datetime import date
from firebase_admin.exceptions import FirebaseError

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class PromotionRepository:
    @staticmethod
    async def create_promotion(promotion: PromotionDTO):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("promotions").document()

            # Convertir DTO a diccionario correctamente
            promotion_data = promotion.model_dump()

            # Agregar ID generado por Firestore
            promotion_data["id"] = ref.id

            # Convertir fechas a formato ISO-8601 antes de enviarlas a Firestore
            if isinstance(promotion_data["start_date"], (datetime, date)):
                promotion_data["start_date"] = promotion_data["start_date"].isoformat()
            if isinstance(promotion_data["end_date"], (datetime, date)):
                promotion_data["end_date"] = promotion_data["end_date"].isoformat()


            # Eliminar claves con valores `None`
            promotion_data = {k: v for k, v in promotion_data.items() if v is not None}

            # Guardar en Firestore
            await loop.run_in_executor(None, lambda: ref.set(promotion_data))

            return StandardResponse(
                status="success",
                message="Promoción creada exitosamente",
                data=promotion_data if promotion_data else None
            ).model_dump(exclude_none=True)

        except FirebaseError as e:
            logger.error(f"❌ Firebase Error: {str(e)}")
            return StandardResponse(status="error", message="Error al conectar con Firestore.").model_dump()
        except Exception as e:
            logger.error(f"❌ Error registrando promoción: {str(e)}")
            return StandardResponse(status="error", message=f"Error registrando la promoción: {str(e)}").model_dump()

    @staticmethod
    @staticmethod
    async def get_all_promotions():
        try:
            loop = asyncio.get_running_loop()
            docs = await loop.run_in_executor(None, lambda: db.collection("promotions").stream())

            promotions = [PromotionDTO(**doc.to_dict()) for doc in docs]

            if not promotions:
                return PromotionsResponse(status="success", message="No hay promociones registradas.", promotions=[]).model_dump()

            return PromotionsResponse(status="success", promotions=promotions).model_dump()

        except Exception as e:
            return PromotionsResponse(status="error", message=f"Error obteniendo promociones: {str(e)}").model_dump()


    @staticmethod
    async def update_promotion(promotion_id: str, promotion: PromotionDTO):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("promotions").document(promotion_id)

            # Convertir DTO a diccionario correctamente
            promotion_data = promotion.model_dump()

            # Convertir fechas a formato ISO-8601
            if "start_date" in promotion_data and promotion_data["start_date"]:
                promotion_data["start_date"] = promotion_data["start_date"].isoformat()
            if "end_date" in promotion_data and promotion_data["end_date"]:
                promotion_data["end_date"] = promotion_data["end_date"].isoformat()

            # Eliminar claves con valores `None`
            promotion_data = {k: v for k, v in promotion_data.items() if v is not None}

            # Validar si la promoción existe antes de actualizar
            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return StandardResponse(status="error", message="La promoción no existe.").model_dump()

            await loop.run_in_executor(None, lambda: ref.update(promotion_data))

            return StandardResponse(
                status="success",
                message="Promoción actualizada exitosamente",
                data=promotion_data if promotion_data else None
            ).model_dump(exclude_none=True)

        except FirebaseError as e:
            logger.error(f"❌ Firebase Error: {str(e)}")
            return StandardResponse(status="error", message="Error al conectar con Firestore.").model_dump()
        except Exception as e:
            logger.error(f"❌ Error actualizando la promoción: {str(e)}")
            return StandardResponse(status="error", message=f"Error actualizando la promoción: {str(e)}").model_dump()

    @staticmethod
    async def delete_promotion(promotion_id: str):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("promotions").document(promotion_id)

            # Validar si la promoción existe antes de eliminar
            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return StandardResponse(status="error", message="La promoción no existe.").model_dump()

            await loop.run_in_executor(None, lambda: ref.delete())

            return StandardResponse(status="success", message="Promoción eliminada exitosamente").model_dump()

        except FirebaseError as e:
            logger.error(f"❌ Firebase Error: {str(e)}")
            return StandardResponse(status="error", message="Error al conectar con Firestore.").model_dump()
        except Exception as e:
            logger.error(f"❌ Error eliminando la promoción: {str(e)}")
            return StandardResponse(status="error", message=f"Error eliminando la promoción: {str(e)}").model_dump()
