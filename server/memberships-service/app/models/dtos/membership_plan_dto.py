# app/models/dtos/membership_plan_dto.py

from pydantic import BaseModel, ConfigDict, Field, constr, conint, confloat, validator
from typing import Optional, List
from datetime import date

class MembershipPlanDTO(BaseModel):
    # --- configuración Pydantic v2 ---
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "83yyHgPkXblCHuMZT01z",
                "name": "Plan Premium",
                "description": "Acceso completo a todos los servicios durante 6 meses.",
                "capacity": 30,
                "duration_months": 6,
                "price": 29.99,
                "services_offered": ["Servicio X", "Servicio Y"]
            }
        }
    )

    id: Optional[str] = Field(None, description="ID del plan de membresía")
    name: constr(min_length=3, max_length=100) = Field(..., description="Nombre del plan de membresía")
    description: constr(min_length=10, max_length=255) = Field(..., description="Descripción del plan")
    capacity: conint(gt=0) = Field(..., description="Capacidad máxima de usuarios para este plan")
    duration_months: conint(gt=0) = Field(..., description="Duración del plan en meses")
    price: confloat(gt=0) = Field(..., description="Precio del plan (en la moneda correspondiente)")
    services_offered: List[constr(min_length=1)] = Field(
        ...,
        min_items=1,
        description="Lista de servicios incluidos en el plan (al menos uno)"
    )

    @validator("services_offered")
    def no_services_empty(cls, v):
        if any(not s.strip() for s in v):
            raise ValueError("Cada servicio ofrecido debe ser una cadena no vacía.")
        return v

    def to_entity(self, entity_id: Optional[str] = None) -> "MembershipPlanEntity":
        from app.models.membership_plan_model import MembershipPlanEntity
        return MembershipPlanEntity(
            id=self.id or entity_id,
            name=self.name,
            description=self.description,
            capacity=self.capacity,
            duration_months=self.duration_months,
            price=self.price,
            services_offered=self.services_offered
        )
