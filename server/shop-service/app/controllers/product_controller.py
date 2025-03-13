"""
Controlador para gestionar los endpoints relacionados con productos.

Proporciona rutas para crear, listar, obtener, actualizar y eliminar productos, 
aplicando validaciones de seguridad y rol (gym_owner).
"""
import traceback
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
from typing import List, Optional
from pydantic import BaseModel, Field
import logging
from app.models.product_model import ProductBase, ProductResponse
from app.services.product_service import ProductService
from app.services.auth_service import AuthService

router = APIRouter()

# Configurar logging
logging.basicConfig(level=logging.INFO)

class ErrorResponse(BaseModel):
    """
    Modelo de respuesta para los casos de error.
    """
    detail: str = Field(..., description="Descripción del error ocurrido.")


@router.post(
    "/",
    summary="Crear un nuevo producto",
    description="Crea un nuevo producto en el inventario. Requiere rol `gym_owner`.",
    response_model=ProductResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse}
    }
)
async def create_product(
    # Campos obligatorios
    name: str = Form(...),
    sku: str = Form(...),
    category: str = Form(...),
    purchase_price: float = Form(...),
    sale_price: float = Form(...),
    current_stock: int = Form(0),
    min_stock: int = Form(5),
    supplier_id: str = Form(...),

    # Campos opcionales
    description: Optional[str] = Form(None),
    expiration_date: Optional[str] = Form(None),
    barcode: Optional[str] = Form(None),
    status: Optional[str] = Form("activo"),

    # Imagen (opcional)
    product_image: UploadFile = File(None),

    # Dependencia de autenticación
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Crea un nuevo producto en la base de datos.
    Se pueden enviar los datos por `multipart/form-data` junto con un archivo de imagen.
    Solo el `gym_owner` puede crear productos.
    """
    try:
        # Construir objeto de datos basado en ProductBase
        product_data = ProductBase(
            name=name,
            sku=sku,
            category=category,
            purchase_price=purchase_price,
            sale_price=sale_price,
            current_stock=current_stock,
            min_stock=min_stock,
            supplier_id=supplier_id,
            description=description,
            expiration_date=expiration_date if expiration_date else None,
            barcode=barcode,
            status=status
        )
        logging.info(f"Datos de producto recibidos: {product_data.dict()}")
        new_product = await ProductService.create_product(product_data, product_image, user)
        logging.info(f"Producto creado exitosamente con ID: {new_product.id}")
        return new_product
    except HTTPException:
        raise
    except Exception as e:
        error_details = traceback.format_exc()
        logging.error("Error en create_product: %s", error_details)
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get(
    "/",
    summary="Listar productos",
    description="Devuelve la lista de todos los productos en el inventario. Requiere usuario autenticado.",
    response_model=List[ProductResponse],
    responses={401: {"model": ErrorResponse}}
)
async def list_products(
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Retorna la lista completa de productos disponibles.
    Cualquier usuario autenticado puede listar productos.
    """
    return await ProductService.get_all_products()


@router.get(
    "/{product_id}",
    summary="Obtener producto por ID",
    description="Retorna la información de un producto específico.",
    response_model=ProductResponse,
    responses={
        404: {"model": ErrorResponse},
        401: {"model": ErrorResponse}
    }
)
async def get_product(
    product_id: str,
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Obtiene los datos de un producto a partir de su ID.  
    Requiere que el usuario esté autenticado.
    """
    product = await ProductService.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado.")
    return product


@router.put(
    "/{product_id}",
    summary="Actualizar producto",
    description="Actualiza uno o varios campos de un producto existente. Requiere rol `gym_owner`.",
    response_model=ProductResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse}
    }
)
async def update_product(
    product_id: str,
    sale_price: Optional[float] = Form(None),
    current_stock: Optional[int] = Form(None),
    min_stock: Optional[int] = Form(None),
    status: Optional[str] = Form(None),
    description: Optional[str] = Form(None),

    user: dict = Depends(AuthService.get_current_user)
):
    """
    Actualiza campos específicos del producto, como precio de venta, stock, estado, etc.  
    Solo el `gym_owner` puede actualizar.
    """
    if user.get("role") != "gym_owner":
        raise HTTPException(status_code=403, detail="No tienes permiso para actualizar productos.")

    update_data = {
        "sale_price": sale_price,
        "current_stock": current_stock,
        "min_stock": min_stock,
        "status": status,
        "description": description
    }
    updated_product = await ProductService.update_product(product_id, update_data)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado o no se pudo actualizar.")
    return updated_product


@router.delete(
    "/{product_id}",
    summary="Eliminar producto",
    description="Elimina un producto del inventario. Requiere rol `gym_owner`.",
    response_model=dict,
    responses={
        404: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse}
    }
)
async def delete_product(
    product_id: str,
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Elimina por completo un producto de la base de datos.
    Solo el `gym_owner` puede eliminar productos.
    """
    if user.get("role") != "gym_owner":
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar productos.")

    success = await ProductService.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Producto no encontrado o no se pudo eliminar.")
    return {"message": "Producto eliminado correctamente"}
