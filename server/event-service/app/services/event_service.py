from app.models.dtos.event_dto import EventDTO
from app.repositories.event_repository import EventRepository
from app.utils.response_standardization import SuccessResponse, ErrorResponse
from firebase_admin.exceptions import FirebaseError
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

class EventService:

    @staticmethod
    async def create_event(event_dto: EventDTO):
        try:
            entity = event_dto.to_entity()
            created = await EventRepository.create_event(entity)

            if created["status"] == "error":
                return ErrorResponse(
                    message="Error al crear el evento",
                    errors=[created["message"]],
                    status_code=400
                )

            return SuccessResponse(message="Evento creado exitosamente", data=created["data"])

        except ValidationError as ve:
            logger.error(f"❌ ValidationError en create_event: {ve.errors()}")
            return ErrorResponse(
                message="Error de validación",
                errors=[str(ve)],
                status_code=422
            )

        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en create_event: {str(fe)}")
            return ErrorResponse(
                message="Error en la base de datos",
                errors=[str(fe)],
                status_code=500
            )

        except Exception as e:
            logger.error(f"❌ Error inesperado en create_event: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al crear evento",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def get_all_events():
        try:
            result = await EventRepository.get_all_events()

            if result["status"] == "error":
                return ErrorResponse(
                    message="Error al obtener eventos",
                    errors=[result["message"]],
                    status_code=500
                )

            return SuccessResponse(data=result["data"])

        except Exception as e:
            logger.error(f"❌ Error inesperado en get_all_events: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al obtener eventos",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def get_event_by_id(event_id: str):
        try:
            result = await EventRepository.get_event_by_id(event_id)

            if result["status"] == "error":
                return ErrorResponse(
                    message="Evento no encontrado",
                    errors=[result["message"]],
                    status_code=404
                )

            return SuccessResponse(message="Evento encontrado", data=result["data"])

        except Exception as e:
            logger.error(f"❌ Error inesperado en get_event_by_id: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al obtener evento",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def delete_event(event_id: str):
        try:
            result = await EventRepository.delete_event(event_id)

            if result["status"] == "error":
                return ErrorResponse(
                    message="Evento no encontrado",
                    errors=[result["message"]],
                    status_code=404
                )

            return SuccessResponse(message="Evento eliminado exitosamente")

        except Exception as e:
            logger.error(f"❌ Error inesperado en delete_event: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al eliminar evento",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def update_event(event_id: str, event_dto: EventDTO):
        try:
            entity = event_dto.to_entity(event_id)
            result = await EventRepository.update_event(event_id, entity)

            if result["status"] == "error":
                return ErrorResponse(
                    message="Error al actualizar evento",
                    errors=[result["message"]],
                    status_code=400
                )

            return SuccessResponse(message="Evento actualizado exitosamente", data=result["data"])

        except ValidationError as ve:
            logger.error(f"❌ ValidationError en update_event: {ve.errors()}")
            return ErrorResponse(
                message="Error de validación",
                errors=[str(ve)],
                status_code=422
            )

        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en update_event: {str(fe)}")
            return ErrorResponse(
                message="Error en la base de datos",
                errors=[str(fe)],
                status_code=500
            )

        except Exception as e:
            logger.error(f"❌ Error inesperado en update_event: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al actualizar evento",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def update_event_partial(event_id: str, updates: dict):
        try:
            result = await EventRepository.update_event_partial(event_id, updates)

            if result["status"] == "error":
                return ErrorResponse(
                    message="Error al actualizar evento",
                    errors=[result["message"]],
                    status_code=400
                )

            return SuccessResponse(message="Evento actualizado exitosamente", data=result["data"])

        except Exception as e:
            logger.error(f"❌ Error inesperado en update_event_partial: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al actualizar evento",
                errors=[str(e)],
                status_code=500
            )