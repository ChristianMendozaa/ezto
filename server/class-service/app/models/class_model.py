from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ClassEntity:
    id: Optional[str]
    name: str
    description: str
    instructor: str
    start_time: datetime
    end_time: datetime
    capacity: int
    location: Optional[str]
    status: bool

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "instructor": self.instructor,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "capacity": self.capacity,
            "location": self.location,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: dict):
        return ClassEntity(
            id=data.get("id"),
            name=data["name"],
            description=data["description"],
            instructor=data["instructor"],
            start_time=datetime.fromisoformat(data["start_time"]),
            end_time=datetime.fromisoformat(data["end_time"]),
            capacity=data["capacity"],
            location=data.get("location"),
            status=data["status"]
        )

    def to_dto(self):
        from app.models.dtos.class_dto import ClassDTO
        return ClassDTO(**self.to_dict())
