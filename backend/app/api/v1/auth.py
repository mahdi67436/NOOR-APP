"""
NoorGuard Ultimate - Authentication API
User Registration, Login, Token Refresh
"""

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from typing import Optional

from app.core.database import get_db
from app.core.security import (
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    rate_limiter,
    ip_blocker
)
from app.core.config import settings
from app.models.user import User, RefreshToken, Device
from app.schemas.user import (
    UserLogin,
    UserRegister,
    TokenResponse,
    UserResponse,
    UserUpdate,
    ChangePassword,
    RefreshTokenRequest,
    DeviceRegister,
    DeviceResponse,
    MessageResponse
)
from app.core.security import get_current_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db),
    request: Request = None
):
    """Register a new user"""
    
    # Check if email already exists
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user = User(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone,
        role=user_data.role.value if hasattr(user_data.role, 'value') else user_data.role
    )
    user.set_password(user_data.password)
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Generate tokens
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "role": user.role.value}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.id, "email": user.email}
    )
    
    # Save refresh token
    client_ip = request.client.host if request else "unknown"
    refresh_token_obj = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        device_name="web",
        ip_address=client_ip
    )
    db.add(refresh_token_obj)
    await db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.jwt_access_token_expire_minutes * 60
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db),
    request: Request = None
):
    """Login with email and password"""
    
    client_ip = request.client.host if request else "unknown"
    
    # Check if IP is blocked
    if ip_blocker.is_blocked(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many failed attempts. Please try again later."
        )
    
    # Find user
    result = await db.execute(
        select(User).where(User.email == login_data.email)
    )
    user = result.scalar_one_or_none()
    
    if not user or not user.verify_password(login_data.password):
        ip_blocker.record_failed_attempt(client_ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Check if account is locked
    if user.is_locked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is locked. Please try again later."
        )
    
    # Update login info
    user.failed_login_attempts = 0
    user.locked_until = None
    user.last_login = datetime.utcnow()
    user.last_login_ip = client_ip
    
    await db.commit()
    
    # Generate tokens
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "role": user.role.value}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.id, "email": user.email}
    )
    
    # Save refresh token
    refresh_token_obj = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        device_name=login_data.device_name,
        ip_address=client_ip
    )
    db.add(refresh_token_obj)
    
    # Register device if provided
    if login_data.device_id:
        device_result = await db.execute(
            select(Device).where(Device.device_id == login_data.device_id)
        )
        device = device_result.scalar_one_or_none()
        
        if not device:
            device = Device(
                user_id=user.id,
                device_id=login_data.device_id,
                device_name=login_data.device_name or "Unknown Device",
                device_type="android",
                fcm_token=login_data.fcm_token,
                last_seen=datetime.utcnow(),
                ip_address=client_ip
            )
            db.add(device)
    
    await db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.jwt_access_token_expire_minutes * 60
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    token_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
    request: Request = None
):
    """Refresh access token"""
    
    # Decode refresh token
    token_payload = decode_token(token_data.refresh_token)
    
    if not token_payload or token_payload.role != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    # Check if token exists in database
    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token == token_data.refresh_token,
            RefreshToken.is_revoked == False
        )
    )
    stored_token = result.scalar_one_or_none()
    
    if not stored_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found or revoked"
        )
    
    # Get user
    user_result = await db.execute(
        select(User).where(User.id == token_payload.user_id)
    )
    user = user_result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Revoke old refresh token
    stored_token.is_revoked = True
    
    # Generate new tokens
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "role": user.role.value}
    )
    new_refresh_token = create_refresh_token(
        data={"sub": user.id, "email": user.email}
    )
    
    # Save new refresh token
    client_ip = request.client.host if request else "unknown"
    new_refresh_obj = RefreshToken(
        user_id=user.id,
        token=new_refresh_token,
        device_name=stored_token.device_name,
        ip_address=client_ip
    )
    db.add(new_refresh_obj)
    await db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",
        expires_in=settings.jwt_access_token_expire_minutes * 60
    )


@router.post("/logout", response_model=MessageResponse)
async def logout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Logout and revoke refresh token"""
    
    # Revoke all refresh tokens for this user
    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.user_id == current_user.id,
            RefreshToken.is_revoked == False
        )
    )
    tokens = result.scalars().all()
    
    for token in tokens:
        token.is_revoked = True
    
    await db.commit()
    
    return MessageResponse(message="Successfully logged out")


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """Get current user information"""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user information"""
    
    if user_data.first_name is not None:
        current_user.first_name = user_data.first_name
    if user_data.last_name is not None:
        current_user.last_name = user_data.last_name
    if user_data.phone is not None:
        current_user.phone = user_data.phone
    if user_data.avatar_url is not None:
        current_user.avatar_url = user_data.avatar_url
    if user_data.language is not None:
        current_user.language = user_data.language
    if user_data.timezone is not None:
        current_user.timezone = user_data.timezone
    if user_data.notification_enabled is not None:
        current_user.notification_enabled = user_data.notification_enabled
    
    await db.commit()
    await db.refresh(current_user)
    
    return current_user


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    password_data: ChangePassword,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Change user password"""
    
    if not current_user.verify_password(password_data.old_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    current_user.set_password(password_data.new_password)
    await db.commit()
    
    return MessageResponse(message="Password changed successfully")


@router.post("/device/register", response_model=DeviceResponse)
async def register_device(
    device_data: DeviceRegister,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    request: Request = None
):
    """Register a new device"""
    
    client_ip = request.client.host if request else "unknown"
    
    # Check if device already exists
    result = await db.execute(
        select(Device).where(Device.device_id == device_data.device_id)
    )
    device = result.scalar_one_or_none()
    
    if device:
        # Update existing device
        device.device_name = device_data.device_name
        device.fcm_token = device_data.fcm_token
        device.last_seen = datetime.utcnow()
    else:
        # Create new device
        device = Device(
            user_id=current_user.id,
            device_id=device_data.device_id,
            device_name=device_data.device_name,
            device_type=device_data.device_type,
            device_model=device_data.device_model,
            device_manufacturer=device_data.device_manufacturer,
            os_version=device_data.os_version,
            app_version=device_data.app_version,
            fcm_token=device_data.fcm_token,
            last_seen=datetime.utcnow(),
            ip_address=client_ip
        )
        db.add(device)
    
    await db.commit()
    await db.refresh(device)
    
    return device


@router.get("/devices", response_model=list[DeviceResponse])
async def get_user_devices(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all devices for current user"""
    
    result = await db.execute(
        select(Device).where(Device.user_id == current_user.id)
    )
    devices = result.scalars().all()
    
    return devices
