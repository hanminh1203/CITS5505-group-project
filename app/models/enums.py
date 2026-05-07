from enum import StrEnum
from app.exceptions import IllegalArgumentException


class SkillLevel(StrEnum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"


class RequestStatus(StrEnum):
    OPEN = "OPEN"
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

    @classmethod
    def can_be_searched(cls):
        return [cls.OPEN, cls.PENDING]
    
    @staticmethod
    def from_value(value):
        try:
            return RequestStatus(value)
        except ValueError:
            raise IllegalArgumentException(f"Value {value} is not supported")


class SessionFormat(StrEnum):
    ONLINE = "Online"
    OFFLINE = "Offline"
    HYBRID = "Hybrid"
