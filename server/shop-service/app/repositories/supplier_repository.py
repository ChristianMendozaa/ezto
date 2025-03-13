"""
Repository para la colección 'suppliers' en Firestore.
"""

from app.utils.firebase_config import db

class SupplierRepository:
    """
    Métodos CRUD para proveedores (colección 'suppliers').
    """

    @staticmethod
    def create_supplier(supplier_dict: dict) -> None:
        supplier_id = supplier_dict["id"]
        db.collection("suppliers").document(supplier_id).set(supplier_dict)

    @staticmethod
    def get_all_suppliers():
        docs = db.collection("suppliers").stream()
        return [doc.to_dict() for doc in docs]

    @staticmethod
    def get_supplier_by_id(supplier_id: str):
        doc_ref = db.collection("suppliers").document(supplier_id).get()
        if doc_ref.exists:
            return doc_ref.to_dict()
        return None

    @staticmethod
    def delete_supplier(supplier_id: str) -> bool:
        doc_ref = db.collection("suppliers").document(supplier_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True
