"""
Servicio para la gestión de proveedores, usando SupplierRepository.
"""

from fastapi import HTTPException
from datetime import date

from app.models.supplier_model import SupplierBase, SupplierResponse
from app.repositories.supplier_repository import SupplierRepository
from uuid import uuid4

class SupplierService:
    """
    Encapsula la lógica de negocio para proveedores,
    delegando la persistencia al SupplierRepository.
    """

    @staticmethod
    async def create_supplier(supplier_data: SupplierBase, user: dict):
        """
        Crea un proveedor en la colección 'suppliers'.

        1. Valida rol 'gym_owner'.
        2. Genera un ID único.
        3. Construye el diccionario y llama al repositorio.
        """
        if user.get("role") != "gym_owner":
            raise HTTPException(status_code=403, detail="No tienes permiso para crear proveedores.")

        supplier_id = str(uuid4())
        now_str = str(date.today())

        supplier_dict = {
            "id": supplier_id,
            "name": supplier_data.name,
            "contact_email": supplier_data.contact_email,
            "phone": supplier_data.phone,
            "address": supplier_data.address,
            "tax_id": supplier_data.tax_id,
            "payment_terms": supplier_data.payment_terms,
            "status": supplier_data.status.value,
            "created_at": now_str,
            "last_updated": now_str,
            "products_offered": 0
        }

        SupplierRepository.create_supplier(supplier_dict)
        return SupplierResponse(**supplier_dict)

    @staticmethod
    async def get_all_suppliers():
        """
        Retorna la lista completa de proveedores.
        """
        data_list = SupplierRepository.get_all_suppliers()
        return [SupplierResponse(**data) for data in data_list]

    @staticmethod
    async def get_supplier_by_id(supplier_id: str):
        """
        Obtiene un proveedor por ID.
        """
        data = SupplierRepository.get_supplier_by_id(supplier_id)
        if not data:
            return None
        return SupplierResponse(**data)

    @staticmethod
    async def delete_supplier(supplier_id: str):
        """
        Elimina un proveedor.
        """
        return SupplierRepository.delete_supplier(supplier_id)
