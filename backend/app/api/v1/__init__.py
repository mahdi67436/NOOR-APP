"""
NoorGuard Ultimate - API Routes
"""

from fastapi import APIRouter
from app.api.v1 import auth, children, prayers

api_router = APIRouter(prefix="/v1")

# Include routers
api_router.include_router(auth.router)
api_router.include_router(children.router)
api_router.include_router(prayers.router)
