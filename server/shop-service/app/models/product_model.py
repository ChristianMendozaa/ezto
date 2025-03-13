# app/models/product_model.py

from pydantic import BaseModel, Field, condecimal, validator
from datetime import date
from typing import List, Optional
from enum import Enum

class ProductCategory(str, Enum):
    """
    Categorías disponibles para clasificación de productos.
    
    Valores:
    - SUPLEMENTOS: Productos nutricionales y suplementos dietéticos
    - ROPA: Indumentaria deportiva y accesorios de vestir
    - EQUIPO: Equipamiento de entrenamiento y maquinaria
    - ACCESORIOS: Accesorios deportivos menores
    - BEBIDAS: Bebidas energéticas y suplementos líquidos
    - OTROS: Categoría genérica para productos no clasificados
    """
    SUPLEMENTOS = "suplementos"
    ROPA = "ropa"
    EQUIPO = "equipo"
    ACCESORIOS = "accesorios"
    BEBIDAS = "bebidas"
    OTROS = "otros"

class ProductStatus(str, Enum):
    """
    Estados de disponibilidad de un producto en el inventario.
    
    Valores:
    - ACTIVO: Producto disponible para venta
    - DESCONTINUADO: Producto retirado del catálogo
    - AGOTADO: Producto temporalmente sin stock
    """
    ACTIVO = "activo"
    DESCONTINUADO = "descontinuado"
    AGOTADO = "agotado"

class ProductBase(BaseModel):
    """
    Modelo base para la gestión de productos en el inventario.
    
    Atributos:
    - name: Nombre comercial del producto
    - sku: Identificador único del producto (formato: 8-15 caracteres alfanuméricos con guiones)
    - category: Clasificación principal del producto
    - description: Detalles técnicos o características relevantes
    - purchase_price: Costo unitario de adquisición
    - sale_price: Precio unitario de venta al público
    - current_stock: Unidades disponibles en inventario
    - min_stock: Umbral mínimo para alertas de reabastecimiento
    - expiration_date: Fecha límite de consumo/uso (si aplica)
    - supplier_id: Identificador único del proveedor
    - barcode: Código de barras para escaneo (opcional)
    - status: Estado actual en el sistema de inventario
    - image_base64: Imagen del producto en formato Base64 (opcional)
    """
    name: str = Field(
        ...,
        min_length=3, 
        max_length=100, 
        example="Proteína Whey 2kg",
        description="Nombre comercial del producto"
    )
    sku: str = Field(
        ...,
        pattern=r'^[A-Z0-9\-]{8,15}$',
        example="PROT-WHEY-01",
        description="Código único identificador (8-15 caracteres, mayúsculas, números y guiones)"
    )
    category: ProductCategory = Field(
        ...,
        example=ProductCategory.SUPLEMENTOS,
        description="Clasificación principal del producto"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        example="Proteína de suero de leche isolate, sabor vainilla",
        description="Características técnicas y detalles del producto"
    )
    purchase_price: condecimal(gt=0) = Field(
        ...,
        example=25.99,
        description="Costo unitario de compra al proveedor (USD)"
    )
    sale_price: condecimal(gt=0) = Field(
        ...,
        example=39.99,
        description="Precio unitario de venta al público (USD)"
    )
    current_stock: int = Field(
        0,
        ge=0,
        example=50,
        description="Unidades físicamente disponibles en inventario"
    )
    min_stock: int = Field(
        5,
        ge=0,
        example=10,
        description="Cantidad mínima para activar alerta de reposición"
    )
    expiration_date: Optional[date] = Field(
        None,
        example="2025-12-31",
        description="Fecha de caducidad (para productos perecederos)"
    )
    supplier_id: str = Field(
        ...,
        example="SUP-001",
        description="Identificador único del proveedor registrado"
    )
    barcode: Optional[str] = Field(
        None,
        example="123456789012",
        description="Código de barras EAN-13 o UPC (opcional)"
    )
    status: ProductStatus = Field(
        ProductStatus.ACTIVO,
        example=ProductStatus.ACTIVO,
        description="Estado actual en el sistema de inventario"
    )
    image_base64: Optional[str] = Field(
        None,
        description="Imagen del producto en formato Base64"
    )

    @validator("sale_price")
    def validate_prices(cls, v, values):
        """
        Valida que el precio de venta sea mayor al de compra.
        
        Args:
            v (float): Valor del precio de venta
            values (dict): Diccionario con los demás valores del modelo
            
        Raises:
            ValueError: Si el precio de venta es menor o igual al de compra
        """
        if "purchase_price" in values and v <= values["purchase_price"]:
            raise ValueError("El precio de venta debe ser mayor al precio de compra")
        return v

class ProductResponse(ProductBase):
    """
    Modelo de respuesta para operaciones con productos, incluye campos calculados y de auditoría.
    
    Atributos Adicionales:
    - id: Identificador único en la base de datos
    - created_at: Fecha de registro inicial
    - last_updated: Fecha de última modificación
    - profit_margin: Margen de ganancia calculado (porcentaje)
    """
    id: str = Field(
        ...,
        example="6489a5d2fae8b1b9f7654321",
        description="ID único generado por la base de datos"
    )
    created_at: date = Field(
        ...,
        example="2023-06-12",
        description="Fecha de creación del registro"
    )
    last_updated: date = Field(
        ...,
        example="2023-06-15",
        description="Fecha de última actualización"
    )
    profit_margin: float = Field(
        ...,
        example=53.8,
        description="Margen de ganancia porcentual calculado ((sale_price - purchase_price)/purchase_price * 100)"
    )

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "6489a5d2fae8b1b9f7654321",
                "name": "Proteína Whey 2kg",
                "sku": "PROT-WHEY-01",
                "category": "suplementos",
                "description": "Proteína de suero de leche isolate, sabor vainilla",
                "purchase_price": 25.99,
                "sale_price": 39.99,
                "current_stock": 50,
                "min_stock": 10,
                "expiration_date": "2025-12-31",
                "supplier_id": "SUP-001",
                "barcode": "123456789012",
                "status": "activo",
                "image_base64": "iVBORw0KGgoAAAANSUhEUgAAA...",
                "created_at": "2023-06-12",
                "last_updated": "2023-06-15",
                "profit_margin": 53.8
            }
        }
