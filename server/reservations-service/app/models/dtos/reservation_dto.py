# app/models/dtos/reservation_dto.py

from pydantic import BaseModel, ConfigDict, Field, constr, field_validator
from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone
from enum import Enum

if TYPE_CHECKING:
    from app.models.reservation_model import ReservationEntity

class ReservationStatus(str, Enum):
    ACTIVE    = "active"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class ReservationDTO(BaseModel):
    model_config = ConfigDict(
        # Aquí puedes añadir json_schema_extra para tu ejemplo si lo necesitas
    )

    id: Optional[str] = Field(None, description="ID único de la reserva")
    user_id: constr(min_length=3, max_length=50) = Field(..., description="ID del usuario que realiza la reserva")
    class_id: constr(min_length=3, max_length=50) = Field(..., description="ID de la clase reservada")
    reservation_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Fecha y hora de la reserva (UTC)"
    )
    status: ReservationStatus = Field(default=ReservationStatus.ACTIVE, description="Estado de la reserva")

    @field_validator("reservation_date", mode="before")
    def parse_iso_z(cls, v):
        # 1) Si viene como str con 'Z', lo convertimos a '+00:00'
        if isinstance(v, str):
            if v.endswith("Z"):
                v = v[:-1] + "+00:00"
            # Esto produce un datetime aware de UTC
            return datetime.fromisoformat(v)
        return v

    @field_validator("reservation_date")
    def no_past(cls, v: datetime) -> datetime:
        # 2) Nos aseguramos de que v sea aware y esté en UTC
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        else:
            v = v.astimezone(timezone.utc)
        # 3) Comparamos con el ahora UTC, también aware
        now = datetime.now(timezone.utc)
        if v < now:
            raise ValueError("La fecha de la reserva no puede ser en el pasado.")
        return v

    def to_entity(self, entity_id: Optional[str] = None) -> "ReservationEntity":
        from app.models.reservation_model import ReservationEntity
        return ReservationEntity(
            id=self.id or entity_id,
            user_id=self.user_id,
            class_id=self.class_id,
            reservation_date=self.reservation_date,
            status=self.status
        )
