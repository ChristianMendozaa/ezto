"""
Servicio para la gestión de movimientos de inventario,
usando InventoryRepository.
"""

import uuid
from fastapi import HTTPException
from typing import Optional, Dict
from app.repositories.inventory_repository import InventoryRepository
from app.models.inventory_model import InventoryMovement


class InventoryService:
    """
    Encapsula la lógica de negocio para los movimientos de inventario:
    - Crear un nuevo movimiento (entrada, salida, ajuste, devolución).
    - Listar todos los movimientos.
    - Obtener un movimiento específico por ID.
    - Actualizar un movimiento existente.
    - Eliminar un movimiento.
    """

    @staticmethod
    async def create_movement(movement_data: InventoryMovement, user: dict) -> InventoryMovement:
        """
        Crea un nuevo movimiento de inventario.
        Verifica que el rol sea 'gym_owner'.
        """
        if user.get("role") != "gym_owner":
            raise HTTPException(status_code=403, detail="No tienes permiso para registrar movimientos de inventario.")

        movement_id = str(uuid.uuid4())
        mv = movement_data.model_dump()
        mv.update({
            "movement_id": movement_id,
            "movement_date": movement_data.movement_date.isoformat()
        })

        InventoryRepository.create_movement(mv)
        return InventoryMovement(**mv)

    @staticmethod
    async def get_all_movements() -> list[InventoryMovement]:
        """
        Lista todos los movimientos de inventario.
        """
        data = InventoryRepository.get_all_movements()
        return [InventoryMovement(**item) for item in data]

    @staticmethod
    async def get_movement_by_id(movement_id: str) -> Optional[InventoryMovement]:
        """
        Obtiene la información de un movimiento específico por ID.
        """
        data = InventoryRepository.get_movement_by_id(movement_id)
        return InventoryMovement(**data) if data else None

    @staticmethod
    async def update_movement(
        movement_id: str,
        update_data: Dict,
        user: dict
    ) -> InventoryMovement:
        """
        Actualiza campos de un movimiento existente.
        Verifica rol 'gym_owner'.
        """
        if user.get("role") != "gym_owner":
            raise HTTPException(status_code=403, detail="No tienes permiso para actualizar movimientos de inventario.")

        existing = InventoryRepository.get_movement_by_id(movement_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Movimiento no encontrado.")

        # Filtrar None y aplicar cambios
        filtered = {k: v for k, v in update_data.items() if v is not None}
        InventoryRepository.update_movement(movement_id, filtered)

        updated = InventoryRepository.get_movement_by_id(movement_id)
        return InventoryMovement(**updated)

    @staticmethod
    async def delete_movement(movement_id: str, user: dict) -> dict:
        """
        Elimina un movimiento de inventario por ID.
        Verifica rol 'gym_owner'.
        """
        if user.get("role") != "gym_owner":
            raise HTTPException(status_code=403, detail="No tienes permiso para eliminar movimientos de inventario.")

        existing = InventoryRepository.get_movement_by_id(movement_id)
        if not existing:
            raise HTTPException(status_code=404, detail="Movimiento no encontrado.")

        InventoryRepository.delete_movement(movement_id)
        return {"message": "Movimiento eliminado correctamente"}
