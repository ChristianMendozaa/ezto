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
        if user["role"] != "gym_owner":
            raise HTTPException(status_code=403, detail="No tiene permisos para crear clases")
        
        # Convertir el modelo Pydantic a diccionario
        class_dict = class_data.model_dump()
        
        # Crear la clase y obtener el ID
        class_id = await ClassService.create_class(class_dict)
        
        # Construir la respuesta en el formato correcto
        response_data = {
            "id": class_id,
            "name": class_dict["name"],
            "description": class_dict["description"],
            "instructor_id": class_dict["instructor_id"],
            "instructor_name": class_dict["instructor_id"],  # Aquí deberías obtener el nombre real del instructor
            "duration": class_dict["duration"],
            "capacity": class_dict["capacity"],
            "available_spots": class_dict["capacity"],
            "current_reservations": 0,
            "class_type": str(class_dict["class_type"]),
            "difficulty_level": class_dict["difficulty_level"],
            "room": class_dict["room"],
            "schedule_id": class_id,  # Usando el mismo ID como schedule_id
            "start_time": class_dict["start_time"],
            "end_time": class_dict["end_time"],
            "days_of_week": class_dict["days_of_week"],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": "activa"
        }
        
        return response_data
        
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
        if user["role"] != "gym_owner":
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