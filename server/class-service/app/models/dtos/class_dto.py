from pydantic import BaseModel, Field, constr, conint, validator
from typing import Optional
from datetime import datetime

class ClassDTO(BaseModel):
    id: Optional[str] = Field(None, description="ID único de la clase")
    name: constr(min_length=3, max_length=100) = Field(..., description="Nombre de la clase")
    description: constr(min_length=10, max_length=500) = Field(..., description="Descripción de la clase")
    instructor: constr(min_length=3, max_length=50) = Field(..., description="Nombre del instructor")
    start_time: datetime = Field(..., description="Fecha y hora de inicio")
    end_time: datetime = Field(..., description="Fecha y hora de finalización")
    capacity: conint(gt=0) = Field(..., description="Cupos disponibles en la clase")
    location: Optional[constr(min_length=3, max_length=50)] = Field(None, description="Ubicación física de la clase")
    status: bool = Field(default=True, description="Estado activo o inactivo")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Yoga Avanzado",
                "description": "Clase de yoga para practicantes avanzados",
                "instructor": "Ana López",
                "start_time": "2024-06-01T09:00:00",
                "end_time": "2024-06-01T10:30:00",
                "capacity": 20,
                "location": "Sala 1",
                "status": True
            }
        }

    @validator("end_time")
    def check_end_after_start(cls, end_time, values):
        if 'start_time' in values and end_time <= values['start_time']:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio.")
        return end_time
