from enum import StrEnum


class SkillLevel(StrEnum):
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    EXPERT = "Expert"

class RequestStatus(StrEnum):
    OPEN = "Open"
    PENDING = "Pending"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class SessionFormat(StrEnum):
    ONLINE = "Online"
    OFFLINE = "Offline"
    HYBRID = "Hybrid"