"""
Pydantic schemas for Book validation and serialization
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal

class BookBase(BaseModel):
    """Base Book schema with common fields"""
    name: str = Field(..., min_length=1, max_length=255, description="Book title")
    author: str = Field(..., min_length=1, max_length=255, description="Book author")
    price: Decimal = Field(..., gt=0, le=999999.99, description="Book price (positive number)")
    description: Optional[str] = Field(None, description="Book description")
    id_user: Optional[str] = Field(None, description="User ID who owns the book")

class BookCreate(BookBase):
    """Schema for creating a new book"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Rayuela",
                "author": "Julio Cortázar",
                "price": 22.50,
                "description": "Una novela experimental única."
            }
        }
    )

class BookUpdate(BaseModel):
    """Schema for updating an existing book (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[Decimal] = Field(None, gt=0, le=999999.99)
    description: Optional[str] = Field(None)
    id_user: Optional[str] = Field(None)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Rayuela (Edición Especial)",
                "price": 25.00
            }
        }
    )

class BookResponse(BookBase):
    """Schema for book responses"""
    id_libro: str = Field(..., description="Book UUID")
    is_deleted: bool = Field(default=False, description="Soft delete flag")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    model_config = ConfigDict(from_attributes=True)

class BookListResponse(BaseModel):
    """Schema for book list with pagination"""
    success: bool = True
    data: list[BookResponse]
    pagination: dict
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "data": [
                    {
                        "id_libro": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "Rayuela",
                        "author": "Julio Cortázar",
                        "price": 22.50,
                        "description": "Una novela experimental única.",
                        "id_user": None,
                        "is_deleted": False,
                        "created_at": "2024-01-01T12:00:00",
                        "updated_at": "2024-01-01T12:00:00"
                    }
                ],
                "pagination": {
                    "page": 1,
                    "limit": 10,
                    "total": 150,
                    "total_pages": 15
                }
            }
        }
    )

class BookSingleResponse(BaseModel):
    """Schema for single book response"""
    success: bool = True
    data: BookResponse
    
class ErrorResponse(BaseModel):
    """Schema for error responses"""
    success: bool = False
    error: str
    code: int
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": False,
                "error": "Book not found",
                "code": 404
            }
        }
    )