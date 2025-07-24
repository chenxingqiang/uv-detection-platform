from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "UV-Spectroscopy Pesticide Residue Detection Platform"
    API_V1_STR: str = "/api/v1"

    # Example of other settings that will be added later
    # DATABASE_URL: str = "postgresql://user:password@localhost/uv_detection_db"
    # KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"

    class Config:
        case_sensitive = True

settings = Settings()
