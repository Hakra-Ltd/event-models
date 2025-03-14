import datetime
from typing import Any, Optional

from pydantic import BaseModel, model_validator

from event_models.event.event import MessageHeader
from event_models.trigger.enum import FailureReason, ScrapType


class EventResultHeader(BaseModel):
    message_id: str
    event_id: str
    scrap_type: ScrapType
    data_process_success: bool
    started: datetime.datetime
    finished: datetime.datetime
    data_process_notes: Optional[dict[str, Any]] | None = None
    error_reason: FailureReason | None = None

    @model_validator(mode="before")
    def check_failure(cls: Any, values: Any) -> Any:
        if values["data_process_success"] is False and values.get("error_reason") is None:
            raise ValueError("error must be provided if the event result has a failed status.")

        return values

    @classmethod
    def from_message_header(
        cls,
        message_header: MessageHeader,
        started: datetime.datetime,
        error_reason: FailureReason | None = None,
        data_process_notes: dict[str, Any] | None = None,
    ) -> "EventResultHeader":
        return cls(
            message_id=message_header.event_message_id,
            event_id=message_header.event_id,
            scrap_type=ScrapType(message_header.event_source),
            data_process_success=error_reason is None,
            started=started,
            finished=datetime.datetime.now(),
            error_reason=error_reason,
            data_process_notes=data_process_notes,
        )
