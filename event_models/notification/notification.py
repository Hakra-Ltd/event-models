import datetime
import enum
from typing import Any

from pydantic import BaseModel


class NotificationType(enum.StrEnum):
    DROPS = "drops"
    PRICE_CHANGE = "price-change"
    MOVES = "moves"
    REMAINING_SEATS = "remaining-seats"


class NotificationMessage(BaseModel):
    notification_type: NotificationType
    event_id: str
    timestamp: datetime.datetime
    data: dict[str, Any]
