"""
Repository para la colección 'inventory_movements' en Firestore.
"""

from app.utils.firebase_config import db

class InventoryRepository:
    """
    Métodos CRUD para la colección 'inventory_movements'.
    """

    @staticmethod
    def create_movement(mv: dict) -> None:
        db.collection("inventory_movements").document(mv["movement_id"]).set(mv)

    @staticmethod
    def get_all_movements():
        return [doc.to_dict() for doc in db.collection("inventory_movements").stream()]

    @staticmethod
    def get_movement_by_id(movement_id: str):
        doc = db.collection("inventory_movements").document(movement_id).get()
        return doc.to_dict() if doc.exists else None

    @staticmethod
    def update_movement(movement_id: str, data: dict) -> None:
        db.collection("inventory_movements").document(movement_id).update(data)

    @staticmethod
    def delete_movement(movement_id: str) -> None:
        db.collection("inventory_movements").document(movement_id).delete()
