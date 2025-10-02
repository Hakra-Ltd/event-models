from enum import StrEnum


class LoggerMessage(StrEnum):
    UNKNOWN = "UNKNOWN"

    SENTRY = "sentry"
    RABBIT = "rabbit"
    MONGO = "mongo"
    POSTGRES = "postgres"
    TIME = "time"
    SERVICE = "service"
