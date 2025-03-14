from pydantic import BaseModel, Field, condecimal, field_validator, validator
from datetime import datetime
from typing import List, Optional
from enum import Enum

class PaymentMethod(str, Enum):
    """
    Métodos de pago aceptados.
    
    Valores:
    - EFECTIVO, TARJETA_CREDITO, TARJETA_DEBITO, TRANSFERENCIA, APP
    """
    EFECTIVO = "efectivo"
    TARJETA_CREDITO = "tarjeta_credito"
    TARJETA_DEBITO = "tarjeta_debito"
    TRANSFERENCIA = "transferencia"
    APP = "app_movil"

class SaleStatus(str, Enum):
    """
    Estados de una transacción de venta.
    
    Valores:
    - COMPLETADA, PENDIENTE, CANCELADA, DEVUELTA
    """
    COMPLETADA = "completada"
    PENDIENTE = "pendiente"
    CANCELADA = "cancelada"
    DEVUELTA = "devuelta"

class SaleItem(BaseModel):
    """
    Ítem de una venta.
    
    Atributos:
    - product_id: ID del producto (no vacío)
    - quantity: Unidades vendidas (>0)
    - unit_price: Precio unitario (>0)
    - discount: Descuento por unidad (>=0)
    """
    product_id: str = Field(
        ...,
        example="6489a5d2fae8b1b9f7654321",
        description="ID del producto vendido"
    )
    quantity: int = Field(
        ...,
        gt=0,
        example=2,
        description="Cantidad vendida"
    )
    unit_price: condecimal(gt=0) = Field(
        ...,
        example=39.99,
        description="Precio unitario"
    )
    discount: condecimal(ge=0) = Field(
        0,
        example=5.00,
        description="Descuento aplicado"
    )

    @field_validator("product_id")
    def product_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("product_id no puede estar vacío")
        return v

class SaleCreate(BaseModel):
    """
    Creación de una nueva venta.
    
    Atributos:
    - client_id: ID del cliente (no vacío)
    - items: Lista de ítems (al menos 1)
    - payment_method: Método de pago
    - notes: Observaciones (opcional, máximo 500 caracteres)
    """
    client_id: str = Field(
        ...,
        example="6489a5d2fae8b1b9f7654321",
        description="ID del cliente"
    )
    items: List[SaleItem] = Field(
        ...,
        min_items=1,
        description="Lista de ítems vendidos"
    )
    payment_method: PaymentMethod = Field(
        ...,
        example=PaymentMethod.TARJETA_CREDITO,
        description="Método de pago"
    )
    notes: Optional[str] = Field(
        None,
        max_length=500,
        example="Cliente preferencial, aplicar descuento adicional",
        description="Observaciones"
    )

    @field_validator("client_id")
    def client_id_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("client_id no puede estar vacío")
        return v

class SaleResponse(SaleCreate):
    """
    Respuesta de una venta.
    
    Atributos adicionales:
    - sale_id: ID de la transacción (no vacío)
    - total_amount: Monto total (>0)
    - tax_amount: Impuestos (>=0)
    - sale_date: Fecha y hora de la venta
    - seller_id: ID del vendedor (no vacío)
    - invoice_number: Número de factura (opcional, si se proporciona, no vacío)
    - status: Estado de la transacción
    """
    sale_id: str = Field(
        ...,
        example="6489a5d2fae8b1b9f7654321",
        description="ID de la venta"
    )
    total_amount: condecimal(gt=0) = Field(
        ...,
        example=74.98,
        description="Monto total"
    )
    tax_amount: condecimal(ge=0) = Field(
        ...,
        example=11.25,
        description="Impuestos aplicados"
    )
    sale_date: datetime = Field(
        ...,
        example="2023-06-15T14:30:00",
        description="Fecha y hora de la venta"
    )
    seller_id: str = Field(
        ...,
        example="6489a5d2fae8b1b9f7654321",
        description="ID del vendedor"
    )
    invoice_number: Optional[str] = Field(
        None,
        example="FAC-001-000123",
        description="Número de factura"
    )
    status: SaleStatus = Field(
        ...,
        example=SaleStatus.COMPLETADA,
        description="Estado de la venta"
    )

    @field_validator("sale_id", "seller_id")
    def non_empty_string(cls, v, field):
        if not v or not v.strip():
            raise ValueError(f"{field.name} no puede estar vacío")
        return v

    @field_validator("invoice_number")
    def invoice_number_non_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError("invoice_number no puede estar vacío si se proporciona")
        return v

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "sale_id": "6489a5d2fae8b1b9f7654321",
                "client_id": "6489a5d2fae8b1b9f7654321",
                "items": [
                    {
                        "product_id": "6489a5d2fae8b1b9f7654321",
                        "quantity": 2,
                        "unit_price": 39.99,
                        "discount": 5.00
                    }
                ],
                "payment_method": "tarjeta_credito",
                "notes": "Cliente preferencial, aplicar descuento adicional",
                "total_amount": 74.98,
                "tax_amount": 11.25,
                "sale_date": "2023-06-15T14:30:00",
                "seller_id": "6489a5d2fae8b1b9f7654321",
                "invoice_number": "FAC-001-000123",
                "status": "completada"
            }
        }
