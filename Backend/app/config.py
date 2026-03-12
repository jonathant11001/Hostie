from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=str(_ENV_FILE), extra="ignore")

    DATABASE_URL: str
    GEMINI_API_KEY: str


settings = Settings()