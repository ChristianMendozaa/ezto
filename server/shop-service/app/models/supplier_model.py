from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from enum import Enum
from datetime import date

class SupplierStatus(str, Enum):
    """
    Estados posibles de un proveedor en el sistema.
    
    Valores:
    - ACTIVO: Proveedor disponible para realizar pedidos
    - INACTIVO: Proveedor temporalmente deshabilitado
    - SUSPENDIDO: Proveedor bloqueado por incumplimientos
    """
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    SUSPENDIDO = "suspendido"

class SupplierBase(BaseModel):
    """
    Modelo base para la gestión de proveedores.
    
    Atributos:
    - name: Nombre legal o comercial del proveedor
    - contact_email: Correo electrónico principal de contacto
    - phone: Número de teléfono con código de país
    - address: Dirección física de la sede principal
    - tax_id: Identificación fiscal (RUC, NIT, etc.)
    - payment_terms: Términos de pago acordados
    - status: Estado actual del proveedor en el sistema
    """
    name: str = Field(...,
                    min_length=3,
                    max_length=100,
                    example="Suplementos Fitness S.A.",
                    description="Nombre legal o comercial del proveedor")
    
    contact_email: EmailStr = Field(...,
                                  example="contacto@suplementosfitness.com",
                                  description="Correo electrónico principal de contacto")
    
    phone: str = Field(...,
                      pattern=r'^\+?[1-9]\d{7,14}$',
                      example="+573001234567",
                      description="Número de teléfono con código de país")
    
    address: str = Field(...,
                        example="Calle 123 #45-67, Bogotá, Colombia",
                        description="Dirección física de la sede principal")
    
    tax_id: str = Field(...,
                       example="123456789-1",
                       description="Identificación fiscal (RUC, NIT, etc.)")
    
    payment_terms: str = Field("30 días",
                              example="30 días",
                              description="Términos de pago acordados con el proveedor")
    
    status: SupplierStatus = Field(SupplierStatus.ACTIVO,
                                 example=SupplierStatus.ACTIVO,
                                 description="Estado actual del proveedor en el sistema")

class SupplierCreate(SupplierBase):
    """
    Modelo para la creación de nuevos proveedores.
    Hereda todos los campos de SupplierBase.
    """
    pass

class SupplierResponse(SupplierBase):
    """
    Modelo de respuesta para operaciones con proveedores.
    
    Atributos Adicionales:
    - id: Identificador único en la base de datos
    - created_at: Fecha de registro inicial
    - last_updated: Fecha de última modificación
    - products_offered: Cantidad de productos activos asociados
    """
    id: str = Field(...,
                  example="6489a5d2fae8b1b9f7654321",
                  description="ID único generado por la base de datos")
    
    created_at: date = Field(...,
                           example="2023-06-12",
                           description="Fecha de creación del registro")
    
    last_updated: date = Field(...,
                             example="2023-06-15",
                             description="Fecha de última actualización")
    
    products_offered: int = Field(...,
                                example=15,
                                description="Cantidad de productos activos asociados al proveedor")

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