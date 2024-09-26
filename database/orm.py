from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime

Base = declarative_base()


def generate_uuid():
    return str(uuid4())


class DateTimeMixin(Base):
    __abstract__ = True
    created_at = Column(
        "created_at",
        DateTime,
        default=datetime.now,
    )
    updated_at = Column(
        "updated_at",
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
    )
    deleted_at = Column(
        "deleted_at",
        DateTime,
        nullable=True,
    )


class Author(DateTimeMixin):
    __tablename__ = "author"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    birth_date = Column(Date, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "bio": self.bio,
            "birth_date": self.birth_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class Book(DateTimeMixin):
    __tablename__ = "book"

    id = Column(String, primary_key=True, default=generate_uuid)
    author_id = Column(String, ForeignKey("author.id"))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    publish_date = Column(Date, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "author_id": self.author_id,
            "title": self.title,
            "description": self.description,
            "publish_date": self.publish_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
