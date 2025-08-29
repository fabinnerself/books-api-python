"""
Main FastAPI application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

# Import routers
from api.health import router as health_router
from api.books import router as books_router

# Import database setup
from config.database import create_tables
from config.settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager
    Handles startup and shutdown events
    """
    # Startup
    print("🚀 Starting Books API...")
    print(f"📊 Environment: {settings.APP_ENV}")
    print(f"🔗 Database: {settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
    
    try:
        # Create tables if they don't exist
        await create_tables()
        print("✅ Database tables verified")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        # Don't raise here to allow API to start (useful for health checks)
    
    yield
    
    # Shutdown
    print("🛑 Shutting down Books API...")

# Create FastAPI application
app = FastAPI(
    title="Books API",
    description="A modern RESTful API for managing books with CRUD operations, pagination, search, and filtering",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(books_router)

# Root endpoint
@app.get("/", tags=["Root"])
async def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Books API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health",
        "books": "/api/v1/books"
    }

# Global exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler"""
    return exc.detail if isinstance(exc.detail, dict) else {
        "success": False,
        "error": exc.detail,
        "code": exc.status_code
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.APP_PORT,
        reload=settings.is_development,
        log_level="info" if settings.is_development else "warning"
    )