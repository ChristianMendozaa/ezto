from fastapi import APIRouter, HTTPException, Body, Depends
from typing import Dict, Any
from app.models.dtos.reservation_dto import ReservationDTO
from app.services.reservation_service import ReservationService
from app.utils.response_standardization import SuccessResponse, StandardResponse
from app.services.auth_service import AuthService
import logging

router = APIRouter()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@router.get("/", tags=["Reservas"], response_model=SuccessResponse)
async def list_reservations(user: dict = Depends(AuthService.get_current_user)):
    response = await ReservationService.get_all_reservations()
    if response.status == "error":
        raise HTTPException(500, response.dict())
    return response

@router.post("/create", tags=["Reservas"], response_model=StandardResponse)
async def create_reservation(reservation: ReservationDTO, user: dict = Depends(AuthService.get_current_user)):
    return await ReservationService.create_reservation(reservation)

@router.patch("/update/{reservation_id}", tags=["Reservas"], response_model=SuccessResponse)
async def update_reservation_partial(reservation_id: str, updates: Dict[str, Any] = Body(...), user: dict = Depends(AuthService.get_current_user)):
    response = await ReservationService.update_reservation_partial(reservation_id, updates)
    if response.status == "error":
        raise HTTPException(400, response.dict())
    return response

@router.delete("/delete/{reservation_id}", tags=["Reservas"], response_model=SuccessResponse)
async def delete_reservation(reservation_id: str, user: dict = Depends(AuthService.get_current_user)):
    response = await ReservationService.delete_reservation(reservation_id)
    if response.status == "error":
        raise HTTPException(404, response.dict())
    return response

@router.get("/{reservation_id}", tags=["Reservas"], response_model=SuccessResponse)
async def get_reservation_by_id(reservation_id: str, user: dict = Depends(AuthService.get_current_user)):
    response = await ReservationService.get_reservation_by_id(reservation_id)
    if response.status == "error":
        raise HTTPException(404, response.dict())
    return response
