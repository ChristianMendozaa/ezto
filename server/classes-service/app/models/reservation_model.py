# app/models/reservation_model.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class ReservationStatus(str, Enum):
    CONFIRMED = "confirmada"
    CANCELLED = "cancelada"
    WAITLIST = "lista_espera"
    COMPLETED = "completada"
    NO_SHOW = "no_asistio"

class ReservationBase(BaseModel):
    class_id: str = Field(..., description="ID de la clase reservada")
    user_id: str = Field(..., description="ID del usuario que realiza la reserva")
    date: datetime = Field(..., description="Fecha y hora de la clase")

class ReservationCreate(ReservationBase):
    notes: Optional[str] = Field(None, max_length=200, description="Notas opcionales para la reserva")

class ReservationUpdate(BaseModel):
    status: ReservationStatus
    attendance: Optional[bool] = Field(None, description="Marca de asistencia a la clase")
    notes: Optional[str] = Field(None, max_length=200)

class ReservationResponse(ReservationBase):
    id: str
    status: ReservationStatus
    created_at: datetime
    updated_at: datetime
    attendance: Optional[bool]
    notes: Optional[str]
    class_name: str
    instructor_name: str
    
    class Config:
        orm_mode = True

class WaitlistEntry(BaseModel):
    position: int = Field(..., description="Posición en la lista de espera")
    user_id: str
    created_at: datetime

    class Config:
        orm_mode = True

# Mantenemos los modelos existentes y añadimos nuevos para el dashboard
class DashboardResponse(BaseModel):
    """
    Respuesta para el Panel de Administración.
    """
    message: str = Field(..., title="Mensaje", description="Mensaje de bienvenida al Dashboard")
    user: dict = Field(..., title="Usuario", description="Información del usuario autenticado")
    statistics: dict = Field(..., description="Estadísticas de reservas y clases")
    recent_reservations: List[ReservationResponse] = Field(..., description="Últimas reservas realizadas")
    upcoming_classes: List[dict] = Field(..., description="Próximas clases programadas")

class ClientResponse(BaseModel):
    """
    Respuesta para el Panel de Cliente.
    """
    message: str = Field(..., title="Mensaje", description="Mensaje de bienvenida al Panel de Cliente")
    user: dict = Field(..., title="Usuario", description="Información del usuario autenticado")
    active_reservations: List[ReservationResponse] = Field(..., description="Reservas activas del usuario")
    reservation_history: List[ReservationResponse] = Field(..., description="Historial de reservas")
    waitlist_positions: List[WaitlistEntry] = Field(..., description="Posiciones en listas de espera")

class ReservationStats(BaseModel):
    """
    Estadísticas de reservas para análisis.
    """
    total_reservations: int
    confirmed_reservations: int
    cancelled_reservations: int
    waitlist_count: int
    attendance_rate: float
    most_popular_classes: List[dict]
    peak_hours: List[dict]

    class Config:
        orm_mode = True