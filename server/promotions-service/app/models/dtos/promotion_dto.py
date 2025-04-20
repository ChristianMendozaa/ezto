from pydantic import BaseModel, Field, constr, conint, validator
from typing import Optional
from datetime import date
from enum import Enum

# Enums
class DiscountType(str, Enum):
    percentage = "percentage"
    fixed = "fixed"
    free_month = "free_month"

class ApplicableTo(str, Enum):
    all_users = "all_users"
    new_users = "new_users"
    loyal_users = "loyal_users"
    specific_plan = "specific_plan"

# DTO principal
class PromotionDTO(BaseModel):
    id: Optional[str] = Field(None, description="ID de la promoción")
    name: constr(min_length=3, max_length=50) = Field(..., description="Nombre de la promoción")
    description: constr(min_length=10, max_length=255) = Field(..., description="Descripción de la promoción")
    start_date: date = Field(..., description="Fecha de inicio en formato ISO (YYYY-MM-DD)")
    end_date: date = Field(..., description="Fecha de finalización en formato ISO (YYYY-MM-DD)")
    discount_type: DiscountType = Field(..., description="Tipo de descuento válido")
    discount_value: conint(gt=0) = Field(..., description="Valor del descuento, debe ser mayor a 0")
    applicable_to: ApplicableTo = Field(..., description="A quién aplica la promoción")
    auto_apply: bool = Field(..., description="Indica si la promoción se aplica automáticamente")
    promo_code: Optional[constr(min_length=3, max_length=20)] = Field(None, description="Código de promoción opcional")
    status: bool = Field(..., description="Estado de la promoción")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Promo Especial 10%",
                "description": "Descuento del 10% en todas las membresías",
                "start_date": "2024-06-01",
                "end_date": "2024-06-30",
                "discount_type": "percentage",
                "discount_value": 10,
                "applicable_to": "new_users",
                "auto_apply": False,
                "promo_code": "VERANO10",
                "status": True
            }
        }

    @validator("end_date")
    def validate_end_date(cls, end_date, values):
        start_date = values.get("start_date")
        if start_date and end_date <= start_date:
            raise ValueError("La fecha de finalización debe ser posterior a la fecha de inicio.")
        return end_date

    def to_entity(self, entity_id: Optional[str] = None) -> "PromotionEntity":
        from app.models.promotion_model import PromotionEntity
        return PromotionEntity(
            id=self.id if hasattr(self, "id") else entity_id,
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
