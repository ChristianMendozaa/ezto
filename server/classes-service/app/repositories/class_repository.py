# app/repositories/class_repository.py
from app.utils.firebase_config import db
import asyncio
from datetime import datetime

class ClassRepository:
    @staticmethod
    async def create_class(class_data: dict):
        try:
            loop = asyncio.get_running_loop()
            class_ref = await loop.run_in_executor(
                None,
                lambda: db.collection("classes").add({
                    **class_data,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                    "status": "activa"
                })
            )
            return class_ref.id
        except Exception as e:
            raise Exception(f"Error creando la clase: {str(e)}")

    @staticmethod
    async def get_class(class_id: str):
        try:
            loop = asyncio.get_running_loop()
            class_doc = await loop.run_in_executor(
                None,
                lambda: db.collection("classes").document(class_id).get()
            )
            return class_doc.to_dict() if class_doc.exists else None
        except Exception as e:
            raise Exception(f"Error obteniendo la clase: {str(e)}")