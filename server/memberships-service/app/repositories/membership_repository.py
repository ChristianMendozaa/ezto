# app/repositories/membership_repository.py

from firebase_admin import firestore
from app.models.membership_plan_model import MembershipPlanEntity
from app.utils.firebase_config import db
import asyncio
import logging

logger = logging.getLogger(__name__)

class MembershipRepository:

    @staticmethod
    async def create_membership(entity: MembershipPlanEntity):
        """
        Crea un nuevo plan de membresía en Firestore y asigna su ID auto-generado.
        """
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("membership_plans").document()

            # Asignar el ID generado por Firestore al entity
            entity.id = ref.id
            data = entity.to_dict()

            await loop.run_in_executor(None, lambda: ref.set(data))
            return {
                "status": "success",
                "data": data
            }

        except Exception as e:
            logger.error(f"❌ Error creando plan de membresía: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    async def get_all_memberships():
        """
        Recupera todos los planes de membresía almacenados.
        """
        try:
            loop = asyncio.get_running_loop()
            docs = await loop.run_in_executor(
                None,
                lambda: list(db.collection("membership_plans").stream())
            )
            memberships = [doc.to_dict() for doc in docs]
            return {
                "status": "success",
                "data": memberships
            }

        except Exception as e:
            logger.error(f"❌ Error obteniendo planes de membresía: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    async def get_membership_by_id(plan_id: str):
        """
        Recupera un plan de membresía por su ID.
        """
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("membership_plans").document(plan_id)
            doc = await loop.run_in_executor(None, lambda: ref.get())

            if not doc.exists:
                return {
                    "status": "error",
                    "message": "Plan de membresía no encontrado"
                }

            return {
                "status": "success",
                "data": doc.to_dict()
            }

        except Exception as e:
            logger.error(f"❌ Error obteniendo plan de membresía: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    async def delete_membership(plan_id: str):
        """
        Elimina un plan de membresía por su ID.
        """
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("membership_plans").document(plan_id)
            doc = await loop.run_in_executor(None, lambda: ref.get())

            if not doc.exists:
                return {
                    "status": "error",
                    "message": "Plan de membresía no encontrado"
                }

            await loop.run_in_executor(None, lambda: ref.delete())
            return {
                "status": "success"
            }

        except Exception as e:
            logger.error(f"❌ Error eliminando plan de membresía: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    async def update_membership(plan_id: str, entity: MembershipPlanEntity):
        """
        Reemplaza completamente un plan de membresía por los datos de la entidad.
        """
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("membership_plans").document(plan_id)
            doc = await loop.run_in_executor(None, lambda: ref.get())

            if not doc.exists:
                return {
                    "status": "error",
                    "message": "Plan de membresía no encontrado"
                }

            data = entity.to_dict()
            await loop.run_in_executor(None, lambda: ref.set(data))

            updated = await loop.run_in_executor(None, lambda: ref.get())
            return {
                "status": "success",
                "data": updated.to_dict()
            }

        except Exception as e:
            logger.error(f"❌ Error actualizando plan de membresía: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    @staticmethod
    async def update_membership_partial(plan_id: str, updates: dict):
        """
        Actualiza parcialmente campos de un plan de membresía:
        valida campos numéricos y la lista de servicios antes de aplicar.
        """
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("membership_plans").document(plan_id)
            doc = await loop.run_in_executor(None, lambda: ref.get())

            if not doc.exists:
                return {
                    "status": "error",
                    "message": "Plan de membresía no encontrado"
                }

            # Validaciones básicas
            if "capacity" in updates and updates["capacity"] <= 0:
                return {"status": "error", "message": "La capacidad debe ser mayor a 0."}
            if "duration_months" in updates and updates["duration_months"] <= 0:
                return {"status": "error", "message": "La duración debe ser mayor a 0 meses."}
            if "price" in updates and updates["price"] <= 0:
                return {"status": "error", "message": "El precio debe ser mayor a 0."}
            if "services_offered" in updates:
                services = updates["services_offered"]
                if (
                    not isinstance(services, list) or
                    any(not isinstance(s, str) or not s.strip() for s in services)
                ):
                    return {
                        "status": "error",
                        "message": "Cada servicio ofrecido debe ser una cadena no vacía."
                    }

            # Aplicar los cambios
            await loop.run_in_executor(None, lambda: ref.update(updates))
            updated = await loop.run_in_executor(None, lambda: ref.get())

            return {
                "status": "success",
                "data": updated.to_dict()
            }

        except Exception as e:
            logger.error(f"❌ Error actualizando parcialmente plan de membresía: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
