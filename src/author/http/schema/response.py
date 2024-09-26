from pydantic import BaseModel
from typing import Dict, List, Any, Optional


class CreateAuthorResponse(BaseModel):
    data: Dict[str, Any]
    status: int = 201
    message: str = "Author created successfully"


class UpdateAuthorResponse(BaseModel):
    data: Optional[Dict[str, Any]]
    status: int = 200
    message: str = "Author updated successfully"


class DeleteAuthorResponse(BaseModel):
    status: int = 200
    message: str = "Author deleted successfully"


class GetAuthorResponse(BaseModel):
    data: Optional[Dict[str, Any]]
    status: int = 200
    message: str = "Get author successfully"


class ListAuthorResponse(BaseModel):
    data: List[Dict[str, Any]]
    status: int = 200
    message: str = "List author successfully"


class ListBookByAuthorIDResponse(BaseModel):
    data: List[Dict[Any, Any]]
    status: int = 200
    message: str = "List book by author ID successfully"
