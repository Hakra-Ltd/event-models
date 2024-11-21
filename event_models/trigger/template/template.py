import datetime
from typing import Any

from pydantic import UUID4

from event_models.trigger.enum import FailureReason, ScrapType
from event_models.trigger.model import JobScrapMessage


def get_success_job_message(
    event_id: str,
    job_id: UUID4,
    scrap_type: ScrapType,
    started: datetime.datetime,
    finished: datetime.datetime,
    scrap_notes: dict[str, Any] | None = None,
) -> JobScrapMessage:
    return JobScrapMessage(
        event_id=event_id,
        job_id=job_id,
        scrap_type=scrap_type,
        job_scrap_started_at=started,
        job_scrap_finished_at=finished,
        scrap_success=True,
        scrap_notes=scrap_notes,
    )


def get_error_job_message(
    event_id: str,
    job_id: UUID4,
    scrap_type: ScrapType,
    started: datetime.datetime,
    finished: datetime.datetime,
    scrap_notes: dict[str, Any],
    failure_reason: FailureReason,
) -> JobScrapMessage:
    return JobScrapMessage(
        event_id=event_id,
        job_id=job_id,
        scrap_type=scrap_type,
        job_scrap_started_at=started,
        job_scrap_finished_at=finished,
        scrap_success=False,
        scrap_notes=scrap_notes,
        failure_reason=failure_reason,
    )
