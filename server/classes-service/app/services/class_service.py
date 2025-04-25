from fastapi import HTTPException, Request
from app.utils.firebase_config import db
from datetime import datetime
import asyncio
from typing import List, Optional, Dict, Any

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
            
            class_data = class_doc.to_dict()
            
            # Transformar al formato esperado por ClassResponse
            class_response = {
                "id": class_id,
                "name": class_data.get("name", ""),
                "description": class_data.get("description", ""),
                "instructor_id": class_data.get("instructor_id", ""),
                "instructor_name": class_data.get("instructor_id", ""),  # Aquu00ed deberu00edas obtener el nombre real
                "duration": class_data.get("duration", 0),
                "capacity": class_data.get("capacity", 0),
                "available_spots": class_data.get("capacity", 0) - class_data.get("current_reservations", 0),
                "current_reservations": class_data.get("current_reservations", 0),
                "class_type": str(class_data.get("class_type", "")),
                "difficulty_level": class_data.get("difficulty_level", ""),
                "room": class_data.get("room", ""),
                "schedule_id": class_id,  # Usando el mismo ID como schedule_id
                "start_time": class_data.get("start_time", ""),
                "end_time": class_data.get("end_time", ""),
                "days_of_week": class_data.get("days_of_week", []),
                "created_at": class_data.get("created_at", datetime.now()).isoformat() if hasattr(class_data.get("created_at", datetime.now()), "isoformat") else str(class_data.get("created_at", datetime.now())),
                "updated_at": class_data.get("updated_at", datetime.now()).isoformat() if hasattr(class_data.get("updated_at", datetime.now()), "isoformat") else str(class_data.get("updated_at", datetime.now())),
                "status": class_data.get("status", "activa")
            }
            
            return class_response
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener la clase: {str(e)}")
            
    @staticmethod
    async def list_classes(date: Optional[datetime] = None, instructor: Optional[str] = None, available_only: bool = False):
        try:
            # Iniciar con la colección de clases
            query = db.collection("classes")
            
            # Aplicar filtros si se proporcionan
            if instructor:
                query = query.where("instructor_id", "==", instructor)
                
            # Obtener todas las clases que cumplen con los filtros
            loop = asyncio.get_running_loop()
            classes_docs = await loop.run_in_executor(None, lambda: query.get())
            
            # Convertir documentos a diccionarios
            classes = []
            for doc in classes_docs:
                class_data = doc.to_dict()
                class_data["id"] = doc.id
                
                # Transformar al formato esperado por ClassResponse
                class_response = {
                    "id": doc.id,
                    "name": class_data.get("name", ""),
                    "description": class_data.get("description", ""),
                    "instructor_id": class_data.get("instructor_id", ""),
                    "instructor_name": class_data.get("instructor_id", ""),  # Aquí deberías obtener el nombre real
                    "duration": class_data.get("duration", 0),
                    "capacity": class_data.get("capacity", 0),
                    "available_spots": class_data.get("capacity", 0) - class_data.get("current_reservations", 0),
                    "current_reservations": class_data.get("current_reservations", 0),
                    "class_type": str(class_data.get("class_type", "")),
                    "difficulty_level": class_data.get("difficulty_level", ""),
                    "room": class_data.get("room", ""),
                    "schedule_id": doc.id,  # Usando el mismo ID como schedule_id
                    "start_time": class_data.get("start_time", ""),
                    "end_time": class_data.get("end_time", ""),
                    "days_of_week": class_data.get("days_of_week", []),
                    "created_at": class_data.get("created_at", datetime.now()).isoformat() if hasattr(class_data.get("created_at", datetime.now()), "isoformat") else str(class_data.get("created_at", datetime.now())),
                    "updated_at": class_data.get("updated_at", datetime.now()).isoformat() if hasattr(class_data.get("updated_at", datetime.now()), "isoformat") else str(class_data.get("updated_at", datetime.now())),
                    "status": class_data.get("status", "activa")
                }
                classes.append(class_response)
            
            # Filtrar por fecha si se proporciona
            if date:
                date_str = date.strftime("%Y-%m-%d")
                classes = [c for c in classes if c.get("date") == date_str]
                
            # Filtrar por disponibilidad si se solicita
            if available_only:
                classes = [c for c in classes if c.get("available_spots", 0) > 0]
                
            return classes
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al listar las clases: {str(e)}")
    
    @staticmethod
    async def update_class(class_id: str, class_data: Dict[str, Any]):
        try:
            # Verificar si la clase existe
            class_doc = db.collection("classes").document(class_id).get()
            if not class_doc.exists:
                raise HTTPException(status_code=404, detail="Clase no encontrada")
            
            # Actualizar solo los campos proporcionados
            update_data = {k: v for k, v in class_data.items() if v is not None}
            update_data["updated_at"] = datetime.now()
            
            # Realizar la actualización
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                lambda: db.collection("classes").document(class_id).update(update_data)
            )
            
            # Obtener la clase actualizada
            updated_class_doc = await loop.run_in_executor(
                None,
                lambda: db.collection("classes").document(class_id).get()
            )
            updated_class_data = updated_class_doc.to_dict()
            
            # Transformar al formato esperado por ClassResponse
            class_response = {
                "id": class_id,
                "name": updated_class_data.get("name", ""),
                "description": updated_class_data.get("description", ""),
                "instructor_id": updated_class_data.get("instructor_id", ""),
                "instructor_name": updated_class_data.get("instructor_id", ""),  # Aquí deberías obtener el nombre real
                "duration": updated_class_data.get("duration", 0),
                "capacity": updated_class_data.get("capacity", 0),
                "available_spots": updated_class_data.get("capacity", 0) - updated_class_data.get("current_reservations", 0),
                "current_reservations": updated_class_data.get("current_reservations", 0),
                "class_type": str(updated_class_data.get("class_type", "")),
                "difficulty_level": updated_class_data.get("difficulty_level", ""),
                "room": updated_class_data.get("room", ""),
                "schedule_id": class_id,  # Usando el mismo ID como schedule_id
                "start_time": updated_class_data.get("start_time", ""),
                "end_time": updated_class_data.get("end_time", ""),
                "days_of_week": updated_class_data.get("days_of_week", []),
                "created_at": updated_class_data.get("created_at", datetime.now()).isoformat() if hasattr(updated_class_data.get("created_at", datetime.now()), "isoformat") else str(updated_class_data.get("created_at", datetime.now())),
                "updated_at": updated_class_data.get("updated_at", datetime.now()).isoformat() if hasattr(updated_class_data.get("updated_at", datetime.now()), "isoformat") else str(updated_class_data.get("updated_at", datetime.now())),
                "status": updated_class_data.get("status", "activa")
            }
            
            return class_response
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al actualizar la clase: {str(e)}")
    
    @staticmethod
    async def delete_class(class_id: str):
        try:
            # Verificar si la clase existe
            loop = asyncio.get_running_loop()
            class_doc = await loop.run_in_executor(
                None,
                lambda: db.collection("classes").document(class_id).get()
            )
            
            if not class_doc.exists:
                raise HTTPException(status_code=404, detail="Clase no encontrada")
            
            # Eliminar la clase (o marcarla como inactiva)
            await loop.run_in_executor(
                None,
                lambda: db.collection("classes").document(class_id).update({"status": "inactiva", "updated_at": datetime.now()})
            )
            
            return True
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al eliminar la clase: {str(e)}")
    
    @staticmethod
    async def check_availability(class_id: str):
        try:
            # Obtener la clase
            loop = asyncio.get_running_loop()
            class_doc = await loop.run_in_executor(
                None,
                lambda: db.collection("classes").document(class_id).get()
            )
            
            if not class_doc.exists:
                raise HTTPException(status_code=404, detail="Clase no encontrada")
            
            class_data = class_doc.to_dict()
            capacity = class_data.get("capacity", 0)
            current_reservations = class_data.get("current_reservations", 0)
            available_spots = max(0, capacity - current_reservations)
            
            return {
                "class_id": class_id,
                "name": class_data.get("name"),
                "capacity": capacity,
                "current_reservations": current_reservations,
                "available_spots": available_spots,
                "is_available": available_spots > 0
            }
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al verificar disponibilidad: {str(e)}")