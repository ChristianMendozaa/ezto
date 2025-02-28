from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.models.user_model import UserRegister
from app.services.user_service import UserService
from pydantic import EmailStr
from typing import Optional, List
from datetime import date

router = APIRouter()

@router.post(
    "/register",
    summary="Registro de nuevo usuario",
    description="Registra un nuevo usuario como miembro o dueño de un gimnasio en la plataforma.",
    response_description="El usuario ha sido registrado exitosamente.",
    responses={
        200: {
            "description": "Usuario registrado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Usuario registrado exitosamente",
                        "uid": "abc123xyz"
                    }
                }
            }
        },
        400: {
            "description": "Error en los datos proporcionados",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Las contraseñas no coinciden."
                    }
                }
            }
        }
    },
    tags=["Registro de Usuarios"]
)
async def register_user(
    full_name: str = Form(..., description="Nombre completo del usuario"),
    email: EmailStr = Form(..., description="Correo electrónico válido del usuario"),
    password: str = Form(..., description="Contraseña del usuario"),
    confirm_password: str = Form(..., description="Confirmación de la contraseña"),
    phone: str = Form(..., description="Número de teléfono del usuario"),
    user_type: str = Form(..., description="Tipo de usuario (gym_owner o gym_member)"),
    gym_name: Optional[str] = Form(None, description="Nombre del gimnasio (solo para dueños)"),
    gym_address: Optional[str] = Form(None, description="Dirección del gimnasio (solo para dueños)"),
    gym_phone: Optional[str] = Form(None, description="Teléfono del gimnasio (solo para dueños)"),
    opening_hours: Optional[str] = Form(None, description="Horario de atención del gimnasio (solo para dueños)"),
    services_offered: Optional[str] = Form(None, description="Servicios ofrecidos por el gimnasio (separados por comas)"),
    capacity: Optional[int] = Form(None, description="Capacidad máxima del gimnasio"),
    social_media: Optional[str] = Form(None, description="Redes sociales del gimnasio"),
    gym_id: Optional[str] = Form(None, description="ID del gimnasio (solo para miembros)"),
    membership_number: Optional[str] = Form(None, description="Número de membresía del usuario (solo para miembros)"),
    birth_date: Optional[date] = Form(None, description="Fecha de nacimiento del usuario (solo para miembros)"),
    gender: Optional[str] = Form(None, description="Género del usuario (solo para miembros)"),
    training_goals: Optional[str] = Form(None, description="Objetivos de entrenamiento del usuario (separados por comas)"),
    activity_preferences: Optional[str] = Form(None, description="Preferencias de actividades del usuario (separados por comas)"),
    gym_logo: Optional[UploadFile] = File(None, description="Logo del gimnasio en formato de imagen (opcional)")
):
    """
    Registra un nuevo usuario en la plataforma.

    - **full_name**: Nombre completo del usuario
    - **email**: Correo electrónico válido
    - **password** y **confirm_password**: Contraseñas que deben coincidir
    - **phone**: Número de teléfono del usuario
    - **user_type**: Tipo de usuario (`gym_owner` o `gym_member`)
    - **gym_info**: Información del gimnasio (solo para dueños de gimnasio)
    - **member_info**: Información del miembro (solo para miembros de gimnasio)
    - **gym_logo**: Imagen opcional del logo del gimnasio
    """
    try:
        # Procesar las listas enviadas como cadenas separadas por comas
        services_list = services_offered.split(",") if services_offered else []
        training_goals_list = training_goals.split(",") if training_goals else []
        activity_preferences_list = activity_preferences.split(",") if activity_preferences else []

        # Construir el diccionario de datos del usuario
        user_data = {
            "full_name": full_name,
            "email": email,
            "password": password,
            "confirm_password": confirm_password,
            "phone": phone,
            "user_type": user_type,
            "gym_info": {
                "name": gym_name,
                "address": gym_address,
                "phone": gym_phone,
                "opening_hours": opening_hours,
                "services_offered": services_list,
                "capacity": capacity,
                "social_media": social_media,
            } if user_type == "gym_owner" else None,
            "member_info": {
                "gym_id": gym_id,
                "membership_number": membership_number,
                "birth_date": birth_date,
                "gender": gender,
                "training_goals": training_goals_list,
                "activity_preferences": activity_preferences_list,
            } if user_type == "gym_member" else None,
        }

        # Crear un objeto UserRegister desde el diccionario
        user = UserRegister(**user_data)

        # Pasar la imagen al servicio de usuario
        return await UserService.register_user(user, gym_logo)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
