from fastapi import APIRouter, HTTPException
from app.models.membership_model import MembershipPlan, MembershipAssignment, MembershipRenewal, MembershipCancellation
from app.services.membership_service import MembershipService
import logging

router = APIRouter()

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@router.get("/", tags=["Planes de Membresía"])
async def list_membership_plans():
    """Obtiene la lista de todos los planes de membresía disponibles."""
    logger.debug("Recibida petición GET /membership_plans")  #  Ver si la petición llega
    try:
        plans = await MembershipService.get_all_plans()  #  CORRECTO
        logger.debug(f"Planes obtenidos: {plans}")  #  Ver si Firestore devuelve datos
        return [{"id": plan["id"], **plan} for plan in plans]
    except Exception as e:
        logger.error(f"Error en GET /membership_plans: {str(e)}")  #  Si algo falla
        raise HTTPException(status_code=500, detail=str(e))

@router.post(
    "/create",
    summary="Crear un nuevo plan de membresía",
    description="Registra un nuevo plan de membresía en la plataforma.",
    response_description="El plan de membresía ha sido registrado exitosamente.",
    responses={
        200: {"description": "Plan de membresía creado exitosamente"},
        400: {"description": "Error en los datos proporcionados"},
    },
    tags=["Planes de Membresía"]
)
async def create_membership_plan(plan: MembershipPlan):
    """Crea un nuevo plan de membresía en la plataforma."""
    try:
        log.console("probando")
        return await MembershipService.create_plan(plan)
    except Exception as e:
        logger.error(f"Error en POST /membership_plans/create: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put(
    "/update/{plan_id}",
    summary="Actualizar un plan de membresía",
    description="Actualiza los datos de un plan de membresía existente.",
    tags=["Planes de Membresía"]
)
async def update_membership_plan(plan_id: str, plan: MembershipPlan):
    """Actualiza un plan de membresía en la plataforma."""
    try:
        return await MembershipService.update_plan(plan_id, plan)
    except Exception as e:
        logger.error(f"Error en PUT /membership_plans/update/{plan_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.delete(
    "/delete/{plan_id}",
    summary="Eliminar un plan de membresía",
    description="Elimina un plan de membresía de la plataforma.",
    tags=["Planes de Membresía"]
)
async def delete_membership_plan(plan_id: str):
    """Elimina un plan de membresía por su ID."""
    try:
        return await MembershipService.delete_plan(plan_id)
    except Exception as e:
        logger.error(f"Error en DELETE /membership_plans/delete/{plan_id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post(
    "/assign",
    summary="Asignar membresía a un usuario",
    description="Asigna un plan de membresía a un usuario.",
    tags=["Membresías"]
)
async def assign_membership(assignment: MembershipAssignment):
    """Asigna una membresía a un usuario."""
    try:
        return await MembershipService.assign_membership(assignment)
    except Exception as e:
        logger.error(f"Error en POST /membership_plans/assign: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post(
    "/renew",
    summary="Renovar membresía",
    description="Renueva un plan de membresía para un usuario.",
    tags=["Membresías"]
)
async def renew_membership(renewal: MembershipRenewal):
    """Renueva una membresía automáticamente para un usuario."""
    try:
        return await MembershipService.renew_membership(renewal)
    except Exception as e:
        logger.error(f"Error en POST /membership_plans/renew: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post(
    "/cancel",
    summary="Cancelar membresía",
    description="Cancela un plan de membresía para un usuario.",
    tags=["Membresías"]
)
async def cancel_membership(cancellation: MembershipCancellation):
    """Cancela una membresía de un usuario."""
    try:
        return await MembershipService.cancel_membership(cancellation)
    except Exception as e:
        logger.error(f"Error en POST /membership_plans/cancel: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
