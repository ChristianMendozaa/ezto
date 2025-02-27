from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date

# Información del Gimnasio (Si el usuario es dueño de un gimnasio)
class GymInfo(BaseModel):
    name: str
    address: str
    phone: str
    opening_hours: str
    services_offered: List[str]
    capacity: int
    social_media: Optional[str]

# Información del Miembro de Gimnasio
class MemberInfo(BaseModel):
    gym_id: str
    membership_number: Optional[str]
    birth_date: date
    gender: Optional[str]
    training_goals: List[str]
    activity_preferences: List[str]

# Modelo principal para el registro de usuarios
class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    confirm_password: str
    phone: str
    user_type: str = Field(..., pattern="^(gym_owner|gym_member)$")
    gym_info: Optional[GymInfo] = None
    member_info: Optional[MemberInfo] = None
