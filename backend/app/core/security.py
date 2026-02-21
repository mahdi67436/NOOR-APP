"""
NoorGuard Ultimate - Security Module
JWT Authentication, Password Hashing, and Token Management
"""

from datetime import datetime, timedelta
from typing import Optional, List, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
import secrets
import string

from app.core.config import settings
from app.core.database import get_db


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_v1_prefix}/auth/login")


class TokenData:
    """Token payload data"""
    def __init__(self, user_id: str, email: str, role: str):
        self.user_id = user_id
        self.email = email
        self.role = role


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.jwt_secret_key, 
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create a JWT refresh token"""
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(days=settings.jwt_refresh_token_expire_days)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.jwt_secret_key, 
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def decode_token(token: str) -> Optional[TokenData]:
    """Decode and validate a JWT token"""
    try:
        payload = jwt.decode(
            token, 
            settings.jwt_secret_key, 
            algorithms=[settings.jwt_algorithm]
        )
        
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        role: str = payload.get("role", "user")
        
        if user_id is None or email is None:
            return None
        
        return TokenData(user_id=user_id, email=email, role=role)
    except JWTError:
        return None


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """Get current authenticated user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = decode_token(token)
    
    if token_data is None:
        raise credentials_exception
    
    # Import here to avoid circular imports
    from app.models.user import User
    
    # Query user from database
    from sqlalchemy import select
    result = await db.execute(
        select(User).where(User.id == token_data.user_id)
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    return user


async def get_current_active_user(
    current_user = Depends(get_current_user)
):
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def require_role(allowed_roles: List[str]):
    """Dependency to check user role"""
    async def role_checker(current_user = Depends(get_current_active_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker


def generate_device_id() -> str:
    """Generate a unique device ID"""
    return secrets.token_urlsafe(32)


def generate_verification_code(length: int = 6) -> str:
    """Generate a numeric verification code"""
    return ''.join(secrets.choice(string.digits) for _ in range(length))


def generate_api_key() -> str:
    """Generate an API key"""
    return f"ng_{secrets.token_urlsafe(32)}"


def verify_api_key(api_key: str) -> bool:
    """Verify an API key format"""
    if not api_key.startswith("ng_"):
        return False
    if len(api_key) < 40:
        return False
    return True


class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: dict = {}
    
    async def check_rate_limit(self, identifier: str) -> bool:
        """Check if request is within rate limit"""
        now = datetime.utcnow()
        
        if identifier not in self.requests:
            self.requests[identifier] = []
        
        # Remove old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if (now - req_time).total_seconds() < self.window_seconds
        ]
        
        if len(self.requests[identifier]) >= self.max_requests:
            return False
        
        self.requests[identifier].append(now)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter()


class IPBlocker:
    """IP-based blocking for security"""
    
    def __init__(self):
        self.blocked_ips: set = {}
        self.failed_attempts: dict = {}
    
    def record_failed_attempt(self, ip: str):
        """Record a failed login attempt"""
        if ip not in self.failed_attempts:
            self.failed_attempts[ip] = 0
        
        self.failed_attempts[ip] += 1
        
        # Block after 5 failed attempts
        if self.failed_attempts[ip] >= 5:
            self.blocked_ips.add(ip)
    
    def is_blocked(self, ip: str) -> bool:
        """Check if IP is blocked"""
        return ip in self.blocked_ips
    
    def unblock_ip(self, ip: str):
        """Unblock an IP"""
        self.blocked_ips.discard(ip)
        if ip in self.failed_attempts:
            del self.failed_attempts[ip]


# Global IP blocker instance
ip_blocker = IPBlocker()
