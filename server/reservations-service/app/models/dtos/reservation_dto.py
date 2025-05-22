from pydantic import BaseModel, Field, constr, validator
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    # Sólo para anotaciones de tipo, no se ejecuta en tiempo de importación
    from app.models.reservation_model import ReservationEntity

class ReservationStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class ReservationDTO(BaseModel):
    id: Optional[str] = Field(None, description="ID único de la reserva")
    user_id: constr(min_length=3, max_length=50) = Field(..., description="ID del usuario que realiza la reserva")
    class_id: constr(min_length=3, max_length=50) = Field(..., description="ID de la clase reservada")
    reservation_date: datetime = Field(default_factory=datetime.utcnow, description="Fecha y hora de la reserva")
    status: ReservationStatus = Field(default=ReservationStatus.ACTIVE, description="Estado de la reserva")

    @validator("reservation_date")
    def no_past(cls, v):
        if v < datetime.utcnow():
            raise ValueError("La fecha de la reserva no puede ser en el pasado.")
        return v

    def to_entity(self, entity_id: Optional[str] = None) -> "ReservationEntity":
        # import interno: aquí sí existe ReservationEntity
        from app.models.reservation_model import ReservationEntity

        return ReservationEntity(
            id=self.id or entity_id,
            user_id=self.user_id,
            class_id=self.class_id,
            reservation_date=self.reservation_date,
            status=self.status
        )
