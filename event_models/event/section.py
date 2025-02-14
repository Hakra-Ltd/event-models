from typing import Optional

from pydantic import BaseModel, NonNegativeInt


class VividseatsSectionInfo(BaseModel):
    section: str
    section_code: Optional[str] | None
    section_grouping_code: Optional[str] | None

class VividseatsSections(BaseModel):
    total: NonNegativeInt
    sections: list[VividseatsSectionInfo]
