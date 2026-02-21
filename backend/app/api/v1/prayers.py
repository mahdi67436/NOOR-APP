"""
NoorGuard Ultimate - Prayer Times API
Islamic Prayer Times and Islamic Features
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from typing import Optional
import json
import httpx
from dateutil import parser as date_parser

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import settings, PrayerConfig
from app.models.user import User
from app.models.child import Child, PrayerLog


router = APIRouter(prefix="/prayers", tags=["Prayer Times"])


class PrayerTimesCalculator:
    """Calculate prayer times based on location"""
    
    @staticmethod
    def calculate_times(latitude: float, longitude: float, date: datetime = None):
        """Calculate prayer times for a given location and date"""
        if date is None:
            date = datetime.utcnow()
        
        # Using praytimes library for calculation
        try:
            from praytimes import PrayTimes
            
            pt = PrayTimes('MWL')
            pt.set_method(PrayerConfig.CALCULATION_METHOD)
            
            times = pt.get_times(
                date.date(),
                (latitude, longitude),
                timezone=0  # UTC
            )
            
            return {
                "fajr": times['fajr'],
                "sunrise": times['sunrise'],
                "dhuhr": times['dhuhr'],
                "asr": times['asr'],
                "maghrib": times['maghrib'],
                "isha": times['isha']
            }
        except Exception as e:
            # Fallback to default times
            return {
                "fajr": "05:30",
                "sunrise": "06:45",
                "dhuhr": "12:30",
                "asr": "15:45",
                "maghrib": "18:30",
                "isha": "20:00"
            }
    
    @staticmethod
    def get_month_times(latitude: float, longitude: float, year: int = None, month: int = None):
        """Get prayer times for an entire month"""
        if year is None:
            year = datetime.utcnow().year
        if month is None:
            month = datetime.utcnow().month
        
        start_date = datetime(year, month, 1)
        
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        times = []
        current = start_date
        while current < end_date:
            day_times = PrayerTimesCalculator.calculate_times(latitude, longitude, current)
            day_times['date'] = current.date().isoformat()
            times.append(day_times)
            current += timedelta(days=1)
        
        return times


@router.get("/times")
async def get_prayer_times(
    latitude: float = Query(..., description="Latitude"),
    longitude: float = Query(..., description="Longitude"),
    date: Optional[str] = Query(None, description="Date (YYYY-MM-DD)")
):
    """Get prayer times for a location"""
    
    if date:
        try:
            prayer_date = date_parser.parse(date)
        except Exception:
            prayer_date = datetime.utcnow()
    else:
        prayer_date = datetime.utcnow()
    
    times = PrayerTimesCalculator.calculate_times(latitude, longitude, prayer_date)
    
    return {
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "date": prayer_date.date().isoformat(),
        "times": times,
        "method": "MWL"
    }


@router.get("/times/month")
async def get_monthly_prayer_times(
    latitude: float = Query(..., description="Latitude"),
    longitude: float = Query(..., description="Longitude"),
    year: int = Query(None, description="Year"),
    month: int = Query(None, description="Month (1-12)")
):
    """Get prayer times for a month"""
    
    times = PrayerTimesCalculator.get_month_times(latitude, longitude, year, month)
    
    return {
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "year": year or datetime.utcnow().year,
        "month": month or datetime.utcnow().month,
        "times": times
    }


@router.get("/times/next")
async def get_next_prayer(
    latitude: float = Query(..., description="Latitude"),
    longitude: float = Query(..., description="Longitude")
):
    """Get next prayer time"""
    
    now = datetime.utcnow()
    current_time = now.time().strftime("%H:%M")
    
    times = PrayerTimesCalculator.calculate_times(latitude, longitude, now)
    
    prayers = {
        "fajr": times['fajr'],
        "dhuhr": times['dhuhr'],
        "asr": times['asr'],
        "maghrib": times['maghrib'],
        "isha": times['isha']
    }
    
    next_prayer = None
    next_time = None
    
    for prayer, time_str in prayers.items():
        if time_str > current_time:
            next_prayer = prayer
            next_time = time_str
            break
    
    if not next_prayer:
        # Next day's fajr
        next_date = now + timedelta(days=1)
        next_times = PrayerTimesCalculator.calculate_times(latitude, longitude, next_date)
        next_prayer = "fajr"
        next_time = next_times['fajr']
    
    return {
        "current_time": current_time,
        "next_prayer": next_prayer,
        "next_prayer_time": next_time,
        "remaining_minutes": calculate_remaining_minutes(current_time, next_time)
    }


def calculate_remaining_minutes(current: str, target: str) -> int:
    """Calculate minutes between current time and target time"""
    try:
        current_h, current_m = map(int, current.split(':'))
        target_h, target_m = map(int, target.split(':'))
        
        current_minutes = current_h * 60 + current_m
        target_minutes = target_h * 60 + target_m
        
        if target_minutes < current_minutes:
            target_minutes += 24 * 60
        
        return target_minutes - current_minutes
    except:
        return 0


# ===================
# Islamic Content
# ===================

class IslamicContent:
    """Islamic content helpers"""
    
    # Sample Hadiths (in production, load from database or API)
    HADITHS = [
        {
            "id": 1,
            "text": "The best among you are those who learn the Quran and teach it to others.",
            "source": "Sahih Bukhari",
            "narrator": "Abu Musa al-Ashari"
        },
        {
            "id": 2,
            "text": "Whoever follows a path in pursuit of knowledge, Allah will make his path to Paradise easy.",
            "source": "Sahih Bukhari",
            "narrator": "Abu Hurayrah"
        },
        {
            "id": 3,
            "text": "The world is sweet and green, and verily Allah has made you stewards in it.",
            "source": "Sahih Muslim",
            "narrator": "Anas ibn Malik"
        }
    ]
    
    # Dhikr collections
    DHIKR_MORNING = [
        {"arabic": "أَصْبَحْنَا وَأَصْبَحَ الْمُلْكُ لِلَّهِ", "transliteration": "Asbahna wa asbah al-mulku lillah"},
        {"arabic": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ", "transliteration": "Al-hamdu lillahi rabbi al-alamin"},
    ]
    
    DHIKR_EVENING = [
        {"arabic": "أَمْسَيْنَا وَأَمْسَى الْمُلْكُ لِلَّهِ", "transliteration": "Amsayna wa amsa al-mulku lillah"},
        {"arabic": "أَعُوذُ بِكَلِمَاتِ اللَّهِ التَّامَّاتِ", "transliteration": "Auzu bi kalimatillah al-tammat"},
    ]
    
    # Quran Ayahs (selected)
    QURAN_AYAHS = [
        {"surah": "Al-Baqarah", "ayah": 255, "text": "Allah - there is no deity except Him, the Ever-Living, the Self-Sustaining..."},
        {"surah": "Al-Ikhlas", "ayah": 1-4, "text": "Say, He is Allah, the One. Allah, the Absolute..."},
        {"surah": "Al-Falaq", "ayah": 1-5, "text": "Say, I seek refuge in the Lord of daybreak..."}
    ]


@router.get("/hadith/random")
async def get_random_hadith():
    """Get a random hadith"""
    import random
    hadith = random.choice(IslamicContent.HADITHS)
    
    return {
        "hadith": hadith,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/dhikr/morning")
async def get_morning_dhikr():
    """Get morning dhikr"""
    return {
        "type": "morning",
        "dhikr": IslamicContent.DHIKR_MORNING,
        "count": len(IslamicContent.DHIKR_MORNING)
    }


@router.get("/dhikr/evening")
async def get_evening_dhikr():
    """Get evening dhikr"""
    return {
        "type": "evening",
        "dhikr": IslamicContent.DHIKR_EVENING,
        "count": len(IslamicContent.DHIKR_EVENING)
    }


@router.get("/quran/ayah/random")
async def get_random_ayah():
    """Get a random Quran ayah"""
    import random
    ayah = random.choice(IslamicContent.QURAN_AYAHS)
    
    return {
        "ayah": ayah,
        "timestamp": datetime.utcnow().isoformat()
    }


# ===================
# Prayer Compliance
# ===================

@router.get("/{child_id}/compliance")
async def get_prayer_compliance(
    child_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    days: int = Query(7, ge=1, le=30)
):
    """Get prayer compliance for child"""
    
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
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get prayer logs
    result = await db.execute(
        select(PrayerLog).where(
            PrayerLog.child_id == child_id,
            PrayerLog.prayer_date >= start_date
        )
    )
    logs = result.scalars().all()
    
    # Calculate compliance
    total_prayers = len(logs)
    compliant_prayers = sum(1 for log in logs if log.was_compliant)
    
    compliance_rate = (compliant_prayers / total_prayers * 100) if total_prayers > 0 else 0
    
    # Group by prayer
    by_prayer = {}
    for prayer in ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha']:
        prayer_logs = [log for log in logs if log.prayer_name == prayer]
        prayer_compliant = sum(1 for log in prayer_logs if log.was_compliant)
        prayer_total = len(prayer_logs)
        
        by_prayer[prayer] = {
            "total": prayer_total,
            "compliant": prayer_compliant,
            "rate": (prayer_compliant / prayer_total * 100) if prayer_total > 0 else 0
        }
    
    return {
        "child_id": child_id,
        "period_days": days,
        "total_prayers": total_prayers,
        "compliant_prayers": compliant_prayers,
        "compliance_rate": compliance_rate,
        "by_prayer": by_prayer
    }


@router.post("/{child_id}/prayer-log")
async def log_prayer_compliance(
    child_id: str,
    prayer_name: str,
    was_locked: bool,
    was_compliant: bool,
    phone_usage: int = Query(0, description="Phone usage during prayer in minutes"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Log prayer compliance"""
    
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
    
    # Get prayer times
    child_result = await db.execute(
        select(Child).where(Child.id == child_id)
    )
    child = child_result.scalar_one()
    
    # Get scheduled time (in production, calculate based on location)
    from app.api.v1.prayers import PrayerTimesCalculator
    times = PrayerTimesCalculator.calculate_times(
        float(child.latitude or 21.4225), 
        float(child.longitude or 39.8262)
    )
    
    prayer_log = PrayerLog(
        child_id=child_id,
        prayer_name=prayer_name,
        scheduled_time=times.get(prayer_name, "00:00"),
        was_locked=was_locked,
        was_compliant=was_compliant,
        phone_usage_during_prayer=phone_usage,
        prayer_date=datetime.utcnow()
    )
    
    db.add(prayer_log)
    await db.commit()
    
    return {"message": "Prayer log recorded", "compliant": was_compliant}
