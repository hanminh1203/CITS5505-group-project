from enum import StrEnum


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


class SessionFormat(StrEnum):
    ONLINE = "Online"
    OFFLINE = "Offline"
    HYBRID = "Hybrid"
