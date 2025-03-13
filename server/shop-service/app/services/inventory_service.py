"""
Servicio para la gestión de movimientos de inventario,
usando InventoryRepository.
"""
import uuid
from fastapi import HTTPException
from app.repositories.inventory_repository import InventoryRepository
from app.models.inventory_model import InventoryMovement

class InventoryService:
    """
    Encapsula la lógica de negocio para los movimientos de inventario:
    - Crear un nuevo movimiento (entrada, salida, ajuste, devolución).
    - Listar todos los movimientos.
    - Obtener un movimiento específico por ID.
    - (Opcional) Actualizar stock en productos según tipo de movimiento.
    """

    @staticmethod
    async def create_movement(movement_data: InventoryMovement, user: dict):
        """
        Crea un nuevo movimiento de inventario.
        Verifica que el rol sea 'gym_owner'.
        """
        if user.get("role") != "gym_owner":
            raise HTTPException(status_code=403, detail="No tienes permiso para registrar movimientos de inventario.")

        movement_id = str(uuid.uuid4())
        movement_date = movement_data.movement_date.isoformat()

        movement_dict = {
            "movement_id": movement_id,
            "product_id": movement_data.product_id,
            "movement_type": movement_data.movement_type.value,
            "quantity": movement_data.quantity,
            "reason": movement_data.reason,
            "reference_id": movement_data.reference_id,
            "movement_date": movement_date,
            "responsible_id": movement_data.responsible_id
        }

        InventoryRepository.create_movement(movement_dict)

        # Opcional: Lógica para actualizar stock del producto si el movement_type es ENTRADA o SALIDA
        # ...
        return InventoryMovement(**movement_dict)

    @staticmethod
    async def get_all_movements():
        """
        Lista todos los movimientos de inventario.
        """
        movements_data = InventoryRepository.get_all_movements()
        return [InventoryMovement(**data) for data in movements_data]

    @staticmethod
    async def get_movement_by_id(movement_id: str):
        """
        Obtiene la información de un movimiento específico por ID.
        """
        data = InventoryRepository.get_movement_by_id(movement_id)
        if not data:
            return None
        return InventoryMovement(**data)
