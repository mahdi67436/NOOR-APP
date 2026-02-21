"""
NoorGuard Ultimate - Children Management API
Child Profile CRUD, Monitoring, and Control
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_
from datetime import datetime, timedelta
from typing import Optional, List
import json

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import MonitoringConfig
from app.models.user import User, Device
from app.models.child import (
    Child, Activity, AppUsage, BlockedAttempt, 
    ScreenTimeLog, PrayerLog, ChildStatus
)
from app.schemas.child import (
    ChildCreate, ChildUpdate, ChildResponse, ChildListResponse,
    ActivityCreate, ActivityResponse, ActivityListResponse,
    BlockedAttemptCreate, BlockedAttemptResponse, BlockedAttemptListResponse,
    ScreenTimeLogCreate, ScreenTimeLogResponse, DailyScreenTimeResponse,
    ScreenTimeAnalyticsResponse, AppUsageCreate, AppUsageResponse, AppUsageListResponse,
    AnalyticsOverview, RiskAssessment, WeeklyReport, FilterLevel, ChildStatusUpdate
)
from app.schemas.user import MessageResponse


router = APIRouter(prefix="/children", tags=["Children"])


# ===================
# Child Profile CRUD
# ===================

@router.post("", response_model=ChildResponse, status_code=status.HTTP_201_CREATED)
async def create_child(
    child_data: ChildCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new child profile"""
    
    # If device_id provided, verify ownership
    if child_data.device_id:
        result = await db.execute(
            select(Device).where(
                Device.id == child_data.device_id,
                Device.user_id == current_user.id
            )
        )
        device = result.scalar_one_or_none()
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Device not found or not owned by user"
            )
    
    # Create child profile
    child = Child(
        parent_id=current_user.id,
        device_id=child_data.device_id,
        name=child_data.name,
        avatar_url=child_data.avatar_url,
        birth_date=child_data.birth_date,
        age=child_data.age,
        filter_level=child_data.filter_level.value,
        blocked_keywords=json.dumps(child_data.blocked_keywords),
        blocked_apps=json.dumps(child_data.blocked_apps),
        blocked_urls=json.dumps(child_data.blocked_urls),
        allowed_apps=json.dumps(child_data.allowed_apps),
        daily_screen_time_limit=child_data.daily_screen_time_limit,
        night_mode_enabled=child_data.night_mode_enabled,
        night_mode_start=child_data.night_mode_start,
        night_mode_end=child_data.night_mode_end,
        ramadan_mode=child_data.ramadan_mode,
        ramadan_screen_time_limit=child_data.ramadan_screen_time_limit,
        school_mode_enabled=child_data.school_mode_enabled,
        school_mode_schedule=json.dumps(child_data.school_mode_schedule) if child_data.school_mode_schedule else None,
        auto_lock_during_prayer=child_data.auto_lock_during_prayer,
        prayer_times_enabled=child_data.prayer_times_enabled,
        prayer_reminder_enabled=child_data.prayer_reminder_enabled,
        dhikr_reminder_enabled=child_data.dhikr_reminder_enabled,
        quran_widget_enabled=child_data.quran_widget_enabled,
        daily_hadith_enabled=child_data.daily_hadith_enabled,
        emergency_contact=child_data.emergency_contact,
        emergency_number=child_data.emergency_number
    )
    
    db.add(child)
    await db.commit()
    await db.refresh(child)
    
    return child


@router.get("", response_model=ChildListResponse)
async def get_children(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """Get all children for current user"""
    
    # Count total
    count_result = await db.execute(
        select(func.count(Child.id)).where(Child.parent_id == current_user.id)
    )
    total = count_result.scalar()
    
    # Get children
    offset = (page - 1) * page_size
    result = await db.execute(
        select(Child)
        .where(Child.parent_id == current_user.id)
        .order_by(desc(Child.created_at))
        .offset(offset)
        .limit(page_size)
    )
    children = result.scalars().all()
    
    return ChildListResponse(
        children=[ChildResponse.model_validate(c) for c in children],
        total=total
    )


@router.get("/{child_id}", response_model=ChildResponse)
async def get_child(
    child_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get child profile by ID"""
    
    result = await db.execute(
        select(Child).where(
            Child.id == child_id,
            Child.parent_id == current_user.id
        )
    )
    child = result.scalar_one_or_none()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    return child


@router.put("/{child_id}", response_model=ChildResponse)
async def update_child(
    child_id: str,
    child_data: ChildUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update child profile"""
    
    result = await db.execute(
        select(Child).where(
            Child.id == child_id,
            Child.parent_id == current_user.id
        )
    )
    child = result.scalar_one_or_none()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    # Update fields
    if child_data.name is not None:
        child.name = child_data.name
    if child_data.avatar_url is not None:
        child.avatar_url = child_data.avatar_url
    if child_data.birth_date is not None:
        child.birth_date = child_data.birth_date
    if child_data.age is not None:
        child.age = child_data.age
    if child_data.filter_level is not None:
        child.filter_level = child_data.filter_level.value
    if child_data.blocked_keywords is not None:
        child.blocked_keywords = json.dumps(child_data.blocked_keywords)
    if child_data.blocked_apps is not None:
        child.blocked_apps = json.dumps(child_data.blocked_apps)
    if child_data.blocked_urls is not None:
        child.blocked_urls = json.dumps(child_data.blocked_urls)
    if child_data.allowed_apps is not None:
        child.allowed_apps = json.dumps(child_data.allowed_apps)
    if child_data.daily_screen_time_limit is not None:
        child.daily_screen_time_limit = child_data.daily_screen_time_limit
    if child_data.night_mode_enabled is not None:
        child.night_mode_enabled = child_data.night_mode_enabled
    if child_data.night_mode_start is not None:
        child.night_mode_start = child_data.night_mode_start
    if child_data.night_mode_end is not None:
        child.night_mode_end = child_data.night_mode_end
    if child_data.ramadan_mode is not None:
        child.ramadan_mode = child_data.ramadan_mode
    if child_data.ramadan_screen_time_limit is not None:
        child.ramadan_screen_time_limit = child_data.ramadan_screen_time_limit
    if child_data.school_mode_enabled is not None:
        child.school_mode_enabled = child_data.school_mode_enabled
    if child_data.school_mode_schedule is not None:
        child.school_mode_schedule = json.dumps(child_data.school_mode_schedule)
    if child_data.auto_lock_during_prayer is not None:
        child.auto_lock_during_prayer = child_data.auto_lock_during_prayer
    if child_data.prayer_times_enabled is not None:
        child.prayer_times_enabled = child_data.prayer_times_enabled
    if child_data.prayer_reminder_enabled is not None:
        child.prayer_reminder_enabled = child_data.prayer_reminder_enabled
    if child_data.dhikr_reminder_enabled is not None:
        child.dhikr_reminder_enabled = child_data.dhikr_reminder_enabled
    if child_data.quran_widget_enabled is not None:
        child.quran_widget_enabled = child_data.quran_widget_enabled
    if child_data.daily_hadith_enabled is not None:
        child.daily_hadith_enabled = child_data.daily_hadith_enabled
    if child_data.emergency_contact is not None:
        child.emergency_contact = child_data.emergency_contact
    if child_data.emergency_number is not None:
        child.emergency_number = child_data.emergency_number
    if child_data.status is not None:
        child.status = child_data.status.value
    
    await db.commit()
    await db.refresh(child)
    
    return child


@router.delete("/{child_id}", response_model=MessageResponse)
async def delete_child(
    child_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete child profile"""
    
    result = await db.execute(
        select(Child).where(
            Child.id == child_id,
            Child.parent_id == current_user.id
        )
    )
    child = result.scalar_one_or_none()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    await db.delete(child)
    await db.commit()
    
    return MessageResponse(message="Child profile deleted successfully")


# ===================
# Activity Logging
# ===================

@router.post("/activity", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def log_activity(
    activity_data: ActivityCreate,
    db: AsyncSession = Depends(get_db)
):
    """Log an activity from child device"""
    
    activity = Activity(
        child_id=activity_data.child_id,
        device_id=activity_data.child_id,  # This should be device_id in real implementation
        activity_type=activity_data.activity_type,
        title=activity_data.title,
        content=activity_data.content,
        url=activity_data.url,
        app_package=activity_data.app_package,
        is_blocked=activity_data.is_blocked,
        category=activity_data.category,
        ai_confidence=activity_data.ai_confidence,
        timestamp=activity_data.timestamp,
        duration=activity_data.duration,
        latitude=activity_data.latitude,
        longitude=activity_data.longitude,
        metadata=json.dumps(activity_data.metadata) if activity_data.metadata else None
    )
    
    db.add(activity)
    await db.commit()
    
    return MessageResponse(message="Activity logged")


@router.get("/{child_id}/activities", response_model=ActivityListResponse)
async def get_child_activities(
    child_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    activity_type: Optional[str] = None,
    is_blocked: Optional[bool] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """Get child activities"""
    
    # Verify ownership
    child_result = await db.execute(
        select(Child).where(
            Child.id == child_id,
            Child.parent_id == current_user.id
        )
    )
    child = child_result.scalar_one_or_none()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    # Build query
    query = select(Activity).where(Activity.child_id == child_id)
    
    if activity_type:
        query = query.where(Activity.activity_type == activity_type)
    if is_blocked is not None:
        query = query.where(Activity.is_blocked == is_blocked)
    if start_date:
        query = query.where(Activity.timestamp >= start_date)
    if end_date:
        query = query.where(Activity.timestamp <= end_date)
    
    # Count total
    count_result = await db.execute(
        select(func.count(Activity.id)).where(Activity.child_id == child_id)
    )
    total = count_result.scalar()
    
    # Get activities
    offset = (page - 1) * page_size
    result = await db.execute(
        query.order_by(desc(Activity.timestamp))
        .offset(offset)
        .limit(page_size)
    )
    activities = result.scalars().all()
    
    return ActivityListResponse(
        activities=[ActivityResponse.model_validate(a) for a in activities],
        total=total
    )


# ===================
# Blocked Attempts
# ===================

@router.post("/blocked", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def log_blocked_attempt(
    attempt_data: BlockedAttemptCreate,
    db: AsyncSession = Depends(get_db)
):
    """Log a blocked attempt"""
    
    attempt = BlockedAttempt(
        child_id=attempt_data.child_id,
        block_type=attempt_data.block_type,
        category=attempt_data.category,
        url=attempt_data.url,
        search_query=attempt_data.search_query,
        app_package=attempt_data.app_package,
        app_name=attempt_data.app_name,
        ai_detected=attempt_data.ai_detected,
        ai_confidence=attempt_data.ai_confidence,
        ai_reason=attempt_data.ai_reason,
        timestamp=attempt_data.timestamp,
        latitude=attempt_data.latitude,
        longitude=attempt_data.longitude
    )
    
    db.add(attempt)
    await db.commit()
    
    return MessageResponse(message="Blocked attempt logged")


@router.get("/{child_id}/blocked", response_model=BlockedAttemptListResponse)
async def get_blocked_attempts(
    child_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    block_type: Optional[str] = None,
    category: Optional[str] = None
):
    """Get blocked attempts for child"""
    
    # Verify ownership
    child_result = await db.execute(
        select(Child).where(
            Child.id == child_id,
            Child.parent_id == current_user.id
        )
    )
    if not child_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    # Build query
    query = select(BlockedAttempt).where(BlockedAttempt.child_id == child_id)
    
    if block_type:
        query = query.where(BlockedAttempt.block_type == block_type)
    if category:
        query = query.where(BlockedAttempt.category == category)
    
    # Count total
    count_result = await db.execute(
        select(func.count(BlockedAttempt.id)).where(BlockedAttempt.child_id == child_id)
    )
    total = count_result.scalar()
    
    # Get attempts
    offset = (page - 1) * page_size
    result = await db.execute(
        query.order_by(desc(BlockedAttempt.timestamp))
        .offset(offset)
        .limit(page_size)
    )
    attempts = result.scalars().all()
    
    return BlockedAttemptListResponse(
        attempts=[BlockedAttemptResponse.model_validate(a) for a in attempts],
        total=total
    )


# ===================
# Screen Time
# ===================

@router.post("/screen-time", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def log_screen_time(
    screen_time_data: ScreenTimeLogCreate,
    db: AsyncSession = Depends(get_db)
):
    """Log screen time data"""
    
    log = ScreenTimeLog(
        child_id=screen_time_data.child_id,
        date=screen_time_data.date,
        hour=screen_time_data.hour,
        total_screen_time=screen_time_data.total_screen_time,
        app_usage_time=screen_time_data.app_usage_time,
        web_usage_time=screen_time_data.web_usage_time,
        unlock_count=screen_time_data.unlock_count,
        night_usage_minutes=screen_time_data.night_usage_minutes
    )
    
    db.add(log)
    await db.commit()
    
    return MessageResponse(message="Screen time logged")


@router.get("/{child_id}/screen-time/daily", response_model=List[DailyScreenTimeResponse])
async def get_daily_screen_time(
    child_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    days: int = Query(7, ge=1, le=30)
):
    """Get daily screen time for child"""
    
    # Verify ownership
    child_result = await db.execute(
        select(Child).where(
            Child.id == child_id,
            Child.parent_id == current_user.id
        )
    )
    if not child_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    result = await db.execute(
        select(ScreenTimeLog)
        .where(
            ScreenTimeLog.child_id == child_id,
            ScreenTimeLog.date >= start_date
        )
        .order_by(ScreenTimeLog.date)
    )
    logs = result.scalars().all()
    
    # Aggregate by date
    daily_data = {}
    for log in logs:
        date_key = log.date.date().isoformat()
        if date_key not in daily_data:
            daily_data[date_key] = {
                "date": date_key,
                "total_minutes": 0,
                "app_minutes": 0,
                "web_minutes": 0,
                "night_minutes": 0,
                "unlock_count": 0
            }
        daily_data[date_key]["total_minutes"] += log.total_screen_time
        daily_data[date_key]["app_minutes"] += log.app_usage_time
        daily_data[date_key]["web_minutes"] += log.web_usage_time
        daily_data[date_key]["night_minutes"] += log.night_usage_minutes
        daily_data[date_key]["unlock_count"] += log.unlock_count
    
    return [DailyScreenTimeResponse(**v) for v in daily_data.values()]


@router.get("/{child_id}/analytics", response_model=AnalyticsOverview)
async def get_child_analytics(
    child_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get analytics overview for child"""
    
    # Verify ownership
    child_result = await db.execute(
        select(Child).where(
            Child.id == child_id,
            Child.parent_id == current_user.id
        )
    )
    child = child_result.scalar_one_or_none()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Get screen time totals
    today_start = datetime.combine(today, datetime.min.time())
    
    # Today's screen time
    today_st_result = await db.execute(
        select(func.sum(ScreenTimeLog.total_screen_time))
        .where(
            ScreenTimeLog.child_id == child_id,
            ScreenTimeLog.date >= today_start
        )
    )
    total_screen_time_today = today_st_result.scalar() or 0
    
    # Week screen time
    week_st_result = await db.execute(
        select(func.sum(ScreenTimeLog.total_screen_time))
        .where(
            ScreenTimeLog.child_id == child_id,
            ScreenTimeLog.date >= week_ago
        )
    )
    total_screen_time_week = week_st_result.scalar() or 0
    
    # Month screen time
    month_st_result = await db.execute(
        select(func.sum(ScreenTimeLog.total_screen_time))
        .where(
            ScreenTimeLog.child_id == child_id,
            ScreenTimeLog.date >= month_ago
        )
    )
    total_screen_time_month = month_st_result.scalar() or 0
    
    # Today's blocked attempts
    blocked_today_result = await db.execute(
        select(func.count(BlockedAttempt.id))
        .where(
            BlockedAttempt.child_id == child_id,
            BlockedAttempt.timestamp >= today_start
        )
    )
    blocked_attempts_today = blocked_today_result.scalar() or 0
    
    # Week blocked attempts
    blocked_week_result = await db.execute(
        select(func.count(BlockedAttempt.id))
        .where(
            BlockedAttempt.child_id == child_id,
            BlockedAttempt.timestamp >= week_ago
        )
    )
    blocked_attempts_week = blocked_week_result.scalar() or 0
    
    # Top apps
    top_apps_result = await db.execute(
        select(AppUsage.app_name, func.sum(AppUsage.usage_time_minutes).label("total"))
        .where(AppUsage.child_id == child_id)
        .group_by(AppUsage.app_name)
        .order_by(desc("total"))
        .limit(5)
    )
    top_apps = [{"name": row[0], "minutes": row[1]} for row in top_apps_result.all()]
    
    return AnalyticsOverview(
        total_screen_time_today=total_screen_time_today,
        total_screen_time_week=total_screen_time_week,
        total_screen_time_month=total_screen_time_month,
        blocked_attempts_today=blocked_attempts_today,
        blocked_attempts_week=blocked_attempts_week,
        addiction_risk_score=child.addiction_risk_score,
        islamic_habit_score=child.islamic_habit_score,
        prayer_compliance_rate=75.0,  # Calculate from prayer logs
        top_apps=top_apps,
        activity_timeline=[]
    )


@router.get("/{child_id}/risk-assessment", response_model=RiskAssessment)
async def get_risk_assessment(
    child_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get risk assessment for child"""
    
    # Verify ownership
    child_result = await db.execute(
        select(Child).where(
            Child.id == child_id,
            Child.parent_id == current_user.id
        )
    )
    child = child_result.scalar_one_or_none()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    # Determine risk level
    score = child.addiction_risk_score
    if score >= MonitoringConfig.HIGH_RISK_SCORE:
        risk_level = "critical"
    elif score >= 60:
        risk_level = "high"
    elif score >= MonitoringConfig.MEDIUM_RISK_SCORE:
        risk_level = "medium"
    else:
        risk_level = "low"
    
    # Generate recommendations
    recommendations = []
    if child.late_night_usage_hours > 2:
        recommendations.append("Consider enabling stricter night mode restrictions")
    if child.suspicious_search_count > 10:
        recommendations.append("Review search history and update content filters")
    if child.addiction_risk_score > MonitoringConfig.MEDIUM_RISK_SCORE:
        recommendations.append("Consider setting up device-free family time")
    if child.islamic_habit_score < 50:
        recommendations.append("Enable Islamic reminders to improve habits")
    
    return RiskAssessment(
        addiction_risk_score=child.addiction_risk_score,
        risk_level=risk_level,
        late_night_usage_hours=child.late_night_usage_hours,
        suspicious_search_count=child.suspicious_search_count,
        recommendations=recommendations
    )


# ===================
# Remote Control
# ===================

@router.post("/{child_id}/lock", response_model=MessageResponse)
async def lock_child_device(
    child_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Lock child's device remotely"""
    
    child_result = await db.execute(
        select(Child).where(
            Child.id == child_id,
            Child.parent_id == current_user.id
        )
    )
    child = child_result.scalar_one_or_none()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    # TODO: Send push notification to child's device to lock
    # This would integrate with FCM
    
    return MessageResponse(message="Device lock command sent")


@router.post("/{child_id}/unlock", response_model=MessageResponse)
async def unlock_child_device(
    child_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Unlock child's device remotely"""
    
    child_result = await db.execute(
        select(Child).where(
            Child.id == child_id,
            Child.parent_id == current_user.id
        )
    )
    child = child_result.scalar_one_or_none()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    # TODO: Send push notification to child's device to unlock
    
    return MessageResponse(message="Device unlock command sent")


@router.post("/{child_id}/screenshot-block", response_model=MessageResponse)
async def toggle_screenshot_block(
    child_id: str,
    enabled: bool,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Toggle screenshot blocking"""
    
    child_result = await db.execute(
        select(Child).where(
            Child.id == child_id,
            Child.parent_id == current_user.id
        )
    )
    child = child_result.scalar_one_or_none()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child profile not found"
        )
    
    # Update would be stored in settings
    # TODO: Send update to child device
    
    return MessageResponse(
        message=f"Screenshot blocking {'enabled' if enabled else 'disabled'}"
    )
