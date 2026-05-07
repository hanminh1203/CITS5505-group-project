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
