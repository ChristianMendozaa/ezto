#app/services/usermembership_service.py
from app.models.dtos.UserMembershipDTO import UserMembershipDTO
from app.repositories.usermembership_repository import UserMembershipRepository
from app.utils.response_standardization import SuccessResponse, ErrorResponse
from firebase_admin.exceptions import FirebaseError
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

class UserMembershipService:

    @staticmethod
    async def create_membership(membership: UserMembershipDTO):
        try:
            entity = membership.to_entity()
            created = await UserMembershipRepository.create_membership(entity)

            if created["status"] == "error":
                return ErrorResponse(
                    message="Error al crear la membresía",
                    errors=[created["message"]],
                    status_code=400
                )
            return SuccessResponse(message="Membresía creada exitosamente", data=created["data"])

        except ValidationError as ve:
            logger.error(f"❌ ValidationError en create_membership: {ve.errors()}")
            return ErrorResponse(message="Error de validación", errors=[str(ve)], status_code=422)

        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en create_membership: {str(fe)}")
            return ErrorResponse(message="Error en la base de datos", errors=[str(fe)], status_code=500)

        except Exception as e:
            logger.error(f"❌ Error inesperado en create_membership: {str(e)}")
            return ErrorResponse(message="Error inesperado al crear membresía", errors=[str(e)], status_code=500)

    @staticmethod
    async def get_all_memberships():
        try:
            result = await UserMembershipRepository.get_all_memberships()
            if result["status"] == "error":
                return ErrorResponse(message="Error al obtener membresías", errors=[result["message"]], status_code=500)

            return SuccessResponse(data=result["data"])

        except Exception as e:
            logger.error(f"❌ Error inesperado en get_all_memberships: {str(e)}")
            return ErrorResponse(message="Error inesperado al obtener membresías", errors=[str(e)], status_code=500)

    @staticmethod
    async def get_membership_by_id(membership_id: str):
        try:
            result = await UserMembershipRepository.get_membership_by_id(membership_id)

            if result["status"] == "error":
                return ErrorResponse(message="Membresía no encontrada", errors=[result["message"]], status_code=404)

            return SuccessResponse(message="Membresía encontrada", data=result["data"])

        except Exception as e:
            logger.error(f"❌ Error inesperado en get_membership_by_id: {str(e)}")
            return ErrorResponse(message="Error inesperado al obtener membresía", errors=[str(e)], status_code=500)

    @staticmethod
    async def get_memberships_by_user(user_id: str):
        try:
            result = await UserMembershipRepository.get_memberships_by_user(user_id)

            if result["status"] == "error":
                return ErrorResponse(message="Error al buscar membresías del usuario", errors=[result["message"]], status_code=404)

            return SuccessResponse(message="Membresías encontradas", data=result["data"])

        except Exception as e:
            logger.error(f"❌ Error inesperado en get_memberships_by_user: {str(e)}")
            return ErrorResponse(message="Error inesperado al obtener membresías del usuario", errors=[str(e)], status_code=500)

    @staticmethod
    async def delete_membership(membership_id: str):
        try:
            result = await UserMembershipRepository.delete_membership(membership_id)

            if result["status"] == "error":
                return ErrorResponse(message="Membresía no encontrada", errors=[result["message"]], status_code=404)

            return SuccessResponse(message="Membresía eliminada exitosamente")

        except Exception as e:
            logger.error(f"❌ Error inesperado en delete_membership: {str(e)}")
            return ErrorResponse(message="Error inesperado al eliminar membresía", errors=[str(e)], status_code=500)

    @staticmethod
    async def update_membership_partial(membership_id: str, updates: dict):
        try:
            result = await UserMembershipRepository.update_membership_partial(membership_id, updates)

            if result["status"] == "error":
                return ErrorResponse(message="Error al actualizar membresía", errors=[result["message"]], status_code=400)

            return SuccessResponse(message="Membresía actualizada exitosamente", data=result["data"])

        except Exception as e:
            logger.error(f"❌ Error inesperado en update_membership_partial: {str(e)}")
            return ErrorResponse(message="Error inesperado al actualizar membresía", errors=[str(e)], status_code=500)
