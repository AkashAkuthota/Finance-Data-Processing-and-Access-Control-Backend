from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Creating database engine
# pool_pre_ping ensures stale connections are checked before use
# pool_recycle prevents connection timeout issues in long-running apps
# sslmode is configured in DATABASE_URL based on ENVIRONMENT setting
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300
)

# Session factory for database interactions
# autocommit=False ensures explicit transaction control
# autoflush=False prevents automatic flushing of pending changes
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependency for injecting database session into routes
# Ensures session is properly created and closed after request lifecycle
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()