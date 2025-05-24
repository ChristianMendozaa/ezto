from firebase_admin import firestore
from app.models.member_model import MemberEntity
from datetime import datetime
from app.utils.firebase_config import db
import asyncio
import logging

logger = logging.getLogger(__name__)

class MemberRepository:

    @staticmethod
    async def get_all_members():
        try:
            loop = asyncio.get_running_loop()
            docs = await loop.run_in_executor(None, lambda: list(db.collection("members").stream()))
            members = [{"id": doc.id, **doc.to_dict()} for doc in docs]

            return {"status": "success", "data": members}

        except Exception as e:
            logger.error(f"❌ Error obteniendo miembros: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def get_member_by_id(member_id: str):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("members").document(member_id)
            doc = await loop.run_in_executor(None, lambda: ref.get())

            if not doc.exists:
                return {"status": "error", "message": "Miembro no encontrado"}

            return {"status": "success", "data": {"id": doc.id, **doc.to_dict()}}

        except Exception as e:
            logger.error(f"❌ Error obteniendo miembro: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def create_member(data: dict):
        try:
            member_id = data.get("id")
            if not member_id:
                return {"status": "error", "message": "El ID del miembro es requerido"}

            loop = asyncio.get_running_loop()
            ref = db.collection("members").document(member_id)
            await loop.run_in_executor(None, lambda: ref.set(data))

            return {"status": "success", "data": {"id": member_id, **data}}

        except Exception as e:
            logger.error(f"❌ Error creando miembro: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def update_member(member_id: str, updates: dict):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("members").document(member_id)

            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Miembro no encontrado"}

            await loop.run_in_executor(None, lambda: ref.update(updates))

            updated_doc = await loop.run_in_executor(None, lambda: ref.get())
            return {"status": "success", "data": {"id": member_id, **updated_doc.to_dict()}}

        except Exception as e:
            logger.error(f"❌ Error actualizando miembro: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def delete_member(member_id: str):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("members").document(member_id)

            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Miembro no encontrado"}

            await loop.run_in_executor(None, lambda: ref.delete())
            return {"status": "success", "message": f"Miembro {member_id} eliminado exitosamente"}

        except Exception as e:
            logger.error(f"❌ Error eliminando miembro: {e}")
            return {"status": "error", "message": str(e)}
