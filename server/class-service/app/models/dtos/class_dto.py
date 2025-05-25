# app/models/dtos/class_dto.py

from pydantic import BaseModel, ConfigDict, Field, constr, conint, field_validator
from typing import Optional
from datetime import datetime

class ClassDTO(BaseModel):
    # --- configuración Pydantic v2 ---
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Yoga Avanzado",
                "description": "Clase de yoga para practicantes avanzados",
                "instructor": "Ana López",
                "start_time": "2025-06-01T09:00:00",
                "end_time": "2025-06-01T10:30:00",
                "capacity": 20,
                "location": "Sala 1",
                "status": True
            }
        }
    )

    id: Optional[str] = Field(None, description="ID único de la clase")
    name: constr(min_length=3, max_length=100) = Field(..., description="Nombre de la clase")
    description: constr(min_length=10, max_length=500) = Field(..., description="Descripción de la clase")
    instructor: constr(min_length=3, max_length=50) = Field(..., description="Nombre del instructor")
    start_time: datetime = Field(..., description="Fecha y hora de inicio")
    end_time: datetime = Field(..., description="Fecha y hora de finalización")
    capacity: conint(gt=0) = Field(..., description="Cupos disponibles en la clase")
    location: Optional[constr(min_length=3, max_length=50)] = Field(None, description="Ubicación física de la clase")
    status: bool = Field(default=True, description="Estado activo o inactivo")

    @field_validator("end_time")
    def check_end_after_start(cls, end_time: datetime, info) -> datetime:
        start_time = info.data.get("start_time")
        if start_time and end_time <= start_time:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio.")
        return end_time

    def to_entity(self, entity_id: Optional[str] = None) -> "ClassEntity":
        from app.models.class_model import ClassEntity
        return ClassEntity(
            id=self.id or entity_id,
            name=self.name,
            description=self.description,
            instructor=self.instructor,
            start_time=self.start_time,
            end_time=self.end_time,
            capacity=self.capacity,
            location=self.location,
            status=self.status
        )
