"""
Books API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from config.database import get_database_session
from controllers.book_controller import BookController
from schemas.book_schema import (
    BookCreate, 
    BookUpdate, 
    BookListResponse, 
    BookSingleResponse,
    ErrorResponse
)

router = APIRouter(prefix="/api/v1/books", tags=["Books"])

@router.get(
    "/",
    response_model=BookListResponse,
    summary="Get books with pagination and filters",
    description="Retrieve books with support for pagination, search, and filtering by author and price range"
)
async def get_books(
    page: int = Query(1, ge=1, description="Page number (starts at 1)"),
    limit: int = Query(10, ge=1, le=100, description="Items per page (max 100)"),
    q: Optional[str] = Query(None, description="Search query (searches in name, author, description)"),
    author: Optional[str] = Query(None, description="Filter by author"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    db: AsyncSession = Depends(get_database_session)
):
    """Get books with pagination, search and filters"""
    try:
        # Validate price range
        if min_price is not None and max_price is not None and min_price > max_price:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "error": "min_price cannot be greater than max_price",
                    "code": 400
                }
            )
        
        result = await BookController.get_books(
            db=db,
            page=page,
            limit=limit,
            q=q,
            author=author,
            min_price=min_price,
            max_price=max_price
        )
        
        return {
            "success": True,
            "data": result["books"],
            "pagination": result["pagination"]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "code": 500
            }
        )

@router.get(
    "/{book_id}",
    response_model=BookSingleResponse,
    summary="Get book by ID",
    description="Retrieve a single book by its UUID"
)
async def get_book(
    book_id: str,
    db: AsyncSession = Depends(get_database_session)
):
    """Get a single book by UUID"""
    try:
        book = await BookController.get_book_by_id(db, book_id)
        
        if not book:
            raise HTTPException(
                status_code=404,
                detail={
                    "success": False,
                    "error": "Book not found",
                    "code": 404
                }
            )
        
        return {
            "success": True,
            "data": book
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "code": 500
            }
        )

@router.post(
    "/",
    response_model=BookSingleResponse,
    status_code=201,
    summary="Create a new book",
    description="Create a new book with validation"
)
async def create_book(
    book_data: BookCreate,
    db: AsyncSession = Depends(get_database_session)
):
    """Create a new book"""
    try:
        book = await BookController.create_book(db, book_data)
        
        return {
            "success": True,
            "data": book
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "code": 500
            }
        )

@router.put(
    "/{book_id}",
    response_model=BookSingleResponse,
    summary="Update a book",
    description="Update an existing book by UUID"
)
async def update_book(
    book_id: str,
    book_data: BookUpdate,
    db: AsyncSession = Depends(get_database_session)
):
    """Update an existing book"""
    try:
        book = await BookController.update_book(db, book_id, book_data)
        
        if not book:
            raise HTTPException(
                status_code=404,
                detail={
                    "success": False,
                    "error": "Book not found",
                    "code": 404
                }
            )
        
        return {
            "success": True,
            "data": book
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "code": 500
            }
        )

@router.delete(
    "/{book_id}",
    summary="Delete a book",
    description="Soft delete a book by UUID (sets is_deleted = true)"
)
async def delete_book(
    book_id: str,
    db: AsyncSession = Depends(get_database_session)
):
    """Soft delete a book"""
    try:
        deleted = await BookController.delete_book(db, book_id)
        
        if not deleted:
            raise HTTPException(
                status_code=404,
                detail={
                    "success": False,
                    "error": "Book not found",
                    "code": 404
                }
            )
        
        return {
            "success": True,
            "message": "Book deleted successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": str(e),
                "code": 500
            }
        )