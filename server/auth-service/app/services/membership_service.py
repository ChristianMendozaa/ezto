from app.models.membership_model import MembershipPlan, MembershipAssignment, MembershipRenewal, MembershipCancellation
from app.repositories.membership_repository import MembershipRepository

class MembershipService:
    """
    Servicio para la gestión de planes de membresía y asignaciones.
    """

    @staticmethod
    async def create_plan(plan: MembershipPlan):
        return await MembershipRepository.create_plan(plan)

    @staticmethod
    async def get_all_plans():
        return await MembershipRepository.get_all_plans()

    @staticmethod
    async def update_plan(plan_id: str, plan: MembershipPlan):
        return await MembershipRepository.update_plan(plan_id, plan)

    @staticmethod
    async def delete_plan(plan_id: str):
        return await MembershipRepository.delete_plan(plan_id)

    @staticmethod
    async def assign_membership(assignment: MembershipAssignment):
        return await MembershipRepository.assign_membership(assignment)

    @staticmethod
    async def renew_membership(renewal: MembershipRenewal):
        return await MembershipRepository.renew_membership(renewal)

    @staticmethod
    async def cancel_membership(cancellation: MembershipCancellation):
        return await MembershipRepository.cancel_membership(cancellation)