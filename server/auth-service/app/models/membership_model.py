from pydantic import BaseModel, Field
from typing import Optional

class MembershipPlan(BaseModel):
    """
    Modelo para la creación y gestión de planes de membresía.
    """
    name: str = Field(..., title="Nombre del Plan", description="Nombre del plan de membresía.")
    price: float = Field(..., title="Precio", description="Costo del plan de membresía.")
    duration_months: int = Field(..., title="Duración", description="Duración del plan en meses.")
    description: Optional[str] = Field(None, title="Descripción", description="Descripción opcional del plan de membresía.")

class MembershipAssignment(BaseModel):
    """
    Modelo para la asignación de membresías a usuarios.
    """
    user_id: str = Field(..., title="ID del Usuario", description="Identificador único del usuario.")
    plan_id: str = Field(..., title="ID del Plan", description="Identificador único del plan de membresía.")
    start_date: str = Field(..., title="Fecha de Inicio", description="Fecha de inicio de la membresía.")
    end_date: str = Field(..., title="Fecha de Finalización", description="Fecha de finalización de la membresía.")

class MembershipRenewal(BaseModel):
    """
    Modelo para la renovación automática de membresías.
    """
    user_id: str = Field(..., title="ID del Usuario", description="Identificador único del usuario.")
    plan_id: str = Field(..., title="ID del Plan", description="Identificador único del plan de membresía.")
    renew: bool = Field(..., title="Renovación Automática", description="Indica si la membresía se renovará automáticamente.")

class MembershipCancellation(BaseModel):
    """
    Modelo para la cancelación de membresías.
    """
    user_id: str = Field(..., title="ID del Usuario", description="Identificador único del usuario.")
    plan_id: str = Field(..., title="ID del Plan", description="Identificador único del plan de membresía.")
    reason: Optional[str] = Field(None, title="Razón", description="Razón opcional para la cancelación.")