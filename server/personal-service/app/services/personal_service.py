# personal-service/app/services/personal_service.py

import logging
from typing import Dict
from pydantic import ValidationError
from firebase_admin.exceptions import FirebaseError

from app.models.dtos.personal_dto import PersonalDTO
from app.repositories.personal_repository import PersonalRepository
from app.utils.response_standardization import SuccessResponse, ErrorResponse

logger = logging.getLogger(__name__)


class PersonalService:

    @staticmethod
    async def create_personal(dto: PersonalDTO):
        try:
            entity = dto.to_entity()
            created = await PersonalRepository.create_personal(entity)

            if created["status"] == "error":
                return ErrorResponse(
                    message="Error al crear el registro de personal",
                    errors=[created["message"]],
                    status_code=400
                )

            return SuccessResponse(
                message="Personal creado exitosamente",
                data=created.get("data")
            )

        except ValidationError as ve:
            logger.error(f"❌ ValidationError en create_personal: {ve.errors()}")
            return ErrorResponse(
                message="Error de validación al crear personal",
                errors=[str(ve)],
                status_code=422
            )

        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en create_personal: {fe}")
            return ErrorResponse(
                message="Error en la base de datos al crear personal",
                errors=[str(fe)],
                status_code=500
            )

        except Exception as e:
            logger.error(f"❌ Error inesperado en create_personal: {e}", exc_info=True)
            return ErrorResponse(
                message="Error inesperado al crear personal",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def get_all_personal():
        try:
            result = await PersonalRepository.get_all_personal()
            if result["status"] == "error":
                return ErrorResponse(
                    message="Error al obtener la lista de personal",
                    errors=[result["message"]],
                    status_code=500
                )

            return SuccessResponse(data=result.get("data"))

        except Exception as e:
            logger.error(f"❌ Error inesperado en get_all_personal: {e}", exc_info=True)
            return ErrorResponse(
                message="Error inesperado al obtener personal",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def get_personal_by_id(personal_id: str):
        try:
            result = await PersonalRepository.get_personal_by_id(personal_id)
            if result["status"] == "error":
                return ErrorResponse(
                    message="Personal no encontrado",
                    errors=[result["message"]],
                    status_code=404
                )

            return SuccessResponse(
                message="Personal encontrado",
                data=result.get("data")
            )

        except Exception as e:
            logger.error(f"❌ Error inesperado en get_personal_by_id: {e}", exc_info=True)
            return ErrorResponse(
                message="Error inesperado al obtener personal",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def update_personal(personal_id: str, dto: PersonalDTO):
        try:
            entity = dto.to_entity()
            updated = await PersonalRepository.update_personal(personal_id, entity)

            if updated["status"] == "error":
                return ErrorResponse(
                    message="Error al actualizar personal",
                    errors=[updated["message"]],
                    status_code=400
                )

            return SuccessResponse(
                message="Personal actualizado exitosamente",
                data=updated.get("data")
            )

        except ValidationError as ve:
            logger.error(f"❌ ValidationError en update_personal: {ve.errors()}")
            return ErrorResponse(
                message="Error de validación al actualizar personal",
                errors=[str(ve)],
                status_code=422
            )

        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en update_personal: {fe}")
            return ErrorResponse(
                message="Error en la base de datos al actualizar personal",
                errors=[str(fe)],
                status_code=500
            )

        except Exception as e:
            logger.error(f"❌ Error inesperado en update_personal: {e}", exc_info=True)
            return ErrorResponse(
                message="Error inesperado al actualizar personal",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def update_personal_partial(personal_id: str, updates: Dict[str, any]):
        try:
            updated = await PersonalRepository.update_personal_partial(personal_id, updates)

            if updated["status"] == "error":
                return ErrorResponse(
                    message="Error al actualizar parcialmente personal",
                    errors=[updated["message"]],
                    status_code=400
                )

            return SuccessResponse(
                message="Personal actualizado exitosamente",
                data=updated.get("data")
            )

        except Exception as e:
            logger.error(f"❌ Error inesperado en update_personal_partial: {e}", exc_info=True)
            return ErrorResponse(
                message="Error inesperado al actualizar personal",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def delete_personal(personal_id: str):
        try:
            deleted = await PersonalRepository.delete_personal(personal_id)
            if deleted["status"] == "error":
                return ErrorResponse(
                    message="Personal no encontrado",
                    errors=[deleted["message"]],
                    status_code=404
                )

            return SuccessResponse(message="Personal eliminado exitosamente")

        except Exception as e:
            logger.error(f"❌ Error inesperado en delete_personal: {e}", exc_info=True)
            return ErrorResponse(
                message="Error inesperado al eliminar personal",
                errors=[str(e)],
                status_code=500
            )
