from pydantic import BaseModel
from typing import Dict, List, Any, Optional


class CreateBookResponse(BaseModel):
    data: Dict[str, Any]
    status: int = 201
    message: str = "Book created successfully"


class UpdateBookResponse(BaseModel):
    data: Optional[Dict[str, Any]]
    status: int = 200
    message: str = "Book updated successfully"


class DeleteBookResponse(BaseModel):
    status: int = 200
    message: str = "Book deleted successfully"


class GetBookResponse(BaseModel):
    data: Optional[Dict[str, Any]]
    status: int = 200
    message: str = "Get book successfully"


class ListBookResponse(BaseModel):
    data: List[Dict[str, Any]]
    status: int = 200
    message: str = "List book successfully"
