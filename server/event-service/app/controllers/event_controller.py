from fastapi import APIRouter, HTTPException, Body, Depends
from typing import Dict, Any
from app.models.dtos.event_dto import EventDTO
from app.services.event_service import EventService
from app.utils.response_standardization import SuccessResponse, StandardResponse
from app.services.auth_service import AuthService
import logging

router = APIRouter()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@router.get("/", tags=["Eventos"], response_model=SuccessResponse)
async def list_events(user: dict = Depends(AuthService.get_current_user)):
    """Obtiene todos los eventos disponibles."""
    logger.debug("Recibida petición GET /events/")
    response = await EventService.get_all_events()
    if response.status == "error":
        raise HTTPException(status_code=500, detail=response.dict())
    return response

@router.post("/create", tags=["Eventos"], response_model=StandardResponse)
async def create_event(event_dto: EventDTO, user: dict = Depends(AuthService.get_current_user)):
    """Crea un nuevo evento."""
    try:
        return await EventService.create_event(event_dto)
    except Exception as e:
        logger.error(f"❌ Excepción al crear evento: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/update/{event_id}", tags=["Eventos"], response_model=SuccessResponse)
async def update_event_partial(event_id: str, updates: Dict[str, Any] = Body(...), user: dict = Depends(AuthService.get_current_user)):
    """Actualiza parcialmente un evento por ID."""
    logger.debug(f"Recibida petición PATCH /events/update/{event_id}, updates: {updates}")
    response = await EventService.update_event_partial(event_id, updates)
    if response.status == "error":
        raise HTTPException(status_code=400, detail=response.dict())
    return response

@router.delete("/delete/{event_id}", tags=["Eventos"], response_model=SuccessResponse)
async def delete_event(event_id: str, user: dict = Depends(AuthService.get_current_user)):
    """Elimina un evento por su ID."""
    response = await EventService.delete_event(event_id)
    if response.status == "error":
        raise HTTPException(status_code=400, detail=response.dict())
    return response

@router.get("/{event_id}", tags=["Eventos"], response_model=SuccessResponse)
async def get_event_by_id(event_id: str, user: dict = Depends(AuthService.get_current_user)):
    """Obtiene detalles de un evento específico por ID."""
    logger.debug(f"Recibida petición GET /events/{event_id}")
    response = await EventService.get_event_by_id(event_id)
    if response.status == "error":
        raise HTTPException(status_code=404, detail=response.dict())
    return response