from dataclasses import dataclass
from datetime import date
from typing import Optional
from enum import Enum

class DiscountType(str, Enum):
    PERCENTAGE = "percentage"
    FIXED = "fixed"
    FREE_MONTH = "free_month"

class ApplicableTo(str, Enum):
    ALL_USERS = "all_users"
    NEW_USERS = "new_users"
    LOYAL_USERS = "loyal_users"
    SPECIFIC_PLAN = "specific_plan"

@dataclass
class PromotionEntity:
    id: Optional[str]
    name: str
    description: str
    start_date: date
    end_date: date
    discount_type: DiscountType
    discount_value: int
    applicable_to: ApplicableTo
    auto_apply: bool
    promo_code: Optional[str]
    status: bool

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "discount_type": self.discount_type.value,
            "discount_value": self.discount_value,
            "applicable_to": self.applicable_to.value,
            "auto_apply": self.auto_apply,
            "promo_code": self.promo_code,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: dict) -> "PromotionEntity":
        try:
            return PromotionEntity(
                id=data.get("id"),
                name=data["name"],
                description=data["description"],
                start_date=date.fromisoformat(data["start_date"]),
                end_date=date.fromisoformat(data["end_date"]),
                discount_type=DiscountType(data["discount_type"]),
                discount_value=int(data["discount_value"]),
                applicable_to=ApplicableTo(data["applicable_to"]),
                auto_apply=bool(data["auto_apply"]),
                promo_code=data.get("promo_code"),
                status=bool(data["status"])
            )
        except Exception as e:
            raise ValueError(f"Error al convertir documento a PromotionEntity: {e}")

    def to_dto(self) -> "PromotionDTO":
        from app.models.dtos.promotion_dto import PromotionDTO
        return PromotionDTO(
            id=self.id,
            name=self.name,
            description=self.description,
            start_date=self.start_date,
            end_date=self.end_date,
            discount_type=self.discount_type,
            discount_value=self.discount_value,
            applicable_to=self.applicable_to,
            auto_apply=self.auto_apply,
            promo_code=self.promo_code,
            status=self.status
        )
