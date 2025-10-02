from enum import StrEnum


class LoggerMessage(StrEnum):
    UNKNOWN = "UNKNOWN"

    SENTRY = "sentry"
    RABBIT = "rabbit"
    TIME = "time"
    SERVICE = "service"
