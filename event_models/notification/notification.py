import datetime
import enum
from decimal import Decimal
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
    data: Any


class SeatData(BaseModel):
    section: str
    row: str
    seat: str
    price: Decimal


class SeatDataWithPriceChange(SeatData):
    old_price: Decimal
    price_change: Decimal

    # TODO add validator to count price_change


class DropsData(BaseModel):
    seats: list[SeatData]


class ChangeData(BaseModel):
    seats: list[SeatDataWithPriceChange]


class DropsMessage(NotificationMessage):
    notification_type: NotificationType = NotificationType.DROPS
    data: DropsData


class MovesData(BaseModel):
    original_size: int
    new_size: int


class RemainsData(BaseModel):
    remains: int


class PriceChangeMessage(NotificationMessage):
    notification_type: NotificationType = NotificationType.PRICE_CHANGE
    data: ChangeData


class MovesMessage(NotificationMessage):
    notification_type: NotificationType = NotificationType.MOVES
    data: MovesData


class RemainingSeatsMessage(NotificationMessage):
    notification_type: NotificationType = NotificationType.REMAINING_SEATS
    data: RemainsData
