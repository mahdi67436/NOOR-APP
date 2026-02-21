"""
NoorGuard Ultimate - Database Module
SQLAlchemy Async Session Management
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from typing import AsyncGenerator

from app.core.config import settings


# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    poolclass=NullPool if settings.debug else None,
    future=True
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base class for models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    """Drop all database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


class DatabaseManager:
    """Database connection manager"""
    
    def __init__(self):
        self.engine = engine
        self.session_maker = AsyncSessionLocal
    
    async def create_tables(self):
        """Create all tables"""
        await init_db()
    
    async def drop_tables(self):
        """Drop all tables"""
        await drop_db()
    
    async def get_session(self) -> AsyncSession:
        """Get a new database session"""
        async with self.session_maker() as session:
            return session


# Singleton instance
db_manager = DatabaseManager()


# Database health check
async def check_database_connection() -> bool:
    """Check if database connection is healthy"""
    try:
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception:
        return False
