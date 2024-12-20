import datetime
from typing import Any

from pydantic import UUID4, BaseModel, model_validator

from event_models.trigger.enum import ScrapType


class EventResultHeader(BaseModel):
    message_id: UUID4
    scrap_type: ScrapType
    process_result: bool
    finished: datetime.datetime
    error_reason: str | None = None

    @model_validator(mode="before")
    def check_failure(cls: Any, values: Any) -> Any:
        if values["process_result"] is False and values.get("error_reason") is None:
            raise ValueError("error must be provided if the event result has a failed status.")

        return values
