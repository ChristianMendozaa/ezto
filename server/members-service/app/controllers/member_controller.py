from fastapi import APIRouter, HTTPException, Body, Depends
from typing import Dict, Any
from app.models.dtos.member_dto import MemberDTO
from app.services.member_service import MemberService
from app.utils.response_standardization import SuccessResponse, ErrorResponse, StandardResponse
from app.services.auth_service import AuthService
import logging

router = APIRouter()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@router.get("/",tags=["Miembros"], response_model=SuccessResponse)
async def list_members(user: dict = Depends(AuthService.get_current_user)):
    """Obtiene la lista de todos los miembros."""
    logger.debug("Recibida petición GET /members/")
    response = await MemberService.get_all_members()
    if response.status == "error":
        raise HTTPException(status_code=500, detail=response.dict())
    return response


@router.get("/{member_id}", response_model=SuccessResponse)
async def get_member_by_id(member_id: str, user: dict = Depends(AuthService.get_current_user)):
    """Obtiene un miembro por su ID."""
    logger.debug(f"Recibida petición GET /members/{member_id}")
    response = await MemberService.get_member_by_id(member_id)
    if response.status == "error":
        raise HTTPException(status_code=404, detail=response.dict())
    return response


@router.post("/create", response_model=StandardResponse)
async def create_member(member: MemberDTO, user: dict = Depends(AuthService.get_current_user)):
    """Crea un nuevo miembro."""
    logger.debug(f"Recibida petición POST /members/create con datos: {member}")
    try:
        return await MemberService.create_member(member)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/update/{member_id}",tags=["Miembros"], response_model=SuccessResponse)
async def update_member(member_id: str, updates: Dict[str, Any] = Body(...), user: dict = Depends(AuthService.get_current_user)):
    """
    Actualiza un miembro por su ID.
    """
    if "id" in updates:
        updates.pop("id")  # ✅ Eliminar 'id' duplicado si viene en el body
    logger.debug(f"Recibida petición PATCH /members/update/{member_id} con cambios: {updates}")
    response = await MemberService.update_member(member_id, updates)
    if response.status == "error":
        raise HTTPException(status_code=400, detail=response.dict())
    return response


@router.delete("/delete/{member_id}", tags=["Miembros"], response_model=SuccessResponse)
async def delete_member(member_id: str, user: dict = Depends(AuthService.get_current_user)):
    """Elimina un miembro por su ID."""
    logger.debug(f"Recibida petición DELETE /members/delete/{member_id}")
    response = await MemberService.delete_member(member_id)
    if response.status == "error":
        raise HTTPException(status_code=400, detail=response.dict())
    return response
