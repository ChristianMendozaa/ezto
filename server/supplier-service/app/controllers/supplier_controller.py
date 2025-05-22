"""
Controlador para los endpoints de gestión de proveedores.

Incluye:
- Crear un nuevo proveedor (solo gym_owner).
- Listar todos los proveedores.
- Obtener proveedor por ID.
- Eliminar proveedor.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel, Field

from app.services.supplier_service import SupplierService
from app.services.auth_service import AuthService
from app.models.supplier_model import SupplierBase, SupplierResponse

router = APIRouter()

class ErrorResponse(BaseModel):
    """
    Modelo de error estándar.
    """
    detail: str = Field(..., description="Descripción del error.")


@router.post(
    "/",
    summary="Crear nuevo proveedor",
    description="Crea un nuevo proveedor en el sistema. Requiere rol 'gym_owner'.",
    response_model=SupplierResponse,
    responses={
        403: {"model": ErrorResponse},
        401: {"model": ErrorResponse}
    }
)
async def create_supplier(
    supplier_data: SupplierBase,
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Crea un proveedor en la base de datos.
    Solo el 'gym_owner' puede realizar esta operación.
    """
    return await SupplierService.create_supplier(supplier_data, user)


@router.get(
    "/",
    summary="Listar proveedores",
    description="Devuelve la lista de todos los proveedores registrados.",
    response_model=List[SupplierResponse],
    responses={401: {"model": ErrorResponse}}
)
async def list_suppliers(
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Retorna todos los proveedores en Firestore.  
    Cualquier usuario autenticado puede consultar la lista.
    """
    return await SupplierService.get_all_suppliers()


@router.get(
    "/{supplier_id}",
    summary="Obtener proveedor por ID",
    description="Obtiene la información de un proveedor en particular.",
    response_model=SupplierResponse,
    responses={
        404: {"model": ErrorResponse},
        401: {"model": ErrorResponse}
    }
)
async def get_supplier(
    supplier_id: str,
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Retorna los datos de un proveedor específico por su ID.
    """
    supplier = await SupplierService.get_supplier_by_id(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado.")
    return supplier


@router.delete(
    "/{supplier_id}",
    summary="Eliminar proveedor",
    description="Elimina un proveedor de la base de datos. Requiere rol 'gym_owner'.",
    response_model=dict,
    responses={
        404: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse}
    }
)
async def delete_supplier(
    supplier_id: str,
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Elimina un proveedor específico.  
    Solo el 'gym_owner' puede eliminar.
    """
    if user.get("role") != "gym_owner":
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar proveedores.")

    success = await SupplierService.delete_supplier(supplier_id)
    if not success:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado.")
    return {"message": "Proveedor eliminado correctamente"}
"""
Controlador para los endpoints de gestión de proveedores.

Incluye:
- Crear un nuevo proveedor (solo gym_owner).
- Listar todos los proveedores.
- Obtener proveedor por ID.
- Eliminar proveedor.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel, Field

from app.services.supplier_service import SupplierService
from app.services.auth_service import AuthService
from app.models.supplier_model import SupplierBase, SupplierResponse

router = APIRouter()

class ErrorResponse(BaseModel):
    """
    Modelo de error estándar.
    """
    detail: str = Field(..., description="Descripción del error.")


@router.post(
    "/",
    summary="Crear nuevo proveedor",
    description="Crea un nuevo proveedor en el sistema. Requiere rol 'gym_owner'.",
    response_model=SupplierResponse,
    responses={
        403: {"model": ErrorResponse},
        401: {"model": ErrorResponse}
    }
)
async def create_supplier(
    supplier_data: SupplierBase,
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Crea un proveedor en la base de datos.
    Solo el 'gym_owner' puede realizar esta operación.
    """
    return await SupplierService.create_supplier(supplier_data, user)


@router.get(
    "/",
    summary="Listar proveedores",
    description="Devuelve la lista de todos los proveedores registrados.",
    response_model=List[SupplierResponse],
    responses={401: {"model": ErrorResponse}}
)
async def list_suppliers(
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Retorna todos los proveedores en Firestore.  
    Cualquier usuario autenticado puede consultar la lista.
    """
    return await SupplierService.get_all_suppliers()


@router.get(
    "/{supplier_id}",
    summary="Obtener proveedor por ID",
    description="Obtiene la información de un proveedor en particular.",
    response_model=SupplierResponse,
    responses={
        404: {"model": ErrorResponse},
        401: {"model": ErrorResponse}
    }
)
async def get_supplier(
    supplier_id: str,
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Retorna los datos de un proveedor específico por su ID.
    """
    supplier = await SupplierService.get_supplier_by_id(supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado.")
    return supplier


@router.delete(
    "/{supplier_id}",
    summary="Eliminar proveedor",
    description="Elimina un proveedor de la base de datos. Requiere rol 'gym_owner'.",
    response_model=dict,
    responses={
        404: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse}
    }
)
async def delete_supplier(
    supplier_id: str,
    user: dict = Depends(AuthService.get_current_user)
):
    """
    Elimina un proveedor específico.  
    Solo el 'gym_owner' puede eliminar.
    """
    if user.get("role") != "gym_owner":
        raise HTTPException(status_code=403, detail="No tienes permiso para eliminar proveedores.")

    success = await SupplierService.delete_supplier(supplier_id)
    if not success:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado.")
    return {"message": "Proveedor eliminado correctamente"}
