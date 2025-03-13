from firebase_admin import firestore
from app.models.membership_model import MembershipPlan, MembershipAssignment
from app.utils.firebase_config import db
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MembershipRepository:
    @staticmethod
    async def create_plan(plan: MembershipPlan):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("membership_plans").document()
            plan_data = plan.dict()
            plan_data["id"] = ref.id

            await loop.run_in_executor(None, lambda: ref.set(plan_data))
            return {"id": ref.id, **plan_data}
        except Exception as e:
            logger.error(f"Error creating membership plan: {str(e)}")
            raise Exception(f"Error creating membership plan: {str(e)}")

    @staticmethod
    async def get_all_plans():
        try:
            loop = asyncio.get_running_loop()
            docs = await loop.run_in_executor(None, lambda: db.collection("membership_plans").stream())
            plans = [{"id": doc.id, **doc.to_dict()} for doc in docs]
            return plans
        except Exception as e:
            logger.error(f"Error fetching membership plans: {str(e)}")
            raise Exception(f"Error fetching membership plans: {str(e)}")

    @staticmethod
    async def update_plan(plan_id: str, plan: MembershipPlan):
        try:
            loop = asyncio.get_running_loop()
            ref = db.collection("membership_plans").document(plan_id)
            await loop.run_in_executor(None, lambda: ref.update(plan.dict()))
            return {"message": "Plan updated successfully", "id": plan_id}
        except Exception as e:
            logger.error(f"Error updating membership plan: {str(e)}")
            raise Exception(f"Error updating membership plan: {str(e)}")

    @staticmethod
    async def delete_plan(plan_id: str):
        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, lambda: db.collection("membership_plans").document(plan_id).delete())
            return {"message": "Plan deleted successfully", "id": plan_id}
        except Exception as e:
            logger.error(f"Error deleting membership plan: {str(e)}")
            raise Exception(f"Error deleting membership plan: {str(e)}")