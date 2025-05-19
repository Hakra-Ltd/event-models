import datetime
import enum
from decimal import Decimal
from typing import Any

from pydantic import BaseModel


class SeatData(BaseModel):
    section: str
    row: str
    seat: str
    price: Decimal


class SeatDataWithPriceChange(SeatData):
    old_price: Decimal
    price_change: Decimal


class NotificationType(enum.StrEnum):
    DROPS = "drops"
    PRICE_CHANGE = "price-change"
    MOVES = "moves"
    REMAINING_SEATS = "remaining-seats"


class DropsData(BaseModel):
    seats: list[SeatData]


class ChangeData(BaseModel):
    seats: list[SeatDataWithPriceChange]


class MovesData(BaseModel):
    seats: list[SeatData]


class RemainsData(BaseModel):
    remains: int


class NotificationMessage(BaseModel):
    notification_type: NotificationType
    event_id: str
    timestamp: datetime.datetime
    data: DropsData | ChangeData | MovesData | RemainsData


class DropsMessage(NotificationMessage):
    notification_type: NotificationType = NotificationType.DROPS
    data: DropsData


class PriceChangeMessage(NotificationMessage):
    notification_type: NotificationType = NotificationType.PRICE_CHANGE
    data: ChangeData


class MovesMessage(NotificationMessage):
    notification_type: NotificationType = NotificationType.MOVES
    data: MovesData


class RemainingSeatsMessage(NotificationMessage):
    notification_type: NotificationType = NotificationType.REMAINING_SEATS
    data: RemainsData


class NotificationMessageFactory:
    @staticmethod
    def get_message_from_notify_type(
        notify_type: NotificationType,
        data: dict[str, Any],
    ) -> NotificationMessage:
        match notify_type:
            case NotificationType.DROPS:
                return DropsMessage(
                    **data,
                )
            case NotificationType.PRICE_CHANGE:
                return PriceChangeMessage(
                    **data,
                )
            case NotificationType.MOVES:
                return MovesMessage(
                    **data,
                )
            case NotificationType.REMAINING_SEATS:
                return RemainingSeatsMessage(
                    **data,
                )
            case _:
                raise ValueError(f"Unknown notification type: {notify_type}")
