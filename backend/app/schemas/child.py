"""
NoorGuard Ultimate - Child Schemas
Pydantic Models for Child Management
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class FilterLevel(str, Enum):
    """Content filter levels"""
    STRICT = "strict"
    MODERATE = "moderate"
    MINIMAL = "minimal"
    OFF = "off"


class ChildStatus(str, Enum):
    """Child profile status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


# ===================
# Child Schemas
# ===================

class ChildCreate(BaseModel):
    """Create child profile request"""
    name: str = Field(..., min_length=1, max_length=100)
    avatar_url: Optional[str] = None
    birth_date: Optional[datetime] = None
    age: Optional[int] = Field(None, ge=1, le=18)
    device_id: Optional[str] = None
    
    # Filter settings
    filter_level: FilterLevel = FilterLevel.MODERATE
    blocked_keywords: List[str] = []
    blocked_apps: List[str] = []
    blocked_urls: List[str] = []
    allowed_apps: List[str] = []
    
    # Time restrictions
    daily_screen_time_limit: int = Field(240, ge=0)  # minutes
    night_mode_enabled: bool = True
    night_mode_start: str = "20:00"
    night_mode_end: str = "06:00"
    ramadan_mode: bool = False
    ramadan_screen_time_limit: int = Field(120, ge=0)
    school_mode_enabled: bool = False
    school_mode_schedule: Optional[dict] = None
    
    # Islamic features
    auto_lock_during_prayer: bool = True
    prayer_times_enabled: bool = True
    prayer_reminder_enabled: bool = True
    dhikr_reminder_enabled: bool = True
    quran_widget_enabled: bool = True
    daily_hadith_enabled: bool = True
    
    # Emergency
    emergency_contact: Optional[str] = None
    emergency_number: Optional[str] = None


class ChildUpdate(BaseModel):
    """Update child profile request"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    avatar_url: Optional[str] = None
    birth_date: Optional[datetime] = None
    age: Optional[int] = Field(None, ge=1, le=18)
    
    # Filter settings
    filter_level: Optional[FilterLevel] = None
    blocked_keywords: Optional[List[str]] = None
    blocked_apps: Optional[List[str]] = None
    blocked_urls: Optional[List[str]] = None
    allowed_apps: Optional[List[str]] = None
    
    # Time restrictions
    daily_screen_time_limit: Optional[int] = Field(None, ge=0)
    night_mode_enabled: Optional[bool] = None
    night_mode_start: Optional[str] = None
    night_mode_end: Optional[str] = None
    ramadan_mode: Optional[bool] = None
    ramadan_screen_time_limit: Optional[int] = Field(None, ge=0)
    school_mode_enabled: Optional[bool] = None
    school_mode_schedule: Optional[dict] = None
    
    # Islamic features
    auto_lock_during_prayer: Optional[bool] = None
    prayer_times_enabled: Optional[bool] = None
    prayer_reminder_enabled: Optional[bool] = None
    dhikr_reminder_enabled: Optional[bool] = None
    quran_widget_enabled: Optional[bool] = None
    daily_hadith_enabled: Optional[bool] = None
    
    # Emergency
    emergency_contact: Optional[str] = None
    emergency_number: Optional[str] = None
    
    # Status
    status: Optional[ChildStatus] = None


class ChildResponse(BaseModel):
    """Child profile response"""
    id: str
    name: str
    avatar_url: Optional[str]
    age: Optional[int]
    status: str
    is_online: bool
    last_seen: Optional[str]
    filter_level: str
    daily_screen_time_limit: int
    night_mode_enabled: bool
    school_mode_enabled: bool
    addiction_risk_score: int
    islamic_habit_score: int
    auto_lock_during_prayer: bool
    ramadan_mode: bool
    created_at: Optional[str]


class ChildListResponse(BaseModel):
    """List of children response"""
    children: List[ChildResponse]
    total: int


class ChildStatusUpdate(BaseModel):
    """Update child status"""
    status: ChildStatus


# ===================
# Activity Schemas
# ===================

class ActivityCreate(BaseModel):
    """Create activity log"""
    child_id: str
    activity_type: str
    title: Optional[str] = None
    content: Optional[str] = None
    url: Optional[str] = None
    app_package: Optional[str] = None
    is_blocked: bool = False
    category: Optional[str] = None
    ai_confidence: float = 0.0
    timestamp: datetime
    duration: int = 0
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    metadata: Optional[dict] = None


class ActivityResponse(BaseModel):
    """Activity response"""
    id: str
    child_id: str
    activity_type: str
    title: Optional[str]
    content: Optional[str]
    url: Optional[str]
    app_package: Optional[str]
    is_blocked: bool
    category: Optional[str]
    ai_confidence: float
    timestamp: str
    duration: int


class ActivityListResponse(BaseModel):
    """Activity list response"""
    activities: List[ActivityResponse]
    total: int


# ===================
# Blocked Attempt Schemas
# ===================

class BlockedAttemptCreate(BaseModel):
    """Create blocked attempt log"""
    child_id: str
    block_type: str
    category: Optional[str] = None
    url: Optional[str] = None
    search_query: Optional[str] = None
    app_package: Optional[str] = None
    app_name: Optional[str] = None
    ai_detected: bool = False
    ai_confidence: float = 0.0
    ai_reason: Optional[str] = None
    timestamp: datetime
    latitude: Optional[str] = None
    longitude: Optional[str] = None


class BlockedAttemptResponse(BlockedAttemptCreate):
    """Blocked attempt response"""
    id: str
    alert_sent: bool
    parent_notified: bool
    created_at: str
    
    class Config:
        from_attributes = True


class BlockedAttemptListResponse(BaseModel):
    """Blocked attempt list response"""
    attempts: List[BlockedAttemptResponse]
    total: int


# ===================
# Screen Time Schemas
# ===================

class ScreenTimeLogCreate(BaseModel):
    """Create screen time log"""
    child_id: str
    date: datetime
    hour: int
    total_screen_time: int = 0
    app_usage_time: int = 0
    web_usage_time: int = 0
    unlock_count: int = 0
    night_usage_minutes: int = 0


class ScreenTimeLogResponse(BaseModel):
    """Screen time log response"""
    id: str
    child_id: str
    date: str
    hour: int
    total_screen_time: int
    app_usage_time: int
    web_usage_time: int
    unlock_count: int
    night_usage_minutes: int


class DailyScreenTimeResponse(BaseModel):
    """Daily screen time response"""
    date: str
    total_minutes: int
    app_minutes: int
    web_minutes: int
    night_minutes: int
    unlock_count: int


class ScreenTimeAnalyticsResponse(BaseModel):
    """Screen time analytics"""
    daily: List[DailyScreenTimeResponse]
    weekly_average: int
    monthly_average: int
    most_used_apps: List[dict]
    peak_hours: List[int]


# ===================
# App Usage Schemas
# ===================

class AppUsageCreate(BaseModel):
    """Create app usage log"""
    child_id: str
    app_name: str
    app_package: str
    app_category: Optional[str] = None
    usage_time_minutes: int = 0
    open_count: int = 0
    date: datetime


class AppUsageResponse(BaseModel):
    """App usage response"""
    id: str
    child_id: str
    app_name: str
    app_package: str
    app_category: Optional[str]
    usage_time_minutes: int
    open_count: int
    date: str


class AppUsageListResponse(BaseModel):
    """App usage list response"""
    apps: List[AppUsageResponse]
    total: int


# ===================
# Analytics Schemas
# ===================

class AnalyticsOverview(BaseModel):
    """Analytics overview"""
    total_screen_time_today: int
    total_screen_time_week: int
    total_screen_time_month: int
    blocked_attempts_today: int
    blocked_attempts_week: int
    addiction_risk_score: int
    islamic_habit_score: int
    prayer_compliance_rate: float
    top_apps: List[dict]
    activity_timeline: List[dict]


class RiskAssessment(BaseModel):
    """Risk assessment response"""
    addiction_risk_score: int
    risk_level: str  # low, medium, high, critical
    late_night_usage_hours: int
    suspicious_search_count: int
    recommendations: List[str]


class WeeklyReport(BaseModel):
    """Weekly report"""
    week_start: str
    week_end: str
    total_screen_time: int
    daily_average: int
    blocked_attempts: int
    apps_used: List[dict]
    websites_blocked: List[dict]
    prayer_compliance: dict
    islamic_habits: dict
    risk_assessment: RiskAssessment
