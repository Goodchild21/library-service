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


def create_book(session: Session, request: request.CreateBookRequest) -> Dict:
    book_orm = orm.Book(**dict(request))

    session.add(book_orm)
    session.commit()
    return book_orm.to_dict()


def update_book(
    session: Session, book_id: str, request: request.UpdateBookRequest
) -> Optional[Dict]:
    session.execute(
        update(orm.Book)
        .where(
            orm.Book.id == book_id,
            orm.Book.deleted_at.is_(None),
        )
        .values(**{k: v for k, v in dict(request).items() if v is not None})
    )
    session.commit()

    book_orm = (
        session.query(orm.Book)
        .filter(
            orm.Book.id == book_id,
            orm.Book.deleted_at.is_(None),
        )
        .first()
    )
    return book_orm.to_dict() if book_orm else None


def soft_delete_book(session: Session, book_id: str) -> None:
    session.execute(
        update(orm.Book)
        .where(orm.Book.id == book_id)
        .values(
            deleted_at=datetime.now(),
        )
    )
    session.commit()


def get_book_by_id(
    session: Session, book_id: str, redis_client: Redis, use_cache: bool = True
) -> Optional[Dict]:
    if use_cache:
        cached_book = redis_client.get(f"book_{book_id}")
        if cached_book:
            return json.loads(cached_book)

    book_orm = (
        session.query(orm.Book)
        .filter(
            orm.Book.id == book_id,
            orm.Book.deleted_at.is_(None),
        )
        .first()
    )

    if book_orm:
        book_dict = book_orm.to_dict()
        redis_client.setex(
            f"book_{book_id}",
            int(os.getenv("REDIS_EXPIRE_TIME", 600)),
            json.dumps(book_dict, default=custom_serializer),
        )
        return book_dict


def list_book(session: Session) -> List[Dict]:
    book_orm_list = (
        session.query(orm.Book)
        .filter(
            orm.Book.deleted_at.is_(None),
        )
        .all()
    )

    return [book_orm.to_dict() for book_orm in book_orm_list]
