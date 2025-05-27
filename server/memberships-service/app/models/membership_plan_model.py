# app/models/membership_plan_model.py

from dataclasses import dataclass
from typing import Optional, List
from datetime import date

@dataclass
class MembershipPlanEntity:
    id: Optional[str]
    name: str
    description: str
    capacity: int
    duration_months: int
    price: float
    services_offered: List[str]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "capacity": self.capacity,
            "duration_months": self.duration_months,
            "price": self.price,
            "services_offered": self.services_offered
        }

    @staticmethod
    def from_dict(data: dict) -> "MembershipPlanEntity":
        try:
            return MembershipPlanEntity(
                id=data.get("id"),
                name=data["name"],
                description=data["description"],
                capacity=int(data["capacity"]),
                duration_months=int(data["duration_months"]),
                price=float(data["price"]),
                services_offered=list(data["services_offered"])
            )
        except Exception as e:
            raise ValueError(f"Error al convertir dict a MembershipPlanEntity: {e}")

    def to_dto(self) -> "MembershipPlanDTO":
        from app.models.dtos.membership_plan_dto import MembershipPlanDTO
        return MembershipPlanDTO(
            id=self.id,
            name=self.name,
            description=self.description,
            capacity=self.capacity,
            duration_months=self.duration_months,
            price=self.price,
            services_offered=self.services_offered
        )
