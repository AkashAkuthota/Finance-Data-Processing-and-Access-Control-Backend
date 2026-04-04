from pydantic_settings import BaseSettings
from pydantic import field_validator
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """
    Application configuration with support for both direct DATABASE_URL
    and individual database credentials (for flexibility across platforms).
    """

    # Environment setup
    ENVIRONMENT: str = "development"

    # Database configuration with dual support
    DATABASE_URL: str | None = None
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_HOST: str | None = None
    DB_PORT: str | None = None
    DB_NAME: str | None = None

    # JWT Config
    SECRET_KEY: str = "supersecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Redis Config
    REDIS_URL: str = "redis://localhost:6379"

    # Security
    SECURE_COOKIES: bool = False

    @field_validator("DATABASE_URL", mode="before", check_fields=False)
    @classmethod
    def construct_database_url(cls, v):
        """
        Support two approaches:
        1. If DATABASE_URL is provided directly → use it
        2. Otherwise, construct from individual variables
        """
        # Get environment
        environment = os.getenv("ENVIRONMENT", "development")
        sslmode = "require" if environment == "production" else "disable"

        # If DATABASE_URL is directly provided, use it
        if v:
            return v

        # Otherwise, construct from individual variables
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME")

        # Validate all required variables
        missing_vars = []
        if not db_user:
            missing_vars.append("DB_USER")
        if not db_password:
            missing_vars.append("DB_PASSWORD")
        if not db_host:
            missing_vars.append("DB_HOST")
        if not db_name:
            missing_vars.append("DB_NAME")

        if missing_vars:
            error_msg = (
                f"Missing database config: Either set DATABASE_URL directly "
                f"or provide: {', '.join(missing_vars)}"
            )
            raise ValueError(error_msg)

        # Construct and return
        return (
            f"postgresql://{db_user}:{db_password}"
            f"@{db_host}:{db_port}/{db_name}?sslmode={sslmode}"
        )

    @field_validator("SECRET_KEY", mode="after")
    @classmethod
    def validate_secret_key(cls, v):
        """Ensure SECRET_KEY is not default value in production"""
        environment = os.getenv("ENVIRONMENT", "development")
        if v == "supersecretkey" and environment == "production":
            raise ValueError(
                "SECRET_KEY must not be default in production! "
                "Set a strong SECRET_KEY environment variable."
            )
        return v

    @field_validator("SECURE_COOKIES", mode="before")
    @classmethod
    def set_secure_cookies(cls, v):
        """Automatically enable secure cookies in production"""
        environment = os.getenv("ENVIRONMENT", "development")
        return environment == "production"

    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **data):
        super().__init__(**data)
        # Log configuration safely (mask password)
        safe_url = self.DATABASE_URL
        if self.DB_PASSWORD:
            safe_url = self.DATABASE_URL.replace(self.DB_PASSWORD, "****")
        logger.info(f"Database: {safe_url}")
        logger.info(f"Environment: {self.ENVIRONMENT}")
        logger.info(f"Secure cookies: {self.SECURE_COOKIES}")


settings = Settings()