"""
Repository para la colección 'products' en Firestore.
"""

from app.utils.firebase_config import db
from datetime import date

class ProductRepository:
    """
    Contiene métodos CRUD de productos en Firestore.
    """

    @staticmethod
    def create_product(product_dict: dict) -> None:
        """
        Crea un nuevo documento de producto en la colección 'products'.
        """
        product_id = product_dict["id"]
        db.collection("products").document(product_id).set(product_dict)

    @staticmethod
    def get_all_products():
        """
        Retorna todos los productos de la colección.
        """
        docs = db.collection("products").stream()
        return [doc.to_dict() for doc in docs]

    @staticmethod
    def get_product_by_id(product_id: str):
        """
        Retorna un producto por su ID, o None si no existe.
        """
        doc = db.collection("products").document(product_id).get()
        if doc.exists:
            return doc.to_dict()
        return None

    @staticmethod
    def update_product(product_id: str, updated_fields: dict) -> dict:
        """
        Actualiza los campos de un producto y retorna el documento resultante.
        """
        doc_ref = db.collection("products").document(product_id)
        if not doc_ref.get().exists:
            return None

        doc_ref.update(updated_fields)
        return doc_ref.get().to_dict()

    @staticmethod
    def delete_product(product_id: str) -> bool:
        """
        Elimina un producto, retornando True si existía y False si no.
        """
        doc_ref = db.collection("products").document(product_id)
        if not doc_ref.get().exists():
            return False
        doc_ref.delete()
        return True
