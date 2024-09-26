from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class CreateAuthorRequest(BaseModel):
    name: str
    bio: Optional[str] = None
    birth_date: str

    @field_validator("birth_date")
    def parse_date(cls, value):
        return datetime.strptime(value, "%Y-%m-%d").date()


class UpdateAuthorRequest(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    birth_date: Optional[str] = None

    @field_validator("birth_date")
    def parse_date(cls, value):
        if value:
            return datetime.strptime(value, "%Y-%m-%d").date()
        return None
