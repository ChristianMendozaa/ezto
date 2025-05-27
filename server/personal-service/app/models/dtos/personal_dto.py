# app/models/dtos/personal_dto.py

from pydantic import BaseModel, Field, constr
from typing import Optional
from enum import Enum

class Role(str, Enum):
    TRAINER = "trainer"
    RECEPTIONIST = "receptionist"
    MANAGER = "manager"
    MAINTENANCE = "maintenance"

class AccessLevel(str, Enum):
    FULL = "full"
    STANDARD = "standard"
    LIMITED = "limited"

class PersonalDTO(BaseModel):
    id: Optional[str] = Field(None, description="ID del personal")
    name: constr(min_length=3, max_length=100) = Field(..., description="Nombre completo del personal")
    role: Role = Field(..., description="Rol del personal")
    schedule: constr(min_length=5, max_length=100) = Field(..., description="Horario de trabajo, p.ej. 'Mon, Wed, Fri 9AM-5PM'")
    access_level: AccessLevel = Field(..., description="Nivel de acceso dentro del sistema")

    class Config:
        schema_extra = {
            "example": {
                "id": "abc123",
                "name": "John Doe",
                "role": "trainer",
                "schedule": "Mon, Wed, Fri 9AM-5PM",
                "access_level": "full"
            }
        }

    def to_entity(self) -> "PersonalEntity":
        from app.models.personal_model import PersonalEntity
        return PersonalEntity(
            id=self.id,
            name=self.name,
            role=self.role,
            schedule=self.schedule,
            access_level=self.access_level
        )
