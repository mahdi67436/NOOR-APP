"""
NoorGuard Ultimate - User Model
SQLAlchemy User Model for Authentication
"""

from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base
from app.core.security import get_password_hash


class UserRole(str, enum.Enum):
    """User roles"""
    ADMIN = "admin"
    PARENT = "parent"
    CHILD = "child"
    VIEWER = "viewer"


class User(Base):
    """User model for authentication and profile management"""
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Authentication
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    
    # Profile
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Role & Status
    role = Column(SQLEnum(UserRole), default=UserRole.PARENT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_premium = Column(Boolean, default=False, nullable=False)
    
    # Security
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    last_login_ip = Column(String(45), nullable=True)
    
    # Preferences
    language = Column(String(10), default="en")
    timezone = Column(String(50), default="UTC")
    notification_enabled = Column(Boolean, default=True)
    
    # Subscription
    subscription_plan = Column(String(50), default="free")
    subscription_expires = Column(DateTime, nullable=True)
    
    # GDPR
    gdpr_consent = Column(Boolean, default=False)
    gdpr_consent_date = Column(DateTime, nullable=True)
    data_export_requested = Column(Boolean, default=False)
    data_delete_requested = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    devices = relationship("Device", back_populates="user", cascade="all, delete-orphan")
    children = relationship("Child", back_populates="parent", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User {self.email} - {self.role.value}>"
    
    @property
    def full_name(self) -> str:
        """Get full name"""
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name
    
    @property
    def is_locked(self) -> bool:
        """Check if account is locked"""
        if self.locked_until and self.locked_until > func.now():
            return True
        return False
    
    def set_password(self, password: str):
        """Set password hash"""
        self.password_hash = get_password_hash(password)
    
    def verify_password(self, password: str) -> bool:
        """Verify password"""
        from app.core.security import verify_password
        return verify_password(password, self.password_hash)
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "phone": self.phone,
            "avatar_url": self.avatar_url,
            "role": self.role.value,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "is_premium": self.is_premium,
            "language": self.language,
            "timezone": self.timezone,
            "subscription_plan": self.subscription_plan,
            "subscription_expires": self.subscription_expires.isoformat() if self.subscription_expires else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class RefreshToken(Base):
    """Refresh token model for JWT"""
    
    __tablename__ = "refresh_tokens"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False, index=True)
    token = Column(String(500), unique=True, nullable=False)
    device_id = Column(String(100), nullable=True)
    device_name = Column(String(200), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    
    # Status
    is_revoked = Column(Boolean, default=False)
    expires_at = Column(DateTime, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="refresh_tokens")
    
    def __repr__(self):
        return f"<RefreshToken {self.id} - User: {self.user_id}>"


class Device(Base):
    """Device model for device management"""
    
    __tablename__ = "devices"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False, index=True)
    
    # Device info
    device_id = Column(String(100), unique=True, nullable=False, index=True)
    device_name = Column(String(200), nullable=False)
    device_type = Column(String(50), nullable=False)  # android, ios
    device_model = Column(String(100), nullable=True)
    device_manufacturer = Column(String(100), nullable=True)
    os_version = Column(String(50), nullable=True)
    app_version = Column(String(20), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_rooted = Column(Boolean, default=False)
    is_trusted = Column(Boolean, default=False)
    
    # Security
    fcm_token = Column(String(500), nullable=True)  # Firebase Cloud Messaging
    last_seen = Column(DateTime, nullable=True)
    ip_address = Column(String(45), nullable=True)
    
    # Location
    last_latitude = Column(String(20), nullable=True)
    last_longitude = Column(String(20), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="devices")
    child_profile = relationship("Child", back_populates="device", uselist=False)
    activities = relationship("Activity", back_populates="device", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Device {self.device_name} - {self.device_id}>"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "device_id": self.device_id,
            "device_name": self.device_name,
            "device_type": self.device_type,
            "device_model": self.device_model,
            "device_manufacturer": self.device_manufacturer,
            "os_version": self.os_version,
            "app_version": self.app_version,
            "is_active": self.is_active,
            "is_rooted": self.is_rooted,
            "is_trusted": self.is_trusted,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Notification(Base):
    """Notification model"""
    
    __tablename__ = "notifications"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=False, index=True)
    
    # Notification content
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), nullable=False)  # alert, info, warning
    priority = Column(String(20), default="normal")  # low, normal, high
    
    # Data
    data = Column(Text, nullable=True)  # JSON string
    
    # Status
    is_read = Column(Boolean, default=False)
    is_sent = Column(Boolean, default=False)
    sent_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    read_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="notifications")
    
    def __repr__(self):
        return f"<Notification {self.title}>"
