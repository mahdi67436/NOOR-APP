"""
NoorGuard Ultimate - Main Application
FastAPI Backend Entry Point
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from datetime import datetime
import os
import sys

from app.core.config import settings
from app.core.database import init_db
from app.api import api_router
from app.websocket.manager import handle_websocket_client, manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    # Startup
    print(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    
    # Initialize database
    try:
        await init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️ Database initialization warning: {e}")
    
    yield
    
    # Shutdown
    print("🛑 Shutting down application")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API router
app.include_router(api_router, prefix=settings.api_v1_prefix)


# ===================
# WebSocket Endpoint
# ===================

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time updates"""
    await handle_websocket_client(websocket, user_id)


@app.websocket("/ws/{user_id}/device/{device_id}")
async def websocket_device_endpoint(websocket: WebSocket, user_id: str, device_id: str):
    """WebSocket endpoint with device ID"""
    await handle_websocket_client(websocket, user_id, device_id)


# ===================
# Health Check
# ===================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.app_version,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": settings.app_description,
        "docs": "/docs",
        "api": settings.api_v1_prefix
    }


# ===================
# Error Handlers
# ===================

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "path": str(request.url),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# ===================
# Application Info
# ===================

@app.get("/info")
async def app_info():
    """Get application information"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": settings.app_description,
        "environment": "development" if settings.debug else "production",
        "features": [
            "Smart Content Shield",
            "AI Behavioral Monitoring",
            "App Control System",
            "Parent Control Panel",
            "Salah & Islamic Integration",
            "AES-256 Encryption",
            "Real-time WebSocket"
        ],
        "websocket_connections": manager.get_connection_count()
    }


# ===================
# Startup Event
# ===================

@app.on_event("startup")
async def startup_event():
    """Application startup"""
    print(f"""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🛡️  {settings.app_name}                          ║
║                                                           ║
║   Version: {settings.app_version}                                     ║
║   Environment: {'Development' if settings.debug else 'Production'}                         ║
║                                                           ║
║   API: {settings.api_v1_prefix}                                    ║
║   Docs: /docs                                            ║
║   WebSocket: /ws/{{user_id}}                             ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
