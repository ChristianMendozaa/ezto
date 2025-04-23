# app/models/schedule_model.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime, time, date
from enum import Enum

class RecurrenceType(str, Enum):
    DAILY = "diario"
    WEEKLY = "semanal"
    MONTHLY = "mensual"
    NONE = "sin_recurrencia"

class ScheduleBase(BaseModel):
    class_id: str = Field(..., description="ID de la clase programada")
    start_time: time = Field(..., description="Hora de inicio de la clase")
    end_time: time = Field(..., description="Hora de finalización de la clase")
    days_of_week: List[int] = Field(..., description="Días de la semana (0=Lunes, 6=Domingo)")
    room: str = Field(..., description="Sala o espacio asignado")
    instructor_id: str = Field(..., description="ID del instructor asignado")
    recurrence_type: RecurrenceType = Field(..., description="Tipo de recurrencia")
    start_date: date = Field(..., description="Fecha de inicio del horario")
    end_date: Optional[date] = Field(None, description="Fecha de finalización del horario")

class ScheduleCreate(ScheduleBase):
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

    @validator('end_date')
    def validate_date_range(cls, v, values):
        if v and 'start_date' in values and v < values['start_date']:
            raise ValueError('La fecha de fin debe ser posterior a la fecha de inicio')
        return v

class ScheduleUpdate(BaseModel):
    start_time: Optional[time]
    end_time: Optional[time]
    days_of_week: Optional[List[int]]
    room: Optional[str]
    instructor_id: Optional[str]
    recurrence_type: Optional[RecurrenceType]
    end_date: Optional[date]

    @validator('days_of_week')
    def validate_days(cls, v):
        if v is not None:
            if not all(0 <= day <= 6 for day in v):
                raise ValueError('Los días deben estar entre 0 (Lunes) y 6 (Domingo)')
            return sorted(list(set(v)))
        return v

class ScheduleResponse(ScheduleBase):
    id: str
    class_name: str
    instructor_name: str
    created_at: datetime
    updated_at: datetime
    status: str = Field(..., pattern="^(activo|cancelado|completado)$")
    available_spots: int
    total_capacity: int

    class Config:
        orm_mode = True

class WeeklySchedule(BaseModel):
    week_start: date
    week_end: date
    schedules: List[ScheduleResponse]

    class Config:
        orm_mode = True

class InstructorSchedule(BaseModel):
    instructor_id: str
    instructor_name: str
    schedules: List[ScheduleResponse]

    class Config:
        orm_mode = True

class RoomSchedule(BaseModel):
    room: str
    schedules: List[ScheduleResponse]

    class Config:
        orm_mode = True