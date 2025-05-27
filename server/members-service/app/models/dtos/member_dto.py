from pydantic import BaseModel, Field, EmailStr, constr, validator
from typing import Optional
from datetime import datetime
from enum import Enum

class MemberStatus(str, Enum):
    active = "activo"
    inactive = "inactivo"
    suspended = "suspendido"

class MemberDTO(BaseModel):
    id: str = Field(None, description="ID del miembro")
    name: constr(min_length=3, max_length=100) = Field(..., description="Nombre del miembro")
    email: str = Field(..., description="Correo electrónico válido del miembro")
    nfc_id: Optional[str] = Field(None, description="ID NFC del miembro (opcional)")
    status: MemberStatus = Field(..., description="Estado del miembro")
    join_date: datetime = Field(..., description="Fecha de ingreso del miembro")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        json_schema_extra = {
            "example": {
                "id": "123abc",
                "name": "Juan Pérez",
                "email": "juan@example.com",
                "nfc_id": "NFC-456789",
                "status": "activo",
                "join_date": "2025-05-23T14:00:00"
            }
        }

    def to_entity(self, entity_id: Optional[str] = None) -> "MemberEntity":
        from app.models.member_model import MemberEntity
        return MemberEntity(
            id=self.id if hasattr(self, "id") else entity_id,
            name=self.name,
            email=self.email,
            nfc_id=self.nfc_id,
            status=self.status,
            join_date=self.join_date
        )

