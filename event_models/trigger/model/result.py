import datetime
from typing import Any

from pydantic import UUID4, BaseModel, model_validator

from event_models.event.event import MessageHeader
from event_models.trigger.enum import ScrapType


class EventResultHeader(BaseModel):
    message_id: UUID4 | str
    event_id: str
    scrap_type: ScrapType
    data_process_success: bool
    finished: datetime.datetime
    error_reason: str | None = None

    @model_validator(mode="before")
    def check_failure(cls: Any, values: Any) -> Any:
        if values["data_process_success"] is False and values.get("error_reason") is None:
            raise ValueError("error must be provided if the event result has a failed status.")

        return values

    @staticmethod
    def message_header_to_result_dict(message_header: MessageHeader, error_reason: str | None = None) -> dict[str, Any]:
        return {
            "message_id": message_header.event_message_id,
            "event_id": message_header.event_id,
            "scrap_type": ScrapType(message_header.event_source),
            "data_process_success": error_reason is None,
            "finished": datetime.datetime.now(),
            "error_reason": error_reason,
        }
