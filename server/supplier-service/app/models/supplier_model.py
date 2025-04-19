from pydantic import BaseModel, Field, EmailStr, field_validator, validator
from typing import Optional
from enum import Enum
from datetime import date

class SupplierStatus(str, Enum):
    """
    Estados posibles de un proveedor.
    
    Valores:
    - ACTIVO, INACTIVO, SUSPENDIDO
    """
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    SUSPENDIDO = "suspendido"

class SupplierBase(BaseModel):
    """
    Modelo base para la gestión de proveedores.
    
    Atributos:
    - name: Nombre del proveedor (no vacío)
    - contact_email: Email de contacto (válido)
    - phone: Teléfono con código de país (no vacío, patrón específico)
    - address: Dirección física (no vacío)
    - tax_id: Identificación fiscal (no vacío)
    - payment_terms: Términos de pago (no vacío)
    - status: Estado actual
    """
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        example="Suplementos Fitness S.A.",
        description="Nombre del proveedor"
    )
    contact_email: EmailStr = Field(
        ...,
        example="contacto@suplementosfitness.com",
        description="Email de contacto"
    )
    phone: str = Field(
        ...,
        pattern=r'^\+?[1-9]\d{7,14}$',
        example="+573001234567",
        description="Teléfono con código de país"
    )
    address: str = Field(
        ...,
        example="Calle 123 #45-67, Bogotá, Colombia",
        description="Dirección física"
    )
    tax_id: str = Field(
        ...,
        example="123456789-1",
        description="Identificación fiscal"
    )
    payment_terms: str = Field(
        "30 días",
        example="30 días",
        description="Términos de pago"
    )
    status: SupplierStatus = Field(
        SupplierStatus.ACTIVO,
        example=SupplierStatus.ACTIVO,
        description="Estado del proveedor"
    )

    @field_validator("name", "address", "tax_id", "payment_terms", "phone")
    def non_empty_string(cls, v, field):
        if not v or not v.strip():
            raise ValueError(f"{field.name} no puede estar vacío")
        return v

class SupplierCreate(SupplierBase):
    """
    Modelo para crear un nuevo proveedor.
    """
    pass

class SupplierResponse(SupplierBase):
    """
    Respuesta para operaciones con proveedores.
    
    Atributos adicionales:
    - id: ID único (no vacío)
    - created_at: Fecha de creación
    - last_updated: Fecha de última actualización
    - products_offered: Cantidad de productos asociados
    """
    id: str = Field(
        ...,
        example="6489a5d2fae8b1b9f7654321",
        description="ID del proveedor"
    )
    created_at: date = Field(
        ...,
        example="2023-06-12",
        description="Fecha de creación"
    )
    last_updated: date = Field(
        ...,
        example="2023-06-15",
        description="Fecha de última actualización"
    )
    products_offered: int = Field(
        ...,
        example=15,
        description="Productos asociados"
    )

    @field_validator("id")
    def id_non_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("id no puede estar vacío")
        return v

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "6489a5d2fae8b1b9f7654321",
                "name": "Suplementos Fitness S.A.",
                "contact_email": "contacto@suplementosfitness.com",
                "phone": "+573001234567",
                "address": "Calle 123 #45-67, Bogotá, Colombia",
                "tax_id": "123456789-1",
                "payment_terms": "30 días",
                "status": "activo",
                "created_at": "2023-06-12",
                "last_updated": "2023-06-15",
                "products_offered": 15
            }
        }
