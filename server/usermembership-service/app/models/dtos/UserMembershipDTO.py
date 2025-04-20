#app/models/dtos/UserMembershipDTO.py
from pydantic import BaseModel, Field, constr, confloat, validator
from typing import Optional
from datetime import date
from enum import Enum

class MembershipStatus(str, Enum):
    active = "active"
    expired = "expired"
    cancelled = "cancelled"

class UserMembershipDTO(BaseModel):
    id: Optional[str] = Field(None, description="ID de la membresía")
    user_id: constr(min_length=1) = Field(..., description="ID del usuario")
    plan_id: constr(min_length=1) = Field(..., description="ID del plan de membresía")
    start_date: date = Field(..., description="Fecha de inicio de la membresía")
    end_date: date = Field(..., description="Fecha de expiración de la membresía")
    status: MembershipStatus = Field(..., description="Estado actual de la membresía")
    promotion_id: Optional[str] = Field(None, description="ID de la promoción aplicada (si existe)")
    final_price: confloat(gt=0) = Field(..., description="Precio final pagado por la membresía")
    auto_renew: bool = Field(..., description="Indica si la membresía se renovará automáticamente")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user001",
                "plan_id": "plan_mensual",
                "start_date": "2024-06-01",
                "end_date": "2024-07-01",
                "status": "active",
                "promotion_id": "promo10",
                "final_price": 90.0,
                "auto_renew": True
            }
        }
    
    @validator("end_date")
    def validate_dates(cls, end_date, values):
        start_date = values.get("start_date")
        if start_date and end_date <= start_date:
            raise ValueError("La fecha de expiración debe ser posterior a la fecha de inicio.")
        return end_date
    
    def to_entity(self, entity_id: Optional[str] = None) -> "UserMembershipEntity":
        from app.models.UserMembershipEntity import UserMembershipEntity
        return UserMembershipEntity(
            id=self.id if hasattr(self, "id") else entity_id,
            user_id=self.user_id,
            plan_id=self.plan_id,
            start_date=self.start_date,
            end_date=self.end_date,
            status=MembershipStatus(self.status),
            promotion_id=self.promotion_id,
            final_price=self.final_price,
            auto_renew=self.auto_renew
        )

