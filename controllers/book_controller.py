"""
Book controller with business logic
"""
import uuid
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.exc import SQLAlchemyError
from models.book_model import Book
from schemas.book_schema import BookCreate, BookUpdate
import math

class BookController:
    """Controller class for Book operations"""
    
    @staticmethod
    async def get_books(
        db: AsyncSession,
        page: int = 1,
        limit: int = 10,
        q: Optional[str] = None,
        author: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Get books with pagination, search and filters
        
        Args:
            db: Database session
            page: Page number (starts at 1)
            limit: Items per page
            q: Search query (searches in name and description)
            author: Filter by author
            min_price: Minimum price filter
            max_price: Maximum price filter
            
        Returns:
            Dictionary with books data and pagination info
        """
        try:
            # Base query - only non-deleted books
            query = select(Book).where(Book.is_deleted == False)
            
            # Apply search filter
            if q:
                search_filter = or_(
                    Book.name.ilike(f"%{q}%"),
                    Book.description.ilike(f"%{q}%"),
                    Book.author.ilike(f"%{q}%")
                )
                query = query.where(search_filter)
            
            # Apply author filter
            if author:
                query = query.where(Book.author.ilike(f"%{author}%"))
            
            # Apply price filters
            if min_price is not None:
                query = query.where(Book.price >= min_price)
            if max_price is not None:
                query = query.where(Book.price <= max_price)
            
            # Count total records for pagination
            count_query = select(func.count()).select_from(query.subquery())
            total_result = await db.execute(count_query)
            total = total_result.scalar()
            
            # Calculate pagination
            total_pages = math.ceil(total / limit) if total > 0 else 0
            offset = (page - 1) * limit
            
            # Apply pagination and ordering
            query = query.order_by(Book.created_at.desc()).offset(offset).limit(limit)
            
            # Execute query
            result = await db.execute(query)
            books = result.scalars().all()
            
            return {
                "books": books,
                "pagination": {
                    "page": page,
                    "limit": limit,
                    "total": total,
                    "total_pages": total_pages
                }
            }
            
        except SQLAlchemyError as e:
            raise Exception(f"Database error: {str(e)}")
    
    @staticmethod
    async def get_book_by_id(db: AsyncSession, book_id: str) -> Optional[Book]:
        """
        Get a single book by UUID
        
        Args:
            db: Database session
            book_id: Book UUID
            
        Returns:
            Book instance or None if not found
        """
        try:
            # Validate UUID format
            uuid.UUID(book_id)
            
            query = select(Book).where(
                and_(Book.id_libro == book_id, Book.is_deleted == False)
            )
            result = await db.execute(query)
            return result.scalar_one_or_none()
            
        except ValueError:
            raise Exception("Invalid UUID format")
        except SQLAlchemyError as e:
            raise Exception(f"Database error: {str(e)}")
    
    @staticmethod
    async def create_book(db: AsyncSession, book_data: BookCreate) -> Book:
        """
        Create a new book
        
        Args:
            db: Database session
            book_data: Book creation data
            
        Returns:
            Created book instance
        """
        try:
            # Create new book instance
            new_book = Book(
                name=book_data.name,
                author=book_data.author,
                price=book_data.price,
                description=book_data.description,
                id_user=book_data.id_user
            )
            
            # Add to database
            db.add(new_book)
            await db.commit()
            await db.refresh(new_book)
            
            return new_book
            
        except SQLAlchemyError as e:
            await db.rollback()
            raise Exception(f"Database error: {str(e)}")
    
    @staticmethod
    async def update_book(
        db: AsyncSession, 
        book_id: str, 
        book_data: BookUpdate
    ) -> Optional[Book]:
        """
        Update an existing book
        
        Args:
            db: Database session
            book_id: Book UUID
            book_data: Book update data
            
        Returns:
            Updated book instance or None if not found
        """
        try:
            # Get existing book
            book = await BookController.get_book_by_id(db, book_id)
            if not book:
                return None
            
            # Update only provided fields
            update_data = book_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                if hasattr(book, field):
                    setattr(book, field, value)
            
            await db.commit()
            await db.refresh(book)
            
            return book
            
        except SQLAlchemyError as e:
            await db.rollback()
            raise Exception(f"Database error: {str(e)}")
    
    @staticmethod
    async def delete_book(db: AsyncSession, book_id: str) -> bool:
        """
        Soft delete a book (set is_deleted = True)
        
        Args:
            db: Database session
            book_id: Book UUID
            
        Returns:
            True if deleted successfully, False if not found
        """
        try:
            # Get existing book
            book = await BookController.get_book_by_id(db, book_id)
            if not book:
                return False
            
            # Soft delete
            book.is_deleted = True
            await db.commit()
            
            return True
            
        except SQLAlchemyError as e:
            await db.rollback()
            raise Exception(f"Database error: {str(e)}")