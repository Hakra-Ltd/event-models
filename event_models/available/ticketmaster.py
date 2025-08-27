import datetime
from decimal import Decimal

from pydantic import BaseModel, NonNegativeInt


class TicketmasterPlaceAvailable(BaseModel):
    # Existing redis schema
    list_price: Decimal
    total_price: Decimal
    offer_id: str
    offer_name: str
    sellable_quantities: list[int]
    protected: bool
    inventory_type: str

    # added to fit available/update endpoint
    # place_id: str,
    full_section: str
    section: str
    row: str
    row_rank: int | None
    seat_number: str | None
    attributes: list[str]
    # offer_id: str | None,
    # offer_name: str | None,
    # sellable_quantities: list[int] | None,
    # protected: bool | None,
    description: list[str]
    # inventory_type: str | None,
    # list_price: Decimal | None,
    # total_price: Decimal | None,
    inserted: datetime.datetime
    prev_updated: datetime.datetime | None
    update_reason: str | None

class TicketmasterEventAvailable(BaseModel):
    places: dict[int, TicketmasterPlaceAvailable]
