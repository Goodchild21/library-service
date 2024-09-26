from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional


class CreateBookRequest(BaseModel):
    author_id: str
    title: str
    description: Optional[str] = None
    publish_date: str

    @field_validator("publish_date")
    def parse_date(cls, value):
        return datetime.strptime(value, "%Y-%m-%d").date()


class UpdateBookRequest(BaseModel):
    author_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    publish_date: Optional[str] = None

    @field_validator("publish_date")
    def parse_date(cls, value):
        if value:
            return datetime.strptime(value, "%Y-%m-%d").date()
        return None
