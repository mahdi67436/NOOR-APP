"""
NoorGuard Ultimate - Core Configuration
Islamic Digital Protection Ecosystem
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )
    
    # Application
    app_name: str = "NoorGuard Ultimate"
    app_version: str = "1.0.0"
    app_description: str = "Islamic Digital Protection Ecosystem"
    debug: bool = True
    secret_key: str = "dev-secret-key-change-in-production"
    api_v1_prefix: str = "/api/v1"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "noorguard"
    postgres_password: str = "password"
    postgres_db: str = "noorguard_db"
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = ""
    redis_db: int = 0
    
    # JWT
    jwt_secret_key: str = "jwt-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    
    # Encryption
    encryption_key: str = "32-char-encryption-key-here!!"
    aes_key: str = "32byteaeskeyforencryption!!"
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    
    # AWS S3
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    aws_region: str = "us-east-1"
    aws_s3_bucket: str = "noorguard-uploads"
    
    # AI Models
    nsfw_model_path: str = "/models/nsfw_model.tflite"
    content_classifier_path: str = "/models/content_classifier.pkl"
    
    # Islamic API
    prayer_api_url: str = "https://api.aladhan.com/v1"
    
    # Sentry
    sentry_dsn: str = ""
    
    # Rate Limiting
    rate_limit_per_minute: int = 60
    
    @property
    def database_url(self) -> str:
        """Get PostgreSQL database URL"""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    @property
    def sync_database_url(self) -> str:
        """Get synchronous PostgreSQL database URL"""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
    
    @property
    def redis_url(self) -> str:
        """Get Redis URL"""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


# Create singleton instance
settings = Settings()


# Islamic Prayer Times Configuration
class PrayerConfig:
    """Islamic prayer time calculation settings"""
    
    # Calculation methods
    METHOD_Muslim_World_League = 0
    METHOD_Egyptian = 1
    METHOD_Karachi = 2
    METHOD_Mecca = 3
    METHOD_Algeria = 4
    METHOD_Turkey = 5
    METHOD_Tehran = 7
    
    # Juristic methods
    JURISTIC_SHAFII = 0
    JURISTIC_HANFI = 1
    
    # Adjustments
    Fajr_Angle = 18
    Isha_Angle = 17
    
    # Default method
    CALCULATION_METHOD = METHOD_Mecca
    JURISTIC_METHOD = JURISTIC_SHAFII
    
    # Prayer names
    PRAYER_NAMES = {
        "fajr": "Fajr (Subuh)",
        "sunrise": "Sunrise",
        "dhuhr": "Dhuhr (Zuhur)",
        "asr": "Asr (Asar)",
        "maghrib": "Maghrib (Maghrib)",
        "isha": "Isha (Isyak)"
    }
    
    # Default location (Mecca)
    DEFAULT_LATITUDE = 21.4225
    DEFAULT_LONGITUDE = 39.8262


# Content Filtering Configuration
class FilterConfig:
    """Content filtering and blocking configuration"""
    
    # Blocked categories
    ADULT_CONTENT = "adult"
    VIOLENCE = "violence"
    GAMBLING = "gambling"
    DRUGS = "drugs"
    HATE_SPEECH = "hate_speech"
    CYBER_BULLYING = "cyber_bullying"
    
    # Filter levels
    FILTER_STRICT = "strict"
    FILTER_MODERATE = "moderate"
    FILTER_MINIMAL = "minimal"
    
    # Default blocked keywords (Arabic + English)
    DEFAULT_BLOCKED_KEYWORDS = [
        # Adult content
        "adult", "xxx", "porn", "nude", "nsfw",
        # Violence
        "violence", "gore", "death",
        # Gambling
        "casino", "betting", "lottery",
        # Drugs
        "drug", "cannabis", "marijuana",
    ]
    
    # DNS blocklist
    DNS_BLOCKLIST_URLS = [
        "https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts",
        "https://adaway.org/hosts.txt",
    ]
    
    # Safe search APIs
    SAFE_SEARCH_DNS = {
        "google": "8.8.8.8",
        "cloudflare": "1.1.1.1",
        "safe": "185.228.168.168"
    }


# Security Configuration
class SecurityConfig:
    """Security and encryption settings"""
    
    # AES-256 encryption
    AES_KEY_SIZE = 32  # 256 bits
    AES_IV_SIZE = 16   # 128 bits
    
    # Password requirements
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_REQUIRE_UPPERCASE = True
    PASSWORD_REQUIRE_LOWERCASE = True
    PASSWORD_REQUIRE_DIGIT = True
    PASSWORD_REQUIRE_SPECIAL = False
    
    # Session settings
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 30
    SESSION_TIMEOUT_MINUTES = 60
    
    # Device binding
    MAX_DEVICES_PER_USER = 10
    REQUIRE_DEVICE_VERIFICATION = True
    
    # Rate limiting
    DEFAULT_RATE_LIMIT = 60
    AUTH_RATE_LIMIT = 10
    
    # Biometric settings
    BIOMETRIC_ENABLED = True
    BIOMETRIC_TIMEOUT_MINUTES = 5


# Monitoring Configuration
class MonitoringConfig:
    """AI behavioral monitoring settings"""
    
    # Anomaly detection thresholds
    LATE_NIGHT_HOUR = 22  # 10 PM
    EARLY_MORNING_HOUR = 5  # 5 AM
    
    # Usage patterns
    SUSPICIOUS_SEARCH_THRESHOLD = 5  # searches per minute
    ADDICTION_RISK_SCORE_THRESHOLD = 70
    
    # Time limits
    DAILY_SCREEN_TIME_LIMIT_HOURS = 4
    NIGHT_SCREEN_TIME_LIMIT_HOURS = 1
    
    # Scoring weights
    LATE_NIGHT_WEIGHT = 30
    EXCESSIVE_USE_WEIGHT = 25
    SUSPICIOUS_CONTENT_WEIGHT = 35
    IRREGULAR_PATTERN_WEIGHT = 10
    
    # Alert thresholds
    HIGH_RISK_SCORE = 80
    MEDIUM_RISK_SCORE = 50
    LOW_RISK_SCORE = 25


# Report Configuration
class ReportConfig:
    """Analytics and report settings"""
    
    REPORT_GENERATION_DAY = "saturday"  # Weekly reports
    REPORT_RETENTION_DAYS = 90
    
    # Metrics to track
    METRICS = [
        "screen_time",
        "app_usage",
        "websites_visited",
        "search_queries",
        "blocked_attempts",
        "prayer_compliance",
        "islamic_habits"
    ]
