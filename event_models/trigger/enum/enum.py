from enum import StrEnum


# TODO unify with EventSource from event_models.event.event
class ScrapType(StrEnum):
    TICKETMASTER_MAP = "ticketmaster_map"
    TICKETMASTER_FACET = "ticketmaster_facets"
    VIVIDSEATS = "vividseats"
    EVENUE = "evenue"


class FailureReason(StrEnum):
    PROXY_ERROR = "proxy_error"
    NOT_FOUND = "not_found"
    SCRAP_SERVICE_OVERLOAD = "scrap_service_overload"
    DATA_ISSUE = "data_issue"
    PROCESS_SERVICE_OVERLOAD = "process_service_overload"
