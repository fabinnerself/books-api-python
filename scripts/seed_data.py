"""
Script to seed sample data into the database
"""
import asyncio
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import AsyncSessionLocal, create_tables
from models.book_model import Book
from schemas.book_schema import BookCreate
from controllers.book_controller import BookController

async def seed_books():
    """Insert sample books data"""
    
    sample_books = [
        BookCreate(
            name="Cien años de soledad",
            author="Gabriel García Márquez",
            price=25.99,
            description="Obra maestra del realismo mágico"
        ),
        BookCreate(
            name="Rayuela",
            author="Julio Cortázar", 
            price=22.50,
            description="Una novela experimental única"
        ),
        BookCreate(
            name="Ficciones",
            author="Jorge Luis Borges",
            price=18.75,
            description="Colección de cuentos magistrales"
        ),
        BookCreate(
            name="El Aleph",
            author="Jorge Luis Borges",
            price=20.00,
            description="Relatos extraordinarios"
        ),
        BookCreate(
            name="Pedro Páramo",
            author="Juan Rulfo",
            price=16.50,
            description="Clásico de la literatura mexicana"
        ),
        BookCreate(
            name="La Casa de los Espíritus",
            author="Isabel Allende",
            price=24.00,
            description="Saga familiar llena de magia"
        ),
        BookCreate(
            name="El Túnel",
            author="Ernesto Sabato",
            price=15.75,
            description="Una obra psicológica intensa"
        ),
        BookCreate(
            name="Sobre Héroes y Tumbas",
            author="Ernesto Sabato",
            price=28.50,
            description="Novela compleja y profunda"
        ),
        BookCreate(
            name="La Ciudad y los Perros",
            author="Mario Vargas Llosa",
            price=23.25,
            description="Retrato crudo de una institución militar"
        ),
        BookCreate(
            name="Conversación en La Catedral",
            author="Mario Vargas Llosa",
            price=26.75,
            description="Análisis de la sociedad peruana"
        )
    ]
    
    try:
        # Create tables first
        await create_tables()
        print("✅ Tables created successfully")
        
        # Insert sample data
        async with AsyncSessionLocal() as db:
            created_count = 0
            
            for book_data in sample_books:
                try:
                    book = await BookController.create_book(db, book_data)
                    created_count += 1
                    print(f"✅ Created: {book.name} by {book.author}")
                except Exception as e:
                    print(f"❌ Error creating book '{book_data.name}': {e}")
            
            print(f"\n🎉 Successfully created {created_count} books out of {len(sample_books)}")
            
    except Exception as e:
        print(f"❌ Error during seeding: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("🌱 Seeding database with sample books...")
    asyncio.run(seed_books())