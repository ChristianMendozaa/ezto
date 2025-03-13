from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Promotion(BaseModel):
    name: str = Field(..., description="Nombre de la promoción")
    description: str = Field(..., description="Descripción de la promoción")
    start_date: str = Field(..., description="Fecha de inicio de la promoción")
    end_date: str = Field(..., description="Fecha de finalización de la promoción")
    discount_type: str = Field(..., description="Tipo de descuento (percentage, fixed, free_month)")
    discount_value: int = Field(..., description="Valor del descuento (porcentaje, cantidad fija, o '1 Month' para meses gratis)")
    applicable_to: str = Field(..., description="A quién aplica la promoción (all_users, new_users, loyal_users, specific_plan)")
    auto_apply: bool = Field(..., description="Indica si la promoción se aplica automáticamente o requiere un código")
    promo_code: Optional[str] = Field(None, description="Código de promoción, si aplica")
    status: str = Field("active", description="Estado de la promoción (active, inactive)")
