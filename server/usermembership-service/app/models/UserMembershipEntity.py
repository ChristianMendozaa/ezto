#app/models/UserMembershipEntity.py
from dataclasses import dataclass
from datetime import date
from typing import Optional
from enum import Enum


class MembershipStatus(str, Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


@dataclass
class UserMembershipEntity:
    id: Optional[str]               # ID único de la membresía (Firestore lo genera)
    user_id: str                    # ID del usuario
    plan_id: str                    # ID del plan al que pertenece esta membresía
    start_date: date               # Fecha de inicio
    end_date: date                 # Fecha de expiración
    status: MembershipStatus       # Estado de la membresía
    promotion_id: Optional[str]    # ID de la promoción aplicada (si existe)
    final_price: float             # Precio final que pagó el usuario (con descuento si aplica)
    auto_renew: bool               # Si se renovará automáticamente

    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario compatible con Firestore"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "plan_id": self.plan_id,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "status": self.status.value,
            "promotion_id": self.promotion_id,
            "final_price": self.final_price,
            "auto_renew": self.auto_renew
        }

    @staticmethod
    def from_dict(data: dict) -> "UserMembershipEntity":
        """Crea una entidad desde un documento Firestore"""
        try:
            return UserMembershipEntity(
                id=data.get("id"),
                user_id=data.get("user_id", ""),
                plan_id=data.get("plan_id", ""),
                start_date=date.fromisoformat(data.get("start_date")),
                end_date=date.fromisoformat(data.get("end_date")),
                status=MembershipStatus(data.get("status", "active")),
                promotion_id=data.get("promotion_id"),
                final_price=float(data.get("final_price", 0)),
                auto_renew=bool(data.get("auto_renew", False))
            )
        except Exception as e:
            raise ValueError(f"Error al convertir documento a UserMembershipEntity: {e}")

    def to_dto(self) -> "UserMembershipDTO":
        from app.models.dtos.UserMembershipDTO import UserMembershipDTO
        return UserMembershipDTO(
            #id=self.id,  # si se quiere incluirlo en el DTO
            user_id=self.user_id,
            plan_id=self.plan_id,
            start_date=self.start_date,
            end_date=self.end_date,
            status=self.status,
            promotion_id=self.promotion_id,
            final_price=self.final_price,
            auto_renew=self.auto_renew
        )


