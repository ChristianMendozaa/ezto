# app/models/personal_model.py

from dataclasses import dataclass, asdict
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

@dataclass
class PersonalEntity:
    id: Optional[str]
    name: str
    role: Role
    schedule: str
    access_level: AccessLevel

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role.value,
            "schedule": self.schedule,
            "access_level": self.access_level.value
        }

    @staticmethod
    def from_dict(data: dict) -> "PersonalEntity":
        try:
            return PersonalEntity(
                id=data.get("id"),
                name=data["name"],
                role=Role(data["role"]),
                schedule=data["schedule"],
                access_level=AccessLevel(data["access_level"])
            )
        except Exception as e:
            raise ValueError(f"Error al convertir documento a PersonalEntity: {e}")

    def to_dto(self) -> "PersonalDTO":
        from app.models.dtos.personal_dto import PersonalDTO
        return PersonalDTO(
            id=self.id,
            name=self.name,
            role=self.role,
            schedule=self.schedule,
            access_level=self.access_level
        )
