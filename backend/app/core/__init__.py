"""
NoorGuard Ultimate - Core Module
Core configuration, security, database, and encryption
"""

from app.core.config import settings, PrayerConfig, FilterConfig, SecurityConfig, MonitoringConfig, ReportConfig
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_current_user,
    get_current_active_user,
    require_role,
    generate_device_id,
    generate_verification_code,
    generate_api_key,
    verify_api_key,
    rate_limiter,
    ip_blocker
)
from app.core.database import get_db, init_db, db_manager, check_database_connection
from app.core.encryption import (
    AES256Encryption,
    FernetEncryption,
    HashUtils,
    DataMasker,
    aes_encryption,
    fernet_encryption,
    hash_utils,
    data_masker
)

__all__ = [
    # Config
    "settings",
    "PrayerConfig",
    "FilterConfig",
    "SecurityConfig",
    "MonitoringConfig",
    "ReportConfig",
    # Security
    "verify_password",
    "get_password_hash",
    "create_access_token",
    "create_refresh_token",
    "decode_token",
    "get_current_user",
    "get_current_active_user",
    "require_role",
    "generate_device_id",
    "generate_verification_code",
    "generate_api_key",
    "verify_api_key",
    "rate_limiter",
    "ip_blocker",
    # Database
    "get_db",
    "init_db",
    "db_manager",
    "check_database_connection",
    # Encryption
    "AES256Encryption",
    "FernetEncryption",
    "HashUtils",
    "DataMasker",
    "aes_encryption",
    "fernet_encryption",
    "hash_utils",
    "data_masker"
]
