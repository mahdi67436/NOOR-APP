"""
NoorGuard Ultimate - User Schemas
Pydantic Models for Request/Response Validation
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User roles"""
    ADMIN = "admin"
    PARENT = "parent"
    CHILD = "child"
    VIEWER = "viewer"


# ===================
# Auth Schemas
# ===================

class UserLogin(BaseModel):
    """User login request"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    device_id: Optional[str] = None
    device_name: Optional[str] = None
    fcm_token: Optional[str] = None


class UserRegister(BaseModel):
    """User registration request"""
    email: EmailStr
    password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    role: UserRole = UserRole.PARENT
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class RefreshTokenRequest(BaseModel):
    """Refresh token request"""
    refresh_token: str


class TokenResponse(BaseModel):
    """Token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    """User response"""
    id: str
    email: str
    first_name: str
    last_name: Optional[str]
    full_name: str
    phone: Optional[str]
    avatar_url: Optional[str]
    role: str
    is_active: bool
    is_verified: bool
    is_premium: bool
    language: str
    timezone: str
    subscription_plan: str
    subscription_expires: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]


class UserUpdate(BaseModel):
    """User update request"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = None
    language: Optional[str] = Field(None, max_length=10)
    timezone: Optional[str] = Field(None, max_length=50)
    notification_enabled: Optional[bool] = None


class ChangePassword(BaseModel):
    """Change password request"""
    old_password: str = Field(..., min_length=8)
    new_password: str = Field(..., min_length=8)


class PasswordResetRequest(BaseModel):
    """Password reset request"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation"""
    token: str
    new_password: str = Field(..., min_length=8)


# ===================
# Device Schemas
# ===================

class DeviceRegister(BaseModel):
    """Device registration request"""
    device_id: str
    device_name: str
    device_type: str
    device_model: Optional[str] = None
    device_manufacturer: Optional[str] = None
    os_version: Optional[str] = None
    app_version: Optional[str] = None
    fcm_token: Optional[str] = None


class DeviceUpdate(BaseModel):
    """Device update request"""
    device_name: Optional[str] = None
    fcm_token: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None


class DeviceResponse(BaseModel):
    """Device response"""
    id: str
    device_id: str
    device_name: str
    device_type: str
    device_model: Optional[str]
    device_manufacturer: Optional[str]
    os_version: Optional[str]
    app_version: Optional[str]
    is_active: bool
    is_rooted: bool
    is_trusted: bool
    last_seen: Optional[str]
    created_at: Optional[str]


class DeviceLocation(BaseModel):
    """Device location update"""
    latitude: str
    longitude: str
    address: Optional[str] = None


# ===================
# Notification Schemas
# ===================

class NotificationResponse(BaseModel):
    """Notification response"""
    id: str
    title: str
    message: str
    notification_type: str
    priority: str
    is_read: bool
    created_at: str
    read_at: Optional[str]


class NotificationMarkRead(BaseModel):
    """Mark notification as read"""
    notification_ids: List[str]


# ===================
# Common Schemas
# ===================

class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Error response"""
    detail: str
    error_code: Optional[str] = None


class PaginatedResponse(BaseModel):
    """Paginated response"""
    items: List
    total: int
    page: int
    page_size: int
    total_pages: int


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: str
    database: str
    redis: Optional[str] = None
