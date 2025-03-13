from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class MovementType(str, Enum):
    """
    Tipos de movimientos de inventario.
    
    Valores:
    - ENTRADA: Ingreso de productos al inventario
    - SALIDA: Salida de productos del inventario
    - AJUSTE: Corrección de inventario
    - DEVOLUCION: Devolución de productos
    """
    ENTRADA = "entrada"
    SALIDA = "salida"
    AJUSTE = "ajuste"
    DEVOLUCION = "devolucion"

class InventoryMovement(BaseModel):
    """
    Modelo para registrar movimientos de inventario.
    
    Atributos:
    - product_id: Identificador único del producto afectado
    - movement_type: Tipo de movimiento realizado
    - quantity: Cantidad de unidades afectadas
    - reason: Justificación del movimiento
    - reference_id: Identificador de la transacción relacionada
    - movement_date: Fecha y hora del movimiento
    - responsible_id: Identificador del usuario responsable
    """
    product_id: str = Field(...,
                          example="6489a5d2fae8b1b9f7654321",
                          description="Identificador único del producto afectado")
    
    movement_type: MovementType = Field(...,
                                      example=MovementType.ENTRADA,
                                      description="Tipo de movimiento realizado")
    
    quantity: int = Field(...,
                        example=50,
                        description="Cantidad de unidades afectadas")
    
    reason: str = Field(...,
                      max_length=200,
                      example="Compra a proveedor SUP-001",
                      description="Justificación del movimiento")
    
    reference_id: str = Field(...,
                            example="6489a5d2fae8b1b9f7654321",
                            description="Identificador de la transacción relacionada")
    
    movement_date: datetime = Field(default_factory=datetime.now,
                                  example="2023-06-15T14:30:00",
                                  description="Fecha y hora del movimiento")
    
    responsible_id: str = Field(...,
                              example="6489a5d2fae8b1b9f7654321",
                              description="Identificador del usuario responsable")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "product_id": "6489a5d2fae8b1b9f7654321",
                "movement_type": "entrada",
                "quantity": 50,
                "reason": "Compra a proveedor SUP-001",
                "reference_id": "6489a5d2fae8b1b9f7654321",
                "movement_date": "2023-06-15T14:30:00",
                "responsible_id": "6489a5d2fae8b1b9f7654321"
            }
        }