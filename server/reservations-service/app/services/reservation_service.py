from app.models.dtos.reservation_dto import ReservationDTO
from app.repositories.reservation_repository import ReservationRepository
from app.utils.response_standardization import SuccessResponse, ErrorResponse
from firebase_admin.exceptions import FirebaseError
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

class ReservationService:

    @staticmethod
    async def create_reservation(reservation_dto: ReservationDTO):
        try:
            entity = reservation_dto.to_entity()
            created = await ReservationRepository.create_reservation(entity)

            if created["status"] == "error":
                return ErrorResponse("Error al crear la reserva", [created["message"]], 400)

            return SuccessResponse("Reserva creada exitosamente", created["data"])

        except ValidationError as ve:
            logger.error(f"❌ ValidationError en create_reservation: {ve.errors()}")
            return ErrorResponse("Error de validación", [str(ve)], 422)

        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en create_reservation: {str(fe)}")
            return ErrorResponse("Error en la base de datos", [str(fe)], 500)

        except Exception as e:
            logger.error(f"❌ Error inesperado en create_reservation: {str(e)}")
            return ErrorResponse("Error inesperado al crear reserva", [str(e)], 500)

    @staticmethod
    async def get_all_reservations():
        result = await ReservationRepository.get_all_reservations()
        if result["status"] == "error":
            return ErrorResponse("Error al obtener reservas", [result["message"]], 500)

        return SuccessResponse(data=result["data"])

    @staticmethod
    async def get_reservation_by_id(reservation_id: str):
        result = await ReservationRepository.get_reservation_by_id(reservation_id)
        if result["status"] == "error":
            return ErrorResponse("Reserva no encontrada", [result["message"]], 404)

        return SuccessResponse("Reserva encontrada", result["data"])

    @staticmethod
    async def delete_reservation(reservation_id: str):
        result = await ReservationRepository.delete_reservation(reservation_id)
        if result["status"] == "error":
            return ErrorResponse("Reserva no encontrada", [result["message"]], 404)

        return SuccessResponse("Reserva eliminada exitosamente")

    @staticmethod
    async def update_reservation_partial(reservation_id: str, updates: dict):
        result = await ReservationRepository.update_reservation_partial(reservation_id, updates)
        if result["status"] == "error":
            return ErrorResponse("Error al actualizar reserva", [result["message"]], 400)

        return SuccessResponse("Reserva actualizada exitosamente", result["data"])
