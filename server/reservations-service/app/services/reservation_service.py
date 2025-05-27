# app/services/reservation_service.py

from app.models.dtos.reservation_dto import ReservationDTO
from app.repositories.reservation_repository import ReservationRepository
from app.utils.response_standardization import SuccessResponse, ErrorResponse
from firebase_admin.exceptions import FirebaseError
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

class ReservationService:

    @staticmethod
    async def create_reservation(reservation: ReservationDTO):
        try:
            entity = reservation.to_entity()
            created = await ReservationRepository.create_reservation(entity)

            if created["status"] == "error":
                return ErrorResponse(
                    message="Error al crear la reserva",
                    errors=[created["message"]],
                    status_code=400
                )

            return SuccessResponse(
                message="Reserva creada exitosamente",
                data=created["data"]
            )

        except ValidationError as ve:
            logger.error(f"❌ ValidationError en create_reservation: {ve.errors()}")
            return ErrorResponse(
                message="Error de validación",
                errors=[str(ve)],
                status_code=422
            )

        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en create_reservation: {fe}")
            return ErrorResponse(
                message="Error en la base de datos",
                errors=[str(fe)],
                status_code=500
            )

        except Exception as e:
            logger.error(f"❌ Error inesperado en create_reservation: {e}")
            return ErrorResponse(
                message="Error inesperado al crear reserva",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def get_all_reservations():
        try:
            result = await ReservationRepository.get_all_reservations()
            if result["status"] == "error":
                return ErrorResponse(
                    message="Error al obtener reservas",
                    errors=[result["message"]],
                    status_code=500
                )
            return SuccessResponse(data=result["data"])
        except Exception as e:
            logger.error(f"❌ Error inesperado en get_all_reservations: {e}")
            return ErrorResponse(
                message="Error inesperado al obtener reservas",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def get_reservation_by_id(reservation_id: str):
        try:
            result = await ReservationRepository.get_reservation_by_id(reservation_id)
            if result["status"] == "error":
                return ErrorResponse(
                    message="Reserva no encontrada",
                    errors=[result["message"]],
                    status_code=404
                )
            return SuccessResponse(
                message="Reserva encontrada",
                data=result["data"]
            )
        except Exception as e:
            logger.error(f"❌ Error inesperado en get_reservation_by_id: {e}")
            return ErrorResponse(
                message="Error inesperado al obtener reserva",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def delete_reservation(reservation_id: str):
        try:
            result = await ReservationRepository.delete_reservation(reservation_id)
            if result["status"] == "error":
                return ErrorResponse(
                    message="Reserva no encontrada",
                    errors=[result["message"]],
                    status_code=404
                )
            return SuccessResponse(message="Reserva eliminada exitosamente")
        except Exception as e:
            logger.error(f"❌ Error inesperado en delete_reservation: {e}")
            return ErrorResponse(
                message="Error inesperado al eliminar reserva",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def update_reservation(reservation_id: str, reservation: ReservationDTO):
        try:
            entity = reservation.to_entity(reservation_id)
            result = await ReservationRepository.update_reservation(reservation_id, entity)
            if result["status"] == "error":
                return ErrorResponse(
                    message="Error al actualizar reserva",
                    errors=[result["message"]],
                    status_code=400
                )
            return SuccessResponse(
                message="Reserva actualizada exitosamente",
                data=result["data"]
            )
        except ValidationError as ve:
            logger.error(f"❌ ValidationError en update_reservation: {ve.errors()}")
            return ErrorResponse(
                message="Error de validación",
                errors=[str(ve)],
                status_code=422
            )
        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en update_reservation: {fe}")
            return ErrorResponse(
                message="Error en la base de datos",
                errors=[str(fe)],
                status_code=500
            )
        except Exception as e:
            logger.error(f"❌ Error inesperado en update_reservation: {e}")
            return ErrorResponse(
                message="Error inesperado al actualizar reserva",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def update_reservation_partial(reservation_id: str, updates: dict):
        try:
            result = await ReservationRepository.update_reservation_partial(reservation_id, updates)
            if result["status"] == "error":
                return ErrorResponse(
                    message="Error al actualizar reserva",
                    errors=[result["message"]],
                    status_code=400
                )
            return SuccessResponse(
                message="Reserva actualizada exitosamente",
                data=result["data"]
            )
        except Exception as e:
            logger.error(f"❌ Error inesperado en update_reservation_partial: {e}")
            return ErrorResponse(
                message="Error inesperado al actualizar reserva",
                errors=[str(e)],
                status_code=500
            )
