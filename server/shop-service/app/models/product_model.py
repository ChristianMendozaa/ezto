from pydantic import BaseModel, Field, condecimal, field_validator, FieldValidationInfo
from datetime import date
from typing import Optional
from enum import Enum
import base64

class ProductCategory(str, Enum):
    """
    Categorías disponibles para clasificación de productos.
    
    Valores:
    - SUPLEMENTOS, ROPA, EQUIPO, ACCESORIOS, BEBIDAS, OTROS
    """
    SUPLEMENTOS = "suplementos"
    ROPA = "ropa"
    EQUIPO = "equipo"
    ACCESORIOS = "accesorios"
    BEBIDAS = "bebidas"
    OTROS = "otros"

class ProductStatus(str, Enum):
    """
    Estados de disponibilidad de un producto.
    
    Valores:
    - ACTIVO, DESCONTINUADO, AGOTADO
    """
    ACTIVO = "activo"
    DESCONTINUADO = "descontinuado"
    AGOTADO = "agotado"

class ProductBase(BaseModel):
    """
    Modelo base para la gestión de productos.
    
    Atributos:
    - name: Nombre comercial (no vacío)
    - sku: Código único (8-15 caracteres, mayúsculas, números y guiones)
    - category: Clasificación principal
    - description: Detalles del producto (opcional)
    - purchase_price: Precio de compra (>0)
    - sale_price: Precio de venta (> purchase_price)
    - current_stock: Stock disponible (>=0)
    - min_stock: Stock mínimo (>=0)
    - expiration_date: Fecha de caducidad (si se proporciona, debe ser futura)
    - supplier_id: Identificador del proveedor (no vacío)
    - barcode: Código de barras (opcional, 12 o 13 dígitos numéricos)
    - status: Estado del producto
    - image_base64: Imagen en Base64 (opcional, formato válido)
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
        description="Código único (8-15 caracteres, mayúsculas, números y guiones)"
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
        description="Detalles del producto"
    )
    purchase_price: condecimal(gt=0) = Field(
        ...,
        example=25.99,
        description="Precio de compra (USD)"
    )
    sale_price: condecimal(gt=0) = Field(
        ...,
        example=39.99,
        description="Precio de venta (USD)"
    )
    current_stock: int = Field(
        0,
        ge=0,
        example=50,
        description="Stock disponible"
    )
    min_stock: int = Field(
        5,
        ge=0,
        example=10,
        description="Stock mínimo para alerta"
    )
    expiration_date: Optional[date] = Field(
        None,
        example="2025-12-31",
        description="Fecha de caducidad (si aplica)"
    )
    supplier_id: str = Field(
        ...,
        example="SUP-001",
        description="ID del proveedor"
    )
    barcode: Optional[str] = Field(
        None,
        example="123456789012",
        description="Código de barras (EAN-13 o UPC)"
    )
    status: ProductStatus = Field(
        ProductStatus.ACTIVO,
        example=ProductStatus.ACTIVO,
        description="Estado del producto"
    )
    image_base64: Optional[str] = Field(
        None,
        description="Imagen en formato Base64"
    )

    @field_validator("sale_price")
    def validate_prices(cls, sale_price, info: FieldValidationInfo): # type: ignore
        """
        Asegura que sale_price sea mayor que purchase_price.
        En Pydantic V2, info.data es donde encontramos los demás campos del modelo.
        """
        data = info.data  # dict con todos los valores
        purchase_price = data.get("purchase_price")
        if purchase_price is not None and sale_price <= purchase_price:
            raise ValueError("El precio de venta debe ser mayor al precio de compra")
        return sale_price

    @field_validator("name", "supplier_id")
    def non_empty_string(cls, v, field):
        if not v or not v.strip():
            raise ValueError(f"{field.name} no puede estar vacío")
        return v

    @field_validator("expiration_date")
    def expiration_date_future(cls, v):
        from datetime import date
        if v is not None and v < date.today():
            raise ValueError("La fecha de caducidad debe ser una fecha futura")
        return v

    @field_validator("barcode")
    def validate_barcode(cls, v):
        if v is not None:
            if not v.isdigit() or len(v) not in (12, 13):
                raise ValueError("El código de barras debe ser numérico y contener 12 o 13 dígitos")
        return v

    @field_validator("image_base64")
    def validate_image_base64(cls, v):
        if v is not None:
            try:
                base64.b64decode(v, validate=True)
            except Exception:
                raise ValueError("La imagen debe estar en formato Base64 válido")
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
        from_attributes = True  # Antes: orm_mode = True
        json_schema_extra = {   # Antes: schema_extra = { ... }
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