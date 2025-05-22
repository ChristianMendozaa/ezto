from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from app.models.dtos.reservation_dto import ReservationDTO

class ReservationStatus(str, Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

@dataclass
class ReservationEntity:
    id: Optional[str]
    user_id: str
    class_id: str
    reservation_date: datetime
    status: ReservationStatus

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "class_id": self.class_id,
            "reservation_date": self.reservation_date.isoformat(),
            "status": self.status.value
        }

    @staticmethod
    def from_dict(data: dict) -> "ReservationEntity":
        return ReservationEntity(
            id=data.get("id"),
            user_id=data["user_id"],
            class_id=data["class_id"],
            reservation_date=datetime.fromisoformat(data["reservation_date"]),
            status=ReservationStatus(data["status"])
        )

    def to_dto(self) -> "ReservationDTO":
        # import interno: aquí sí existe ReservationDTO
        from app.models.dtos.reservation_dto import ReservationDTO

        return ReservationDTO(
            id=self.id,
            user_id=self.user_id,
            class_id=self.class_id,
            reservation_date=self.reservation_date,
            status=self.status
        )
