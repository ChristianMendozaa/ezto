# app/controllers/schedule_controller.py
from fastapi import APIRouter, Request, HTTPException, Depends
from app.services.auth_service import AuthService
from app.utils.response_helper import success_response, error_response
from app.models.schedule_model import ScheduleCreate, ScheduleUpdate, ScheduleResponse
from app.services.schedule_service import ScheduleService
from typing import List
from datetime import datetime, date

router = APIRouter()

@router.post(
    "/",
    summary="Crear horario",
    description="Crea un nuevo horario para una clase. Solo accesible por administradores.",
    response_model=ScheduleResponse,
    status_code=201
)
async def create_schedule(
    schedule_data: ScheduleCreate,
    request: Request,
    user: dict = Depends(lambda request: AuthService.require_role(request, "gym_owner"))
):
    try:
        new_schedule = await ScheduleService.create_schedule(schedule_data)
        return success_response(new_schedule)
    except Exception as e:
        return error_response(str(e), 400)

@router.get(
    "/weekly",
    summary="Horario semanal",
    description="Obtiene el horario semanal de clases.",
    response_model=List[ScheduleResponse]
)
async def get_weekly_schedule(
    request: Request,
    start_date: date = None,
    gym_id: str = None
):
    try:
        await AuthService.get_current_user(request)
        schedules = await ScheduleService.get_weekly_schedule(start_date, gym_id)
        return success_response(schedules)
    except HTTPException as e:
        raise e

@router.get(
    "/class/{class_id}",
    summary="Horarios por clase",
    description="Obtiene todos los horarios de una clase específica.",
    response_model=List[ScheduleResponse]
)
async def get_class_schedules(
    class_id: str,
    request: Request
):
    try:
        await AuthService.get_current_user(request)
        schedules = await ScheduleService.get_class_schedules(class_id)
        return success_response(schedules)
    except HTTPException as e:
        raise e

@router.put(
    "/{schedule_id}",
    summary="Actualizar horario",
    description="Actualiza un horario existente. Solo accesible por administradores.",
    response_model=ScheduleResponse
)
async def update_schedule(
    schedule_id: str,
    schedule_data: ScheduleUpdate,
    request: Request,
    user: dict = Depends(lambda request: AuthService.require_role(request, "gym_owner"))
):
    try:
        updated_schedule = await ScheduleService.update_schedule(schedule_id, schedule_data)
        return success_response(updated_schedule)
    except HTTPException as e:
        raise e

@router.delete(
    "/{schedule_id}",
    summary="Eliminar horario",
    description="Elimina un horario existente. Solo accesible por administradores."
)
async def delete_schedule(
    schedule_id: str,
    request: Request,
    user: dict = Depends(lambda request: AuthService.require_role(request, "gym_owner"))
):
    try:
        await ScheduleService.delete_schedule(schedule_id)
        return success_response({"message": "Horario eliminado exitosamente"})
    except HTTPException as e:
        raise e

@router.get(
    "/instructor/{instructor_id}",
    summary="Horarios por instructor",
    description="Obtiene todos los horarios asignados a un instructor específico.",
    response_model=List[ScheduleResponse]
)
async def get_instructor_schedules(
    instructor_id: str,
    request: Request,
    start_date: date = None,
    end_date: date = None
):
    try:
        await AuthService.get_current_user(request)
        schedules = await ScheduleService.get_instructor_schedules(
            instructor_id,
            start_date,
            end_date
        )
        return success_response(schedules)
    except HTTPException as e:
        raise e

@router.post(
    "/bulk",
    summary="Crear horarios en lote",
    description="Crea múltiples horarios a la vez. Solo accesible por administradores.",
    response_model=List[ScheduleResponse]
)
async def create_bulk_schedules(
    schedules_data: List[ScheduleCreate],
    request: Request,
    user: dict = Depends(lambda request: AuthService.require_role(request, "gym_owner"))
):
    try:
        new_schedules = await ScheduleService.create_bulk_schedules(schedules_data)
        return success_response(new_schedules)
    except Exception as e:
        return error_response(str(e), 400)