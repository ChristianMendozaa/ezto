from firebase_admin import firestore
from app.models.UserMembershipEntity import UserMembershipEntity
from app.utils.firebase_config import db
import asyncio
import logging

logger = logging.getLogger(__name__)

class UserMembershipRepository:

    @staticmethod
    async def create_membership(entity: UserMembershipEntity):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("user_memberships").document()

            entity.id = ref.id
            data = entity.to_dict()

            await loop.run_in_executor(None, lambda: ref.set(data))
            return {
                "status": "success",
                "data": data
            }

        except Exception as e:
            logger.error(f"❌ Error creando membresía: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    async def get_membership_by_id(membership_id: str):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("user_memberships").document(membership_id)

            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Membresía no encontrada"}

            data = doc.to_dict()
            return {"status": "success", "data": data}

        except Exception as e:
            logger.error(f"❌ Error obteniendo membresía: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def get_memberships_by_user(user_id: str):
        try:
            loop = asyncio.get_running_loop()
            query = db.collection("user_memberships").where("user_id", "==", user_id)

            docs = await loop.run_in_executor(None, lambda: list(query.stream()))
            memberships = [doc.to_dict() for doc in docs]

            return {"status": "success", "data": memberships}

        except Exception as e:
            logger.error(f"❌ Error obteniendo membresías del usuario: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def get_all_memberships():
        try:
            loop = asyncio.get_running_loop()
            docs = await loop.run_in_executor(None, lambda: list(db.collection("user_memberships").stream()))
            memberships = [doc.to_dict() for doc in docs]

            return {"status": "success", "data": memberships}

        except Exception as e:
            logger.error(f"❌ Error obteniendo todas las membresías: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def delete_membership(membership_id: str):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("user_memberships").document(membership_id)

            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Membresía no encontrada"}

            await loop.run_in_executor(None, lambda: ref.delete())
            return {"status": "success"}

        except Exception as e:
            logger.error(f"❌ Error eliminando membresía: {e}")
            return {"status": "error", "message": str(e)}

    @staticmethod
    async def update_membership_partial(membership_id: str, updates: dict):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("user_memberships").document(membership_id)

            doc = await loop.run_in_executor(None, lambda: ref.get())
            if not doc.exists:
                return {"status": "error", "message": "Membresía no encontrada"}

            # Validación simple (puedes expandirla según reglas de negocio)
            if "start_date" in updates:
                updates["start_date"] = updates["start_date"].isoformat()
            if "end_date" in updates:
                updates["end_date"] = updates["end_date"].isoformat()
            if "status" in updates:
                updates["status"] = str(updates["status"])

            await loop.run_in_executor(None, lambda: ref.update(updates))

            updated = await loop.run_in_executor(None, lambda: ref.get())
            return {
                "status": "success",
                "data": updated.to_dict()
            }

        except Exception as e:
            logger.error(f"❌ Error actualizando membresía: {e}")
            return {"status": "error", "message": str(e)}
