import datetime
import enum
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


# Same as ListingStatus in arb
class ActionStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    REMOVED = "REMOVED"
    UPDATED = "UPDATED"
    BLACKLISTED = "BLACKLISTED"
    PARTIALLY_SOLD = "PARTIALLY_SOLD"
    SOLD = "SOLD"
    FINISHED = "FINISHED"
    EXPIRED = "EXPIRED"
    INACTIVE = "INACTIVE"
    DISABLED_SALE = "DISABLED_SALE"


class ActionData(BaseModel):
    source_id: str = Field(description="Source identifier")
    local_datetime: datetime.datetime = Field(description="Local date and time of the event")
    listing_id: int = Field(description="Listing identifier")
    inventory_id: int = Field(description="Inventory identifier")
    section: str = Field(description="Seating section")
    row: str = Field(description="Seating row")
    seats: list[str] = Field(description="List of seat numbers")
    internal_notes: str = Field(description="Internal notes")
    ticket_description: Optional[str] = Field(default=None, description="Ticket description")
    public_notes: str = Field(description="Public notes")
    quantity: int = Field(description="Quantity of tickets")
    tags: list[str] = Field(description="List of tags")
    listing_price: Decimal = Field(description="Listing price")
    original_price: Decimal = Field(description="Original price")


class ActionSchema(BaseModel):
    action_id: int
    created: datetime.datetime
    origin_id: int
    new_id: int | None = None
    external_id: int | None = None
    action: ActionStatus
    data: ActionData | None = None


class ActionLogSchema(BaseModel):
    action_id: int
    sync_time: datetime.datetime
    synced: bool
    error: dict[datetime.datetime, str] | None = None
