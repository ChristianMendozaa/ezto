# app/services/membership_service.py

from app.models.dtos.membership_plan_dto import MembershipPlanDTO
from app.repositories.membership_repository import MembershipRepository
from app.utils.response_standardization import SuccessResponse, ErrorResponse
from firebase_admin.exceptions import FirebaseError
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

class MembershipService:

    @staticmethod
    async def create_membership(plan: MembershipPlanDTO):
        """
        Crea un nuevo plan de membresía y maneja errores de validación y base de datos.
        """
        try:
            entity = plan.to_entity()
            created = await MembershipRepository.create_membership(entity)

            if created["status"] == "error":
                return ErrorResponse(
                    message="Error al crear el plan de membresía",  
                    errors=[created["message"]],
                    status_code=400
                )
            return SuccessResponse(
                message="Plan de membresía creado exitosamente",
                data=created["data"]
            )

        except ValidationError as ve:
            logger.error(f"❌ ValidationError en create_membership: {ve.errors()}")
            return ErrorResponse(
                message="Error de validación",  
                errors=[str(ve)],
                status_code=422
            )

        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en create_membership: {str(fe)}")
            return ErrorResponse(
                message="Error en la base de datos",  
                errors=[str(fe)],
                status_code=500
            )

        except Exception as e:
            logger.error(f"❌ Error inesperado en create_membership: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al crear plan de membresía",  
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def get_all_memberships():
        """
        Recupera todos los planes de membresía.
        """
        try:
            result = await MembershipRepository.get_all_memberships()
            if result["status"] == "error":
                return ErrorResponse(
                    message="Error al obtener planes de membresía",
                    errors=[result["message"]],
                    status_code=500
                )

            return SuccessResponse(data=result["data"])

        except Exception as e:
            logger.error(f"❌ Error inesperado en get_all_memberships: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al obtener planes de membresía",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def get_membership_by_id(plan_id: str):
        """
        Recupera un plan de membresía por su ID.
        """
        try:
            result = await MembershipRepository.get_membership_by_id(plan_id)

            if result["status"] == "error":
                return ErrorResponse(
                    message="Plan de membresía no encontrado",
                    errors=[result["message"]],
                    status_code=404
                )

            return SuccessResponse(
                message="Plan de membresía encontrado",
                data=result["data"]
            )

        except Exception as e:
            logger.error(f"❌ Error inesperado en get_membership_by_id: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al obtener plan de membresía",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def delete_membership(plan_id: str):
        """
        Elimina un plan de membresía por su ID.
        """
        try:
            result = await MembershipRepository.delete_membership(plan_id)

            if result["status"] == "error":
                return ErrorResponse(
                    message="Plan de membresía no encontrado",
                    errors=[result["message"]],
                    status_code=404
                )

            return SuccessResponse(message="Plan de membresía eliminado exitosamente")

        except Exception as e:
            logger.error(f"❌ Error inesperado en delete_membership: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al eliminar plan de membresía",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def update_membership(plan_id: str, plan: MembershipPlanDTO):
        """
        Reemplaza completamente un plan de membresía.
        """
        try:
            entity = plan.to_entity(plan_id)
            result = await MembershipRepository.update_membership(plan_id, entity)

            if result["status"] == "error":
                return ErrorResponse(
                    message="Error al actualizar plan de membresía",
                    errors=[result["message"]],
                    status_code=400
                )

            return SuccessResponse(
                message="Plan de membresía actualizado exitosamente",
                data=result["data"]
            )

        except ValidationError as ve:
            logger.error(f"❌ ValidationError en update_membership: {ve.errors()}")
            return ErrorResponse(
                message="Error de validación",
                errors=[str(ve)],
                status_code=422
            )

        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en update_membership: {str(fe)}")
            return ErrorResponse(
                message="Error en la base de datos",
                errors=[str(fe)],
                status_code=500
            )

        except Exception as e:
            logger.error(f"❌ Error inesperado en update_membership: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al actualizar plan de membresía",
                errors=[str(e)],
                status_code=500
            )

    @staticmethod
    async def update_membership_partial(plan_id: str, updates: dict):
        """
        Actualiza parcialmente campos de un plan de membresía.
        """
        try:
            result = await MembershipRepository.update_membership_partial(plan_id, updates)

            if result["status"] == "error":
                return ErrorResponse(
                    message="Error al actualizar plan de membresía",
                    errors=[result["message"]],
                    status_code=400
                )

            return SuccessResponse(
                message="Plan de membresía actualizado exitosamente",
                data=result["data"]
            )

        except Exception as e:
            logger.error(f"❌ Error inesperado en update_membership_partial: {str(e)}")
            return ErrorResponse(
                message="Error inesperado al actualizar plan de membresía",
                errors=[str(e)],
                status_code=500
            )
