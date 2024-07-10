from pydantic_settings import BaseSettings

from database_models.restaurant_model import DATABASE_URL, RCMD_DATABASE_URL

# Store the database URLs for the primary and secondary databases swithcing to BaseSettings
class Settings(BaseSettings):
    if DATABASE_URL:
        primary_database_url: str = DATABASE_URL
    else:
        raise ValueError("DATABASE_URL must be set in .env file")

    if RCMD_DATABASE_URL:
        secondary_database_url: str = RCMD_DATABASE_URL
    else:
        raise ValueError("RCMD_DATABASE_URL must be set in .env file")
    
    class Config:
        env_file = ".env"