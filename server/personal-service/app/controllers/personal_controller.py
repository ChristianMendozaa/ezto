# personal-service/app/controllers/personal_controller.py

from fastapi import APIRouter, HTTPException, Body, Depends
from typing import Dict, Any
from app.models.dtos.personal_dto import PersonalDTO
from app.services.personal_service import PersonalService
from app.utils.response_standardization import SuccessResponse, StandardResponse
from app.services.auth_service import AuthService
import logging

router = APIRouter(tags=["Personal"])
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@router.get("/", response_model=SuccessResponse)
async def list_personal(user: dict = Depends(AuthService.get_current_user)):
    """
    Obtiene la lista de todo el personal registrado.
    """
    logger.debug("Recibida petición GET /personal/")
    resp = await PersonalService.get_all_personal()
    if resp.status == "error":
        raise HTTPException(status_code=500, detail=resp.dict())
    return resp


@router.post("/create", response_model=StandardResponse)
async def create_personal(
    dto: PersonalDTO,
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Crea un nuevo registro de personal.
    """
    logger.debug(f"Recibida petición POST /personal/create → {dto.json()}")
    try:
        return await PersonalService.create_personal(dto)
    except Exception as e:
        logger.error(f"Error al crear personal: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{personal_id}", response_model=SuccessResponse)
async def get_personal_by_id(
    personal_id: str,
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Obtiene los detalles de un miembro del personal por su ID.
    """
    logger.debug(f"Recibida petición GET /personal/{personal_id}")
    resp = await PersonalService.get_personal_by_id(personal_id)
    if resp.status == "error":
        raise HTTPException(status_code=404, detail=resp.dict())
    return resp


@router.patch("/update/{personal_id}", response_model=SuccessResponse)
async def update_personal_partial(
    personal_id: str,
    updates: Dict[str, Any] = Body(...),
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Actualiza parcialmente los datos de un miembro del personal.
    """
    logger.debug(f"Recibida petición PATCH /personal/update/{personal_id} con cambios: {updates}")
    resp = await PersonalService.update_personal_partial(personal_id, updates)
    if resp.status == "error":
        raise HTTPException(status_code=400, detail=resp.dict())
    return resp


@router.delete("/delete/{personal_id}", response_model=SuccessResponse)
async def delete_personal(
    personal_id: str,
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Elimina un registro de personal por su ID.
    """
    logger.debug(f"Recibida petición DELETE /personal/delete/{personal_id}")
    resp = await PersonalService.delete_personal(personal_id)
    if resp.status == "error":
        raise HTTPException(status_code=400, detail=resp.dict())
    return resp
