"""
Database connection and session management
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from config.settings import settings

# Enable SSL for asyncpg if requested (e.g., when using Neon)
connect_args = {"ssl": True} if settings.DB_SSLMODE.lower() in ("require", "verify-full", "verify-ca") else {}

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.is_development,  # Show SQL queries in development
    future=True,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
    connect_args=connect_args,
)

# Create async session maker
AsyncSessionLocal = async_sessionmaker(
    engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

# Create base model with metadata
metadata = MetaData()
Base = declarative_base(metadata=metadata)

async def get_database_session():
    """
    Dependency to get database session
    This will be used with FastAPI's Depends()
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()

async def create_tables():
    """Create all tables defined in models"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def drop_tables():
    """Drop all tables (use with caution!)"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)