from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class EventEntity:
    id: Optional[str]
    name: str
    description: str
    organizer: str
    start_time: datetime
    end_time: datetime
    capacity: int
    location: Optional[str]
    event_type: Optional[str]
    price: Optional[float]
    status: bool

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "organizer": self.organizer,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "capacity": self.capacity,
            "location": self.location,
            "event_type": self.event_type,
            "price": self.price,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: dict):
        return EventEntity(
            id=data.get("id"),
            name=data["name"],
            description=data["description"],
            organizer=data["organizer"],
            start_time=datetime.fromisoformat(data["start_time"]),
            end_time=datetime.fromisoformat(data["end_time"]),
            capacity=data["capacity"],
            location=data.get("location"),
            event_type=data.get("event_type"),
            price=data.get("price"),
            status=data["status"]
        )

    def to_dto(self):
        from app.models.dtos.event_dto import EventDTO
        return EventDTO(**self.to_dict())
