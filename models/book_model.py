"""
Book model definition using SQLAlchemy
"""
from sqlalchemy import Column, String, Numeric, Text, DateTime, Boolean, UUID
from sqlalchemy.sql import func
from config.database import Base
import uuid

class Book(Base):
    """
    Book model representing the 'libros' table
    """
    __tablename__ = "libros"
    
    # Primary key
    id_libro = Column(
        UUID(as_uuid=False), 
        primary_key=True, 
        default=lambda: str(uuid.uuid4()),
        comment="Unique identifier for the book"
    )
    
    # Required fields
    name = Column(
        String(255), 
        nullable=False,
        comment="Book title"
    )
    author = Column(
        String(255), 
        nullable=False,
        comment="Book author"
    )
    price = Column(
        Numeric(10, 2), 
        nullable=False,
        comment="Book price with 2 decimal places"
    )
    
    # Optional fields
    description = Column(
        Text,
        nullable=True,
        comment="Book description"
    )
    id_user = Column(
        UUID(as_uuid=False),
        nullable=True,
        comment="User ID who created/owns the book"
    )
    
    # Soft delete flag
    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Soft delete flag"
    )
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Creation timestamp"
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Last update timestamp"
    )
    
    def __repr__(self):
        return f"<Book(id_libro='{self.id_libro}', name='{self.name}', author='{self.author}')>"
    
    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            "id_libro": self.id_libro,
            "name": self.name,
            "author": self.author,
            "price": float(self.price) if self.price else None,
            "description": self.description,
            "id_user": self.id_user,
            "is_deleted": self.is_deleted,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }