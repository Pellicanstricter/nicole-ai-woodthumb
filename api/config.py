from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Claude API
    anthropic_api_key: str

    # App Settings
    environment: str = "development"
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Confidence Thresholds
    high_confidence_threshold: float = 0.85
    medium_confidence_threshold: float = 0.60

    # Rate Limiting
    max_requests_per_minute: int = 60

    # Logging
    log_level: str = "INFO"
    log_to_sheets: bool = False
    google_sheets_id: Optional[str] = None

    # Owner Notifications
    owner_email: str = "info@woodthumb.com"
    alert_webhook_url: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
