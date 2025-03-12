"""
Repository para la colección 'inventory_movements' en Firestore.
"""

from app.utils.firebase_config import db

class InventoryRepository:
    """
    Métodos CRUD para la colección 'inventory_movements'.
    """

    @staticmethod
    def create_movement(movement_dict: dict) -> None:
        movement_id = movement_dict["movement_id"]
        db.collection("inventory_movements").document(movement_id).set(movement_dict)

    @staticmethod
    def get_all_movements():
        docs = db.collection("inventory_movements").stream()
        return [doc.to_dict() for doc in docs]

    @staticmethod
    def get_movement_by_id(movement_id: str):
        doc_ref = db.collection("inventory_movements").document(movement_id).get()
        if doc_ref.exists:
            return doc_ref.to_dict()
        return None
