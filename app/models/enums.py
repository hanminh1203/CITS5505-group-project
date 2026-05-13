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
        except ValueError as error:
            raise IllegalArgumentException(
                f"Value {value} is not supported"
            ) from error

    def can_cancel(self):
        return self in {
            RequestStatus.OPEN,
            RequestStatus.PENDING,
            RequestStatus.IN_PROGRESS,
        }

    def can_complete(self):
        return self == RequestStatus.IN_PROGRESS

    def can_edit(self):
        return self in {RequestStatus.OPEN, RequestStatus.PENDING}


class SessionFormat(StrEnum):
    ONLINE = "Online"
    OFFLINE = "Offline"
    HYBRID = "Hybrid"
