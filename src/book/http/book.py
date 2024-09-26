from fastapi import Depends
from fastapi.routing import APIRouter

from database.dependencies import db_session, redis_client
from src.book.http.schema import request, response
from src.book.service import book as book_service

router = APIRouter(prefix="/books", tags=["Book"])


@router.post(
    "",
    status_code=201,
    response_model=response.CreateBookResponse,
)
def create_book(
    request: request.CreateBookRequest,
) -> response.CreateBookResponse:
    """
    This endpoint used to create book
    """
    session = db_session()
    book = book_service.create_book(session, request)
    resp = response.CreateBookResponse(data=book)

    print(resp)

    return resp


@router.put(
    "/{book_id}",
    status_code=200,
    response_model=response.UpdateBookResponse,
)
def update_book(
    book_id: str,
    request: request.UpdateBookRequest,
) -> response.UpdateBookResponse:
    """
    This endpoint used to update book
    """
    session = db_session()
    book = book_service.update_book(
        session,
        book_id,
        request,
    )
    resp = response.UpdateBookResponse(data=book)

    return resp


@router.delete(
    "/{book_id}",
    status_code=200,
    response_model=response.DeleteBookResponse,
)
def delete_book(
    book_id: str,
) -> response.DeleteBookResponse:
    """
    This endpoint used to delete book
    """
    session = db_session()
    book_service.soft_delete_book(session, book_id)

    return response.DeleteBookResponse()


@router.get(
    "/{book_id}",
    status_code=200,
    response_model=response.GetBookResponse,
)
def get_book(
    book_id: str,
) -> response.GetBookResponse:
    """
    This endpoint used to get book by ID
    """
    session = db_session()
    book = book_service.get_book_by_id(
        session,
        book_id,
        redis_client,
    )
    resp = response.GetBookResponse(data=book)

    return resp


@router.get(
    "",
    status_code=200,
    response_model=response.ListBookResponse,
)
def list_book() -> response.ListBookResponse:
    """
    This endpoint used to list all books
    """
    session = db_session()
    book_list = book_service.list_book(session)
    resp = response.ListBookResponse(data=book_list)

    return resp
