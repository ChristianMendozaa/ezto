from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, time
from enum import Enum

class ClassType(str, Enum):
    YOGA = "yoga"
    PILATES = "pilates"
    SPINNING = "spinning"
    CROSSFIT = "crossfit"
    ZUMBA = "zumba"
    FUNCIONAL = "funcional"
    BOXEO = "boxeo"

class ClassBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=10, max_length=500)
    instructor_id: str
    capacity: int = Field(..., gt=0, le=50)
    duration: int = Field(..., gt=0, le=180)
    room: str
    class_type: ClassType
    difficulty_level: str = Field(..., pattern="^(principiante|intermedio|avanzado)$")


class ClassCreate(ClassBase):
    start_time: str
    end_time: str
    days_of_week: List[int] = Field(..., min_items=1, max_items=7)

    @validator('days_of_week')
    def validate_days(cls, v):
        if not all(0 <= day <= 6 for day in v):
            raise ValueError('Los días deben estar entre 0 (Lunes) y 6 (Domingo)')
        return sorted(list(set(v)))

    @validator('end_time')
    def validate_time_range(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('La hora de fin debe ser posterior a la hora de inicio')
        return v

    class Config:
        schema_extra = {
            "example": {
                "name": "Yoga Avanzado",
                "description": "Clase de yoga para niveles avanzados",
                "instructor_id": "instructor-123",
                "duration": 60,
                "capacity": 15,
                "room": "Sala Principal",
                "class_type": "yoga",
                "difficulty_level": "avanzado",
                "start_time": "10:00:00",
                "end_time": "11:00:00",
                "days_of_week": [0, 2, 4]
            }
        }

class ClassUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[str] = Field(None, min_length=10, max_length=500)
    instructor_id: Optional[str]
    capacity: Optional[int] = Field(None, gt=0, le=50)
    duration: Optional[int] = Field(None, gt=0, le=180)
    room: Optional[str]
    class_type: Optional[ClassType]
    difficulty_level: Optional[str] = Field(None, pattern="^(principiante|intermedio|avanzado)$")
    start_time: Optional[time]
    end_time: Optional[time]
    days_of_week: Optional[List[int]]

    @validator('days_of_week')
    def validate_days(cls, v):
        if v is not None:
            if not all(0 <= day <= 6 for day in v):
                raise ValueError('Los días deben estar entre 0 (Lunes) y 6 (Domingo)')
            return sorted(list(set(v)))
        return v

class ClassResponse(BaseModel):
    id: str
    name: str
    description: str
    instructor_id: str
    instructor_name: str
    duration: int
    capacity: int
    available_spots: int
    current_reservations: int
    class_type: str
    difficulty_level: str
    room: str
    schedule_id: str
    start_time: str
    end_time: str
    days_of_week: List[int]
    created_at: str
    updated_at: str
    status: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "class-123",
                "name": "Yoga Avanzado",
                "description": "Clase de yoga para niveles avanzados",
                "instructor_id": "instructor-123",
                "instructor_name": "Maria Rodriguez",
                "duration": 60,
                "capacity": 15,
                "available_spots": 15,
                "current_reservations": 0,
                "class_type": "yoga",
                "difficulty_level": "avanzado",
                "room": "Sala Principal",
                "schedule_id": "schedule-123",
                "start_time": "10:00:00",
                "end_time": "11:00:00",
                "days_of_week": [0, 2, 4],
                "created_at": "2024-01-01T10:00:00",
                "updated_at": "2024-01-01T10:00:00",
                "status": "activa"
            }
        }

class ClassScheduleResponse(BaseModel):
    class_id: str
    name: str
    instructor_name: str
    room: str
    start_time: time
    end_time: time
    available_spots: int
    total_capacity: int
    class_type: ClassType
    difficulty_level: str
    status: str

    class Config:
        orm_mode = True