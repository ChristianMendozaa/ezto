from app.models.dtos.member_dto import MemberDTO
from app.repositories.member_repository import MemberRepository
from app.utils.response_standardization import SuccessResponse, ErrorResponse
from firebase_admin.exceptions import FirebaseError
from pydantic import ValidationError
import logging

logger = logging.getLogger(__name__)

class MemberService:

    @staticmethod
    async def create_member(member: MemberDTO):
        try:
            entity = member.to_entity()
            created = await MemberRepository.create_member(entity)

            if created["status"] == "error":
                return ErrorResponse(
                    message="Error al crear el miembro",
                    errors=[created["message"]],
                    status_code=400
                )
            return SuccessResponse(message="Miembro creado exitosamente", data=created["data"])

        except ValidationError as ve:
            logger.error(f"❌ ValidationError en create_member: {ve.errors()}")
            return ErrorResponse(message="Error de validación", errors=[str(ve)], status_code=422)

        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en create_member: {str(fe)}")
            return ErrorResponse(message="Error en la base de datos", errors=[str(fe)], status_code=500)

        except Exception as e:
            logger.error(f"❌ Error inesperado en create_member: {str(e)}")
            return ErrorResponse(message="Error inesperado al crear miembro", errors=[str(e)], status_code=500)

    @staticmethod
    async def get_all_members():
        try:
            result = await MemberRepository.get_all_members()
            if result["status"] == "error":
                return ErrorResponse(message="Error al obtener miembros", errors=[result["message"]], status_code=500)

            return SuccessResponse(data=result["data"])

        except Exception as e:
            logger.error(f"❌ Error inesperado en get_all_members: {str(e)}")
            return ErrorResponse(message="Error inesperado al obtener miembros", errors=[str(e)], status_code=500)

    @staticmethod
    async def get_member_by_id(member_id: str):
        try:
            result = await MemberRepository.get_member_by_id(member_id)

            if result["status"] == "error":
                return ErrorResponse(message="Miembro no encontrado", errors=[result["message"]], status_code=404)

            return SuccessResponse(message="Miembro encontrado", data=result["data"])

        except Exception as e:
            logger.error(f"❌ Error inesperado en get_member_by_id: {str(e)}")
            return ErrorResponse(message="Error inesperado al obtener miembro", errors=[str(e)], status_code=500)

    @staticmethod
    async def delete_member(member_id: str):
        try:
            result = await MemberRepository.delete_member(member_id)

            if result["status"] == "error":
                return ErrorResponse(message="Miembro no encontrado", errors=[result["message"]], status_code=404)

            return SuccessResponse(message="Miembro eliminado exitosamente")

        except Exception as e:
            logger.error(f"❌ Error inesperado en delete_member: {str(e)}")
            return ErrorResponse(message="Error inesperado al eliminar miembro", errors=[str(e)], status_code=500)

    @staticmethod
    async def update_member(member_id: str, updates: dict):
        try:
            # Reconstruimos el DTO a partir del dict plano
            member_dto = MemberDTO(id=member_id, **updates)

            # Convertimos a entidad y pasamos al repositorio
            entity = member_dto.to_entity()
            result = await MemberRepository.update_member(member_id, entity)

            if result["status"] == "error":
                return ErrorResponse(message="Error al actualizar miembro", errors=[result["message"]], status_code=400)

            return SuccessResponse(message="Miembro actualizado exitosamente", data=result["data"])

        except ValidationError as ve:
            logger.error(f"❌ ValidationError en update_member: {ve.errors()}")
            return ErrorResponse(message="Error de validación", errors=[str(ve)], status_code=422)

        except FirebaseError as fe:
            logger.error(f"❌ FirebaseError en update_member: {str(fe)}")
            return ErrorResponse(message="Error en la base de datos", errors=[str(fe)], status_code=500)

        except Exception as e:
            logger.error(f"❌ Error inesperado en update_member: {str(e)}")
            return ErrorResponse(message="Error inesperado al actualizar miembro", errors=[str(e)], status_code=500)

    @staticmethod
    async def update_member_partial(member_id: str, updates: dict):
        try:
            result = await MemberRepository.update_member_partial(member_id, updates)

            if result["status"] == "error":
                return ErrorResponse(message="Error al actualizar miembro", errors=[result["message"]], status_code=400)

            return SuccessResponse(message="Miembro actualizado exitosamente", data=result["data"])

        except Exception as e:
            logger.error(f"❌ Error inesperado en update_miembro_partial: {str(e)}")
            return ErrorResponse(message="Error inesperado al actualizar miembro", errors=[str(e)], status_code=500)

