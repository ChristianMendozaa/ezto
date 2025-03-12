from fastapi import APIRouter, HTTPException
from app.models.membership_models import MembershipPlan, MembershipAssignment, MembershipRenewal, MembershipCancellation

router = APIRouter()

# Simulación de base de datos temporal
membership_plans = []

@router.post("/plans", response_model=MembershipPlan)
def create_plan(plan: MembershipPlan):
    membership_plans.append(plan)
    return plan

@router.get("/plans", response_model=list[MembershipPlan])
def get_plans():
    return membership_plans

@router.put("/plans/{plan_id}", response_model=MembershipPlan)
def update_plan(plan_id: str, updated_plan: MembershipPlan):
    for index, plan in enumerate(membership_plans):
        if plan.plan_id == plan_id:
            membership_plans[index] = updated_plan
            return updated_plan
    raise HTTPException(status_code=404, detail="Plan no encontrado")

@router.delete("/plans/{plan_id}")
def delete_plan(plan_id: str):
    for index, plan in enumerate(membership_plans):
        if plan.plan_id == plan_id:
            del membership_plans[index]
            return {"message": "Plan eliminado correctamente"}
    raise HTTPException(status_code=404, detail="Plan no encontrado")

@router.post("/assignments", response_model=MembershipAssignment)
def assign_membership(assignment: MembershipAssignment):
    return assignment

@router.post("/renewals", response_model=MembershipRenewal)
def renew_membership(renewal: MembershipRenewal):
    return renewal

@router.post("/cancellations", response_model=MembershipCancellation)
def cancel_membership(cancellation: MembershipCancellation):
    return cancellation