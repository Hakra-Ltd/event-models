import datetime
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, NonNegativeInt

# LISTING_TOTAL_PRICE_INDEX = 1


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
    full_section: str | None
    section: str | None
    row: str | None
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
    event_id: str
    places: dict[str, TicketmasterPlaceAvailable]

    @classmethod
    def from_redis_dict(cls, event_id: str, input_dict: dict[str, Any]) -> "TicketmasterEventAvailable":
        places: dict[str, TicketmasterPlaceAvailable] = {}

        for key, value_list in input_dict.items():
            # old format
            if len(value_list) == 7:
                places[event_id] = TicketmasterPlaceAvailable(
                    list_price=Decimal(f"{value_list[0]:.2f}"),
                    total_price=Decimal(f"{value_list[0]:.2f}"),
                    offer_id=str(value_list[2]),
                    offer_name=str(value_list[3]),
                    sellable_quantities=value_list[4],
                    protected=bool(value_list[5]),
                    inventory_type=str(value_list[6]),
                    full_section=None,
                    section=None,
                    row=None,
                    row_rank=None,
                    seat_number=None,
                    attributes=[],
                    description=[],
                    inserted=datetime.datetime.fromisoformat(value_list[1]),
                    prev_updated=None,
                    update_reason=None,
                )

            elif len(value_list) == 17:
                places[event_id] = TicketmasterPlaceAvailable(
                    list_price=Decimal(f"{value_list[0]:.2f}"),
                    total_price=Decimal(f"{value_list[0]:.2f}"),
                    offer_id=str(value_list[2]),
                    offer_name=str(value_list[3]),
                    sellable_quantities=value_list[4],
                    protected=bool(value_list[5]),
                    inventory_type=str(value_list[6]),
                    full_section=str(value_list[7]),
                    section=str(value_list[8]),
                    row=str(value_list[9]),
                    row_rank=int(value_list[10]) if value_list[10] is not None else None,
                    seat_number=str(value_list[11]) if value_list[11] is not None else None,
                    attributes=value_list[12],
                    description=value_list[13],
                    inserted=datetime.datetime.fromisoformat(value_list[14]),
                    prev_updated=datetime.datetime.fromisoformat(str(value_list[15])) if value_list[15] else None,
                    update_reason=value_list[16] if value_list[15] else None,
                )
            else:
                raise ValueError(
                    f"Unexpected number of values in redis dict for event {event_id}: {len(value_list)} - {value_list}"
                )

        return cls(event_id=event_id, places=places)

    @classmethod
    def from_event_dict(cls, event_id: str, event_dict: dict[str, Any]) -> "TicketmasterEventAvailable":
        return cls(
            event_id=event_id,
            places={place_id: TicketmasterPlaceAvailable(**place_data) for place_id, place_data in event_dict.items()},
        )
