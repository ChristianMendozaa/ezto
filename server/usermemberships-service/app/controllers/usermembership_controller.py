#app/controllers/usermembership_controller.py

from fastapi import APIRouter, HTTPException, Body, Depends
from typing import Dict, Any
from app.models.dtos.UserMembershipDTO import UserMembershipDTO
from app.services.usermembership_service import UserMembershipService
from app.utils.response_standardization import SuccessResponse, StandardResponse
from app.services.auth_service import AuthService
import logging

router = APIRouter()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@router.get("/", tags=["Membresías"], response_model=SuccessResponse)
async def list_user_memberships(user: dict = Depends(AuthService.get_current_user)):
    """Obtiene todas las membresías de usuarios registradas."""
    logger.debug("Recibida petición GET /user-memberships/")
    response = await UserMembershipService.get_all_memberships()
    if response.status == "error":
        raise HTTPException(status_code=500, detail=response.dict())
    return response


@router.get("/user/{user_id}", tags=["Membresías"], response_model=SuccessResponse)
async def get_memberships_by_user(user_id: str, user: dict = Depends(AuthService.get_current_user)):
    """Obtiene todas las membresías de un usuario específico."""
    logger.debug(f"Recibida petición GET /user-memberships/user/{user_id}")
    response = await UserMembershipService.get_memberships_by_user(user_id)
    if response.status == "error":
        raise HTTPException(status_code=404, detail=response.dict())
    return response


@router.get("/{membership_id}", tags=["Membresías"], response_model=SuccessResponse)
async def get_membership_by_id(membership_id: str, user: dict = Depends(AuthService.get_current_user)):
    """Obtiene los detalles de una membresía por su ID."""
    logger.debug(f"Recibida petición GET /user-memberships/{membership_id}")
    response = await UserMembershipService.get_membership_by_id(membership_id)
    if response.status == "error":
        raise HTTPException(status_code=404, detail=response.dict())
    return response


@router.post("/create", tags=["Membresías"], response_model=StandardResponse)
async def create_user_membership(membership: UserMembershipDTO, user: dict = Depends(AuthService.get_current_user)):
    """Crea una nueva membresía para un usuario."""
    try:
        response = await UserMembershipService.create_membership(membership)
        if response.status == "error":
            raise HTTPException(status_code=400, detail=response.dict())
        return response
    except Exception as e:
        logger.exception("❌ Error creando membresía")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{membership_id}", tags=["Membresías"], response_model=SuccessResponse)
async def delete_user_membership(membership_id: str, user: dict = Depends(AuthService.get_current_user)):
    """Elimina una membresía por su ID."""
    response = await UserMembershipService.delete_membership(membership_id)
    if response.status == "error":
        raise HTTPException(status_code=404, detail=response.dict())
    return response

@router.patch("/update/{membership_id}", tags=["Membresías"], response_model=SuccessResponse)
async def update_user_membership_partial(membership_id: str, updates: Dict[str, Any] = Body(...), user: dict = Depends(AuthService.get_current_user)):
    """
    Actualiza parcialmente una membresía por su ID (por ejemplo, solo el estado o la promoción).
    """
    logger.debug(f"Recibida petición PATCH /user-memberships/update/{membership_id} con cambios: {updates}")
    response = await UserMembershipService.update_membership_partial(membership_id, updates)
    if response.status == "error":
        raise HTTPException(status_code=400, detail=response.dict())
    return response