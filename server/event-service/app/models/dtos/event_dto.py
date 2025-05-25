from pydantic import BaseModel, Field, constr, conint, validator
from typing import Optional
from datetime import datetime

class EventDTO(BaseModel):
    id: Optional[str] = Field(None, description="ID único del evento")
    name: constr(min_length=3, max_length=100) = Field(..., description="Nombre del evento")
    description: constr(min_length=10, max_length=500) = Field(..., description="Descripción del evento")
    organizer: constr(min_length=3, max_length=50) = Field(..., description="Nombre del organizador")
    start_time: datetime = Field(..., description="Fecha y hora de inicio")
    end_time: datetime = Field(..., description="Fecha y hora de finalización")
    capacity: conint(gt=0) = Field(..., description="Cupos disponibles en el evento")
    location: Optional[constr(min_length=3, max_length=50)] = Field(None, description="Ubicación física del evento")
    event_type: Optional[constr(min_length=3, max_length=30)] = Field(None, description="Tipo de evento (competencia, taller, seminario, etc.)")
    price: Optional[float] = Field(None, ge=0, description="Precio del evento (opcional, 0 para eventos gratuitos)")
    status: bool = Field(default=True, description="Estado activo o inactivo")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Competencia de CrossFit",
                "description": "Competencia mensual de CrossFit para todos los niveles con premios para los ganadores",
                "organizer": "Carlos Rodríguez",
                "start_time": "2024-06-15T10:00:00",
                "end_time": "2024-06-15T16:00:00",
                "capacity": 50,
                "location": "Área de CrossFit",
                "event_type": "competencia",
                "price": 25.00,
                "status": True
            }
        }

    @validator("end_time")
    def check_end_after_start(cls, end_time, values):
        if 'start_time' in values and end_time <= values['start_time']:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio.")
        return end_time

    @validator("price")
    def validate_price(cls, price):
        if price is not None and price < 0:
            raise ValueError("El precio no puede ser negativo.")
        return price

    def to_entity(self, entity_id: Optional[str] = None) -> "EventEntity":
        from app.models.event_model import EventEntity
        return EventEntity(
            id=self.id if hasattr(self, "id") else entity_id,
            name=self.name,
            description=self.description,
            organizer=self.organizer,
            start_time=self.start_time,
            end_time=self.end_time,
            capacity=self.capacity,
            location=self.location,
            event_type=self.event_type,
            price=self.price,
            status=self.status
        )