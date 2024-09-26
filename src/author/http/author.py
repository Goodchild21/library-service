from fastapi import Depends
from fastapi.routing import APIRouter

from database.dependencies import db_session, redis_client
from src.author.http.schema import request, response
from src.author.service import author as author_service

router = APIRouter(prefix="/authors", tags=["Author"])


@router.post(
    "",
    status_code=201,
    response_model=response.CreateAuthorResponse,
)
def create_author(
    request: request.CreateAuthorRequest,
) -> response.CreateAuthorResponse:
    """
    This endpoint used to create author
    """
    session = db_session()
    author = author_service.create_author(session, request)
    resp = response.CreateAuthorResponse(data=author)

    return resp


@router.put(
    "/{author_id}",
    status_code=200,
    response_model=response.UpdateAuthorResponse,
)
def update_author(
    author_id: str,
    request: request.UpdateAuthorRequest,
) -> response.UpdateAuthorResponse:
    """
    This endpoint used to update author
    """
    session = db_session()
    author = author_service.update_author(
        session,
        author_id,
        request,
    )
    resp = response.UpdateAuthorResponse(data=author)

    return resp


@router.delete(
    "/{author_id}",
    status_code=200,
    response_model=response.DeleteAuthorResponse,
)
def delete_author(
    author_id: str,
) -> response.DeleteAuthorResponse:
    """
    This endpoint used to delete author
    """
    session = db_session()
    author_service.soft_delete_author(session, author_id)

    return response.DeleteAuthorResponse()


@router.get(
    "/{author_id}",
    status_code=200,
    response_model=response.GetAuthorResponse,
)
def get_author(
    author_id: str,
) -> response.GetAuthorResponse:
    """
    This endpoint used to get author by ID
    """
    session = db_session()
    author = author_service.get_author_by_id(
        session,
        author_id,
        redis_client,
    )
    resp = response.GetAuthorResponse(data=author)

    return resp


@router.get(
    "",
    status_code=200,
    response_model=response.ListAuthorResponse,
)
def list_author() -> response.ListAuthorResponse:
    """
    This endpoint used to list all authors
    """
    session = db_session()
    author_list = author_service.list_author(session)
    resp = response.ListAuthorResponse(data=author_list)

    return resp


@router.get(
    "/{author_id}/books",
    status_code=200,
    response_model=response.ListBookByAuthorIDResponse,
)
def list_book_by_author_id(
    author_id: str,
) -> response.ListBookByAuthorIDResponse:
    """
    This endpoint used to list all books by specific author
    """
    session = db_session()
    book_list = author_service.list_book_by_author_id(session, author_id)
    resp = response.ListBookByAuthorIDResponse(data=book_list)

    return resp
