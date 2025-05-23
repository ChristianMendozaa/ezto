from firebase_admin import firestore
from app.models.event_model import EventEntity
from app.utils.firebase_config import db
import asyncio
import logging
from datetime import datetime
logger = logging.getLogger(__name__)

class EventRepository:

    COLLECTION_NAME = "events"

    @staticmethod
    async def create_event(entity: EventEntity):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection(EventRepository.COLLECTION_NAME).document()
            entity.id = ref.id
            data = entity.to_dict()
            await loop.run_in_executor(None, lambda: ref.set(data))
            return {
                "status": "success",
                "data": data
            }

        except Exception as e:
            logger.error(f"❌ Error creando evento: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    async def get_all_events():
        try:
            loop = asyncio.get_running_loop()
            docs = await loop.run_in_executor(None, lambda: list(db.collection(EventRepository.COLLECTION_NAME).stream()))
            events = [doc.to_dict() for doc in docs]
            return {"status": "success", "data": events}

        except Exception as e:
            logger.error(f"❌ Error obteniendo eventos: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def get_event_by_id(event_id: str):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection(EventRepository.COLLECTION_NAME).document(event_id)
            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Evento no encontrado"}
            return {"status": "success", "data": doc.to_dict()}

        except Exception as e:
            logger.error(f"❌ Error obteniendo evento: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def delete_event(event_id: str):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection(EventRepository.COLLECTION_NAME).document(event_id)
            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Evento no encontrado"}

            await loop.run_in_executor(None, lambda: ref.delete())
            return {"status": "success"}

        except Exception as e:
            logger.error(f"❌ Error eliminando evento: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def update_event(event_id: str, entity: EventEntity):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection(EventRepository.COLLECTION_NAME).document(event_id)
            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Evento no encontrado"}

            data = entity.to_dict()
            await loop.run_in_executor(None, lambda: ref.update(data))

            updated_doc = await loop.run_in_executor(None, lambda: ref.get())
            return {
                "status": "success",
                "data": updated_doc.to_dict()
            }

        except Exception as e:
            logger.error(f"❌ Error actualizando evento: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def update_event_partial(event_id: str, updates: dict):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection(EventRepository.COLLECTION_NAME).document(event_id)
            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Evento no encontrado"}

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
            logger.error(f"❌ Error actualizando parcialmente evento: {e}")
            return {"status": "error", "message": str(e)}