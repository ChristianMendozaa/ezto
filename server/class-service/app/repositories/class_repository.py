from firebase_admin import firestore
from app.models.class_model import ClassEntity
from app.utils.firebase_config import db
import asyncio
import logging
from datetime import time
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

            # 1) Fetch existente
            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Clase no encontrada"}

            # 2) Filtrar solo campos permitidos
            allowed = {"name", "description", "instructor", "capacity", "location", "status", "sessions"}
            to_apply = {k: v for k, v in updates.items() if k in allowed}

            # 3) Si vienen 'sessions', validarlas
            if "sessions" in to_apply:
                raw = to_apply["sessions"]
                validated = []
                for sess in raw:
                    # Parsear y validar tiempos
                    st = time.fromisoformat(sess["start_time"])
                    et = time.fromisoformat(sess["end_time"])
                    if et <= st:
                        return {
                            "status": "error",
                            "message": f"En sesión {sess['day']}: end_time debe ser posterior a start_time"
                        }
                    validated.append({
                        "day": sess["day"],
                        "start_time": sess["start_time"],
                        "end_time": sess["end_time"]
                    })
                to_apply["sessions"] = validated

            # 4) Aplicar el update en Firestore
            await loop.run_in_executor(None, lambda: ref.update(to_apply))

            # 5) Leer documento actualizado y devolverlo
            updated = await loop.run_in_executor(None, lambda: ref.get())
            return {
                "status": "success",
                "data": updated.to_dict()
            }

        except Exception as e:
            logger.error(f"❌ Error actualizando parcialmente clase: {e}")
            return {"status": "error", "message": str(e)}
