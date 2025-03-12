from pydantic import BaseModel, Field, condecimal
from datetime import datetime
from typing import List, Optional
from enum import Enum

class PaymentMethod(str, Enum):
    """
    Métodos de pago aceptados en el sistema.
    
    Valores:
    - EFECTIVO: Pago en efectivo
    - TARJETA_CREDITO: Pago con tarjeta de crédito
    - TARJETA_DEBITO: Pago con tarjeta de débito
    - TRANSFERENCIA: Transferencia bancaria
    - APP: Pago a través de aplicación móvil
    """
    EFECTIVO = "efectivo"
    TARJETA_CREDITO = "tarjeta_credito"
    TARJETA_DEBITO = "tarjeta_debito"
    TRANSFERENCIA = "transferencia"
    APP = "app_movil"

class SaleStatus(str, Enum):
    """
    Estados posibles de una transacción de venta.
    
    Valores:
    - COMPLETADA: Venta finalizada exitosamente
    - PENDIENTE: Venta en proceso de pago
    - CANCELADA: Venta anulada
    - DEVUELTA: Venta con productos devueltos
    """
    COMPLETADA = "completada"
    PENDIENTE = "pendiente"
    CANCELADA = "cancelada"
    DEVUELTA = "devuelta"

class SaleItem(BaseModel):
    """
    Modelo para los ítems incluidos en una venta.
    
    Atributos:
    - product_id: Identificador único del producto vendido
    - quantity: Cantidad de unidades vendidas
    - unit_price: Precio unitario al momento de la venta
    - discount: Descuento aplicado por unidad
    """
    product_id: str = Field(...,
                          example="6489a5d2fae8b1b9f7654321",
                          description="Identificador único del producto vendido")
    
    quantity: int = Field(...,
                        gt=0,
                        example=2,
                        description="Cantidad de unidades vendidas")
    
    unit_price: condecimal(gt=0) = Field(...,
                                       example=39.99,
                                       description="Precio unitario al momento de la venta")
    
    discount: condecimal(ge=0) = Field(0,
                                     example=5.00,
                                     description="Descuento aplicado por unidad")

class SaleCreate(BaseModel):
    """
    Modelo para la creación de una nueva venta.
    
    Atributos:
    - client_id: Identificador único del cliente
    - items: Lista de productos vendidos
    - payment_method: Método de pago utilizado
    - notes: Observaciones adicionales de la venta
    """
    client_id: str = Field(...,
                         example="6489a5d2fae8b1b9f7654321",
                         description="Identificador único del cliente")
    
    items: List[SaleItem] = Field(...,
                                min_items=1,
                                description="Lista de productos vendidos")
    
    payment_method: PaymentMethod = Field(...,
                                        example=PaymentMethod.TARJETA_CREDITO,
                                        description="Método de pago utilizado")
    
    notes: Optional[str] = Field(None,
                               max_length=500,
                               example="Cliente preferencial, aplicar descuento adicional",
                               description="Observaciones adicionales de la venta")

class SaleResponse(SaleCreate):
    """
    Modelo de respuesta para operaciones de venta.
    
    Atributos Adicionales:
    - sale_id: Identificador único de la transacción
    - total_amount: Monto total de la venta
    - tax_amount: Impuestos aplicados
    - sale_date: Fecha y hora exacta de la venta
    - seller_id: Identificador del empleado que realizó la venta
    - invoice_number: Número de factura asociado
    - status: Estado actual de la transacción
    """
    sale_id: str = Field(...,
                       example="6489a5d2fae8b1b9f7654321",
                       description="Identificador único de la transacción")
    
    total_amount: condecimal(gt=0) = Field(...,
                                         example=74.98,
                                         description="Monto total de la venta")
    
    tax_amount: condecimal(ge=0) = Field(...,
                                       example=11.25,
                                       description="Impuestos aplicados")
    
    sale_date: datetime = Field(...,
                              example="2023-06-15T14:30:00",
                              description="Fecha y hora exacta de la venta")
    
    seller_id: str = Field(...,
                         example="6489a5d2fae8b1b9f7654321",
                         description="Identificador del empleado que realizó la venta")
    
    invoice_number: Optional[str] = Field(None,
                                        example="FAC-001-000123",
                                        description="Número de factura asociado")
    
    status: SaleStatus = Field(...,
                             example=SaleStatus.COMPLETADA,
                             description="Estado actual de la transacción")

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