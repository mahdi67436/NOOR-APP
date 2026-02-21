"""
NoorGuard Ultimate - Child Profile Model
SQLAlchemy Models for Child Management and Monitoring
"""

from sqlalchemy import Column, String, Boolean, DateTime, Integer, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class ChildStatus(str, enum.Enum):
    """Child profile status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    DELETED = "deleted"


class FilterLevel(str, enum.Enum):
    """Content filter levels"""
    STRICT = "strict"
    MODERATE = "moderate"
    MINIMAL = "minimal"
    OFF = "off"


class Child(Base):
    """Child profile model for monitored device"""
    
    __tablename__ = "children"
    
    # Primary key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    parent_id = Column(String(36), nullable=False, index=True)
    device_id = Column(String(36), ForeignKey("devices.id"), nullable=True)
    
    # Profile
    name = Column(String(100), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    birth_date = Column(DateTime, nullable=True)
    age = Column(Integer, nullable=True)
    
    # Status
    status = Column(String(20), default=ChildStatus.ACTIVE.value)
    is_online = Column(Boolean, default=False)
    last_seen = Column(DateTime, nullable=True)
    
    # Location
    latitude = Column(String(20), nullable=True)
    longitude = Column(String(20), nullable=True)
    address = Column(String(500), nullable=True)
    
    # Filter settings
    filter_level = Column(String(20), default=FilterLevel.MODERATE.value)
    blocked_keywords = Column(JSON, default=list)
    blocked_apps = Column(JSON, default=list)
    blocked_urls = Column(JSON, default=list)
    allowed_apps = Column(JSON, default=list)  # Whitelist mode
    
    # Time restrictions
    daily_screen_time_limit = Column(Integer, default=240)  # minutes
    night_mode_enabled = Column(Boolean, default=True)
    night_mode_start = Column(String(10), default="20:00")  # 8 PM
    night_mode_end = Column(String(10), default="06:00")  # 6 AM
    
    # Ramadan mode
    ramadan_mode = Column(Boolean, default=False)
    ramadan_screen_time_limit = Column(Integer, default=120)  # minutes
    
    # School mode
    school_mode_enabled = Column(Boolean, default=False)
    school_mode_schedule = Column(JSON, nullable=True)  # {start_time, end_time, days}
    
    # Salah mode
    auto_lock_during_prayer = Column(Boolean, default=True)
    prayer_times_enabled = Column(Boolean, default=True)
    
    # AI Monitoring
    addiction_risk_score = Column(Integer, default=0)  # 0-100
    late_night_usage_hours = Column(Integer, default=0)
    suspicious_search_count = Column(Integer, default=0)
    
    # Islamic habits
    prayer_reminder_enabled = Column(Boolean, default=True)
    dhikr_reminder_enabled = Column(Boolean, default=True)
    quran_widget_enabled = Column(Boolean, default=True)
    daily_hadith_enabled = Column(Boolean, default=True)
    islamic_habit_score = Column(Integer, default=50)  # 0-100
    
    # Emergency
    emergency_contact = Column(String(100), nullable=True)
    emergency_number = Column(String(20), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    parent = relationship("User", back_populates="children")
    device = relationship("Device", back_populates="child_profile")
    activities = relationship("Activity", back_populates="child", cascade="all, delete-orphan")
    app_usages = relationship("AppUsage", back_populates="child", cascade="all, delete-orphan")
    blocked_attempts = relationship("BlockedAttempt", back_populates="child", cascade="all, delete-orphan")
    prayer_logs = relationship("PrayerLog", back_populates="child", cascade="all, delete-orphan")
    screen_time_logs = relationship("ScreenTimeLog", back_populates="child", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Child {self.name}>"
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "avatar_url": self.avatar_url,
            "age": self.age,
            "status": self.status,
            "is_online": self.is_online,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "filter_level": self.filter_level,
            "daily_screen_time_limit": self.daily_screen_time_limit,
            "night_mode_enabled": self.night_mode_enabled,
            "school_mode_enabled": self.school_mode_enabled,
            "addiction_risk_score": self.addiction_risk_score,
            "islamic_habit_score": self.islamic_habit_score,
            "auto_lock_during_prayer": self.auto_lock_during_prayer,
            "ramadan_mode": self.ramadan_mode,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Activity(Base):
    """Activity log model for monitoring"""
    
    __tablename__ = "activities"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    child_id = Column(String(36), ForeignKey("children.id"), nullable=False, index=True)
    device_id = Column(String(36), ForeignKey("devices.id"), nullable=False, index=True)
    
    # Activity type
    activity_type = Column(String(50), nullable=False)  # search, app, website, screenshot, etc.
    
    # Content
    title = Column(String(200), nullable=True)
    content = Column(Text, nullable=True)
    url = Column(String(500), nullable=True)
    app_package = Column(String(200), nullable=True)
    
    # Classification
    is_blocked = Column(Boolean, default=False)
    category = Column(String(50), nullable=True)  # adult, violence, gambling, etc.
    ai_confidence = Column(Float, default=0.0)  # AI detection confidence
    
    # Timestamp
    timestamp = Column(DateTime, nullable=False, index=True)
    duration = Column(Integer, default=0)  # seconds
    
    # Location
    latitude = Column(String(20), nullable=True)
    longitude = Column(String(20), nullable=True)
    
    # Additional data
    metadata = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    child = relationship("Child", back_populates="activities")
    device = relationship("Device", back_populates="activities")
    
    def __repr__(self):
        return f"<Activity {self.activity_type} - Child: {self.child_id}>"


class AppUsage(Base):
    """App usage statistics model"""
    
    __tablename__ = "app_usages"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    child_id = Column(String(36), ForeignKey("children.id"), nullable=False, index=True)
    
    # App info
    app_name = Column(String(200), nullable=False)
    app_package = Column(String(200), nullable=False)
    app_category = Column(String(100), nullable=True)
    
    # Usage
    usage_time_minutes = Column(Integer, default=0)
    open_count = Column(Integer, default=0)
    
    # Date
    date = Column(DateTime, nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    child = relationship("Child", back_populates="app_usages")
    
    def __repr__(self):
        return f"<AppUsage {self.app_name}>"


class BlockedAttempt(Base):
    """Blocked content attempts model"""
    
    __tablename__ = "blocked_attempts"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    child_id = Column(String(36), ForeignKey("children.id"), nullable=False, index=True)
    
    # Block type
    block_type = Column(String(50), nullable=False)  # website, app, search, image
    category = Column(String(50), nullable=True)  # adult, violence, etc.
    
    # Content
    url = Column(String(500), nullable=True)
    search_query = Column(String(500), nullable=True)
    app_package = Column(String(200), nullable=True)
    app_name = Column(String(200), nullable=True)
    
    # AI detection
    ai_detected = Column(Boolean, default=False)
    ai_confidence = Column(Float, default=0.0)
    ai_reason = Column(Text, nullable=True)
    
    # Timestamp
    timestamp = Column(DateTime, nullable=False, index=True)
    
    # Location
    latitude = Column(String(20), nullable=True)
    longitude = Column(String(20), nullable=True)
    
    # Alert
    alert_sent = Column(Boolean, default=False)
    parent_notified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    child = relationship("Child", back_populates="blocked_attempts")
    
    def __repr__(self):
        return f"<BlockedAttempt {self.block_type}>"


class ScreenTimeLog(Base):
    """Screen time logging model"""
    
    __tablename__ = "screen_time_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    child_id = Column(String(36), ForeignKey("children.id"), nullable=False, index=True)
    
    # Time
    date = Column(DateTime, nullable=False, index=True)
    hour = Column(Integer, nullable=False)
    
    # Duration
    total_screen_time = Column(Integer, default=0)  # minutes
    app_usage_time = Column(Integer, default=0)
    web_usage_time = Column(Integer, default=0)
    
    # Sessions
    unlock_count = Column(Integer, default=0)
    
    # Night usage
    night_usage_minutes = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    child = relationship("Child", back_populates="screen_time_logs")
    
    def __repr__(self):
        return f"<ScreenTimeLog {self.date}>"


class PrayerLog(Base):
    """Prayer time compliance log"""
    
    __tablename__ = "prayer_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    child_id = Column(String(36), ForeignKey("children.id"), nullable=False, index=True)
    
    # Prayer info
    prayer_name = Column(String(20), nullable=False)  # fajr, dhuhr, asr, maghrib, isha
    scheduled_time = Column(String(10), nullable=False)  # HH:MM
    
    # Compliance
    was_locked = Column(Boolean, default=False)
    was_compliant = Column(Boolean, default=False)
    phone_usage_during_prayer = Column(Integer, default=0)  # minutes
    
    # Time
    prayer_date = Column(DateTime, nullable=False, index=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    child = relationship("Child", back_populates="prayer_logs")
    
    def __repr__(self):
        return f"<PrayerLog {self.prayer_name}>"
