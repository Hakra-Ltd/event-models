from enum import StrEnum


class LoggerMessage(StrEnum):
    UNKNOWN = "UNKNOWN"

    SENTRY = "sentry"
    RABBIT = "rabbit"
    MONGO = "mongo"
    TIME = "time"
    SERVICE = "service"
