from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    SENSOR_API_KEY: str
    DATABASE_URL: str

    model_config = {
        "env_file": ".env",
        "extra": "ignore",
    }

settings = Settings()
