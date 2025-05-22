from app.models.reservation_model import ReservationEntity
from app.utils.firebase_config import db
import asyncio
import logging

logger = logging.getLogger(__name__)

class ReservationRepository:

    COLLECTION_NAME = "reservations"

    @staticmethod
    async def create_reservation(entity: ReservationEntity):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection(ReservationRepository.COLLECTION_NAME).document()
            entity.id = ref.id
            data = entity.to_dict()
            await loop.run_in_executor(None, lambda: ref.set(data))
            return {"status": "success", "data": data}

        except Exception as e:
            logger.error(f"❌ Error creando reserva: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def get_all_reservations():
        try:
            loop = asyncio.get_running_loop()
            docs = await loop.run_in_executor(None, lambda: list(db.collection(ReservationRepository.COLLECTION_NAME).stream()))
            reservations = [doc.to_dict() for doc in docs]
            return {"status": "success", "data": reservations}

        except Exception as e:
            logger.error(f"❌ Error obteniendo reservas: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def get_reservation_by_id(reservation_id: str):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection(ReservationRepository.COLLECTION_NAME).document(reservation_id)
            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Reserva no encontrada"}

            return {"status": "success", "data": doc.to_dict()}

        except Exception as e:
            logger.error(f"❌ Error obteniendo reserva: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def delete_reservation(reservation_id: str):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection(ReservationRepository.COLLECTION_NAME).document(reservation_id)
            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Reserva no encontrada"}

            await loop.run_in_executor(None, lambda: ref.delete())
            return {"status": "success"}

        except Exception as e:
            logger.error(f"❌ Error eliminando reserva: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def update_reservation_partial(reservation_id: str, updates: dict):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection(ReservationRepository.COLLECTION_NAME).document(reservation_id)
            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Reserva no encontrada"}

            await loop.run_in_executor(None, lambda: ref.update(updates))
            updated_doc = await loop.run_in_executor(None, lambda: ref.get())
            return {"status": "success", "data": updated_doc.to_dict()}

        except Exception as e:
            logger.error(f"❌ Error actualizando parcialmente reserva: {e}")
            return {"status": "error", "message": str(e)}
