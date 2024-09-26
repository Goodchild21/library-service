import json
import os

from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import update
from database import orm
from datetime import datetime, date
from redis import Redis

from ..http.schema import request


def custom_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type not serializable")


def create_author(session: Session, request: request.CreateAuthorRequest) -> Dict:
    author_orm = orm.Author(**dict(request))

    session.add(author_orm)
    session.commit()

    return author_orm.to_dict()


def update_author(
    session: Session, author_id: str, request: request.UpdateAuthorRequest
) -> Optional[Dict]:
    session.execute(
        update(orm.Author)
        .where(
            orm.Author.id == author_id,
            orm.Author.deleted_at.is_(None),
        )
        .values(**{k: v for k, v in dict(request).items() if v is not None})
    )
    session.commit()

    author_orm = (
        session.query(orm.Author)
        .filter(
            orm.Author.id == author_id,
            orm.Author.deleted_at.is_(None),
        )
        .first()
    )

    return author_orm.to_dict() if author_orm else None


def soft_delete_author(session: Session, author_id: str) -> None:
    session.execute(
        update(orm.Author)
        .where(orm.Author.id == author_id)
        .values(deleted_at=datetime.now())
    )
    session.commit()


def get_author_by_id(
    session: Session, author_id: str, redis_client: Redis, use_cache: bool = True
) -> Optional[Dict]:
    if use_cache:
        cached_author = redis_client.get(f"author_{author_id}")
        if cached_author:
            return json.loads(cached_author)

    author_orm = (
        session.query(orm.Author)
        .filter(
            orm.Author.id == author_id,
            orm.Author.deleted_at.is_(None),
        )
        .first()
    )

    if author_orm:
        author_dict = author_orm.to_dict()
        print(author_dict)
        redis_client.setex(
            f"author_{author_id}",
            int(os.getenv("REDIS_EXPIRE_TIME", 600)),
            json.dumps(author_dict, default=custom_serializer),
        )
        return author_dict


def list_author(session: Session) -> List[Dict]:
    author_orm_list = (
        session.query(orm.Author)
        .filter(
            orm.Author.deleted_at.is_(None),
        )
        .all()
    )

    return [author_orm.to_dict() for author_orm in author_orm_list]


def list_book_by_author_id(session: Session, author_id: str) -> List[Dict]:
    book_orm_list = (
        session.query(orm.Book)
        .filter(
            orm.Book.author_id == author_id,
            orm.Book.deleted_at.is_(None),
        )
        .all()
    )

    return [book_orm.to_dict() for book_orm in book_orm_list]
