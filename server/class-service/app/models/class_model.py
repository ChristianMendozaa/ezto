# app/models/class_model.py

from dataclasses import dataclass, asdict
from datetime import time
from typing import List, Optional
from enum import Enum

class WeekDay(str, Enum):
    MONDAY    = "Monday"
    TUESDAY   = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY  = "Thursday"
    FRIDAY    = "Friday"
    SATURDAY  = "Saturday"
    SUNDAY    = "Sunday"

@dataclass
class Session:
    day       : WeekDay
    start_time: time
    end_time  : time

    def to_dict(self) -> dict:
        return {
            "day": self.day.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Session":
        return cls(
            day=WeekDay(data["day"]),
            start_time=time.fromisoformat(data["start_time"]),
            end_time=time.fromisoformat(data["end_time"])
        )

@dataclass
class ClassEntity:
    id         : Optional[str]
    name       : str
    description: str
    instructor : str
    capacity   : int
    location   : Optional[str]
    status     : bool
    sessions   : List[Session]

    def to_dict(self) -> dict:
        base = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "instructor": self.instructor,
            "capacity": self.capacity,
            "location": self.location,
            "status": self.status,
        }
        base["sessions"] = [s.to_dict() for s in self.sessions]
        return base

    @classmethod
    def from_dict(cls, data: dict) -> "ClassEntity":
        return cls(
            id=data.get("id"),
            name=data["name"],
            description=data["description"],
            instructor=data["instructor"],
            capacity=int(data["capacity"]),
            location=data.get("location"),
            status=bool(data["status"]),
            sessions=[Session.from_dict(s) for s in data["sessions"]]
        )
