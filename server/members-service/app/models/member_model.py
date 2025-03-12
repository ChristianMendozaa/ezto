from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
from datetime import datetime

class MemberStatus(str, Enum):
    active = "activo"
    inactive = "inactivo"
    suspended = "suspendido"

class Member(BaseModel):
    """
    Modelo para la creación y gestión de miembros.
    """
    name: str = Field(..., title="Nombre del Miembro", description="Nombre del miembro.")
    email: str = Field(..., title="Correo Electrónico", description="Correo electrónico del miembro.")
    nfc_id: Optional[str] = Field(None, title="ID de NFC", description="ID de la tarjeta NFC del miembro.")
    status: MemberStatus = Field(..., title="Estado", description="Estado del miembro (activo, inactivo, suspendido).")
    join_date: datetime = Field(..., title="Fecha de Ingreso", description="Fecha de registro del miembro.")
    
    class Config:
        # Configura la conversión entre tipos de Pydantic y los tipos utilizados por Firebase
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Convierte datetime a string ISO 8601 para Firebase
        }
