from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date

class GymInfo(BaseModel):
    name: str = Field(..., description="Nombre del gimnasio")
    address: str = Field(..., description="Dirección del gimnasio")
    phone: str = Field(..., description="Teléfono de contacto del gimnasio")
    opening_hours: str = Field(..., description="Horario de atención del gimnasio")
    services_offered: List[str] = Field(..., description="Servicios ofrecidos por el gimnasio")
    capacity: int = Field(..., description="Capacidad máxima del gimnasio")
    social_media: Optional[str] = Field(None, description="Redes sociales del gimnasio")

class MemberInfo(BaseModel):
    gym_id: str = Field(..., description="ID del gimnasio al que pertenece el miembro")
    membership_number: Optional[str] = Field(None, description="Número de membresía del usuario")
    birth_date: date = Field(..., description="Fecha de nacimiento del usuario")
    gender: Optional[str] = Field(None, description="Género del usuario")
    training_goals: List[str] = Field(..., description="Objetivos de entrenamiento del usuario")
    activity_preferences: List[str] = Field(..., description="Preferencias de actividades del usuario")

class UserRegister(BaseModel):
    full_name: str = Field(..., description="Nombre completo del usuario")
    email: EmailStr = Field(..., description="Correo electrónico del usuario")
    password: str = Field(..., description="Contraseña del usuario")
    confirm_password: str = Field(..., description="Confirmación de la contraseña")
    phone: str = Field(..., description="Teléfono del usuario")
    user_type: str = Field(..., pattern="^(gym_owner|gym_member)$", description="Tipo de usuario (gym_owner o gym_member)")
    gym_info: Optional[GymInfo] = Field(None, description="Información del gimnasio (solo para dueños)")
    member_info: Optional[MemberInfo] = Field(None, description="Información del miembro (solo para miembros)")
