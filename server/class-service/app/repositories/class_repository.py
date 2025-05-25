from firebase_admin import firestore
from app.models.class_model import ClassEntity
from app.utils.firebase_config import db
import asyncio
import logging
from datetime import datetime
logger = logging.getLogger(__name__)

class ClassRepository:

    COLLECTION_NAME = "classes"

    @staticmethod
    async def create_class(entity: ClassEntity):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection(ClassRepository.COLLECTION_NAME).document()
            entity.id = ref.id
            data = entity.to_dict()
            await loop.run_in_executor(None, lambda: ref.set(data))
            return {
                "status": "success",
                "data": data
            }

        except Exception as e:
            logger.error(f"❌ Error creando clase: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    async def get_all_classes():
        try:
            loop = asyncio.get_running_loop()
            docs = await loop.run_in_executor(None, lambda: list(db.collection(ClassRepository.COLLECTION_NAME).stream()))
            classes = [doc.to_dict() for doc in docs]
            return {"status": "success", "data": classes}

        except Exception as e:
            logger.error(f"❌ Error obteniendo clases: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def get_class_by_id(class_id: str):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection(ClassRepository.COLLECTION_NAME).document(class_id)
            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Clase no encontrada"}
            return {"status": "success", "data": doc.to_dict()}

        except Exception as e:
            logger.error(f"❌ Error obteniendo clase: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def delete_class(class_id: str):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection(ClassRepository.COLLECTION_NAME).document(class_id)
            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Clase no encontrada"}

            await loop.run_in_executor(None, lambda: ref.delete())
            return {"status": "success"}

        except Exception as e:
            logger.error(f"❌ Error eliminando clase: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def update_class(class_id: str, entity: ClassEntity):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection(ClassRepository.COLLECTION_NAME).document(class_id)
            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Clase no encontrada"}

            data = entity.to_dict()
            await loop.run_in_executor(None, lambda: ref.update(data))

            updated_doc = await loop.run_in_executor(None, lambda: ref.get())
            return {
                "status": "success",
                "data": updated_doc.to_dict()
            }

        except Exception as e:
            logger.error(f"❌ Error actualizando clase: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def update_class_partial(class_id: str, updates: dict):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection(ClassRepository.COLLECTION_NAME).document(class_id)
            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Clase no encontrada"}

            current_data = doc.to_dict()

            # Validación de fechas
            start_time = updates.get("start_time", current_data["start_time"])
            end_time = updates.get("end_time", current_data["end_time"])

            start_time_dt = firestore.SERVER_TIMESTAMP if start_time == firestore.SERVER_TIMESTAMP else datetime.fromisoformat(start_time)
            end_time_dt = firestore.SERVER_TIMESTAMP if end_time == firestore.SERVER_TIMESTAMP else datetime.fromisoformat(end_time)

            if end_time_dt <= start_time_dt:
                return {
                    "status": "error",
                    "message": "La hora de fin debe ser posterior a la hora de inicio"
                }

            await loop.run_in_executor(None, lambda: ref.update(updates))

            updated_doc = await loop.run_in_executor(None, lambda: ref.get())
            return {
                "status": "success",
                "data": updated_doc.to_dict()
            }

        except Exception as e:
            logger.error(f"❌ Error actualizando parcialmente clase: {e}")
            return {"status": "error", "message": str(e)}
