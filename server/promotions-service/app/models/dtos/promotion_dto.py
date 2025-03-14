from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum

class DiscountType(str, Enum):
    percentage = "percentage"
    fixed = "fixed"
    free_month = "free_month"

class ApplicableTo(str, Enum):
    all_users = "all_users"
    new_users = "new_users"
    loyal_users = "loyal_users"
    specific_plan = "specific_plan"

class Status(str, Enum):
    active = "active"
    inactive = "inactive"

class PromotionDTO(BaseModel):
    name: str = Field(..., description="Nombre de la promoción")
    description: str = Field(..., description="Descripción de la promoción")
    start_date: date = Field(..., description="Fecha de inicio en formato ISO (YYYY-MM-DD)")
    end_date: date = Field(..., description="Fecha de finalización en formato ISO (YYYY-MM-DD)")
    discount_type: DiscountType = Field(..., description="Tipo de descuento válido")
    discount_value: int = Field(..., description="Valor del descuento")
    applicable_to: ApplicableTo = Field(..., description="A quién aplica la promoción")
    auto_apply: bool = Field(..., description="Indica si la promoción se aplica automáticamente")
    promo_code: Optional[str] = Field(None, description="Código de promoción, si aplica")
    status: Status = Field(default=Status.active, description="Estado de la promoción")

    class Config:
        schema_extra = {
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
                "status": "active"
            }
        }
