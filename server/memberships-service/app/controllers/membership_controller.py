# membership-service/app/controllers/membership_controller.py

from fastapi import APIRouter, HTTPException, Body, Depends
from typing import Dict, Any
from app.models.dtos.membership_plan_dto import MembershipPlanDTO
from app.services.membership_service import MembershipService
from app.utils.response_standardization import SuccessResponse, ErrorResponse, StandardResponse
from app.services.auth_service import AuthService
import logging

router = APIRouter()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@router.get("/", response_model=SuccessResponse)
async def list_membership_plans(user: dict = Depends(AuthService.get_current_user)):
    """Obtiene la lista de todos los planes de membresía."""
    logger.debug("Recibida petición GET /membership-plans/")
    response = await MembershipService.get_all_memberships()
    if response.status == "error":
        raise HTTPException(status_code=500, detail=response.dict())
    return response


@router.post("/create", response_model=StandardResponse)
async def create_membership_plan(
    plan: MembershipPlanDTO,
    user: dict = Depends(AuthService.get_current_user)
):
    """Crea un nuevo plan de membresía en la plataforma."""
    try:
        return await MembershipService.create_membership(plan)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/update/{plan_id}", response_model=SuccessResponse)
async def update_membership_plan_partial(
    plan_id: str,
    updates: Dict[str, Any] = Body(...),
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Actualiza parcialmente un plan de membresía por su ID
    (por ejemplo, solo el precio, la capacidad o la lista de servicios).
    """
    logger.debug(f"Recibida petición PATCH /membership-plans/update/{plan_id} con cambios: {updates}")
    response = await MembershipService.update_membership_partial(plan_id, updates)
    if response.status == "error":
        raise HTTPException(status_code=400, detail=response.dict())
    return response


@router.delete("/delete/{plan_id}", response_model=SuccessResponse)
async def delete_membership_plan(
    plan_id: str,
    user: dict = Depends(AuthService.get_current_user)
):
    """Elimina un plan de membresía por su ID."""
    response = await MembershipService.delete_membership(plan_id)
    if response.status == "error":
        raise HTTPException(status_code=400, detail=response.dict())
    return response


@router.get("/{plan_id}", response_model=SuccessResponse)
async def get_membership_plan_by_id(
    plan_id: str,
    user: dict = Depends(AuthService.get_current_user)
):
    """Obtiene los detalles de un plan de membresía por su ID."""
    logger.debug(f"Recibida petición GET /membership-plans/{plan_id}")
    response = await MembershipService.get_membership_by_id(plan_id)
    if response.status == "error":
        raise HTTPException(status_code=404, detail=response.dict())
    return response
