"""
Repository para la colección 'sales' en Firestore.
"""

from app.utils.firebase_config import db

class SaleRepository:
    """
    Métodos CRUD para la colección 'sales' (ventas).
    """

    @staticmethod
    def create_sale(sale_dict: dict) -> None:
        sale_id = sale_dict["sale_id"]
        db.collection("sales").document(sale_id).set(sale_dict)

    @staticmethod
    def get_all_sales():
        docs = db.collection("sales").stream()
        return [doc.to_dict() for doc in docs]

    @staticmethod
    def get_sale_by_id(sale_id: str):
        doc_ref = db.collection("sales").document(sale_id).get()
        if doc_ref.exists:
            return doc_ref.to_dict()
        return None

    @staticmethod
    def delete_sale(sale_id: str) -> bool:
        doc_ref = db.collection("sales").document(sale_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True
