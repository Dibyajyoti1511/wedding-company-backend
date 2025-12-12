from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    MASTER_DB_NAME: str = "master_db"
    JWT_SECRET: str = "change-me-to-secure-secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXP_HOURS: int = 3

    class Config:
        env_file = ".env"

settings = Settings()
