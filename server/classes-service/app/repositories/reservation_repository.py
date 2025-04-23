# app/repositories/reservation_repository.py
from app.utils.firebase_config import db
import asyncio
from datetime import datetime

class ReservationRepository:
    @staticmethod
    async def create_reservation(reservation_data: dict):
        try:
            loop = asyncio.get_running_loop()
            reservation_ref = await loop.run_in_executor(
                None,
                lambda: db.collection("reservations").add({
                    **reservation_data,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                    "status": "confirmada"
                })
            )
            return reservation_ref.id
        except Exception as e:
            raise Exception(f"Error creando la reserva: {str(e)}")

    @staticmethod
    async def get_user_reservations(user_id: str):
        try:
            loop = asyncio.get_running_loop()
            reservations = await loop.run_in_executor(
                None,
                lambda: db.collection("reservations")
                    .where("user_id", "==", user_id)
                    .get()
            )
            return [doc.to_dict() for doc in reservations]
        except Exception as e:
            raise Exception(f"Error obteniendo las reservas: {str(e)}")