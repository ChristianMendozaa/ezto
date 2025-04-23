# app/services/class_service.py
from fastapi import HTTPException, Request
from app.utils.firebase_config import db
from datetime import datetime

class ClassService:
    @staticmethod
    async def create_class(class_data: dict):
        try:
            class_ref = db.collection("classes").add({
                **class_data,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
                "status": "activa",
                "current_reservations": 0
            })
            return class_ref[1].id
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear la clase: {str(e)}")

    @staticmethod
    async def get_class(class_id: str):
        try:
            class_doc = db.collection("classes").document(class_id).get()
            if not class_doc.exists:
                raise HTTPException(status_code=404, detail="Clase no encontrada")
            return class_doc.to_dict()
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener la clase: {str(e)}")