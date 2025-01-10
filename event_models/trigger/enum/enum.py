from enum import StrEnum


# TODO unify with EventSource from event_models.event.event
class ScrapType(StrEnum):
    TICKETMASTER_MAP = "ticketmaster-map"
    TICKETMASTER_FACET = "ticketmaster-facet"
    VIVIDSEATS = "vividseats"
    EVENUE_SEAT = "evenue-seat"
    EVENUE_SECTION = "evenue-section"
    EVENUE_PRICES = "evenue-prices"


class FailureReason(StrEnum):
    PROXY_ERROR = "proxy_error"
    NOT_FOUND = "not_found"
    SCRAP_SERVICE_OVERLOAD = "scrap_service_overload"
    DATA_ISSUE = "data_issue"
    PROCESS_SERVICE_OVERLOAD = "process_service_overload"
    NO_SECTIONS = "no_sections"
    NOT_ON_SALE = "not_on_sale"
