from fastapi import APIRouter, HTTPException, Body, Depends
from typing import Dict, Any
from app.models.dtos.class_dto import ClassDTO
from app.services.class_service import ClassService
from app.utils.response_standardization import SuccessResponse, StandardResponse
from app.services.auth_service import AuthService
import logging

router = APIRouter()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@router.get("/", tags=["Clases"], response_model=SuccessResponse)
async def list_classes(user: dict = Depends(AuthService.get_current_user)):
    """Obtiene todas las clases disponibles."""
    logger.debug("Recibida petición GET /classes/")
    response = await ClassService.get_all_classes()
    if response.status == "error":
        raise HTTPException(status_code=500, detail=response.dict())
    return response

@router.post("/create", tags=["Clases"], response_model=StandardResponse)
async def create_class(class_dto: ClassDTO, user: dict = Depends(AuthService.get_current_user)):
    """Crea una nueva clase."""
    try:
        return await ClassService.create_class(class_dto)
    except Exception as e:
        logger.error(f"❌ Excepción al crear clase: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/update/{class_id}", tags=["Clases"], response_model=SuccessResponse)
async def update_class_partial(class_id: str, updates: Dict[str, Any] = Body(...), user: dict = Depends(AuthService.get_current_user)):
    """Actualiza parcialmente una clase por ID."""
    logger.debug(f"Recibida petición PATCH /classes/update/{class_id}, updates: {updates}")
    response = await ClassService.update_class_partial(class_id, updates)
    if response.status == "error":
        raise HTTPException(status_code=400, detail=response.dict())
    return response

@router.delete("/delete/{class_id}", tags=["Clases"], response_model=SuccessResponse)
async def delete_class(class_id: str, user: dict = Depends(AuthService.get_current_user)):
    """Elimina una clase por su ID."""
    response = await ClassService.delete_class(class_id)
    if response.status == "error":
        raise HTTPException(status_code=400, detail=response.dict())
    return response

@router.get("/{class_id}", tags=["Clases"], response_model=SuccessResponse)
async def get_class_by_id(class_id: str, user: dict = Depends(AuthService.get_current_user)):
    """Obtiene detalles de una clase específica por ID."""
    logger.debug(f"Recibida petición GET /classes/{class_id}")
    response = await ClassService.get_class_by_id(class_id)
    if response.status == "error":
        raise HTTPException(status_code=404, detail=response.dict())
    return response
