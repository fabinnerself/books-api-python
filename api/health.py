"""
Health check endpoint
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from config.database import get_database_session
from config.settings import settings
from datetime import datetime, timezone

router = APIRouter(prefix="/api/v1", tags=["Health"])

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_database_session)):
    """
    Health check endpoint to verify API and database connectivity
    
    Returns:
        JSON response with API status and database connectivity
    """
    try:
        # Test database connection
        await db.execute(text("SELECT 1"))
        
        return {
            "success": True,
            "message": "Books API is running",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "environment": settings.APP_ENV,
            "database": "connected",
            "version": "1.0.0"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "success": False,
                "error": "Database connection failed",
                "message": str(e),
                "code": 503
            }
        )