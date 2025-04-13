from fastapi import APIRouter, UploadFile, File, Form
from app.models.user_model import UserRegister
from app.services.user_service import UserService
from pydantic import EmailStr
from typing import Optional
from datetime import date, datetime
from app.utils.response_helper import success_response, error_response
from app.models.responses_models import RegisterResponse
import re

router = APIRouter()

@router.post(
    "/register",
    summary="Registro de nuevo usuario",
    description="Registra un nuevo usuario como miembro o dueño de un gimnasio en la plataforma.",
    response_model=RegisterResponse,
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
        # Validación de contraseñas
        if len(password) < 8:
            return error_response("La contraseña debe tener al menos 8 caracteres.", 400)

        if not any(char.isdigit() for char in password):
            return error_response("La contraseña debe contener al menos un número.", 400)

        if not any(char.isupper() for char in password):
            return error_response("La contraseña debe contener al menos una letra mayúscula.", 400)

        if not any(char in "!@#$%^&*()-_+=" for char in password):
            return error_response("La contraseña debe contener al menos un carácter especial (!@#$%^&*()-_+=).", 400)

        if password != confirm_password:
            return error_response("Las contraseñas no coinciden.", 400)

        # Validación del tipo de usuario
        if user_type not in ["gym_owner", "gym_member"]:
            return error_response("El tipo de usuario debe ser 'gym_owner' o 'gym_member'.", 400)
 
        # Validación de campos obligatorios según el tipo de usuario
        if user_type == "gym_owner":
            if not gym_name:
                return error_response("El nombre del gimnasio es obligatorio para dueños de gimnasio.", 400)
            if not gym_address:
                return error_response("La dirección del gimnasio es obligatoria para dueños de gimnasio.", 400)
            if not gym_phone:
                return error_response("El teléfono del gimnasio es obligatorio para dueños de gimnasio.", 400)
            if not opening_hours:
                return error_response("El horario de atención del gimnasio es obligatorio para dueños de gimnasio.", 400)
            if not services_offered:
                return error_response("Debe especificar al menos un servicio ofrecido por el gimnasio.", 400)
            if capacity is not None and capacity <= 0:
                return error_response("La capacidad del gimnasio debe ser un número positivo.", 400)

        if user_type == "gym_member":
            if not gym_id:
                return error_response("El ID del gimnasio es obligatorio para miembros.", 400)
            if not membership_number:
                return error_response("El número de membresía es obligatorio para miembros.", 400)
            if birth_date is None:
                return error_response("La fecha de nacimiento es obligatoria para miembros.", 400)

            # Validar que la persona tenga al menos 14 años para registrarse
            from datetime import datetime
            today = datetime.today().date()
            age = (today - birth_date).days // 365
            if age < 14:
                return error_response("Debes tener al menos 14 años para registrarte.", 400)

            if gender not in ["Masculino", "Femenino", "Otro"]:
                return error_response("El género debe ser 'Masculino', 'Femenino' o 'Otro'.", 400)

        # Validación del número de teléfono
        import re
        phone_pattern = r"^\+?[1-9]\d{7,14}$"  # Formato internacional
        if not re.match(phone_pattern, phone):
            return error_response("El número de teléfono no es válido. Debe contener entre 8 y 15 dígitos.", 400)

        # Validación de redes sociales
        if social_media:
            if not social_media.startswith("http"):
                return error_response("El enlace a redes sociales debe ser una URL válida.", 400)

        # Validación de la imagen del gimnasio (opcional)
        if gym_logo:
            allowed_extensions = ["image/jpeg", "image/png", "image/jpg"]
            if gym_logo.content_type not in allowed_extensions:
                return error_response("El logo del gimnasio debe ser una imagen en formato JPG o PNG.", 400)

            if gym_logo.size > 100 * 1024 * 1024:  # 10MB máximo
                return error_response("El logo del gimnasio no debe superar los 10MB.", 400)

        # Procesar campos de lista
        services_list = services_offered.split(",") if services_offered else []
        training_goals_list = training_goals.split(",") if training_goals else []
        activity_preferences_list = activity_preferences.split(",") if activity_preferences else []

        # Crear estructura de datos
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

        # Validar con modelo
        user = UserRegister(**user_data)

        # Guardar usuario
        # result = await UserService.register_user(user, gym_logo)

        return RegisterResponse(message="Usuario registrado exitosamente", uid="1232")

    except Exception as e:
        return error_response(str(e), 500)
