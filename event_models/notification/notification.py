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

    def to_message(self) -> str:
        return (
            f"Event_ID: {self.event_id}\nNotification Type: {self.notification_type.value}\n"
            f"Timestamp: {self.timestamp}, Data: {self.data}"
        )


class SeatData(BaseModel):
    section: str
    row: str
    seat: str
    price: Decimal

    def __str__(self) -> str:
        return f"Section: {self.section}, Row: {self.row}, Seat: {self.seat}, " f"Price: {self.price}"


class SeatDataWithPriceChange(SeatData):
    old_price: Decimal
    price_change: Decimal

    def __str__(self) -> str:
        return (
            f"Section: {self.section}, Row: {self.row}, Seat: {self.seat}, "
            f"Old Price: {self.old_price}, New Price: {self.price}, "
            f"Price Change: {self.price_change}"
        )

    # TODO add validator to count price_change


class DropsData(BaseModel):
    seats: list[SeatData]

    def __str__(self) -> str:
        return "\n".join(str(seat) for seat in self.seats)


class ChangeData(BaseModel):
    seats: list[SeatDataWithPriceChange]

    def __str__(self) -> str:
        return "\n".join(str(seat) for seat in self.seats)


class DropsMessage(NotificationMessage):
    notification_type: NotificationType = NotificationType.DROPS
    data: DropsData


class MovesData(BaseModel):
    original_size: int
    new_size: int

    def __str__(self) -> str:
        return f"Original size: {self.original_size}, New size: {self.new_size}"


class RemainsData(BaseModel):
    remains: int

    def __str__(self) -> str:
        return f"Remaining seats: {self.remains}"


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
