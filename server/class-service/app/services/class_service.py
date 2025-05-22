from app.models.dtos.class_dto import ClassDTO
from app.repositories.class_repository import ClassRepository
from app.utils.response_standardization import SuccessResponse, ErrorResponse
from firebase_admin.exceptions import FirebaseError
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

class ClassService:

    @staticmethod
    async def create_class(class_dto: ClassDTO):
        try:
            entity = class_dto.to_entity()
            created = await ClassRepository.create_class(entity)

            if created["status"] == "error":
                return ErrorResponse(
                    message="Error al crear la clase",
                    errors=[created["message"]],
                    status_code=400
                )

            return SuccessResponse(message="Clase creada exitosamente", data=created["data"])

        except ValidationError as ve:
            logger.error(f"❌ ValidationError en create_class: {ve.errors()}")
            return ErrorResponse(
                message="Error de validación",
                errors=[str(ve)],
                status_code=422
            )

        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en create_class: {str(fe)}")
            return ErrorResponse(
                message="Error en la base de datos",
                errors=[str(fe)],
                status_code=500
            )

        except Exception as e:
            logger.error(f"❌ Error inesperado en create_class: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al crear clase",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def get_all_classes():
        try:
            result = await ClassRepository.get_all_classes()

            if result["status"] == "error":
                return ErrorResponse(
                    message="Error al obtener clases",
                    errors=[result["message"]],
                    status_code=500
                )

            return SuccessResponse(data=result["data"])

        except Exception as e:
            logger.error(f"❌ Error inesperado en get_all_classes: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al obtener clases",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def get_class_by_id(class_id: str):
        try:
            result = await ClassRepository.get_class_by_id(class_id)

            if result["status"] == "error":
                return ErrorResponse(
                    message="Clase no encontrada",
                    errors=[result["message"]],
                    status_code=404
                )

            return SuccessResponse(message="Clase encontrada", data=result["data"])

        except Exception as e:
            logger.error(f"❌ Error inesperado en get_class_by_id: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al obtener clase",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def delete_class(class_id: str):
        try:
            result = await ClassRepository.delete_class(class_id)

            if result["status"] == "error":
                return ErrorResponse(
                    message="Clase no encontrada",
                    errors=[result["message"]],
                    status_code=404
                )

            return SuccessResponse(message="Clase eliminada exitosamente")

        except Exception as e:
            logger.error(f"❌ Error inesperado en delete_class: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al eliminar clase",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def update_class(class_id: str, class_dto: ClassDTO):
        try:
            entity = class_dto.to_entity(class_id)
            result = await ClassRepository.update_class(class_id, entity)

            if result["status"] == "error":
                return ErrorResponse(
                    message="Error al actualizar clase",
                    errors=[result["message"]],
                    status_code=400
                )

            return SuccessResponse(message="Clase actualizada exitosamente", data=result["data"])

        except ValidationError as ve:
            logger.error(f"❌ ValidationError en update_class: {ve.errors()}")
            return ErrorResponse(
                message="Error de validación",
                errors=[str(ve)],
                status_code=422
            )

        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en update_class: {str(fe)}")
            return ErrorResponse(
                message="Error en la base de datos",
                errors=[str(fe)],
                status_code=500
            )

        except Exception as e:
            logger.error(f"❌ Error inesperado en update_class: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al actualizar clase",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def update_class_partial(class_id: str, updates: dict):
        try:
            result = await ClassRepository.update_class_partial(class_id, updates)

            if result["status"] == "error":
                return ErrorResponse(
                    message="Error al actualizar clase",
                    errors=[result["message"]],
                    status_code=400
                )

            return SuccessResponse(message="Clase actualizada exitosamente", data=result["data"])

        except Exception as e:
            logger.error(f"❌ Error inesperado en update_class_partial: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al actualizar clase",
                errors=[str(e)],
                status_code=500
            )
