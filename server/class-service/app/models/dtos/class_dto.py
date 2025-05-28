# app/models/dtos/class_dto.py

from pydantic import (
    BaseModel,
    Field,
    constr,
    conint,
    field_validator,
    ConfigDict
)
from typing import List, Optional
from datetime import time
from enum import Enum

class WeekDay(str, Enum):
    MONDAY    = "Monday"
    TUESDAY   = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY  = "Thursday"
    FRIDAY    = "Friday"
    SATURDAY  = "Saturday"
    SUNDAY    = "Sunday"

class SessionDTO(BaseModel):
    day       : WeekDay = Field(..., description="Día de la semana")
    start_time: time    = Field(..., description="Hora de inicio (HH:MM:SS)")
    end_time  : time    = Field(..., description="Hora de fin (HH:MM:SS)")

    @field_validator("end_time")
    def check_end_after_start(cls, end_time, info):
        if (start := info.data.get("start_time")) and end_time <= start:
            raise ValueError("end_time debe ser posterior a start_time")
        return end_time

class ClassDTO(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {
            "id": "abc123",
            "name": "Yoga Avanzado",
            "description": "Clase de yoga avanzadas",
            "instructor": "Ana López",
            "capacity": 20,
            "location": "Sala 1",
            "status": True,
            "sessions": [
                {"day":"Thursday", "start_time":"11:30:00", "end_time":"12:00:00"},
                {"day":"Friday",   "start_time":"09:00:00", "end_time":"10:00:00"}
            ]
        }}
    )

    id         : Optional[str]     = Field(None, description="ID único")
    name       : constr(min_length=3, max_length=100)
    description: constr(min_length=10, max_length=500)
    instructor : constr(min_length=0, max_length=50)
    capacity   : conint(gt=0)
    location: Optional[constr(min_length=0, max_length=50)] = Field(None)
    status     : bool               = Field(True, description="Activa/inactiva")
    sessions   : List[SessionDTO]   = Field(..., description="Lista de sesiones semanales")

    def to_entity(self, entity_id: Optional[str] = None) -> "ClassEntity":
        from app.models.class_model import ClassEntity, Session
        return ClassEntity(
            id=self.id or entity_id,
            name=self.name,
            description=self.description,
            instructor=self.instructor,
            capacity=self.capacity,
            location=self.location,
            status=self.status,
            sessions=[Session(**s.model_dump()) for s in self.sessions]
        )
