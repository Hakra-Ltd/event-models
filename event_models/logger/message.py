from enum import StrEnum


class LoggerMessage(StrEnum):
    UNKNOWN = "UNKNOWN"
    SENTRY = "sentry"
    RABBIT = "rabbit"
    REDIS = "redis"
    MONGO = "mongo"
    POSTGRES = "postgres"
    TIME = "time"
    SERVICE = "service"
