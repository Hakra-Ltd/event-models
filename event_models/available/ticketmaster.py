import datetime
from decimal import Decimal
from plistlib import dumps
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

        for place_id, value_list in input_dict.items():
            # old format
            # TODO or ignore completely and load from the endpoint?
            if len(value_list) == 7:
                places[place_id] = TicketmasterPlaceAvailable(
                    list_price=Decimal(f"{value_list[0]:.2f}"),
                    total_price=Decimal(f"{value_list[1]:.2f}"),
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
                    # TODO check if can cause an issue
                    # during the processing, the avail endpoint needs to be called to get relevant data
                    inserted=None,
                    prev_updated=None,
                    update_reason=None,
                )

            elif len(value_list) == 17:
                places[place_id] = TicketmasterPlaceAvailable(
                    list_price=Decimal(f"{value_list[0]:.2f}"),
                    total_price=Decimal(f"{value_list[1]:.2f}"),
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

    def to_redis_dict(self) -> dict[str, Any]:
        return {
            place_id: [
                str(place_data.list_price),
                str(place_data.total_price),
                place_data.offer_id,
                place_data.offer_name,
                place_data.sellable_quantities,
                place_data.protected,
                place_data.inventory_type,
                place_data.full_section,
                place_data.section,
                place_data.row,
                place_data.row_rank,
                place_data.seat_number,
                place_data.attributes,
                place_data.description,
                place_data.inserted.isoformat(),
                place_data.prev_updated.isoformat() if place_data.prev_updated else None,
                place_data.update_reason if place_data.update_reason else None,
            ]
            for place_id, place_data in self.places.items()
        }

    @classmethod
    def from_event_models(cls, event_id: str, event_data: list[BaseModel]) -> "TicketmasterEventAvailable":
        places: dict[str, TicketmasterPlaceAvailable] = {}

        for place_data in event_data:
            dump_dict = place_data.model_dump()
            places[dump_dict["place_id"]] = TicketmasterPlaceAvailable(**dump_dict)

        return cls(event_id=event_id, places=places)
