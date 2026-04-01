import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_TITLE: str = os.getenv("APP_TITLE", "Travel Planner API")

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./travel_planner.db")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-me-use-openssl-rand-hex-32")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))

    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    ARTIC_BASE_URL: str = os.getenv("ARTIC_BASE_URL", "https://api.artic.edu/api/v1")
    ARTIC_CACHE_TTL: int = int(os.getenv("ARTIC_CACHE_TTL", "3600"))


settings = Settings()
