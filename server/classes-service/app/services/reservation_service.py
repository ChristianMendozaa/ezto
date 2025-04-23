# app/services/reservation_service.py
from fastapi import HTTPException, Request
from app.utils.firebase_config import db
from datetime import datetime

class ReservationService:
    @staticmethod
    async def create_reservation(class_id: str, user_id: str):
        try:
            # Verificar clase
            class_doc = db.collection("classes").document(class_id).get()
            if not class_doc.exists:
                raise HTTPException(status_code=404, detail="Clase no encontrada")
            
            class_data = class_doc.to_dict()
            if class_data["current_reservations"] >= class_data["capacity"]:
                raise HTTPException(status_code=400, detail="Clase sin cupos disponibles")

            # Crear reserva
            reservation_ref = db.collection("reservations").add({
                "class_id": class_id,
                "user_id": user_id,
                "status": "confirmada",
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            })

            # Actualizar cupos
            db.collection("classes").document(class_id).update({
                "current_reservations": class_data["current_reservations"] + 1,
                "updated_at": datetime.now()
            })

            return reservation_ref[1].id
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear la reserva: {str(e)}")