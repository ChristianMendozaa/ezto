from fastapi import APIRouter, Request, HTTPException, Response
from pydantic import BaseModel, Field
from app.services.auth_service import AuthService
from app.utils.response_helper import StandardResponse, success_response, error_response
from app.models.class_model import ClassCreate, ClassUpdate, ClassResponse
from app.services.class_service import ClassService
from typing import List
from datetime import datetime

router = APIRouter()

@router.post(
    "/",
    summary="Crear nueva clase",
    description="Crea una nueva clase en el sistema. Requiere permisos de administrador.",
    response_model=ClassResponse,
    status_code=201,
    tags=["Clases"]
)
async def create_class(class_data: ClassCreate, request: Request):
    try:
        user = await AuthService.get_current_user(request)
        if user["role"] != "admin":
            raise HTTPException(status_code=403, detail="No tiene permisos para crear clases")
        
        new_class = await ClassService.create_class(class_data)
        return success_response(new_class)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/{class_id}",
    summary="Obtener clase",
    description="Obtiene los detalles de una clase específica por su ID.",
    response_model=ClassResponse,
    status_code=200,
    tags=["Clases"]
)
async def get_class(class_id: str, request: Request):
    try:
        await AuthService.get_current_user(request)
        class_details = await ClassService.get_class(class_id)
        return success_response(class_details)
    except HTTPException as e:
        raise e

@router.get(
    "/",
    summary="Listar clases",
    description="Obtiene la lista de todas las clases disponibles con opciones de filtrado.",
    response_model=List[ClassResponse],
    status_code=200,
    tags=["Clases"]
)
async def list_classes(
    request: Request,
    date: datetime = None,
    instructor: str = None,
    available_only: bool = False
):
    try:
        await AuthService.get_current_user(request)
        classes = await ClassService.list_classes(
            date=date,
            instructor=instructor,
            available_only=available_only
        )
        return success_response(classes)
    except HTTPException as e:
        raise e

@router.put(
    "/{class_id}",
    summary="Actualizar clase",
    description="Actualiza la información de una clase existente. Requiere permisos de administrador.",
    response_model=ClassResponse,
    status_code=200,
    tags=["Clases"]
)
async def update_class(class_id: str, class_data: ClassUpdate, request: Request):
    try:
        user = await AuthService.get_current_user(request)
        if user["role"] != "admin":
            raise HTTPException(status_code=403, detail="No tiene permisos para actualizar clases")
        
        updated_class = await ClassService.update_class(class_id, class_data)
        return success_response(updated_class)
    except HTTPException as e:
        raise e

@router.delete(
    "/{class_id}",
    summary="Eliminar clase",
    description="Elimina una clase del sistema. Requiere permisos de administrador.",
    response_model=StandardResponse,
    status_code=200,
    tags=["Clases"]
)
async def delete_class(class_id: str, request: Request):
    try:
        user = await AuthService.get_current_user(request)
        if user["role"] != "admin":
            raise HTTPException(status_code=403, detail="No tiene permisos para eliminar clases")
        
        await ClassService.delete_class(class_id)
        return success_response({"message": "Clase eliminada exitosamente"})
    except HTTPException as e:
        raise e

@router.get(
    "/{class_id}/availability",
    summary="Verificar disponibilidad",
    description="Verifica la disponibilidad de cupos en una clase específica.",
    response_model=StandardResponse,
    status_code=200,
    tags=["Clases"]
)
async def check_availability(class_id: str, request: Request):
    try:
        await AuthService.get_current_user(request)
        availability = await ClassService.check_availability(class_id)
        return success_response(availability)
    except HTTPException as e:
        raise e