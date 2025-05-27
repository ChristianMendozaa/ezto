# personal-service/app/repositories/personal_repository.py

import asyncio
import logging
from firebase_admin import firestore
from app.models.personal_model import PersonalEntity
from app.utils.firebase_config import db

logger = logging.getLogger(__name__)


class PersonalRepository:

    @staticmethod
    async def create_personal(entity: PersonalEntity):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("personal").document()

            # asignar el nuevo id al entity
            entity.id = ref.id
            data = entity.to_dict()

            # persistir en Firestore
            await loop.run_in_executor(None, lambda: ref.set(data))
            return {
                "status": "success",
                "data": data
            }

        except Exception as e:
            logger.error(f"❌ Error creando personal: {e}", exc_info=True)
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    async def get_all_personal():
        try:
            loop = asyncio.get_running_loop()
            # obtener todos los documentos
            docs = await loop.run_in_executor(
                None,
                lambda: list(db.collection("personal").stream())
            )
            personal_list = [doc.to_dict() for doc in docs]
            return {
                "status": "success",
                "data": personal_list
            }

        except Exception as e:
            logger.error(f"❌ Error obteniendo personal: {e}", exc_info=True)
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    async def get_personal_by_id(personal_id: str):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("personal").document(personal_id)

            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {
                    "status": "error",
                    "message": "Personal no encontrado"
                }

            return {
                "status": "success",
                "data": doc.to_dict()
            }

        except Exception as e:
            logger.error(f"❌ Error obteniendo personal por ID: {e}", exc_info=True)
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    async def update_personal(personal_id: str, entity: PersonalEntity):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("personal").document(personal_id)

            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {
                    "status": "error",
                    "message": "Personal no encontrado"
                }

            data = entity.to_dict()
            await loop.run_in_executor(None, lambda: ref.update(data))

            updated = await loop.run_in_executor(None, lambda: ref.get())
            return {
                "status": "success",
                "data": updated.to_dict()
            }

        except Exception as e:
            logger.error(f"❌ Error actualizando personal: {e}", exc_info=True)
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    async def update_personal_partial(personal_id: str, updates: dict):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("personal").document(personal_id)

            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {
                    "status": "error",
                    "message": "Personal no encontrado"
                }

            # aplicar sólo los campos recibidos en updates
            await loop.run_in_executor(None, lambda: ref.update(updates))

            updated = await loop.run_in_executor(None, lambda: ref.get())
            return {
                "status": "success",
                "data": updated.to_dict()
            }

        except Exception as e:
            logger.error(f"❌ Error actualizando parcialmente personal: {e}", exc_info=True)
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    async def delete_personal(personal_id: str):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("personal").document(personal_id)

            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {
                    "status": "error",
                    "message": "Personal no encontrado"
                }

            await loop.run_in_executor(None, lambda: ref.delete())
            return {
                "status": "success"
            }

        except Exception as e:
            logger.error(f"❌ Error eliminando personal: {e}", exc_info=True)
            return {
                "status": "error",
                "message": str(e)
            }
